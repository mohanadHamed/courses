// Image Prompt Lab: a bad first picture, then a prompt that fits the slide.
await wait(800); IP.gen(); await wait(1500);
IP.set({ subject: "an office desk with a laptop and folders", style: "flat illustration", colours: "orange and white", shape: "wide 16:9", text: "no text in the picture" }); await wait(900);
IP.gen(); await wait(1300); IP.alt("An office desk with a laptop and coloured folders"); await wait(700); IP.note(); await wait(1800);
