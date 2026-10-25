// Video Settings Lab: from a blocky, long ProRes start to a store trailer that passes.
await wait(900); VS.set({ codec: "H.264 in MP4" }); await wait(1200); VS.set({ res: "1920 × 1080" }); await wait(1200);
VS.set({ fps: 30 }); await wait(1000); VS.set({ br: 10 }); await wait(1300); VS.set({ len: 30 }); await wait(2000);
