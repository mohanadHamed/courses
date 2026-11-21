// The words of the teacher's recording, with the time of every word, heard on
// this Mac only (macOS speech recognition, Arabic, on-device: nothing leaves the
// computer). Used by tools/clean_voice.py ("find"), which builds it into a small
// app (macOS asks once to allow speech recognition) and gives it the parts of
// the recording (WAV files of about 40 seconds, cut at pauses).
//
//   transcribe <in-dir> <out.json>     (a log next to out.json)
import Foundation
import Speech
let args = CommandLine.arguments
let inDir = URL(fileURLWithPath: args[1]), out = URL(fileURLWithPath: args[2])
func log(_ s: String) { try? (s + "\n").appendToFile(out.deletingPathExtension().appendingPathExtension("log")) }
extension String { func appendToFile(_ u: URL) throws {
  if let h = try? FileHandle(forWritingTo: u) { h.seekToEndOfFile(); h.write(self.data(using: .utf8)!); h.closeFile() }
  else { try self.write(to: u, atomically: true, encoding: .utf8) } } }
let sem = DispatchSemaphore(value: 0)
SFSpeechRecognizer.requestAuthorization { st in log("auth \(st.rawValue)"); sem.signal() }
sem.wait()
guard SFSpeechRecognizer.authorizationStatus() == .authorized else { log("not authorized"); exit(2) }
let rec = SFSpeechRecognizer(locale: Locale(identifier: "ar-SA"))!
rec.queue = OperationQueue()
let files = try FileManager.default.contentsOfDirectory(atPath: inDir.path).filter { $0.hasSuffix(".wav") }.sorted()
var all: [[String: Any]] = []
final class Collect: NSObject, SFSpeechRecognitionTaskDelegate {
  var words: [[String: Any]] = [], text: [String] = [], ok = false
  let done = DispatchSemaphore(value: 0)
  func speechRecognitionTask(_ task: SFSpeechRecognitionTask, didFinishRecognition result: SFSpeechRecognitionResult) {
    text.append(result.bestTranscription.formattedString)
    words += result.bestTranscription.segments.map { ["w": $0.substring, "t": $0.timestamp, "d": $0.duration] }
  }
  func speechRecognitionTask(_ task: SFSpeechRecognitionTask, didFinishSuccessfully successfully: Bool) {
    ok = successfully; if !successfully { log("error \(String(describing: task.error))") }; done.signal()
  }
}
for f in files {
  let req = SFSpeechURLRecognitionRequest(url: inDir.appendingPathComponent(f))
  req.requiresOnDeviceRecognition = true
  req.shouldReportPartialResults = false
  req.addsPunctuation = true
  let c = Collect()
  let task = rec.recognitionTask(with: req, delegate: c)
  c.done.wait()
  _ = task
  all.append(["file": f, "text": c.text.joined(separator: " | "), "words": c.words])
  log("\(f) \(c.words.count) words")
}
let data = try JSONSerialization.data(withJSONObject: all, options: [.prettyPrinted])
try data.write(to: out)
log("done")
exit(0)
