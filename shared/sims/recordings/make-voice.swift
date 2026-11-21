// The voice-over and the captions of a course video (AUTHORING.md, "Blended
// courses"): the voice reads the script word for word, and the captions are
// the same lines at the same times.
//
//   swift make-voice.swift <script.txt> <voice.m4a> <captions.vtt> <timing.json> [recordings-dir]
//
// The script has one caption line per line and a blank line between scenes.
// Without recordings, macOS `say` speaks each line (Samantha, 165 words a
// minute; Majed for a line in Arabic: a draft of the teacher's voice). With a
// recordings dir (the teacher's voice, courses/big-data/NOTES.md, "The prep
// video"), the dir holds the teacher's recordings (m4a, mp3, wav, aiff,
// caf). The first number of a file's name is the scene where it starts
// (scene-01.m4a); it holds that scene and the next ones, up to the scene of
// the next file. So one file can hold the whole script (silent about 3
// seconds between scenes), and after a mistake the teacher starts a new file
// at the beginning of the same scene (scene-07.m4a): what the first file
// holds after the end of scene 6 is left out. The silence before and after
// each scene is cut, and the times of the lines are found from the pauses of
// the speaker (a scene without a recording is still spoken by `say`). A short pause follows each line and a longer one each
// scene. The times of the lines go into the captions and into timing.json,
// which the pictures of the video read, so every scene starts with its first
// line. Only the tools of macOS (say, AVFoundation) are used.
import AVFoundation
import Foundation

let args = CommandLine.arguments
guard args.count == 5 || args.count == 6 else {
  print("usage: swift make-voice.swift <script.txt> <voice.m4a> <captions.vtt> <timing.json> [recordings-dir]")
  exit(1)
}
let text = try String(contentsOf: URL(fileURLWithPath: args[1]), encoding: .utf8)
var scenes: [[String]] = [[]]
for raw in text.components(separatedBy: .newlines) {
  let line = raw.trimmingCharacters(in: .whitespaces)
  if line.isEmpty {
    if !scenes[scenes.count - 1].isEmpty { scenes.append([]) }
  } else {
    scenes[scenes.count - 1].append(line)
  }
}
if scenes[scenes.count - 1].isEmpty { scenes.removeLast() }

let tmp = FileManager.default.temporaryDirectory.appendingPathComponent("voice-\(ProcessInfo.processInfo.processIdentifier)")
try FileManager.default.createDirectory(at: tmp, withIntermediateDirectories: true)

func speak(_ line: String, to url: URL) {
  let p = Process()
  p.executableURL = URL(fileURLWithPath: "/usr/bin/say")
  let arabic = line.unicodeScalars.contains { (0x0600...0x06FF).contains($0.value) }
  p.arguments = (arabic ? ["-v", "Majed", "-r", "150"] : ["-v", "Samantha", "-r", "165"]) + ["-o", url.path, line]
  try! p.run()
  p.waitUntilExit()
}

// The teacher's recordings: scene number -> file.
var recordings: [Int: URL] = [:]
if args.count == 6 {
  let dir = URL(fileURLWithPath: args[5])
  let kinds = ["m4a", "mp3", "wav", "aif", "aiff", "caf", "mp4", "m4b"]
  for name in (try? FileManager.default.contentsOfDirectory(atPath: dir.path)) ?? [] {
    let url = dir.appendingPathComponent(name)
    guard kinds.contains(url.pathExtension.lowercased()),
          let r = name.range(of: "[0-9]+", options: .regularExpression), let n = Int(name[r]) else { continue }
    if let other = recordings[n] {
      print("make-voice: two recordings for scene \(n): \(other.lastPathComponent) and \(name)")
      exit(1)
    }
    recordings[n] = url
  }
}

// The loudness of a recording, every 10 ms, in dB (mono, 16 kHz).
func envelope(_ url: URL) throws -> [Double] {
  let asset = AVURLAsset(url: url)
  let reader = try AVAssetReader(asset: asset)
  let out = AVAssetReaderTrackOutput(track: asset.tracks(withMediaType: .audio)[0], outputSettings: [
    AVFormatIDKey: kAudioFormatLinearPCM, AVLinearPCMBitDepthKey: 32, AVLinearPCMIsFloatKey: true,
    AVLinearPCMIsBigEndianKey: false, AVLinearPCMIsNonInterleaved: false, AVNumberOfChannelsKey: 1, AVSampleRateKey: 16000,
  ])
  reader.add(out)
  reader.startReading()
  var samples: [Float] = []
  while let buf = out.copyNextSampleBuffer(), let block = CMSampleBufferGetDataBuffer(buf) {
    let n = CMBlockBufferGetDataLength(block) / 4
    var chunk = [Float](repeating: 0, count: n)
    CMBlockBufferCopyDataBytes(block, atOffset: 0, dataLength: n * 4, destination: &chunk)
    samples += chunk
  }
  var db: [Double] = []
  var i = 0
  while i + 160 <= samples.count {
    var sum = 0.0
    for j in i..<(i + 160) { sum += Double(samples[j]) * Double(samples[j]) }
    db.append(20 * log10(sqrt(sum / 160) + 1e-9))
    i += 160
  }
  return db
}

