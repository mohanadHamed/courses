// Shared simulator helper. Include in every simulator:
//   <script src="<relative path>/shared/sims/sim-base.js"></script>
// When the simulator is embedded in a lesson, it tells the lesson page its
// height, so the iframe fits without an inner scrollbar.
(() => {
  if (window.parent === window) return;
  const send = () =>
    window.parent.postMessage({ simHeight: document.documentElement.scrollHeight }, "*");
  new ResizeObserver(send).observe(document.body);
  window.addEventListener("load", send);
})();
