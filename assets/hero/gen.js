// Hero image for the README: one loop that grows through three cumulative stages,
// from the digital world to the physical world.
// Usage (from the repository root):  NODE_PATH=$(npm root -g) node assets/hero/gen.js
// Writes assets/hero/hero-{light,dark}.svg and renders hero-{light,dark}.png at 2x with Playwright.
// Fonts: Inter Display, Inter and JetBrains Mono must be installed where the PNG is rendered.
const fs = require('fs');
const path = require('path');
const OUT = __dirname;
const DISP = `'Inter Display', Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif`;
const SANS = `Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif`;
const MONO = `'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`;

// ---- geometry (one 1200-unit grid; the README shows it at about 830 px and 360 px wide)
const W = 1200, H = 692, M = 44;
const AX = 140, CY = 306;                 // agent centre; every loop starts and ends here
const RX = [158, 295, 445];               // loop half-widths: each stage reaches further right
const RY = [94, 144, 186];                // loop half-heights
const NX = RX.map((r) => AX + 2 * r);     // far end of each loop = what that stage reaches
const CARD_W = [108, 168, 204], CARD_H = [116, 116, 124]; // far-end cards
const AXIS_Y = CY + RY[2] + 44;           // digital -> physical axis

const themes = {
  light: {
    bg: '#FFFFFF', ink: '#14181F', sub: '#57606A', faint: '#8C959F', rule: '#D0D7DE',
    card: '#FFFFFF', agentFill: '#14181F', agentInk: '#FFFFFF',
    stroke: ['#0969DA', '#8250DF', '#C2500A'],   // loop lines, icons
    text: ['#0860C7', '#7743D6', '#B34707'],     // coloured type (a touch darker for contrast)
    fill: ['#D6EEFF', '#ECE4FF', '#FFEBD9'],     // loop interiors
    shadow: 0.10, glow: 0,
  },
  dark: {
    bg: '#0A0E17', ink: '#F2F5FA', sub: '#A3AEC2', faint: '#6F7B94', rule: '#2A3348',
    card: '#0A0E17', agentFill: '#F2F5FA', agentInk: '#0A0E17',
    stroke: ['#4CB8FF', '#A98BFF', '#FF9F4A'],
    text: ['#6CC5FF', '#B9A1FF', '#FFAE66'],
    fill: ['#0D2A45', '#1F1C4A', '#38230F'],
    shadow: 0, glow: 0.5,
  },
};

const stages = [
  { title: ['Visual as', 'Feedback'], verb: 'write code', node: 'artifact' },
  { title: ['Orchestrating', 'Models as Tools'], verb: 'call models', node: 'models' },
  { title: ['Bridging Digital &amp;', 'Physical Worlds'], verb: 'act', node: 'sim &amp; real' },
];

// ---- pictograms, drawn on a 2.4-unit stroke around (0,0)
const IC = {
  agent: `<rect x="-20" y="-13" width="40" height="29" rx="9"/><path d="M0 -13 V-21"/><circle cx="0" cy="-24" r="3"/><path d="M-8 -1 V4 M8 -1 V4"/>`,
  eye: `<path d="M-14 0 Q0 -11.5 14 0 Q0 11.5 -14 0 Z"/><circle r="3.4"/>`,
  window: `<rect x="-24" y="-19" width="48" height="38" rx="6"/><path d="M-24 -9 H24"/><path d="M-13 11 V4 M-4.5 11 V-2 M4.5 11 V1 M13 11 V-4"/>`,
  image: `<rect x="-13" y="-11" width="26" height="22" rx="4"/><path d="M-13 7 L-5 -1 L1 5 L5 1 L13 8"/><circle cx="6" cy="-5" r="2"/>`,
  video: `<rect x="-13" y="-10" width="26" height="20" rx="4"/><path d="M-3.5 -4.5 L4.5 0 L-3.5 4.5 Z"/>`,
  scan: `<path d="M-12 -5 V-12 H-5 M5 -12 H12 V-5 M12 5 V12 H5 M-5 12 H-12 V5"/><circle r="4.5"/>`,
  cube: `<path d="M0 -12 L11 -6 V6 L0 12 L-11 6 V-6 Z M0 0 V12 M0 0 L11 -6 M0 0 L-11 -6"/>`,
  arm: `<path d="M-15 16 H9 M-9 16 V9 H3 V16"/><path d="M-3 9 L-10 -7 L7 -13"/><path d="M7 -13 L13 -9 M13 -9 L18 -14 M13 -9 L16 -3"/>`,
};

