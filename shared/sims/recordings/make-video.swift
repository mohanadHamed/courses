// Join the frames of an animation and a voice-over into a small MP4 (H.264 video,
// AAC audio) for a short video made for a course (AUTHORING.md, "Blended
// courses"; the course videos of the online activities).
//
//   swift make-video.swift <frames-dir> <fps> <voice.m4a> <out.mp4>
//
// <frames-dir> holds PNG frames named in order (00000.png, 00001.png …), one
// frame every 1/fps second, all the same size (for example 1280 × 720). When
// the voice is longer than the frames, the last frame stays on screen.
// The voice-over: macOS `say` and `afconvert`, for example
//   say -v Samantha -r 165 -o voice.aiff -f script.txt
//   afconvert -f m4af -d aac -b 64000 voice.aiff voice.m4a
// Only the tools of macOS (AVFoundation) are used.
import AVFoundation
import AppKit

let args = CommandLine.arguments
guard args.count == 5, let fps = Int32(args[2]) else {
  print("usage: swift make-video.swift <frames-dir> <fps> <voice.m4a> <out.mp4>")
  exit(1)
}
let dir = URL(fileURLWithPath: args[1]), audio = URL(fileURLWithPath: args[3]), out = URL(fileURLWithPath: args[4])
let files = try FileManager.default.contentsOfDirectory(atPath: dir.path).filter { $0.hasSuffix(".png") }.sorted()
guard let firstName = files.first, let first = NSImage(contentsOf: dir.appendingPathComponent(firstName)) else {
  print("no PNG frames in \(dir.path)")
  exit(1)
}
let w = first.representations[0].pixelsWide, h = first.representations[0].pixelsHigh

// 1. The frames as an H.264 video (no sound yet).
let silent = out.deletingPathExtension().appendingPathExtension("frames.mp4")
try? FileManager.default.removeItem(at: silent)
try? FileManager.default.removeItem(at: out)
let writer = try AVAssetWriter(outputURL: silent, fileType: .mp4)
let input = AVAssetWriterInput(mediaType: .video, outputSettings: [
  AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: w, AVVideoHeightKey: h,
  AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: 900_000, AVVideoProfileLevelKey: AVVideoProfileLevelH264MainAutoLevel],
])
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: input, sourcePixelBufferAttributes: [
  kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB,
  kCVPixelBufferWidthKey as String: w, kCVPixelBufferHeightKey as String: h,
])
writer.add(input)
writer.startWriting()
writer.startSession(atSourceTime: .zero)
let voice = AVURLAsset(url: audio)
let total = max(files.count, Int(ceil(CMTimeGetSeconds(voice.duration) * Double(fps))))
for i in 0..<total {
  let image = NSImage(contentsOf: dir.appendingPathComponent(files[min(i, files.count - 1)]))!
  let cg = image.cgImage(forProposedRect: nil, context: nil, hints: nil)!
  var buffer: CVPixelBuffer?
  CVPixelBufferPoolCreatePixelBuffer(nil, adaptor.pixelBufferPool!, &buffer)
  CVPixelBufferLockBaseAddress(buffer!, [])
  let ctx = CGContext(data: CVPixelBufferGetBaseAddress(buffer!), width: w, height: h, bitsPerComponent: 8,
                      bytesPerRow: CVPixelBufferGetBytesPerRow(buffer!), space: CGColorSpaceCreateDeviceRGB(),
                      bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue)!
  ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))
  CVPixelBufferUnlockBaseAddress(buffer!, [])
  while !input.isReadyForMoreMediaData { usleep(1000) }
  adaptor.append(buffer!, withPresentationTime: CMTime(value: CMTimeValue(i), timescale: fps))
}
input.markAsFinished()
let done = DispatchSemaphore(value: 0)
writer.finishWriting { done.signal() }
done.wait()

// 2. The video and the voice-over in one file.
let comp = AVMutableComposition()
let video = AVURLAsset(url: silent)
let vt = comp.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid)!
try vt.insertTimeRange(CMTimeRange(start: .zero, duration: video.duration), of: video.tracks(withMediaType: .video)[0], at: .zero)
let at = comp.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)!
try at.insertTimeRange(CMTimeRange(start: .zero, duration: voice.duration), of: voice.tracks(withMediaType: .audio)[0], at: .zero)
let export = AVAssetExportSession(asset: comp, presetName: AVAssetExportPresetPassthrough)!
export.outputURL = out
export.outputFileType = .mp4
export.exportAsynchronously { done.signal() }
done.wait()
try? FileManager.default.removeItem(at: silent)
print(export.status == .completed ? "make-video: wrote \(out.path)" : "make-video: failed \(String(describing: export.error))")
