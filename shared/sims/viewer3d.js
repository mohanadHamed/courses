// Reusable 3D viewer for simulators (three.js, served from shared/sims/vendor).
//
// Coordinates follow Unity: x → right, y → up, z → forward (into the screen).
// All functions take Unity-style [x, y, z]; the viewer converts for three.js.
//
// Use in a simulator page (paths relative to the page):
//   <script type="importmap">{"imports":{"three":"<path>/shared/sims/vendor/three.module.min.js"}}</script>
//   <script type="module">
//     import { createViewer } from "<path>/shared/sims/viewer3d.js";
//     const v = createViewer(document.getElementById("view"));
//     v.axes(6); v.ground(6);
//     const p = v.ball({ color: "#2F9E44" }); v.place(p, [4, 3, 2]);
//     v.arrow([0, 0, 0], [4, 3, 2], "#e67e22");    // a vector
//     v.onFrame((dt) => { ... });                    // animation
//   </script>

import * as THREE from "three";
import { OrbitControls } from "./vendor/OrbitControls.js";

export const AXIS_COLORS = { x: "#c0392b", y: "#27ae60", z: "#2471a3" };

export function createViewer(el, opts = {}) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(opts.background || "#fbfdfa");

  const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 200);
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  el.appendChild(renderer.domElement);
  renderer.domElement.style.display = "block";
  renderer.domElement.style.touchAction = "none";

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.enablePan = false;
  controls.minDistance = 4;
  controls.maxDistance = 40;

  scene.add(new THREE.HemisphereLight("#ffffff", "#d3e6cc", 1.6));
  const sun = new THREE.DirectionalLight("#ffffff", 1.4);
  sun.position.set(-4, 10, 6);
  scene.add(sun);

  // Unity [x, y, z] → three.js Vector3 (three.js z points toward the viewer).
  const v3 = ([x, y, z]) => new THREE.Vector3(x, y, -z);

  let home = { pos: [7.5, 6.8, -10], target: [3, 1.6, 3] };   // front-right view
  function view(pos, target) {
    home = { pos, target };
    camera.position.copy(v3(pos));
    controls.target.copy(v3(target));
    controls.update();
  }
  view(home.pos, home.target);

  function resize() {
    const w = el.clientWidth || 300;
    const h = el.clientHeight || 300;
    renderer.setSize(w, h, false);
    renderer.domElement.style.width = w + "px";
    renderer.domElement.style.height = h + "px";
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(el);
  resize();

  const frameFns = [];
  const clock = new THREE.Clock();
  renderer.setAnimationLoop(() => {
    const dt = Math.min(clock.getDelta(), 0.05);
    for (const fn of frameFns) fn(dt, clock.elapsedTime);
    controls.update();
    renderer.render(scene, camera);
  });

  // ---------- Drawing helpers ----------

  function line(points, color, { dashed = false, width = 1 } = {}) {
    const geo = new THREE.BufferGeometry().setFromPoints(points.map(v3));
    const mat = dashed
      ? new THREE.LineDashedMaterial({ color, dashSize: 0.18, gapSize: 0.12, linewidth: width })
      : new THREE.LineBasicMaterial({ color, linewidth: width });
    const obj = new THREE.Line(geo, mat);
    if (dashed) obj.computeLineDistances();
    scene.add(obj);
    return obj;
  }

  function label(text, at, { color = "#1d1b2e", size = 0.5, bold = true, onTop = false } = {}) {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    const tex = new THREE.CanvasTexture(canvas);
    tex.colorSpace = THREE.SRGBColorSpace;
    const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthTest: !onTop, transparent: true }));
    sprite.renderOrder = onTop ? 10 : 0;
    sprite.setText = (t) => {
      const px = 64;
      ctx.font = `${bold ? 800 : 600} ${px}px Nunito, system-ui, sans-serif`;
      const w = Math.ceil(ctx.measureText(t).width) + 24;
      canvas.width = w;
      canvas.height = px + 24;
      ctx.font = `${bold ? 800 : 600} ${px}px Nunito, system-ui, sans-serif`;
      ctx.fillStyle = color;
      ctx.textBaseline = "middle";
      ctx.fillText(t, 12, canvas.height / 2 + 2);
      tex.needsUpdate = true;
      sprite.scale.set(size * (w / canvas.height), size, 1);
    };
    sprite.setText(text);
    sprite.position.copy(v3(at));
    scene.add(sprite);
    return sprite;
  }

  function arrow(from, to, color, { head = 0.35 } = {}) {
    const a = v3(from), b = v3(to);
    const dir = b.clone().sub(a);
    const len = dir.length();
    const obj = new THREE.ArrowHelper(dir.normalize(), a, len, color, Math.min(head, len * 0.4), Math.min(head * 0.6, len * 0.25));
    obj.setTo = (f, t) => {
      const A = v3(f), B = v3(t), d = B.clone().sub(A), L = d.length();
      obj.position.copy(A);
      if (L > 1e-6) { obj.setDirection(d.normalize()); obj.setLength(L, Math.min(head, L * 0.4), Math.min(head * 0.6, L * 0.25)); }
    };
    scene.add(obj);
    return obj;
  }

  // Axes with arrows, names and tick numbers. names: { x, y, z } texts.
  function axes(length = 6, { names = { x: "x", y: "y", z: "z" }, ticks = true } = {}) {
    const L = length + 0.8;
    arrow([0, 0, 0], [L, 0, 0], AXIS_COLORS.x, { head: 0.4 });
    arrow([0, 0, 0], [0, L, 0], AXIS_COLORS.y, { head: 0.4 });
    arrow([0, 0, 0], [0, 0, L], AXIS_COLORS.z, { head: 0.4 });
    label(names.x, [L + 0.9, 0, 0], { color: AXIS_COLORS.x, size: 0.6 });
    label(names.y, [0, L + 0.5, 0], { color: AXIS_COLORS.y, size: 0.6 });
    label(names.z, [0, 0, L + 1.1], { color: AXIS_COLORS.z, size: 0.8 });
    if (ticks) {
      for (let i = 1; i <= length; i++) {
        label(String(i), [i, -0.35, 0], { color: AXIS_COLORS.x, size: 0.38 });
        label(String(i), [-0.35, i, 0], { color: AXIS_COLORS.y, size: 0.38 });
        label(String(i), [0, -0.35, i], { color: AXIS_COLORS.z, size: 0.38 });
      }
      label("0", [-0.3, -0.3, -0.3], { color: "#6b6880", size: 0.32 });
    }
  }

  // Ground grid on the x–z plane, from 0 to size.
  function ground(size = 6, color = "#d5e8cf") {
    for (let i = 0; i <= size; i++) {
      line([[i, 0, 0], [i, 0, size]], color);
      line([[0, 0, i], [size, 0, i]], color);
    }
    const plane = new THREE.Mesh(
      new THREE.PlaneGeometry(size, size),
      new THREE.MeshBasicMaterial({ color: "#ffffff", transparent: true, opacity: 0.6, side: THREE.DoubleSide }),
    );
    plane.rotation.x = -Math.PI / 2;
    plane.position.copy(v3([size / 2, -0.002, size / 2]));
    scene.add(plane);
  }

  function ball({ color = "#2F9E44", radius = 0.32, eyes = true } = {}) {
    const g = new THREE.Group();
    const body = new THREE.Mesh(
      new THREE.SphereGeometry(radius, 32, 24),
      new THREE.MeshStandardMaterial({ color, roughness: 0.45 }),
    );
    g.add(body);
    if (eyes) {
      const eyeMat = new THREE.MeshBasicMaterial({ color: "#ffffff" });
      for (const s of [-1, 1]) {
        const e = new THREE.Mesh(new THREE.SphereGeometry(radius * 0.17, 12, 8), eyeMat);
        e.position.set(s * radius * 0.36, radius * 0.22, radius * 0.88);
        g.add(e);
      }
    }
    scene.add(g);
    return g;
  }

  function coin({ color = "#f2b705", radius = 0.25 } = {}) {
    const m = new THREE.Mesh(
      new THREE.CylinderGeometry(radius, radius, 0.07, 32),
      new THREE.MeshStandardMaterial({ color, metalness: 0.4, roughness: 0.35, emissive: "#6b4a00", emissiveIntensity: 0.25 }),
    );
    m.rotation.x = Math.PI / 2;
    scene.add(m);
    return m;
  }

  function place(obj, p) { obj.position.copy(v3(p)); }

  return {
    THREE, scene, camera, renderer, controls,
    v3, view, resetView: () => view(home.pos, home.target),
    line, label, arrow, axes, ground, ball, coin, place,
    onFrame: (fn) => frameFns.push(fn),
  };
}
