// A tiny frame of Rooftop Rescue for the video simulators of Lectures 10 and 11.
//   RS.draw(ctx, x, y, w, h, t, look)  t = time in seconds; look = { tint, block (pixel size), boat }
(function () {
  function draw(c, x, y, w, h, t, look) {
    look = look || {};
    c.save(); c.beginPath(); c.rect(x, y, w, h); c.clip();
    c.fillStyle = look.sky || "#a5d8ff"; c.fillRect(x, y, w, h);
    c.fillStyle = "#4dabf7"; c.fillRect(x, y + h * 0.66, w, h * 0.34);
    for (let i = 0; i < 6; i++) { c.fillStyle = "rgba(255,255,255,.35)"; c.fillRect(x + ((i * 0.19 + t * 0.07) % 1) * w, y + h * (0.72 + (i % 3) * 0.08), w * 0.06, 2); }
    c.fillStyle = "#868e96"; c.fillRect(x + w * 0.62, y + h * 0.42, w * 0.3, h * 0.24);
    c.fillStyle = "#495057"; c.fillRect(x + w * 0.6, y + h * 0.4, w * 0.34, h * 0.04);
    if (look.cat !== false) { c.fillStyle = "#fd7e14"; c.beginPath(); c.arc(x + w * 0.8, y + h * 0.37, h * 0.04, 0, 7); c.fill(); }
    const k = (Math.sin(t * 0.9) + 1) / 2, bx = x + w * (0.05 + 0.45 * k), by = y + h * 0.66 + Math.sin(t * 3) * h * 0.01;
    c.fillStyle = "#e8590c"; c.beginPath(); c.moveTo(bx, by); c.lineTo(bx + w * 0.2, by); c.lineTo(bx + w * 0.16, by + h * 0.1); c.lineTo(bx + w * 0.04, by + h * 0.1); c.closePath(); c.fill();
    c.fillStyle = "#ffd8a8"; c.beginPath(); c.arc(bx + w * 0.1, by - h * 0.07, h * 0.06, 0, 7); c.fill();
    if (look.tint) { c.fillStyle = look.tint; c.fillRect(x, y, w, h); }
    c.restore();
    if (look.block && look.block > 1) {   // blocky compression: average squares of the picture
      const b = Math.round(look.block), dpr = window.devicePixelRatio || 1;
      try {
        const img = c.getImageData(Math.round(x * dpr), Math.round(y * dpr), Math.round(w * dpr), Math.round(h * dpr)), d = img.data, W = img.width, H = img.height, B = Math.max(2, Math.round(b * dpr));
        for (let by2 = 0; by2 < H; by2 += B) for (let bx2 = 0; bx2 < W; bx2 += B) {
          const i0 = (by2 * W + bx2) * 4, r = d[i0], g = d[i0 + 1], bl = d[i0 + 2];
          for (let yy = by2; yy < Math.min(H, by2 + B); yy++) for (let xx = bx2; xx < Math.min(W, bx2 + B); xx++) { const j = (yy * W + xx) * 4; d[j] = r; d[j + 1] = g; d[j + 2] = bl; }
        }
        c.putImageData(img, Math.round(x * dpr), Math.round(y * dpr));
      } catch (e) { /* no pixel access */ }
    }
  }
  window.RS = { draw };
})();
