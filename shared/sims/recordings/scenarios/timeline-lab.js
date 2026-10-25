// Timeline Lab: three clips, split the boat chase, ripple delete, title and music.
await wait(700); TLB.add("rooftop.mp4"); await wait(500); TLB.add("boat-chase.mp4"); await wait(500); TLB.add("pasha.mp4"); await wait(900);
TLB.ph(10); await wait(800); TLB.split(); await wait(800); TLB.del(); await wait(1000);
TLB.ph(0); await wait(600); TLB.add("title"); await wait(900); TLB.add("music.wav"); await wait(700);
TLB.sel("a1", 0); for (let i = 0; i < 5; i++) { TLB.trim(-1); await wait(250); } await wait(1500);
