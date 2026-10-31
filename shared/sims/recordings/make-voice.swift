// The voice-over and the captions of a course video (AUTHORING.md, "Blended
// courses"): the voice reads the script word for word, and the captions are
// the same lines at the same times.
//
//   swift make-voice.swift <script.txt> <voice.m4a> <captions.vtt> <timing.json>
//
// The script has one caption line per line (A2, about 12 words at most) and a
// blank line between scenes. macOS `say` (Samantha, 165 words a minute) speaks
// each line; a short pause follows each line and a longer one each scene. The
// times of the lines go into the captions and into timing.json, which the
// pictures of the video read, so every scene starts with its first line.
// Only the tools of macOS (say, AVFoundation) are used.
import AVFoundation
import Foundation

let args = CommandLine.arguments
guard args.count == 5 else {
  print("usage: swift make-voice.swift <script.txt> <voice.m4a> <captions.vtt> <timing.json>")
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
  p.arguments = ["-v", "Samantha", "-r", "165", "-o", url.path, line]
  try! p.run()
  p.waitUntilExit()
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

for (i, scene) in scenes.enumerated() {
  if i > 0 { t += scenePause }
  var lines: [[String: Any]] = []
  let start = t
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
print(String(format: "make-voice: %d lines in %d scenes, %.1f seconds", n, scenes.count, total))
