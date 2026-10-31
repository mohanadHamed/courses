// A made-up recording of Pasha's meow for the audio sims of Lecture 7 and Seminar 7:
// TK.make(problems) builds the samples; TK.draw(ctx, x, y, w, h, data, opts) draws the waveform.
// problems: { lead: seconds of silence at the start, hum: level of a 50 Hz hum, gain: level of the meow,
//             clip: true if the meow is clipped, click: true for a click at the end }
(function () {
  const RATE = 8000;
  function make(p = {}) {
    const lead = p.lead ?? 0.1, len = lead + 1.1 + 0.4, n = Math.round(len * RATE), d = new Float32Array(n);
    let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647) * 2 - 1;
    for (let i = 0; i < n; i++) {
      const t = i / RATE; let v = rnd() * 0.01 + (p.hum || 0) * Math.sin(2 * Math.PI * 50 * t);
      const m = t - lead;
      if (m > 0 && m < 1.1) {                             // the meow: a rising, then falling tone
        const env = Math.sin(Math.PI * m / 1.1) ** 0.6, f = 520 + 260 * Math.sin(Math.PI * m / 1.1);
        v += (p.gain ?? 0.8) * env * (Math.sin(2 * Math.PI * f * m) * 0.8 + Math.sin(4 * Math.PI * f * m) * 0.2);
      }
      if (p.click && t > len - 0.02) v = (i % 2 ? 0.5 : -0.5);
      d[i] = p.clip ? Math.max(-0.7, Math.min(0.7, v * 1.6)) / 0.7 : v;
    }
    return d;
  }
  function peak(d) { let m = 0; for (const v of d) m = Math.max(m, Math.abs(v)); return m; }
  function draw(c, x, y, w, h, d, o = {}) {
    c.fillStyle = o.bg || "#fbf8ff"; c.fillRect(x, y, w, h);
    const mid = y + h / 2;
    c.strokeStyle = "#e5dbff"; c.lineWidth = 1;
    for (const yy of [y + 2, mid, y + h - 2]) { c.beginPath(); c.moveTo(x, yy); c.lineTo(x + w, yy); c.stroke(); }
    const per = d.length / w;
    c.strokeStyle = o.color || "#9C36B5"; c.lineWidth = 1;
    for (let px = 0; px < w; px++) {
      let lo = 0, hi = 0;
      for (let i = Math.floor(px * per); i < Math.floor((px + 1) * per); i++) { lo = Math.min(lo, d[i]); hi = Math.max(hi, d[i]); }
      c.beginPath(); c.moveTo(x + px + 0.5, mid - hi * (h / 2 - 2)); c.lineTo(x + px + 0.5, mid - lo * (h / 2 - 2)); c.stroke();
      if (hi >= 0.999 || lo <= -0.999) { c.fillStyle = "#e03131"; c.fillRect(x + px, y, 1, 4); c.fillRect(x + px, y + h - 4, 1, 4); }
    }
  }
  function play(d) {
    try {
      const a = (window.__ac = window.__ac || new (window.AudioContext || window.webkitAudioContext)());
      const b = a.createBuffer(1, d.length, RATE); b.getChannelData(0).set(d.map((v) => v * 0.3));
      const s = a.createBufferSource(); s.buffer = b; s.connect(a.destination); s.start();
    } catch (_) {}
  }
  window.TK = { RATE, make, peak, draw, play };
})();
