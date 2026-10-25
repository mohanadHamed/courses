// Frame Lab: the wide shot is done at once; then come closer to Nour (medium shot).
await wait(600); FrameLab.check(); await wait(1500);
for (let v = 0; v <= 52; v += 4) { setVal("#ctl input", v); FrameLab.cam.cx += (27 - FrameLab.cam.cx) * 0.3; FrameLab.cam.cy += (36 - FrameLab.cam.cy) * 0.3; await wait(120); }
FrameLab.cam.cx = 27.5; FrameLab.cam.cy = 36; FrameLab.check(); await wait(2000);
for (let v = 52; v <= 100; v += 6) { setVal("#ctl input", v); FrameLab.cam.cx += (82 - FrameLab.cam.cx) * 0.35; FrameLab.cam.cy += (17 - FrameLab.cam.cy) * 0.35; await wait(120); }
FrameLab.cam.cx = 82; FrameLab.cam.cy = 17; FrameLab.check(); await wait(1600);
