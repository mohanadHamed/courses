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
// each scene is cut; the scene breaks are the pauses that fit the length of
// each scene's text best, and the times of the lines are found from the pauses
// of the speaker (a scene without a recording is still spoken by `say`). A
// pause inside a scene longer than MAX_PAUSE (0.8 s) is shortened to it; a
// sentence read twice is cut first with tools/clean_voice.py. A short pause
// follows each line and a longer one each scene. The times of the lines go into the captions and into timing.json,
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
  let kinds = ["m4a", "mp3", "wav", "aif", "aiff", "aifc", "caf", "mp4", "m4b"]
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
  let per = (end - start) / all
  for w in weights.dropLast() {
    acc += w
    let want = start + (end - start) * acc / all
    // A pause is a cut only when the line before it and the lines after it
    // keep at least half of the time their text needs.
    let near = gaps.filter { let mid = ($0.0 + $0.1) / 2
        return $0.0 > lastCut + 0.3 && abs(mid - want) < reach && mid - lastCut >= 0.5 * w * per && end - mid >= 0.5 * (all - acc) * per }
      .min { abs(($0.0 + $0.1) / 2 - want) < abs(($1.0 + $1.1) / 2 - want) }
    let cut = near ?? (want, want)
    cuts.append(cut)
    lastCut = cut.1
  }
  return cuts
}

// One scene of a recording: where its speech starts and ends, and the times of its lines.
struct Part { let url: URL; let start: Double; let end: Double; let cuts: [(Double, Double)]; var long: [(Double, Double)] = [] }

// The longest pause inside a scene of a recording (seconds): a longer one is
// shortened to it (MAX_PAUSE, 0.8 by default; 0 keeps every pause).
let maxPause = Double(ProcessInfo.processInfo.environment["MAX_PAUSE"] ?? "") ?? 0.8