// Which parts of a recording are speech: true for every 10 ms that is loud.
func speech(_ url: URL) throws -> [Bool] {
  let db = try envelope(url)
  guard !db.isEmpty else { return [] }
  let sorted = db.sorted()
  let floor = sorted[Int(Double(sorted.count - 1) * 0.10)], peak = sorted[Int(Double(sorted.count - 1) * 0.98)]
  let thr = max(floor + 6, floor + 0.3 * (peak - floor))
  var loud = db.map { $0 > thr }
  // Join speech that a very short dip (under 80 ms) splits.
  var k = 0
  while k < loud.count {
    if !loud[k] {
      var e = k
      while e < loud.count && !loud[e] { e += 1 }
      if k > 0 && e < loud.count && e - k < 8 { for j in k..<e { loud[j] = true } }
      k = e
    } else { k += 1 }
  }
  return loud
}

// The pauses (start, end in seconds) of at least `min` seconds between a and b (in 10 ms steps).
func pauses(_ loud: [Bool], _ a: Int, _ b: Int, _ min: Double) -> [(Double, Double)] {
  var gaps: [(Double, Double)] = []
  var k = a
  while k < b {
    if !loud[k] {
      var e = k
      while e < b && !loud[e] { e += 1 }
      if Double(e - k) / 100 >= min { gaps.append((Double(k) / 100, Double(e) / 100)) }
      k = e
    } else { k += 1 }
  }
  return gaps
}

let weight = { (s: String) -> Double in Double(max(1, s.filter { $0.isLetter || $0.isNumber }.count)) }

// Split the time from start to end into parts of the given weights: each cut
// goes to the pause nearest to where the weights put it (within `reach`).
func cutsAt(_ start: Double, _ end: Double, _ weights: [Double], _ gaps: [(Double, Double)], _ reach: Double) -> [(Double, Double)] {
  let all = weights.reduce(0, +)
  var cuts: [(Double, Double)] = []
  var acc = 0.0, lastCut = start
  for w in weights.dropLast() {
    acc += w
    let want = start + (end - start) * acc / all
    let near = gaps.filter { $0.0 > lastCut + 0.3 && abs(($0.0 + $0.1) / 2 - want) < reach }
      .min { abs(($0.0 + $0.1) / 2 - want) < abs(($1.0 + $1.1) / 2 - want) }
    let cut = near ?? (want, want)
    cuts.append(cut)
    lastCut = cut.1
  }
  return cuts
}

// One scene of a recording: where its speech starts and ends, and the times of its lines.
struct Part { let url: URL; let start: Double; let end: Double; let cuts: [(Double, Double)] }

// A recording holds one scene or several in order (the teacher stays silent
// about 3 seconds between scenes). The scenes are split at the long pauses
// (1.5 s or more); what comes after the pause that ends the last scene is
// left out (a scene stopped by a mistake and read again in the next file).
// With too few long pauses, the scenes are split by the length of their text.
func splitScenes(_ url: URL, _ sc: [[String]]) throws -> [Part] {
  let loud = try speech(url)
  guard let first = loud.firstIndex(of: true), let last = loud.lastIndex(of: true) else {
    print("make-voice: no speech in \(url.lastPathComponent)")
    exit(1)
  }
  var bounds: [(Int, Int)] = []          // each scene: from, to (10 ms steps)
  let long = pauses(loud, first, last + 1, 1.5)
  let sceneWeights = sc.map { $0.map(weight).reduce(0, +) }
  if sc.count == 1 {
    bounds = [(first, last + 1)]
  } else if long.count >= sc.count - 1 {
    var from = first
    for j in 0..<sc.count {
      let to = j < long.count ? Int(long[j].0 * 100) : last + 1
      bounds.append((from, to))
      if j < long.count { from = Int(long[j].1 * 100) }
    }
    // A long pause inside a scene moves every scene after it: then the
    // length of a scene no longer fits its text, and the text decides.
    let rates = zip(bounds, sceneWeights).map { Double($0.1 - $0.0) / $1 }
    let mid = rates.sorted()[rates.count / 2]
    if rates.contains(where: { $0 < mid * 0.5 || $0 > mid * 2 }) { bounds = [] }
  }
  if bounds.isEmpty {
    print("make-voice: \(url.lastPathComponent): the long pauses do not match the \(sc.count) scenes; the scenes are split by their text")
    let cuts = cutsAt(Double(first) / 100, Double(last + 1) / 100, sceneWeights, pauses(loud, first, last + 1, 1.0), 8)
    var from = first
    for c in cuts { bounds.append((from, Int(c.0 * 100))); from = Int(c.1 * 100) }
    bounds.append((from, last + 1))
  }
  return zip(sc, bounds).map { lines, b in
    let a = loud[b.0..<b.1].firstIndex(of: true) ?? b.0, z = (loud[b.0..<b.1].lastIndex(of: true) ?? b.1 - 1) + 1
    let s0 = Double(a) / 100, s1 = Double(z) / 100
    return Part(url: url, start: s0, end: s1, cuts: cutsAt(s0, s1, lines.map(weight), pauses(loud, a, z, 0.18), 1.6))
  }
}

