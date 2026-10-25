// Slide Builder: layout, title, points, theme, picture with alt text.
await wait(1000); SB.set({ layout: "Title and Content" }); await wait(900); SB.set({ title: "New shop hours" }); await wait(900);
SB.set({ body: ["Sun–Thu: 9:00–20:00", "Friday: closed", "Saturday: 10:00–18:00", "From 1 December"] }); await wait(1000);
SB.set({ theme: "Sunrise" }); await wait(900); SB.set({ pic: true }); await wait(800); SB.set({ alt: "The Sunrise shop next to the bus stop" }); await wait(2000);
