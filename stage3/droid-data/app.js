(() => {
  const $ = s => document.querySelector(s);
  const I18N = window.DROID_I18N[document.documentElement.lang];
  const tr = (key, values = {}) => I18N.labels[key].replace(/\{(\w+)\}/g, (_, name) => values[name]);
  const NS = "http://www.w3.org/2000/svg";
  let DATA = null, C = null, step = 0, timer = null;
  const sprites = {};
  const updaters = [];

  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const f = (v, n) => (v < 0 ? "−" : "") + Math.abs(v).toFixed(n);
  const el = (tag, attrs = {}, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };

  const META = I18N.META;
  const TEXT = I18N.TEXT;

  function renderTree() {
    const u = C.uuid, m = META[C.key];
    const rows = [
      ["", u + "/", "", tr("episode_id")],
      ["star", "├─ trajectory.h5", m.size, tr("trajectory_file")],
      ["", "├─ " + m.file, "1.7 KB", tr("metadata_file")],
      ["", "└─ recordings/", "", ""],
      ["", "   ├─ MP4/22008760.mp4", "", tr("camera_one")],
      ["", "   ├─ MP4/24400334.mp4", "", tr("camera_two")],
      ["", "   └─ SVO/22008760.svo, 24400334.svo", "", tr("stereo_file")],
    ];
    $("#tree").innerHTML = rows.map(([c, a, s, b]) =>
      `<tr class="${c}"><td>${a}</td><td class="size">${s}</td><td>${b}</td></tr>`).join("");
    $("#meta").innerHTML = m.meta.map(([k, v, d]) =>
      `<dt>${k}</dt><dd><span class="mono">${v}</span><br><span class="muted">${d}</span></dd>`).join("");
  }

  function renderRow7() {
    const s = C.keys[2].step;
    const vals = [["x", C.x[s], 3], ["y", C.y[s], 3], ["z", C.z[s], 3], ["roll", C.roll[s], 2], ["pitch", C.pitch[s], 2], ["yaw", C.yaw[s], 2], [tr("gripper_short"), C.go[s], 2]];
    $("#row7").innerHTML = vals.map(([k, v, n]) => `<div><div class="v">${f(v, n)}</div><div class="k">${k}</div></div>`).join("");
    $("#row7-when").textContent = tr("row_when", { case: C.key, step: s, time: C.t[s].toFixed(2), label: C.keys[2].label });
    $("#intro-len").textContent = tr("intro_length", { case: C.key, duration: C.duration.toFixed(1), total: C.T });
    $("#tbl-len").textContent = tr("table_length", { case: C.key, total: C.T });
  }

  function renderKeys() {
    const cam = C.cam, rows = Math.ceil(100 / cam.cols);
    $("#keys").innerHTML = C.keys.map(({ step: s, label }) => {
      const fr = cam.s2f[s], col = fr % cam.cols, row = Math.floor(fr / cam.cols);
      const bg = `background-image:url(${cam.sprite});background-size:${cam.cols * 100}% ${rows * 100}%;background-position:${col / (cam.cols - 1) * 100}% ${row / (rows - 1) * 100}%`;
      return `<tr data-step="${s}" tabindex="0"><td class="l"><div class="thumb" style="${bg}"></div></td><td>${s}</td><td>${C.t[s].toFixed(2)}</td>` +
        `<td>${f(C.x[s], 3)}</td><td>${f(C.y[s], 3)}</td><td>${f(C.z[s], 3)}</td><td>${f(C.roll[s], 2)}</td><td>${f(C.pitch[s], 2)}</td><td>${f(C.yaw[s], 2)}</td>` +
        `<td>${C.ga[s].toFixed(2)}</td><td>${C.go[s].toFixed(2)}</td><td class="l">${label}</td></tr>`;
    }).join("");
    for (const tr of $("#keys").children) {
      const go = () => { seek(+tr.dataset.step); $("#viewer").scrollIntoView({ behavior: "smooth", block: "start" }); };
      tr.addEventListener("click", go);
      tr.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } });
    }
  }

  function renderPhases() {
    $("#phases").innerHTML = C.phases.map((p, i) => `<button type="button" data-i="${i}">${p.name}</button>`).join("");
    for (const b of $("#phases").children) b.addEventListener("click", () => { stop(); seek(C.phases[+b.dataset.i].a + (+b.dataset.i === 0 ? 0 : 2)); });
  }

  // ---------- charts ----------
  const W = 440, H = 190, L = document.documentElement.lang === "en" ? 64 : 40, R = 10, T = 10, B = 26;

  function timeChart(host, { series, ymin, ymax, yticks, yfmt }) {
    host.innerHTML = "";
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": host.closest(".chart").querySelector("h3").textContent }, host);
    const tmax = C.t[C.T - 1];
    const X = t => L + t / tmax * (W - L - R);
    const Y = v => T + (1 - (v - ymin) / (ymax - ymin)) * (H - T - B);
    C.phases.forEach((p, i) => {
      const x0 = X(C.t[p.a]), x1 = X(C.t[Math.min(p.b + 1, C.T - 1)]);
      el("rect", { x: x0, y: T, width: Math.max(0, x1 - x0), height: H - T - B, class: i % 2 ? "band-b" : "band-a" }, svg);
    });
    for (const v of yticks) {
      el("line", { x1: L, x2: W - R, y1: Y(v), y2: Y(v), class: "grid" }, svg);
      el("text", { x: L - 6, y: Y(v) + 3.5, "text-anchor": "end" }, svg).textContent = yfmt(v);
    }
    for (let s = 0; s <= Math.floor(tmax); s++) {
      el("line", { x1: X(s), x2: X(s), y1: H - B, y2: H - B + 4, class: "axis" }, svg);
      el("text", { x: X(s), y: H - B + 15, "text-anchor": "middle" }, svg).textContent = s + (s === Math.floor(tmax) ? " " + tr("seconds") : "");
    }
    el("line", { x1: L, x2: W - R, y1: H - B, y2: H - B, class: "axis" }, svg);
    for (const sr of series) {
      const d = sr.vals.map((v, i) => `${i ? "L" : "M"}${X(C.t[i]).toFixed(1)},${Y(v).toFixed(1)}`).join("");
      el("path", { d, fill: "none", stroke: sr.color, "stroke-width": sr.dash ? 1.6 : 2.2, "stroke-dasharray": sr.dash ? "4 3" : "none", "stroke-linejoin": "round" }, svg);
    }
    const cur = el("line", { y1: T, y2: H - B, class: "cursor" }, svg);
    const dots = series.filter(s => !s.dash).map(sr => ({ sr, c: el("circle", { r: 4, fill: sr.color, stroke: "var(--surface)", "stroke-width": 1.5 }, svg) }));
    svg.addEventListener("click", e => {
      const p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY;
      const q = p.matrixTransform(svg.getScreenCTM().inverse());
      const t = (q.x - L) / (W - L - R) * tmax;
      let best = 0; C.t.forEach((v, i) => { if (Math.abs(v - t) < Math.abs(C.t[best] - t)) best = i; });
      stop(); seek(best);
    });
    updaters.push(s => {
      const x = X(C.t[s]); cur.setAttribute("x1", x); cur.setAttribute("x2", x);
      for (const { sr, c } of dots) { c.setAttribute("cx", x); c.setAttribute("cy", Y(sr.vals[s])); }
    });
  }

  function topChart(host, interactive) {
    host.innerHTML = "";
    const w = W, h = 270, pad = 30;
    const svg = el("svg", { viewBox: `0 0 ${w} ${h}`, role: "img", "aria-label": tr("top_view") }, host);
    const hs = C.y.map(v => -v), vs = C.x;
    let hmin = Math.min(0, ...hs) - .06, hmax = Math.max(0, ...hs) + .06, vmin = -.04, vmax = Math.max(...vs) + .05;
    const k = Math.min((w - 2 * pad) / (hmax - hmin), (h - 2 * pad) / (vmax - vmin));
    const ox = (w - k * (hmax - hmin)) / 2, oy = (h - k * (vmax - vmin)) / 2;
    const PX = v => ox + (v - hmin) * k, PY = v => h - oy - (v - vmin) * k;
    // 10 cm grid
    for (let g = Math.ceil(hmin * 10) / 10; g <= hmax; g += .1) el("line", { x1: PX(g), x2: PX(g), y1: PY(vmin), y2: PY(vmax), class: "grid" }, svg);
    for (let g = 0; g <= vmax; g += .1) el("line", { x1: PX(hmin), x2: PX(hmax), y1: PY(g), y2: PY(g), class: "grid" }, svg);
    // base and axes
    const bx = PX(0), by = PY(0);
    el("rect", { x: bx - 9, y: by - 9, width: 18, height: 18, rx: 3, fill: "var(--sunk)", stroke: "var(--muted)" }, svg);
    el("text", { x: bx, y: by + 22, "text-anchor": "middle" }, svg).textContent = tr("base_origin");
    const arrow = (x2, y2, label, lx, ly, anchor) => {
      el("line", { x1: bx, y1: by, x2, y2, stroke: "var(--muted)", "stroke-width": 1.4, "marker-end": "url(#ah)" }, svg);
      el("text", { x: lx, y: ly, "text-anchor": anchor }, svg).textContent = label;
    };
    const defs = el("defs", {}, svg), mk = el("marker", { id: "ah", viewBox: "0 0 8 8", refX: 7, refY: 4, markerWidth: 7, markerHeight: 7, orient: "auto" }, defs);
    el("path", { d: "M0,0 L8,4 L0,8 z", fill: "var(--muted)" }, mk);
    arrow(bx, PY(.12), tr("axis_x"), bx + 5, PY(.12) + 4, "start");
    arrow(PX(-.12), by, tr("axis_y"), PX(-.12), by - 6, "middle");
    el("text", { x: w - 6, y: h - 6, "text-anchor": "end" }, svg).textContent = tr("grid_scale");
    // path colored by gripper command
    for (let i = 1; i < C.T; i++) {
      el("line", { x1: PX(hs[i - 1]), y1: PY(vs[i - 1]), x2: PX(hs[i]), y2: PY(vs[i]), stroke: C.ga[i] >= .5 ? "var(--closed)" : "var(--open)", "stroke-width": 3, "stroke-linecap": "round" }, svg);
    }
    const s0 = C.phases[1].a;
    el("circle", { cx: PX(hs[s0]), cy: PY(vs[s0]), r: 3, fill: "var(--muted)" }, svg);
    el("text", { x: PX(hs[s0]) + 7, y: PY(vs[s0]) + 4 }, svg).textContent = tr("start");
    if (!interactive) {
      const s = C.keys[2].step;
      el("circle", { cx: PX(hs[s]), cy: PY(vs[s]), r: 5.5, fill: "var(--closed)", stroke: "var(--surface)", "stroke-width": 2 }, svg);
      el("text", { x: PX(hs[s]) - 8, y: PY(vs[s]) - 8, "text-anchor": "end" }, svg).textContent = tr("step", { step: s });
      return;
    }
    const dot = el("circle", { r: 6, stroke: "var(--surface)", "stroke-width": 2 }, svg);
    svg.addEventListener("click", e => {
      const p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY;
      const q = p.matrixTransform(svg.getScreenCTM().inverse());
      let best = 0, bd = 1e9;
      for (let i = 0; i < C.T; i++) { const d = (PX(hs[i]) - q.x) ** 2 + (PY(vs[i]) - q.y) ** 2; if (d < bd) { bd = d; best = i; } }
      stop(); seek(best);
    });
    updaters.push(s => { dot.setAttribute("cx", PX(hs[s])); dot.setAttribute("cy", PY(vs[s])); dot.setAttribute("fill", C.ga[s] >= .5 ? "var(--closed)" : "var(--open)"); });
  }

  function renderCharts() {
    updaters.length = 0;
    const cm = a => a.map(v => v * 100);
    const zs = cm(C.z).concat(cm(C.az));
    const zmin = Math.floor(Math.min(...zs) / 10) * 10, zmax = Math.ceil(Math.max(...zs) / 10) * 10;
    const rng = (a, b, st) => { const o = []; for (let v = a; v <= b + 1e-9; v += st) o.push(Math.round(v)); return o; };
    timeChart($("#c-z"), { series: [{ vals: cm(C.az), color: "var(--cmd)", dash: true }, { vals: cm(C.z), color: "var(--accent)" }],
      ymin: zmin, ymax: zmax, yticks: rng(zmin, zmax, 10), yfmt: v => v + " cm" });
    const xy = cm(C.x).concat(cm(C.y), cm(C.ax), cm(C.ay));
    const amin = Math.floor(Math.min(...xy) / 10) * 10, amax = Math.ceil(Math.max(...xy) / 10) * 10;
    timeChart($("#c-xy"), { series: [{ vals: cm(C.ax), color: "var(--cmd)", dash: true }, { vals: cm(C.ay), color: "var(--cmd)", dash: true },
      { vals: cm(C.x), color: "var(--accent)" }, { vals: cm(C.y), color: "var(--y)" }],
      ymin: amin, ymax: amax, yticks: rng(amin, amax, 10), yfmt: v => v + " cm" });
    const host = $("#c-xy");
    const lg = document.createElement("div"); lg.className = "legend";
    lg.innerHTML = `<span><i style="background:var(--accent)"></i>${tr("x_motion")}</span><span><i style="background:var(--y)"></i>${tr("y_motion")}</span><span><i style="background:repeating-linear-gradient(90deg,var(--cmd) 0 4px,transparent 4px 7px)"></i>${tr("command")}</span>`;
    host.appendChild(lg);
    timeChart($("#c-g"), { series: [{ vals: C.ga, color: "var(--cmd)", dash: true }, { vals: C.go, color: "var(--closed)" }],
      ymin: 0, ymax: 1, yticks: [0, .5, 1], yfmt: v => v === 0 ? tr("open_zero") : v === 1 ? tr("closed_one") : "0.5" });
    topChart($("#c-top"), true);
    topChart($("#topview-static"), false);
  }

  // ---------- frame canvas ----------
  function loadSprite(c) {
    if (sprites[c.key]) return sprites[c.key];
    const img = new Image();
    img.onload = () => { if (C && C.key === c.key) { draw(); } };
    img.onerror = () => { $("#status").classList.add("err"); $("#status").textContent = tr("image_error"); };
    img.src = c.cam.sprite;
    sprites[c.key] = img;
    return img;
  }

  function draw() {
    const cv = $("#cv"), ctx = cv.getContext("2d"), Wc = cv.width, Hc = cv.height;
    const cam = C.cam, img = sprites[C.key], fr = cam.s2f[step];
    ctx.fillStyle = "#000"; ctx.fillRect(0, 0, Wc, Hc);
    if (img && img.complete && img.naturalWidth) {
      ctx.drawImage(img, (fr % cam.cols) * cam.cw, Math.floor(fr / cam.cols) * cam.ch, cam.cw, cam.ch, 0, 0, Wc, Hc);
    } else {
      ctx.fillStyle = "#888"; ctx.font = "28px sans-serif"; ctx.fillText(tr("image_loading"), 30, 50);
    }
    const P = cam.proj.map(p => p ? [p[0] * Wc, p[1] * Hc] : null);
    const open = css("--ov-open"), closed = css("--ov-closed"), fut = css("--ov-future");
    ctx.lineCap = "round"; ctx.lineJoin = "round";
    ctx.setLineDash([10, 9]); ctx.lineWidth = 3; ctx.strokeStyle = fut; ctx.beginPath();
    let started = false;
    for (let i = step; i < C.T; i++) { if (!P[i]) { started = false; continue; } if (!started) { ctx.moveTo(...P[i]); started = true; } else ctx.lineTo(...P[i]); }
    ctx.stroke(); ctx.setLineDash([]);
    ctx.lineWidth = 5;
    for (let i = 1; i <= step; i++) {
      if (!P[i] || !P[i - 1]) continue;
      ctx.strokeStyle = C.ga[i] >= .5 ? closed : open;
      ctx.beginPath(); ctx.moveTo(...P[i - 1]); ctx.lineTo(...P[i]); ctx.stroke();
    }
    if (P[step]) {
      ctx.beginPath(); ctx.arc(P[step][0], P[step][1], 11, 0, Math.PI * 2);
      ctx.fillStyle = C.ga[step] >= .5 ? closed : open; ctx.fill();
      ctx.lineWidth = 3; ctx.strokeStyle = "#fff"; ctx.stroke();
    }
    $("#cap").textContent = P[step] && (P[step][1] < 0) ? tr("above_frame") : tr("frame_caption", { step });
  }

  // ---------- rotation helpers ----------
  function rot(r, p, y) {
    const cr = Math.cos(r), sr = Math.sin(r), cp = Math.cos(p), sp = Math.sin(p), cy = Math.cos(y), sy = Math.sin(y);
    return [[cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr], [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr], [-sp, cp * sr, cp * cr]];
  }
  function angleBetween(A, Bm) {
    let tr = 0; for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) tr += A[j][i] * Bm[j][i];
    return Math.acos(Math.max(-1, Math.min(1, (tr - 1) / 2))) * 180 / Math.PI;
  }

  function gripWords(s) {
    const a = C.ga[s], o = C.go[s];
    if (a < .05 && o < .05) return tr("fully_open");
    if (a > o + .12) return tr("closing");
    if (a < o - .12) return tr("opening");
    if (o > .3) return tr("holding");
    return tr("mostly_open");
  }

  function seek(s) {
    step = Math.max(0, Math.min(C.T - 1, s));
    $("#slider").value = step;
    $("#slabel").textContent = `${step} / ${C.T - 1}`;
    $("#now-step").innerHTML = `${tr("step", { step })}<small>${tr("total_steps", { total: C.T })}</small>`;
    $("#now-time").textContent = tr("time", { time: C.t[step].toFixed(2) });
    const pi = C.phases.findIndex(p => step >= p.a && step <= p.b);
    const ph = C.phases[pi];
    $("#now-phase").innerHTML = `<b>${ph.name}</b> · ${ph.desc}${C.skip[step] ? '<br><span class="muted">' + tr("skip_step") + '</span>' : ""}`;
    [...$("#phases").children].forEach((b, i) => b.setAttribute("aria-current", i === pi ? "true" : "false"));
    const x = C.x[step], y = C.y[step], z = C.z[step];
    const deg = angleBetween(rot(C.roll[0], C.pitch[0], C.yaw[0]), rot(C.roll[step], C.pitch[step], C.yaw[step]));
    $("#decode").innerHTML = [
      ["x", f(x, 3) + " m", tr("position_x", { value: (x * 100).toFixed(1) })],
      ["y", f(y, 3) + " m", tr(y >= 0 ? "position_left" : "position_right", { value: Math.abs(y * 100).toFixed(1) })],
      ["z", f(z, 3) + " m", tr("position_z", { value: (z * 100).toFixed(1) })],
      null,
      ["roll", f(C.roll[step], 2), tr("roll_explanation")],
      ["pitch", f(C.pitch[step], 2), ""],
      ["yaw", f(C.yaw[step], 2), tr("rotation_explanation", { value: deg.toFixed(0) })],
    ].map(r => r ? `<span class="k">${r[0]}</span><span class="v">${r[1]}</span><span class="h">${r[2]}</span>` : '<span class="sep"></span>').join("");
    const bar = (label, v, color) => `<div class="bar"><span>${label}</span><span class="track"><span class="fill" style="width:${(v * 100).toFixed(1)}%;background:${color}"></span></span><span class="num">${v.toFixed(2)}</span></div>`;
    $("#bars").innerHTML = `<div class="muted" style="font-size:13px">${tr("gripper")}: <b style="color:var(--ink)">${gripWords(step)}</b></div>` +
      bar(tr("command"), C.ga[step], "var(--cmd)") + bar(tr("measured"), C.go[step], "var(--closed)") + `<div class="bar-scale"><span>${tr("open_zero")}</span><span>${tr("closed_one")}</span></div>`;
    for (const tr of $("#keys").children) tr.classList.toggle("on", +tr.dataset.step === step);
    for (const u of updaters) u(step);
    draw();
  }

  function stop() { if (timer) { clearInterval(timer); timer = null; $("#play").textContent = tr("play"); } }
  function play() {
    if (!C) return;
    if (timer) return stop();
    if (step >= C.T - 1) seek(0);
    $("#play").textContent = tr("pause");
    timer = setInterval(() => { if (step >= C.T - 1) return stop(); seek(step + 1); }, 1000 / C.hz);
  }

  function pick(key) {
    stop();
    if (!DATA) return;
    const raw = DATA.cases.find(c => c.key === key);
    const labels = I18N.cases[key];
    C = { ...raw,
      phases: raw.phases.map((phase, i) => ({ ...phase, ...labels.phases[i] })),
      keys: raw.keys.map((row, i) => ({ ...row, label: labels.keys[i] })),
    };
    for (const b of document.querySelectorAll(".switch button")) b.setAttribute("aria-pressed", b.dataset.case === key ? "true" : "false");
    $("#slider").max = C.T - 1;
    loadSprite(C);
    renderTree(); renderRow7(); renderKeys(); renderPhases(); renderCharts();
    $("#lead-text").textContent = TEXT[key].lead;
    $("#grip-text").textContent = TEXT[key].grip;
    seek(C.keys[2].step);
    for (const link of document.querySelectorAll(".languages a")) link.hash = key === "B" ? "case-b" : "case-a";
    try { history.replaceState(null, "", key === "B" ? "#case-b" : "#case-a"); } catch (e) {}
  }

  function renderFields(fields) {
    $("#flist").innerHTML = fields.map(([p, sh]) => `<tr><td>${p}</td><td>${Array.isArray(sh) ? sh.join(" × ") : sh}</td></tr>`).join("");
  }

  $("#slider").addEventListener("input", e => { if (C) { stop(); seek(+e.target.value); } });
  $("#play").addEventListener("click", play);
  for (const b of document.querySelectorAll(".switch button")) b.addEventListener("click", () => pick(b.dataset.case));
  window.addEventListener("hashchange", () => { const k = location.hash === "#case-b" ? "B" : "A"; if (DATA && C && C.key !== k) pick(k); });
  if (window.matchMedia) matchMedia("(prefers-color-scheme: dark)").addEventListener?.("change", () => C && draw());

  fetch("cases.json").then(r => { if (!r.ok) throw new Error(r.status); return r.json(); }).then(d => {
    DATA = d;
    renderFields(d.fields);
    pick(location.hash === "#case-b" ? "B" : "A");
  }).catch(err => {
    $("#status").classList.add("err");
    $("#status").textContent = tr("data_error", { message: err.message });
  });
})();
