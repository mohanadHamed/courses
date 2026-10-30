// Small drawing and counting helpers for the probability simulators of Lecture 10 and Seminar 10.
//   DC.die(ctx, x, y, size, face, fill)   draws a die
//   DC.coin(ctx, x, y, r, "H" | "T")      draws a coin
//   DC.frac(k, n) -> "k/n (= a/b)" and DC.gcd(a, b)
(function () {
  const PIPS = { 1: [[0.5, 0.5]], 2: [[0.27, 0.27], [0.73, 0.73]], 3: [[0.25, 0.25], [0.5, 0.5], [0.75, 0.75]],
    4: [[0.27, 0.27], [0.73, 0.27], [0.27, 0.73], [0.73, 0.73]], 5: [[0.27, 0.27], [0.73, 0.27], [0.5, 0.5], [0.27, 0.73], [0.73, 0.73]],
    6: [[0.27, 0.24], [0.73, 0.24], [0.27, 0.5], [0.73, 0.5], [0.27, 0.76], [0.73, 0.76]] };
  function die(c, x, y, s, face, fill) {
    Kit.rrect(c, x, y, s, s, s * 0.18, fill || "#fff", "#2a2f2c", Math.max(1.5, s / 22));
    c.fillStyle = "#2a2f2c";
    (PIPS[face] || []).forEach(([px, py]) => { c.beginPath(); c.arc(x + px * s, y + py * s, s * 0.085, 0, 7); c.fill(); });
  }
  function coin(c, x, y, r, side, dim) {
    c.globalAlpha = dim ? 0.35 : 1;
    c.fillStyle = side === "H" ? "#fab005" : "#dee2e6"; c.strokeStyle = side === "H" ? "#e67700" : "#868e96"; c.lineWidth = 2;
    c.beginPath(); c.arc(x, y, r, 0, 7); c.fill(); c.stroke();
    Kit.text(c, side, x, y + r * 0.35, r, "#2a2f2c"); c.globalAlpha = 1;
  }
  const gcd = (a, b) => (b ? gcd(b, a % b) : a);
  function frac(k, n) { const g = gcd(k, n) || 1; return k + "/" + n + (g > 1 && k ? " = " + k / g + "/" + n / g : ""); }
  window.DC = { die, coin, gcd, frac };
})();
