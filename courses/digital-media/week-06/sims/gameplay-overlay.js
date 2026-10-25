// Drawings on top of a gameplay panel: the HUD, the player's input and the
// game's feedback. Used by the gameplay storyboard simulators of this folder.
(() => {
  const GO = {};
  GO.heart = (c, x, y, s, col = "#e03131") => {
    c.fillStyle = col; c.beginPath();
    c.moveTo(x, y + s * 0.35);
    c.bezierCurveTo(x - s, y - s * 0.4, x - s * 0.35, y - s, x, y - s * 0.35);
    c.bezierCurveTo(x + s * 0.35, y - s, x + s, y - s * 0.4, x, y + s * 0.35);
    c.fill();
  };
  // Lives (hearts) at the top left, the score at the top right.
  GO.hud = (c, x, y, w, h, o = {}) => {
    const s = Math.max(6, h * 0.045), lives = o.lives ?? 3;
    for (let i = 0; i < 3; i++) GO.heart(c, x + 14 + i * s * 2.4, y + 14 + s * 0.4, s, i < lives ? "#e03131" : "rgba(255,255,255,0.5)");
    c.fillStyle = "rgba(0,0,0,0.35)"; c.fillRect(x + w - 82, y + 6, 76, 22);
    Kit.text(c, "★ " + (o.score ?? 120), x + w - 44, y + 22, 13, "#fff");
  };
  // A finger icon (a circle with rings) for a tap, with an arrow for a swipe.
  GO.input = (c, x, y, kind, r = 14) => {
    if (!kind || kind === "none") return;
    c.strokeStyle = "rgba(255,255,255,0.95)"; c.lineWidth = 2.5;
    for (const k of [1.6, 2.3]) { c.beginPath(); c.arc(x, y, r * k, 0, 7); c.stroke(); }
    c.fillStyle = "#ffd43b"; c.beginPath(); c.arc(x, y, r, 0, 7); c.fill();
    Kit.text(c, kind === "tap" ? "TAP" : "SWIPE", x, y + r * 3.1, Math.max(10, r * 0.8), "#fff");
    if (kind === "swipe") Kit.arrow(c, x - r * 3, y - r * 2.6, x + r * 3, y - r * 2.6, "#ffd43b", 3, 12);
  };
  // Feedback: "splash" draws drops; anything else is a popping text.
  GO.feedback = (c, x, y, kind, s = 1) => {
    if (!kind || kind === "none") return;
    if (kind === "splash") {
      c.fillStyle = "rgba(255,255,255,0.9)";
      for (let i = 0; i < 7; i++) { const a = Math.PI * (1.1 + i * 0.13); c.beginPath(); c.arc(x + Math.cos(a) * 24 * s, y + Math.sin(a) * 20 * s, 4 * s, 0, 7); c.fill(); }
      Kit.text(c, "SPLASH!", x, y + 22 * s, 13 * s, "#fff");
    } else Kit.text(c, kind, x, y, 18 * s, "#ffd43b");
  };
  window.GO = GO;
})();
