// The opening scene of Rooftop Rescue (Lectures 5 and 6), drawn as a small world
// that a "camera" can frame. Shared by the storyboard simulators of this folder.
//   RS.draw(ctx, x, y, w, h, cam, opts)   cam = { cx, cy, vh, flip }   (vh = world units in view height)
//   RS.SHOTS: the shots of the storyboard lessons.
(() => {
  const RS = {};
  RS.W = 100; RS.H = 56;
  RS.nourX = 26;
  RS.SHOTS = {
    wideStreet: { name: "Wide shot: the flooded street", cx: 50, cy: 28, vh: 56, size: "wide" },
    medNour: { name: "Medium shot: Nour in the boat", cx: 27.5, cy: 36, vh: 9, size: "medium", who: "Nour" },
    closeNour: { name: "Close-up: Nour", cx: 26.3, cy: 34.5, vh: 3.4, size: "close-up", who: "Nour" },
    wideRoof: { name: "Wide shot: the roof", cx: 82, cy: 24, vh: 24, size: "wide" },
    medSalma: { name: "Medium shot: Salma and the cat", cx: 84.5, cy: 19, vh: 9, size: "medium", who: "Salma" },
    closeSalma: { name: "Close-up: Salma", cx: 82, cy: 17, vh: 3.4, size: "close-up", who: "Salma" },
  };

  function person(c, P, fx, fy, col, dir, mood) {
    // fx, fy: the feet (world). dir: 1 looks right, -1 looks left (world).
    const hx = fx, hy = fy - 5.1;
    c.fillStyle = col;
    c.beginPath(); P.rr(fx - 1.1, fy - 4.2, 2.2, 3.3, 0.7); c.fill();          // body
    c.strokeStyle = col; c.lineWidth = P.s(0.45); c.lineCap = "round";
    c.beginPath(); c.moveTo(P.X(fx - 0.5), P.Y(fy - 1.1)); c.lineTo(P.X(fx - 0.7), P.Y(fy)); c.stroke();
    c.beginPath(); c.moveTo(P.X(fx + 0.5), P.Y(fy - 1.1)); c.lineTo(P.X(fx + 0.7), P.Y(fy)); c.stroke();
    c.fillStyle = "#f3c9a0"; c.beginPath(); c.arc(P.X(hx), P.Y(hy), P.s(0.95), 0, 7); c.fill();
    c.fillStyle = col; c.beginPath(); c.arc(P.X(hx), P.Y(hy - 0.25), P.s(0.98), Math.PI, 2 * Math.PI); c.fill();   // hair
    const d = dir * P.dir;
    c.fillStyle = "#2a211c";
    c.beginPath(); c.arc(P.X(hx) + d * P.s(0.35), P.Y(hy + 0.05), Math.max(1, P.s(0.11)), 0, 7); c.fill();
    if (P.s(1) > 18) {                                                         // a face in close-ups
      c.beginPath(); c.arc(P.X(hx) + d * P.s(0.05), P.Y(hy + 0.05), P.s(0.1), 0, 7); c.fill();
      c.strokeStyle = "#2a211c"; c.lineWidth = P.s(0.06);
      c.beginPath();
      if (mood === "fear") c.arc(P.X(hx) + d * P.s(0.25), P.Y(hy + 0.6), P.s(0.18), Math.PI * 1.15, Math.PI * 1.85);
      else c.arc(P.X(hx) + d * P.s(0.25), P.Y(hy + 0.35), P.s(0.22), Math.PI * 0.2, Math.PI * 0.8);
      c.stroke();
    }
  }

  RS.draw = (c, x, y, w, h, cam, opts = {}) => {
    const sc = h / cam.vh, flip = cam.flip ? -1 : 1;
    const P = {
      X: (wx) => x + w / 2 + (wx - cam.cx) * sc * flip,
      Y: (wy) => y + h / 2 + (wy - cam.cy) * sc,
      s: (u) => u * sc, dir: flip,
      rr: (rx, ry, rw, rh, r) => { const a = P.X(flip > 0 ? rx : rx + rw), b = P.Y(ry); if (c.roundRect) c.roundRect(a, b, rw * sc, rh * sc, r * sc); else c.rect(a, b, rw * sc, rh * sc); },
    };
    c.save();
    c.beginPath(); c.rect(x, y, w, h); c.clip();
    const sky = c.createLinearGradient(0, P.Y(0), 0, P.Y(40));
    sky.addColorStop(0, "#5f3dc4"); sky.addColorStop(1, "#ffa94d");
    c.fillStyle = sky; c.fillRect(x, y, w, h);
    c.fillStyle = "#ffd43b"; c.beginPath(); c.arc(P.X(60), P.Y(37), P.s(4), 0, 7); c.fill();       // the setting sun
    const blds = [[2, 18, 12], [16, 26, 9], [28, 14, 11], [42, 22, 13], [58, 16, 10], [96, 20, 6]];
    blds.forEach(([bx, top, bw]) => {
      c.fillStyle = "#495057"; c.beginPath(); P.rr(bx, top, bw, 40 - top, 0.3); c.fill();
      c.fillStyle = "#ffe066";
      for (let wy = top + 2; wy < 37; wy += 4) for (let wx = bx + 1.5; wx < bx + bw - 2; wx += 3.5) { c.beginPath(); P.rr(wx, wy, 1.4, 1.6, 0.1); c.fill(); }
    });
    c.fillStyle = "#862e9c"; c.beginPath(); P.rr(72, 22, 22, 18, 0.3); c.fill();                       // Salma's house
    c.fillStyle = "#5f3dc4"; c.beginPath(); P.rr(71, 21, 24, 1.2, 0.3); c.fill();                      // the roof edge
    c.fillStyle = "#4dabf7"; c.fillRect(x, P.Y(40), w, h);                                               // water
    c.strokeStyle = "rgba(255,255,255,0.5)"; c.lineWidth = Math.max(1, P.s(0.2));
    for (let i = 0; i < 12; i++) { c.beginPath(); c.arc(P.X(4 + i * 8.5), P.Y(43 + (i % 3) * 3), P.s(1.6), Math.PI * 1.1, Math.PI * 1.9); c.stroke(); }
    const nx = opts.nourX ?? RS.nourX;
    person(c, P, nx, 39.6, "#1c7ed6", 1, opts.nourMood);
    c.fillStyle = "#a0522d"; c.beginPath();                                                             // the boat
    c.moveTo(P.X(nx - 4), P.Y(38.6)); c.lineTo(P.X(nx + 4.5), P.Y(38.6)); c.lineTo(P.X(nx + 3.2), P.Y(40.8)); c.lineTo(P.X(nx - 3), P.Y(40.8)); c.closePath(); c.fill();
    person(c, P, 82, 21, "#e8590c", -1, "fear");
    c.fillStyle = "#212529"; c.beginPath(); c.ellipse(P.X(87), P.Y(20.3), P.s(1.1), P.s(0.7), 0, 0, 7); c.fill();   // the cat
    c.beginPath(); c.arc(P.X(88.1), P.Y(19.4), P.s(0.55), 0, 7); c.fill();
    if (opts.arrow) {                                                                                   // movement arrow
      const a = opts.arrow, ax = P.X(a[0]), ay = P.Y(a[1]), bx = P.X(a[2]), by = P.Y(a[3]);
      window.Kit && Kit.arrow(c, ax, ay, bx, by, "#fff", Math.max(2, P.s(0.5)), Math.max(10, P.s(1.8)));
    }
    c.restore();
    if (opts.thirds) {
      c.strokeStyle = "rgba(255,255,255,0.8)"; c.lineWidth = 1; c.setLineDash([4, 4]);
      [1, 2].forEach((k) => { c.beginPath(); c.moveTo(x + w * k / 3, y); c.lineTo(x + w * k / 3, y + h); c.stroke(); c.beginPath(); c.moveTo(x, y + h * k / 3); c.lineTo(x + w, y + h * k / 3); c.stroke(); });
      c.setLineDash([]);
    }
    c.strokeStyle = "#2a211c"; c.lineWidth = 2; c.strokeRect(x, y, w, h);
    return P;
  };
  // Where a world point lands in the frame, as a fraction (0..1) of the width and height.
  RS.where = (cam, wx, wy) => {
    const flip = cam.flip ? -1 : 1, aspect = 16 / 9;
    return [0.5 + (wx - cam.cx) * flip / (cam.vh * aspect), 0.5 + (wy - cam.cy) / cam.vh];
  };
  window.RS = RS;
})();