function build(key) {
  const t = themes[key];
  const o = [];
  const S = (c, w = 2.4) => `fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"`;
  const text = (x, y, s, { f = SANS, size = 22, w = 500, fill = t.ink, anchor = 'start', ls = 0 } = {}) =>
    `<text x="${x}" y="${y}" font-family="${f}" font-size="${size}" font-weight="${w}" fill="${fill}" text-anchor="${anchor}"${ls ? ` letter-spacing="${ls}"` : ''}>${s}</text>`;

  o.push(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Multimodal agentic coding: one agent loop that grows through three stages, from the digital world to the physical world">`);
  o.push(`<defs>`);
  o.push(`<linearGradient id="axis" gradientUnits="userSpaceOnUse" x1="${AX}" x2="${W - M}"><stop offset="0" stop-color="${t.stroke[0]}"/><stop offset="0.5" stop-color="${t.stroke[1]}"/><stop offset="1" stop-color="${t.stroke[2]}"/></linearGradient>`);
  if (t.shadow) o.push(`<filter id="lift" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#1B2A4A" flood-opacity="${t.shadow}"/></filter>`);
  if (t.glow) o.push(`<filter id="glow" x="-20%" y="-30%" width="140%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>`);
  o.push(`</defs>`);
  o.push(`<rect width="${W}" height="${H}" fill="${t.bg}"/>`);
  const lift = t.shadow ? ` filter="url(#lift)"` : '';

  // ---- header
  o.push(text(M, 70, 'Multimodal Agentic Coding', { f: DISP, size: 44, w: 700, ls: -0.6 }));
  o.push(text(W - M - 34, 66, 'TOWARD PHYSICAL AGI', { f: MONO, size: 21, w: 700, fill: t.text[2], anchor: 'end', ls: 2.2 }));
  o.push(`<path d="M${W - M - 24} 58.500 H${W - M - 2} M${W - M - 10} 51 L${W - M - 2} 58.500 L${W - M - 10} 66" ${S(t.text[2], 2.6)}/>`);

  // ---- loops: nested, all tangent at the agent; outermost first
  for (let i = 2; i >= 0; i--) {
    const cx = AX + RX[i];
    if (t.glow) o.push(`<ellipse cx="${cx}" cy="${CY}" rx="${RX[i]}" ry="${RY[i]}" fill="none" stroke="${t.stroke[i]}" stroke-width="5" opacity="${t.glow}" filter="url(#glow)"/>`);
    o.push(`<ellipse cx="${cx}" cy="${CY}" rx="${RX[i]}" ry="${RY[i]}" fill="${t.fill[i]}" stroke="${t.stroke[i]}" stroke-width="4"/>`);
  }

  // ---- drop lines from each far end to its tick on the axis
  NX.forEach((x, i) => o.push(`<path d="M${x} ${CY + CARD_H[i] / 2 + 12} V${AXIS_Y - 12}" stroke="${t.stroke[i]}" stroke-width="2.200" stroke-dasharray="0.100 7.500" stroke-linecap="round"/>`));

  // ---- direction arrows and verbs on the loops
  stages.forEach((st, i) => {
    let cx = AX + RX[i];
    const c = t.stroke[i];
    const head = (deg) => {
      const th = (deg * Math.PI) / 180;
      const x = cx + RX[i] * Math.cos(th), y = CY - RY[i] * Math.sin(th);
      const rot = (Math.atan2(RY[i] * Math.cos(th), RX[i] * Math.sin(th)) * 180) / Math.PI;
      return `<g transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${rot.toFixed(1)})"><path d="M-8 -8.500 L4 0 L-8 8.500" ${S(c, 4)}/></g>`;
    };
    o.push(head([57, 42, 46][i]), head([-124, -121, -116][i]));
    // verb chip at the top of the loop (outbound)
    const fs_ = 22, tw = st.verb.length * fs_ * 0.6 + 30, y = CY - RY[i];
    if (i === 0) cx -= 22;
    o.push(`<rect x="${cx - tw / 2}" y="${y - 19}" width="${tw}" height="38" rx="19" fill="${t.card}" stroke="${c}" stroke-width="2.4"/>`);
    o.push(text(cx, y + 7.500, st.verb, { f: MONO, size: fs_, w: 700, fill: t.text[i], anchor: 'middle' }));
  });
  // "observe" chip on the return path of the innermost loop: visual feedback is where it all starts
  {
    const cx = AX + RX[0] + 20, y = CY + RY[0], c = t.stroke[0], tw = 7 * 22 * 0.6 + 64;
    o.push(`<rect x="${cx - tw / 2}" y="${y - 19}" width="${tw}" height="38" rx="19" fill="${t.card}" stroke="${c}" stroke-width="2.4"/>`);
    o.push(`<g transform="translate(${cx - tw / 2 + 28} ${y}) scale(0.9)" ${S(c, 2.6)}>${IC.eye}</g>`);
    o.push(text(cx + 17, y + 7.500, 'observe', { f: MONO, size: 22, w: 700, fill: t.text[0], anchor: 'middle' }));
  }

  // ---- agent
  o.push(`<circle cx="${AX}" cy="${CY}" r="52" fill="${t.agentFill}" stroke="${t.bg}" stroke-width="5"${lift}/>`);
  o.push(`<g transform="translate(${AX} ${CY + 4}) scale(1.3)" ${S(t.agentInk, 2.3)}>${IC.agent}</g>`);

  // ---- far ends
  NX.forEach((x, i) => {
    const w = CARD_W[i], h = CARD_H[i];
    o.push(`<rect x="${x - w / 2}" y="${CY - h / 2}" width="${w}" height="${h}" rx="18" fill="${t.card}" stroke="${t.stroke[i]}" stroke-width="3.200"${lift}/>`);
    o.push(text(x, CY + h / 2 - 17, stages[i].node, { size: 22, w: 600, fill: t.text[i], anchor: 'middle' }));
  });
  const IY = CY - 15;                      // icon row inside the cards
  // 1 · a rendered artifact
  o.push(`<g transform="translate(${NX[0]} ${IY}) scale(1.2)" ${S(t.stroke[0], 2.2)}>${IC.window}</g>`);
  // 2 · models used as tools
  ['image', 'video', 'scan'].forEach((k, j) => o.push(`<g transform="translate(${NX[1] + (j - 1) * 48} ${IY}) scale(1.2)" ${S(t.stroke[1], 2.1)}>${IC[k]}</g>`));
  // 3 · simulation (dashed) and reality (solid)
  {
    const x = NX[2], y = CY - 17, c = t.stroke[2];
    o.push(`<rect x="${x - 86}" y="${y - 30}" width="60" height="60" rx="10" fill="none" stroke="${c}" stroke-width="2.200" stroke-dasharray="5 5.500"/>`);
    o.push(`<g transform="translate(${x - 56} ${y}) scale(1.15)" ${S(c, 2.1)}>${IC.cube}</g>`);
    o.push(`<path d="M${x - 9} ${y - 7} H${x + 9} M${x + 3} ${y - 13} L${x + 9} ${y - 7} L${x + 3} ${y - 1}" ${S(c, 2.4)}/>`);
    o.push(`<path d="M${x + 9} ${y + 7} H${x - 9} M${x - 3} ${y + 1} L${x - 9} ${y + 7} L${x - 3} ${y + 13}" ${S(c, 2.4)}/>`);
    o.push(`<g transform="translate(${x + 54} ${y + 2}) scale(1.4)" ${S(c, 1.900)}>${IC.arm}</g>`);
  }

  // ---- axis: digital -> physical, with one tick per stage
  o.push(`<path d="M${M} ${AXIS_Y} H${AX}" stroke="${t.rule}" stroke-width="3" stroke-linecap="round"/>`);
  o.push(`<path d="M${AX} ${AXIS_Y} H${W - M - 3}" stroke="url(#axis)" stroke-width="3" stroke-linecap="round"/>`);
  o.push(`<path d="M${W - M - 13} ${AXIS_Y - 9} L${W - M - 2} ${AXIS_Y} L${W - M - 13} ${AXIS_Y + 9}" ${S(t.stroke[2], 3)}/>`);
  o.push(`<circle cx="${AX}" cy="${AXIS_Y}" r="7" fill="${t.agentFill}" stroke="${t.bg}" stroke-width="3"/>`);
  NX.forEach((x, i) => o.push(`<circle cx="${x}" cy="${AXIS_Y}" r="7" fill="${t.stroke[i]}" stroke="${t.bg}" stroke-width="3"/>`));
  o.push(text(M, AXIS_Y - 16, 'DIGITAL', { f: MONO, size: 19, w: 700, fill: t.text[0], ls: 2.2 }));
  o.push(text(W - M, AXIS_Y - 16, 'PHYSICAL', { f: MONO, size: 19, w: 700, fill: t.text[2], anchor: 'end', ls: 2.2 }));

  // ---- labels under the ticks
  const y0 = AXIS_Y + 42;
  o.push(text(AX, y0, 'AGENT', { f: MONO, size: 20, w: 700, fill: t.sub, anchor: 'middle', ls: 1.6 }));
  ['writes code,', 'observes, improves'].forEach((l, k) => o.push(text(AX, y0 + 37 + k * 29, l, { size: 21, w: 500, fill: t.sub, anchor: 'middle' })));
  stages.forEach((st, i) => {
    o.push(text(NX[i], y0, `STAGE ${i + 1}`, { f: MONO, size: 20, w: 700, fill: t.text[i], anchor: 'middle', ls: 1.6 }));
    st.title.forEach((l, k) => o.push(text(NX[i], y0 + 40 + k * 38, l, { f: DISP, size: 32, w: 700, anchor: 'middle', ls: -0.3 })));
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
