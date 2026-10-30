// Draws a simple 16:9 slide for the PowerPoint simulators of Lecture 8 and Online activity 9.
//   SK.draw(ctx, x, y, w, s) with s = { theme, layout, title, body: [lines], pic, alt, contrast, stretch }
//   Animations (slide show): shown = the number of points on the slide, anim = Appear | Fade | Spin
//   and k = 0…1, the progress of the newest point.
(function () {
  const THEMES = {
    Sunrise: { bg: "#fff4e6", bar: "#D9480F", title: "#a33b0a", text: "#2a211c", font: "Georgia, serif" },
    Sky: { bg: "#e7f5ff", bar: "#1c7ed6", title: "#1864ab", text: "#1d1b2e", font: "Trebuchet MS, sans-serif" },
    Night: { bg: "#212529", bar: "#fab005", title: "#ffd43b", text: "#f8f9fa", font: "Verdana, sans-serif" },
    Plain: { bg: "#ffffff", bar: "#ffffff", title: "#000000", text: "#000000", font: "Calibri, Arial, sans-serif" },
  };
  function wrap(c, t, maxW) { const words = t.split(" "), out = []; let line = ""; words.forEach((w) => { const tt = line ? line + " " + w : w; if (c.measureText(tt).width > maxW && line) { out.push(line); line = w; } else line = tt; }); if (line) out.push(line); return out; }
  function draw(c, x, y, w, s) {
    const h = w * 9 / 16, T = { ...(THEMES[s.theme] || THEMES.Plain) }, u = w / 100;
    c.save(); c.fillStyle = T.bg; c.fillRect(x, y, w, h);
    if (s.contrast === "low") { T.text = "#c5c9cc"; T.title = "#d0d4d7"; }
    c.fillStyle = T.bar; c.fillRect(x, y, w, u * 1.6);
    c.strokeStyle = "#ced4da"; c.lineWidth = 1; c.strokeRect(x + 0.5, y + 0.5, w - 1, h - 1);
    const title = s.title || "Click to add title";
    if (s.layout === "Title Slide" || s.layout === "Section Header") {
      c.fillStyle = s.title ? T.title : "#adb5bd"; c.font = `700 ${u * 6.5}px ${T.font}`; c.textAlign = "center";
      wrap(c, title, w * 0.85).forEach((ln, i) => c.fillText(ln, x + w / 2, y + h * 0.45 + i * u * 7.5));
      c.fillStyle = T.text; c.font = `${u * 3.4}px ${T.font}`;
      (s.body || []).slice(0, 2).forEach((ln, i) => c.fillText(ln, x + w / 2, y + h * 0.68 + i * u * 4.5));
    } else {
      c.fillStyle = s.title ? T.title : "#adb5bd"; c.font = `700 ${u * 5}px ${T.font}`; c.textAlign = "left";
      wrap(c, title, w * 0.88).slice(0, 2).forEach((ln, i) => c.fillText(ln, x + u * 6, y + u * 11 + i * u * 6));
      const two = s.layout === "Two Content" || s.pic, colW = two ? w * 0.5 : w * 0.86;
      const show = s.shown === undefined ? Infinity : s.shown;
      const lines = s.body && s.body.length ? s.body : (s.shown === undefined ? ["Click to add text"] : []);
      const fs = lines.length > 7 ? u * 2.2 : u * 3.3;
      c.font = `${fs}px ${T.font}`; c.fillStyle = s.body && s.body.length ? T.text : "#adb5bd";
      let yy = y + u * 22;
      lines.forEach((ln, i) => {
        const parts = wrap(c, ln, colW - u * 4);
        if (i < show) {
          const k = i === show - 1 && s.k !== undefined ? Math.max(0, Math.min(1, s.k)) : 1;
          c.save();
          if (s.anim === "Fade") c.globalAlpha = k;
          if (s.anim === "Spin" && k < 1) { const cx = x + u * 20, cy = yy - fs * 0.3; c.translate(cx, cy); c.rotate((1 - k) * Math.PI * 4); c.scale(Math.max(0.05, k), Math.max(0.05, k)); c.translate(-cx, -cy); }
          parts.forEach((l2, j) => { const ly = yy + j * fs * 1.35; if (ly < y + h - u * 2) c.fillText((j ? "  " : "• ") + l2, x + u * 6, ly); });
          c.restore();
        }
        yy += parts.length * fs * 1.35;
      });
      if (s.pic) {
        const px = x + w * 0.6, py = y + u * 20, pw = w * 0.34, ph = s.stretch ? h * 0.62 : pw * 0.66;
        c.fillStyle = "#ffe8cc"; c.fillRect(px, py, pw, ph);
        c.fillStyle = "#D9480F"; c.beginPath(); c.arc(px + pw * 0.7, py + ph * 0.3, pw * 0.08, 0, 7); c.fill();
        c.fillStyle = "#2b8a3e"; c.beginPath(); c.moveTo(px, py + ph); c.lineTo(px + pw * 0.35, py + ph * 0.45); c.lineTo(px + pw * 0.6, py + ph * 0.75); c.lineTo(px + pw * 0.75, py + ph * 0.55); c.lineTo(px + pw, py + ph); c.fill();
        c.fillStyle = "#495057"; c.font = `${u * 2.2}px sans-serif`; c.textAlign = "center"; c.fillText("shop.jpg", px + pw / 2, py + ph + u * 3);
      }
    }
    c.restore();
    return h;
  }
  window.SK = { draw, THEMES };
})();
