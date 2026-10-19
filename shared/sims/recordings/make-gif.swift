// Join the PNG frames of record.ts into a looping animated GIF (macOS ImageIO).
//
//   swift shared/sims/recordings/make-gif.swift <frames-dir> <out.gif> [max-width]
//
// <frames-dir> holds frame_0000.png … and delays.txt (seconds per frame).
import Foundation
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
let dir = URL(fileURLWithPath: args[1])
let out = URL(fileURLWithPath: args[2])
let maxWidth = args.count > 3 ? Int(args[3])! : 560

let files = try FileManager.default.contentsOfDirectory(atPath: dir.path)
  .filter { $0.hasPrefix("frame_") && $0.hasSuffix(".png") }.sorted()
let delays = (try? String(contentsOf: dir.appendingPathComponent("delays.txt"), encoding: .utf8))?
  .split(separator: "\n").compactMap { Double($0) } ?? []

guard let dest = CGImageDestinationCreateWithURL(out as CFURL, UTType.gif.identifier as CFString, files.count, nil) else {
  fatalError("cannot create \(out.path)")
}
CGImageDestinationSetProperties(dest, [kCGImagePropertyGIFDictionary: [kCGImagePropertyGIFLoopCount: 0]] as CFDictionary)
for (i, name) in files.enumerated() {
  guard let src = CGImageSourceCreateWithURL(dir.appendingPathComponent(name) as CFURL, nil),
        let img = CGImageSourceCreateThumbnailAtIndex(src, 0, [
          kCGImageSourceCreateThumbnailFromImageAlways: true,
          kCGImageSourceThumbnailMaxPixelSize: maxWidth,
        ] as CFDictionary) else { continue }
  let delay = i < delays.count ? delays[i] : 0.11
  CGImageDestinationAddImage(dest, img, [kCGImagePropertyGIFDictionary: [kCGImagePropertyGIFDelayTime: delay]] as CFDictionary)
}
guard CGImageDestinationFinalize(dest) else { fatalError("cannot write \(out.path)") }
let size = (try? FileManager.default.attributesOfItem(atPath: out.path)[.size] as? Int) ?? 0
print("\(out.lastPathComponent): \(files.count) frames, \(size / 1024) KB")
