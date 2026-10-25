// Compatibility Lab: fix the minimum Android, the graphics APIs and the menu.
await wait(1100); CL.set({ api: "Android 8 (API 26)" }); await wait(1500); CL.set({ gfx: "Vulkan + OpenGL ES 3" }); await wait(1500); CL.set({ ui: "anchored to the safe area" }); await wait(2000);
