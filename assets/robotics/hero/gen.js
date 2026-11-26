// Hero image for the robotics branch README: one Real2Sim2Real loop (Act -> Build -> Learn -> Apply)
// around a real robot and its simulated twin, with the coding agent between the two worlds.
// Usage (from the repository root):  NODE_PATH=$(npm root -g) node assets/robotics/hero/gen.js
// Writes assets/robotics/hero/hero-{light,dark}.svg and renders hero-{light,dark}.png at 2x with Playwright.
// Fonts: Inter Display, Inter and JetBrains Mono must be installed where the PNG is rendered.
const fs = require('fs');
const path = require('path');
const OUT = __dirname;
const DISP = `'Inter Display', Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif`;
const SANS = `Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif`;
const MONO = `'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`;

// ---- geometry (1200-unit grid; the README shows it at about 830 px and 360 px wide)
const W = 1200, H = 700, M = 44;
const FX = M, FY = 108, FW = W - 2 * M, FH = 556;     // the two-world frame
const MID = W / 2;                                    // boundary between real (left) and sim (right)
const LX0 = 132, LX1 = W - 132, LY0 = 198, LY1 = 574; // the loop, a rounded rectangle
const LR = 70;                                        // loop corner radius
const SX = [330, W - 330];                            // station columns
const AY = 392;                                       // agent centre y
const FLOOR = 492;                                    // bench level of both robots
const BASE = [262, W - 262];                          // robot base x (real, sim)

const themes = {
  light: {
    bg: '#FFFFFF', ink: '#14181F', sub: '#57606A', rule: '#D0D7DE', card: '#FFFFFF',
    agentFill: '#14181F', agentInk: '#FFFFFF',
    real: { line: '#C2500A', text: '#B34707', panel: '#FFF4E8', body: '#FFD9B5', pillInk: '#FFFFFF' },
    sim: { line: '#0B6FC2', text: '#0A63AD', panel: '#EDF6FF', body: '#EDF6FF', pillInk: '#FFFFFF', grid: '#0B6FC2', gridOp: 0.11 },
    shadow: 0.12, glow: 0,
  },
  dark: {
    bg: '#0A0E17', ink: '#F2F5FA', sub: '#A3AEC2', rule: '#2A3348', card: '#0A0E17',
    agentFill: '#F2F5FA', agentInk: '#0A0E17',
    real: { line: '#FF9F4A', text: '#FFAE66', panel: '#1F160E', body: '#6B3A12', pillInk: '#1B0E02' },
    sim: { line: '#4CB8FF', text: '#6CC5FF', panel: '#0B1B2E', body: '#0B1B2E', pillInk: '#03131F', grid: '#4CB8FF', gridOp: 0.13 },
    shadow: 0, glow: 0.55,
  },
};

// Stations, clockwise from top-left: real -> sim -> sim -> real.
const steps = [
  { n: 1, word: 'ACT', cap: 'drive robots with code', world: 'real', x: SX[0], y: LY0 },
  { n: 2, word: 'BUILD', cap: 'build worlds to practise in', world: 'sim', x: SX[1], y: LY0 },
  { n: 3, word: 'LEARN', cap: 'improve from experience', world: 'sim', x: SX[1], y: LY1 },
  { n: 4, word: 'APPLY', cap: 'reach the physical world', world: 'real', x: SX[0], y: LY1 },
];