// A recording holds one scene or several in order (the teacher stays silent
// about 3 seconds between scenes). The scene breaks are the pauses (0.8 s or
// more) that fit best: each scene about as long as its text (the speed of
// the whole recording), and longer pauses first. When a later file starts at
// a later scene (the teacher stopped after a mistake), the end of this one
// may be left out: the scene that was stopped and read again.
func splitScenes(_ url: URL, _ sc: [[String]], mayDropTail: Bool) throws -> [Part] {
  let loud = try speech(url)
  guard let first = loud.firstIndex(of: true), let last = loud.lastIndex(of: true) else {
    print("make-voice: no speech in \(url.lastPathComponent)")
    exit(1)
  }
  let t0 = Double(first) / 100, t1 = Double(last + 1) / 100
  let gaps = pauses(loud, first, last + 1, 0.8)
  let w = sc.map { $0.map(weight).reduce(0, +) }
  let rate = (t1 - t0) / w.reduce(0, +)
  let m = sc.count, g = gaps.count
  func cost(_ a: Double, _ b: Double, _ j: Int) -> Double { let e = rate * w[j]; return (b - a - e) * (b - a - e) / e }
  func bonus(_ k: Int) -> Double { 4 * (gaps[k].1 - gaps[k].0) }
  // ends[j]: the scene j ends at this gap (nil: at the end of the speech).
  var ends: [Int?] = []
  if m == 1 {
    var best = cost(t0, t1, 0), at: Int? = nil
    if mayDropTail { for k in 0..<g where cost(t0, gaps[k].0, 0) - bonus(k) < best { best = cost(t0, gaps[k].0, 0) - bonus(k); at = k } }
    ends = [at]
  } else if g >= m - 1 {
    let inf = Double.infinity
    var dp = Array(repeating: Array(repeating: inf, count: g), count: m), from = Array(repeating: Array(repeating: -1, count: g), count: m)
    for k in 0..<g { dp[0][k] = cost(t0, gaps[k].0, 0) - bonus(k) }
    for j in 1..<(m - 1) {
      for k in 0..<g { for h in 0..<k where dp[j - 1][h] < inf {
        let v = dp[j - 1][h] + cost(gaps[h].1, gaps[k].0, j) - bonus(k)
        if v < dp[j][k] { dp[j][k] = v; from[j][k] = h }
      } }
    }
    var best = inf, prev = -1, at: Int? = nil
    for h in 0..<g where dp[m - 2][h] < inf {
      let v = dp[m - 2][h] + cost(gaps[h].1, t1, m - 1)
      if v < best { best = v; prev = h; at = nil }
      if mayDropTail { for k in (h + 1)..<max(h + 1, g) {
        let d = dp[m - 2][h] + cost(gaps[h].1, gaps[k].0, m - 1) - bonus(k)
        if d < best { best = d; prev = h; at = k }
      } }
    }
    var chain = [prev]
    for j in stride(from: m - 2, to: 0, by: -1) { chain.append(from[j][chain.last!]) }
    ends = chain.reversed().map { Optional($0) } + [at]
  } else {
    print("make-voice: \(url.lastPathComponent): \(g) pauses for \(m) scenes; the scenes are split by their text")
    let cuts = cutsAt(t0, t1, w, [], 0)
    ends = []
    var parts: [Part] = []
    var from = t0
    for (j, lines) in sc.enumerated() {
      let to = j < cuts.count ? cuts[j].0 : t1
      parts.append(Part(url: url, start: from, end: to, cuts: cutsAt(from, to, lines.map(weight), pauses(loud, Int(from * 100), Int(to * 100), 0.18), 1.6)))
      from = to
    }
    return parts
  }
  var parts: [Part] = []
  var from = first
  for (j, lines) in sc.enumerated() {
    let to = ends[j].map { Int(gaps[$0].0 * 100) } ?? last + 1
    let a = loud[from..<to].firstIndex(of: true) ?? from, z = (loud[from..<to].lastIndex(of: true) ?? to - 1) + 1
    let s0 = Double(a) / 100, s1 = Double(z) / 100
    parts.append(Part(url: url, start: s0, end: s1, cuts: cutsAt(s0, s1, lines.map(weight), pauses(loud, a, z, 0.18), 1.6),
                      long: maxPause > 0 ? pauses(loud, a, z, maxPause + 0.01) : []))
    if let k = ends[j] { from = Int(gaps[k].1 * 100) }
  }
  return parts
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
  for (o, part) in try splitScenes(recordings[s]!, Array(scenes[(s - 1)..<upto]), mayDropTail: upto < scenes.count).enumerated() { parts[s + o] = part }
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
    // The pieces of the scene that are kept: every long pause is shortened to
    // maxPause (half of it on each side), and a time of the recording is moved
    // to its place in the voice-over.
    var pieces: [(Double, Double)] = []
    var from = a
    for q in part.long where q.0 > a && q.1 < b {
      pieces.append((from, q.0 + maxPause / 2))
      from = q.1 - maxPause / 2
    }
    pieces.append((from, b))
    var at = t
    var starts: [Double] = []
    for pc in pieces {
      starts.append(at)
      try track.insertTimeRange(CMTimeRange(start: CMTime(seconds: pc.0, preferredTimescale: scale), end: CMTime(seconds: pc.1, preferredTimescale: scale)),
                                of: asset.tracks(withMediaType: .audio)[0], at: CMTime(seconds: at, preferredTimescale: scale))
      at += pc.1 - pc.0
    }
    func place(_ x: Double) -> Double {
      for (k, pc) in pieces.enumerated() {
        if x <= pc.1 { return starts[k] + max(0, x - pc.0) }
      }
      return at
    }
    let bounds = [(s0, s0)] + cuts + [(s1, s1)]
    for (j, line) in scene.enumerated() {
      n += 1
      let ls = place(bounds[j].1), le = place(bounds[j + 1].0)
      lines.append(["text": line, "start": ls, "end": le])
      vtt += "\n\(n)\n\(stamp(ls)) --> \(stamp(le))\n\(line)\n"
    }
    end = at
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