// Seconds: before the first line, after each line, and the extra pause of a scene.
let lead = 0.6, pause = 0.35, scenePause = 0.6, tail = 1.2
let scale: CMTimeScale = 44100
let comp = AVMutableComposition()
let track = comp.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)!
var t = lead, end = 0.0, n = 0
var timing: [[String: Any]] = []
var vtt = "WEBVTT\n"

func stamp(_ s: Double) -> String {
  let ms = Int((s * 1000).rounded())
  return String(format: "%02d:%02d:%02d.%03d", ms / 3_600_000, ms / 60_000 % 60, ms / 1000 % 60, ms % 1000)
}

// The scenes that each recording holds: from its scene to the scene before the next recording.
var parts: [Int: Part] = [:]
let starts = recordings.keys.sorted()
for (j, s) in starts.enumerated() where s >= 1 && s <= scenes.count {
  let upto = j + 1 < starts.count ? min(starts[j + 1] - 1, scenes.count) : scenes.count
  for (o, part) in try splitScenes(recordings[s]!, Array(scenes[(s - 1)..<upto])).enumerated() { parts[s + o] = part }
}

var recorded = 0
for (i, scene) in scenes.enumerated() {
  if i > 0 { t += scenePause }
  var lines: [[String: Any]] = []
  let start = t
  if let part = parts[i + 1] {
    // The teacher's voice: the speech of the scene, without the silence around it.
    recorded += 1
    let asset = AVURLAsset(url: part.url)
    let total = CMTimeGetSeconds(asset.duration)
    let (s0, s1, cuts) = (part.start, part.end, part.cuts)
    let a = max(0, s0 - 0.12), b = min(total, s1 + 0.2)
    if t > end {
      track.insertEmptyTimeRange(CMTimeRange(start: CMTime(seconds: end, preferredTimescale: scale),
                                             end: CMTime(seconds: t, preferredTimescale: scale)))
    }
    try track.insertTimeRange(CMTimeRange(start: CMTime(seconds: a, preferredTimescale: scale), end: CMTime(seconds: b, preferredTimescale: scale)),
                              of: asset.tracks(withMediaType: .audio)[0], at: CMTime(seconds: t, preferredTimescale: scale))
    let bounds = [(s0, s0)] + cuts + [(s1, s1)]
    for (j, line) in scene.enumerated() {
      n += 1
      let ls = t + bounds[j].1 - a, le = t + bounds[j + 1].0 - a
      lines.append(["text": line, "start": ls, "end": le])
      vtt += "\n\(n)\n\(stamp(ls)) --> \(stamp(le))\n\(line)\n"
    }
    end = t + (b - a)
    t = end + pause
  } else {
    for line in scene {
      n += 1
      let url = tmp.appendingPathComponent("line-\(n).aiff")
      speak(line, to: url)
      let asset = AVURLAsset(url: url)
      let dur = CMTimeGetSeconds(asset.duration)
      if t > end {
        track.insertEmptyTimeRange(CMTimeRange(start: CMTime(seconds: end, preferredTimescale: scale),
                                               end: CMTime(seconds: t, preferredTimescale: scale)))
      }
      try track.insertTimeRange(CMTimeRange(start: .zero, duration: asset.duration),
                                of: asset.tracks(withMediaType: .audio)[0], at: CMTime(seconds: t, preferredTimescale: scale))
      end = t + dur
      lines.append(["text": line, "start": t, "end": end])
      vtt += "\n\(n)\n\(stamp(t)) --> \(stamp(end))\n\(line)\n"
      t = end + pause
    }
  }
  timing.append(["start": start, "lines": lines])
}
let total = end + tail

let out = URL(fileURLWithPath: args[2])
try? FileManager.default.removeItem(at: out)
let export = AVAssetExportSession(asset: comp, presetName: AVAssetExportPresetAppleM4A)!
export.outputURL = out
export.outputFileType = .m4a
let done = DispatchSemaphore(value: 0)
export.exportAsynchronously { done.signal() }
done.wait()
guard export.status == .completed else {
  print("make-voice: failed \(String(describing: export.error))")
  exit(1)
}
try vtt.write(toFile: args[3], atomically: true, encoding: .utf8)
let json = try JSONSerialization.data(withJSONObject: ["total": total, "scenes": timing], options: [.prettyPrinted, .sortedKeys])
try json.write(to: URL(fileURLWithPath: args[4]))
try? FileManager.default.removeItem(at: tmp)
print(String(format: "make-voice: %d lines in %d scenes (%d recorded), %.1f seconds", n, scenes.count, recorded, total))
for (i, sc) in timing.enumerated() {
  let ls = sc["lines"] as! [[String: Any]]
  print(String(format: "  scene %2d: %5.1f s", i + 1, (ls.last!["end"] as! Double) - (sc["start"] as! Double)) + (parts[i + 1].map { " " + $0.url.lastPathComponent } ?? ""))
}
