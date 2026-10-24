// Shared simulator helper. Include in every simulator, before its own script:
//   <script src="<relative path>/shared/sims/sim-base.js"></script>
(() => {
  // One clock for every simulator. In a lesson page the simulator runs in an
  // iframe, and there the browser can give requestAnimationFrame a time that
  // is many seconds behind performance.now() (a lazy iframe keeps the clock of
  // the page). A game that starts an animation at performance.now() and draws
  // it with the frame time then stands still. So every frame gets
  // performance.now(), as on the full-screen page.
  const raf = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = (cb) => raf(() => cb(performance.now()));

  if (window.parent === window) return;

  // When the simulator is embedded in a lesson, it tells the lesson page its
  // height, so the iframe fits without an inner scrollbar.
  // Measure the content, not the window (the window is as tall as the iframe).
  const send = () =>
    window.parent.postMessage({ simHeight: Math.ceil(document.body.getBoundingClientRect().height) }, "*");
  new ResizeObserver(send).observe(document.body);
  window.addEventListener("load", send);

  // Space and the arrow keys play the game; they must not scroll the lesson page.
  const GAME_KEYS = ["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"];
  window.addEventListener("keydown", (e) => {
    // (A field or a button keeps its own keys: a button never scrolls the page.)
    const t = e.target, own = t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT|BUTTON)$/.test(t.tagName));
    if (!own && GAME_KEYS.includes(e.code)) e.preventDefault();
  });

  // A field that gets the focus must not scroll the lesson page to the simulator.
  const focus = HTMLElement.prototype.focus;
  HTMLElement.prototype.focus = function (opts) { focus.call(this, Object.assign({ preventScroll: true }, opts)); };
})();