function build(key) {
  const t = themes[key];
  const o = [];
  const S = (c, w = 2.4) => `fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"`;
  const text = (x, y, s, { f = SANS, size = 22, w = 500, fill = t.ink, anchor = 'start', ls = 0 } = {}) =>
    `<text x="${x}" y="${y}" font-family="${f}" font-size="${size}" font-weight="${w}" fill="${fill}" text-anchor="${anchor}"${ls ? ` letter-spacing="${ls}"` : ''}>${s}</text>`;
  const lift = t.shadow ? ` filter="url(#lift)"` : '';

  o.push(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Multimodal agentic coding, robotics branch: a Real2Sim2Real loop of act, build, learn and apply around a real robot and its simulated twin">`);
  o.push(`<defs>`);
  o.push(`<linearGradient id="loop" gradientUnits="userSpaceOnUse" x1="${SX[0] + 90}" x2="${SX[1] - 90}"><stop offset="0" stop-color="${t.real.line}"/><stop offset="1" stop-color="${t.sim.line}"/></linearGradient>`);
  o.push(`<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse" x="${MID}" y="${FY}"><path d="M28 0 H0 V28" fill="none" stroke="${t.sim.grid}" stroke-width="1" opacity="${t.sim.gridOp}"/></pattern>`);
  o.push(`<clipPath id="frame"><rect x="${FX}" y="${FY}" width="${FW}" height="${FH}" rx="28"/></clipPath>`);
  if (t.shadow) o.push(`<filter id="lift" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#1B2A4A" flood-opacity="${t.shadow}"/></filter>`);
  if (t.glow) o.push(`<filter id="glow" x="-10%" y="-20%" width="120%" height="140%"><feGaussianBlur stdDeviation="9"/></filter>`);
  o.push(`</defs>`);
  o.push(`<rect width="${W}" height="${H}" fill="${t.bg}"/>`);

  // ---- header: the upstream name, a branch mark, and this branch
  {
    const y = 70;
    o.push(text(M, y, 'Multimodal Agentic Coding', { f: DISP, size: 44, w: 700, ls: -0.6 }));
    const bx = M + 566, c = t.real.line;             // generic branch mark: a line that forks
    o.push(`<g transform="translate(${bx} ${y - 16})" ${S(c, 3.4)}><path d="M-9 -15 V15 M-9 5 C-9 -4 9 -1 9 -10"/><circle cx="-9" cy="-19" r="4.500" fill="${t.bg}"/><circle cx="-9" cy="19" r="4.500" fill="${t.bg}"/><circle cx="9" cy="-14" r="4.500" fill="${t.bg}"/></g>`);
    o.push(text(bx + 28, y, 'Robotics', { f: DISP, size: 44, w: 700, fill: t.real.text, ls: -0.6 }));
    o.push(text(W - M, y - 4, 'REAL2SIM2REAL', { f: MONO, size: 21, w: 700, fill: t.sub, anchor: 'end', ls: 2.2 }));
  }

  // ---- two worlds in one frame
  o.push(`<g clip-path="url(#frame)">`);
  o.push(`<rect x="${FX}" y="${FY}" width="${MID - FX}" height="${FH}" fill="${t.real.panel}"/>`);
  o.push(`<rect x="${MID}" y="${FY}" width="${MID - FX}" height="${FH}" fill="${t.sim.panel}"/>`);
  o.push(`<rect x="${MID}" y="${FY}" width="${MID - FX}" height="${FH}" fill="url(#grid)"/>`);
  o.push(`</g>`);
  o.push(`<path d="M${MID} ${FY} V${FY + FH}" stroke="${t.sub}" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round" opacity="0.7"/>`);
  o.push(text(MID - 26, 262, 'REAL WORLD', { f: MONO, size: 21, w: 700, fill: t.real.text, anchor: 'end', ls: 2 }));
  o.push(text(MID + 26, 262, 'SIMULATION', { f: MONO, size: 21, w: 700, fill: t.sim.text, ls: 2 }));

  // ---- the loop
  const loopD = `M${LX0 + LR} ${LY0} H${LX1 - LR} A${LR} ${LR} 0 0 1 ${LX1} ${LY0 + LR} V${LY1 - LR} A${LR} ${LR} 0 0 1 ${LX1 - LR} ${LY1} H${LX0 + LR} A${LR} ${LR} 0 0 1 ${LX0} ${LY1 - LR} V${LY0 + LR} A${LR} ${LR} 0 0 1 ${LX0 + LR} ${LY0} Z`;
  if (t.glow) o.push(`<path d="${loopD}" fill="none" stroke="url(#loop)" stroke-width="6" opacity="${t.glow}" filter="url(#glow)"/>`);
  o.push(`<path d="${loopD}" fill="none" stroke="url(#loop)" stroke-width="4.500"/>`);
  const head = (x, y, rot, c) => `<g transform="translate(${x} ${y}) rotate(${rot})"><path d="M-9 -9.500 L4 0 L-9 9.500" ${S(c, 4.500)}/></g>`;
  o.push(head(LX1, (LY0 + LY1) / 2, 90, t.sim.line), head(LX0, (LY0 + LY1) / 2, -90, t.real.line));
  o.push(head(SX[0] + 134, LY0, 0, t.real.line), head(SX[1] - 134, LY1, 180, t.sim.line));
  o.push(head(SX[1] - 150, LY0, 0, t.sim.line), head(SX[0] + 150, LY1, 180, t.real.line));

  // ---- robots: the real one is solid, its simulated twin is a dashed wireframe (mirrored)
  const robot = (bx, world, mirror) => {
    const w = t[world], sim = world === 'sim';
    const dash = sim ? ` stroke-dasharray="7 5.500"` : '';
    const sw = sim ? 2.8 : 3.2;
    const body = `fill="${w.body}" stroke="${w.line}" stroke-width="${sw}" stroke-linejoin="round" stroke-linecap="round"${dash}`;
    const link = (x1, y1, x2, y2, th) => {
      const len = Math.hypot(x2 - x1, y2 - y1), ang = (Math.atan2(y2 - y1, x2 - x1) * 180) / Math.PI;
      return `<rect x="${-th / 2}" y="${-th / 2}" width="${(len + th).toFixed(1)}" height="${th}" rx="${th / 2}" transform="translate(${x1} ${y1}) rotate(${ang.toFixed(2)})" ${body}/>`;
    };
    const joint = (x, y, r) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${t.card}" stroke="${w.line}" stroke-width="${sw}"/><circle cx="${x}" cy="${y}" r="${sim ? 2.6 : 3.4}" fill="${w.line}"/>`;
    const g = [];
    g.push(`<g transform="translate(${bx} ${FLOOR})${mirror ? ' scale(-1 1)' : ''}">`);
    // floor: a solid bench in the real world, a perspective grid in simulation
    if (sim) {
      g.push(`<path d="M-96 0 H236 M-116 20 H256 M-142 46 H282" ${S(w.line, 2)} stroke-dasharray="7 5.500" opacity="0.75"/>`);
      g.push(`<path d="M-40 0 L-66 46 M30 0 L26 46 M100 0 L118 46 M170 0 L210 46" ${S(w.line, 2)} stroke-dasharray="7 5.500" opacity="0.75"/>`);
    } else {
      g.push(`<path d="M-96 0 H236" ${S(w.line, 3.2)}/>`);
      g.push(`<path d="M-78 10 L-90 24 M-46 10 L-58 24 M-14 10 L-26 24 M18 10 L6 24 M50 10 L38 24 M82 10 L70 24 M114 10 L102 24 M146 10 L134 24 M178 10 L166 24 M210 10 L198 24" ${S(w.line, 2.2)} opacity="0.55"/>`);
    }
    // object on the bench
    g.push(`<rect x="134" y="-38" width="38" height="38" rx="5" ${body}/>`);
    // pedestal
    g.push(`<path d="M-36 0 V-14 Q-36 -22 -28 -22 H28 Q36 -22 36 -14 V0 Z" ${body}/>`);
    g.push(`<rect x="-19" y="-48" width="38" height="26" rx="5" ${body}/>`);
    // links: shoulder -> elbow -> wrist -> hand
    g.push(link(0, -58, -34, -150, 30), link(-34, -150, 96, -186, 24), link(96, -186, 153, -104, 18));
    // gripper
    g.push(`<path d="M135 -66 V-88 Q135 -94 141 -94 H165 Q171 -94 171 -88 V-66" ${S(w.line, sim ? 3 : 4.200)}${dash}/>`);
    g.push(joint(0, -58, 12), joint(-34, -150, 11), joint(96, -186, 9.500));
    g.push(`</g>`);
    return g.join('');
  };
  o.push(robot(BASE[0], 'real', false), robot(BASE[1], 'sim', true));

  // ---- the coding agent sits on the boundary: code goes out to both worlds, observations come back
  {
    const r = 48, x0 = 58, x1 = 150;
    [-1, 1].forEach((d) => {
      const c = d < 0 ? t.real : t.sim;
      const a = MID + d * x0, b = MID + d * x1;
      o.push(`<path d="M${a} ${AY - 13} H${b} M${b - d * 9} ${AY - 21} L${b} ${AY - 13} L${b - d * 9} ${AY - 5}" ${S(c.line, 3)}/>`);
      o.push(`<path d="M${b} ${AY + 13} H${a} M${a + d * 9} ${AY + 5} L${a} ${AY + 13} L${a + d * 9} ${AY + 21}" ${S(c.line, 3)}/>`);
      o.push(text((a + b) / 2 + d * 2, AY - 29, 'code', { f: MONO, size: 19, w: 700, fill: c.text, anchor: 'middle' }));
      o.push(text((a + b) / 2 + d * 2, AY + 42, 'observe', { f: MONO, size: 19, w: 700, fill: c.text, anchor: 'middle' }));
    });
    o.push(`<circle cx="${MID}" cy="${AY}" r="${r}" fill="${t.agentFill}" stroke="${t.bg}" stroke-width="5"${lift}/>`);
    o.push(`<g transform="translate(${MID} ${AY + 4}) scale(1.22)" ${S(t.agentInk, 2.3)}><rect x="-20" y="-13" width="40" height="29" rx="9"/><path d="M0 -13 V-21"/><circle cx="0" cy="-24" r="3"/><path d="M-8 -1 V4 M8 -1 V4"/></g>`);
    const tw = 12 * 19 * 0.6 + 30;
    o.push(`<rect x="${MID - tw / 2}" y="${AY + r + 26}" width="${tw}" height="34" rx="17" fill="${t.card}" stroke="${t.rule}" stroke-width="2"/>`);
    o.push(text(MID, AY + r + 49.500, 'coding agent', { f: MONO, size: 19, w: 700, fill: t.ink, anchor: 'middle' }));
  }

  // ---- crossings between the worlds
  [['real2sim', LY0], ['sim2real', LY1]].forEach(([s, y]) => {
    const tw = s.length * 20 * 0.6 + 32;
    o.push(`<rect x="${MID - tw / 2}" y="${y - 19}" width="${tw}" height="38" rx="19" fill="${t.card}" stroke="${t.ink}" stroke-width="2.400"/>`);
    o.push(text(MID, y + 7, s, { f: MONO, size: 20, w: 700, fill: t.ink, anchor: 'middle' }));
  });

  // ---- stations
  steps.forEach((st) => {
    const w = t[st.world], top = st.y === LY0;
    const pw = 64 + st.word.length * 21.500, ph = 52;
    o.push(`<rect x="${st.x - pw / 2}" y="${st.y - ph / 2}" width="${pw}" height="${ph}" rx="${ph / 2}" fill="${w.line}" stroke="${t.bg}" stroke-width="4"${lift}/>`);
    o.push(`<circle cx="${st.x - pw / 2 + 27}" cy="${st.y}" r="15" fill="${w.pillInk}"/>`);
    o.push(text(st.x - pw / 2 + 27, st.y + 7, st.n, { f: MONO, size: 20, w: 800, fill: w.line, anchor: 'middle' }));
    o.push(text(st.x + 19, st.y + 10, st.word, { f: DISP, size: 29, w: 800, fill: w.pillInk, anchor: 'middle', ls: 1.6 }));
    o.push(text(st.x, top ? st.y - 42 : st.y + 57, st.cap, { size: 22, w: 500, fill: t.sub, anchor: 'middle' }));
  });

  o.push(`</svg>`);
  return o.join('\n');
}

(async () => {
  const { chromium } = require('playwright');
  const browser = await chromium.launch();
  for (const key of ['light', 'dark']) {
    const svg = build(key);
    fs.writeFileSync(path.join(OUT, `hero-${key}.svg`), svg);
    const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
    await page.setContent(`<body style="margin:0"><img src="data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}" style="width:${W}px;display:block"></body>`);
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(OUT, `hero-${key}.png`) });
    await page.close();
  }
  await browser.close();
})();
