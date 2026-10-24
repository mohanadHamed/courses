// Unit Circle Lab: the point jumps to 30°, 90°, 150°, 210° and 330°.
for (const a of [30, 90, 150, 210, 330]) { click(`[data-a="${a}"]`); await wait(1700); }
