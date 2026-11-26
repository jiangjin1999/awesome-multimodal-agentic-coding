// Hero image for the README: three cumulative stages of multimodal agentic coding.
// Usage (from the repository root):  node assets/hero/gen.js
// Writes assets/hero/hero-{light,dark}.svg and renders hero-{light,dark}.png at 2x with Playwright.
const fs = require('fs');
const path = require('path');
const OUT = __dirname;
const SANS = `-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif`;

const W = 1600, H = 748, PW = 480, PY = 132, PH = 580;
const PX = [50, 560, 1070];
const SL = 40, SW = 400;          // slot (tray / world band) x and width inside a panel

const themes = {
  light: {
    bg: '#FFFFFF', card: '#F6F8FA', cardStroke: '#D8DEE4', ink: '#1F2328', sub: '#59636E',
    neutral: '#8C959F', neutralText: '#59636E', nodeFill: '#FFFFFF', chipFill: '#FFFFFF', ghost: '#C9D1D9',
    accents: ['#0969DA', '#8250DF', '#C4500B'], tints: ['#DDF4FF', '#F3EEFF', '#FFF1E5'], glow: false,
  },
  dark: {
    bg: '#0B0F1A', card: '#121829', cardStroke: '#222B45', ink: '#EEF2F8', sub: '#98A2B8',
    neutral: '#6C7896', neutralText: '#8E99B0', nodeFill: '#161D31', chipFill: '#121829', ghost: '#2A3452',
    accents: ['#5CC8FF', '#B69CFF', '#FFB65C'], tints: ['#12293D', '#231F45', '#3A2A18'], glow: true,
  },
};

const stages = [
  { num: '01', title: 'Visual as Feedback', plus: '+ sees what it builds', cap: 'web · charts · CAD · games' },
  { num: '02', title: 'Orchestrating Models as Tools', plus: '+ calls models as tools', cap: 'design · video · interactive worlds' },
  { num: '03', title: 'Bridging Digital &amp; Physical Worlds', plus: '+ acts in simulation and reality', cap: 'simulators · robots · real-world data' },
];

function build(key) {
  const t = themes[key];
  const o = [];
  const S = (c, w = 2.5) => `fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"`;
  o.push(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Awesome Multimodal Agentic Coding: three cumulative stages — visual as feedback, orchestrating models as tools, bridging digital and physical worlds">`);
  o.push(`<defs>`);
  const mk = (id, c) => `<marker id="${id}" viewBox="0 0 12 12" refX="9" refY="6" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M2 1.5 L10 6 L2 10.5" fill="none" stroke="${c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></marker>`;
  o.push(mk('ah-n', t.neutral));
  t.accents.forEach((c, i) => o.push(mk(`ah-${i}`, c)));
  if (t.glow) o.push(`<filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="7" result="b"/><feColorMatrix in="b" type="matrix" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0.55 0" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>`);
  o.push(`</defs>`);
  o.push(`<rect width="${W}" height="${H}" fill="${t.bg}"/>`);

  // ---- header
  o.push(`<text x="50" y="88" font-family="${SANS}" font-size="52" font-weight="700" fill="${t.ink}" letter-spacing="-1">Awesome Multimodal Agentic Coding</text>`);
  o.push(`<text x="1550" y="86" text-anchor="end" font-family="${SANS}" font-size="24" font-weight="650" fill="${t.accents[2]}" letter-spacing="3">TOWARD PHYSICAL AGI</text>`);

  // ---- panels
  stages.forEach((st, i) => {
    const ac = t.accents[i], tint = t.tints[i];
    const N = t.neutral;
    const col = (s) => (s === i ? ac : N);
    const sw = (s) => (s === i ? 3.2 : 2.4);
    const mark = (s) => (s === i ? `ah-${i}` : 'ah-n');
    const hl = (s) => (s === i && t.glow ? ` filter="url(#glow)"` : '');
    o.push(`<g transform="translate(${PX[i]} ${PY})">`);
    o.push(`<rect x="0" y="0" width="${PW}" height="${PH}" rx="22" fill="${t.card}" stroke="${t.cardStroke}" stroke-width="1.5"/>`);
    o.push(`<text x="30" y="50" font-family="${SANS}" font-size="22" font-weight="700" fill="${ac}" letter-spacing="2">${st.num}</text>`);
    o.push(`<text x="450" y="50" text-anchor="end" font-family="${SANS}" font-size="22" font-weight="600" fill="${ac}">${st.plus}</text>`);
    o.push(`<text x="30" y="92" font-family="${SANS}" font-size="${i === 2 ? 25.5 : 27}" font-weight="700" fill="${t.ink}">${st.title}</text>`);

    o.push(`<g transform="translate(0 -4)">`);
    const cx = 240, ax = 102, sx = 378, cy = 308, R = 46, top = 232, bot = 384;
    const bandY = bot + 64, bandH = 64;
    const ghost = (x, y, w, h) => o.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="16" fill="none" stroke="${t.ghost}" stroke-width="1.8" stroke-dasharray="3 7" stroke-linecap="round"/>`);
    if (i < 1) ghost(SL, 140, SW, 56);
    if (i < 2) ghost(SL, bandY, SW, bandH);

    // --- model tray (stage 2+), icons with labels
    if (i >= 1) {
      const c = col(1), w = sw(1);
      o.push(`<g${hl(1)}>`);
      o.push(`<rect x="${SL}" y="140" width="${SW}" height="56" rx="16" fill="${i === 1 ? tint : 'none'}" stroke="${c}" stroke-width="${w}"/>`);
      o.push(`<line x1="${cx}" y1="196" x2="${cx}" y2="${top - 21}" stroke="${c}" stroke-width="${w}" stroke-linecap="round"/>`);
      const ICONS = {
        image: `<path d="M-13 9 L-5 -3 L1 4 L5 -1 L13 9 Z"/><circle cx="7" cy="-8" r="2.6"/>`,
        video: `<rect x="-13" y="-9" width="26" height="18" rx="4"/><path d="M-3.5 -4.5 L4.5 0 L-3.5 4.5 Z"/>`,
        world: `<circle r="12"/><ellipse rx="5" ry="12"/><path d="M-12 0 H12 M-10.4 -6 H10.4 M-10.4 6 H10.4"/>`,
        perception: `<path d="M-12 -5 V-12 H-5 M5 -12 H12 V-5 M12 5 V12 H5 M-5 12 H-12 V5"/><circle r="4.5"/>`,
        action: `<g transform="translate(-1 -1) scale(0.78)"><path d="M-16 18 H10 M-9 18 V11 H3 V18"/><path d="M-3 9 L-10 -7 L7 -13"/><path d="M7 -13 L13 -9 M13 -9 L18 -14 M13 -9 L16 -3"/></g>`,
      };
      const items = (i === 1 ? ['image', 'video', 'world'] : ['perception', 'world', 'action']).map((k) => [k, 0, ICONS[k]]);
      // measured-ish widths (Inter/SF semibold @19px); equal gaps across the tray
      const FS = 19, ICON = 26, GAP = 7;
      const widths = { image: 53, video: 49, world: 50, perception: 97, action: 56 };
      const tot = items.reduce((a, [lab]) => a + ICON + GAP + widths[lab], 0);
      const pad = (SW - tot) / (items.length + 1);
      let xcur = SL + pad;
      items.forEach(([lab, tw, path]) => {
        const ix = xcur + ICON / 2;
        o.push(`<g transform="translate(${ix} 168)" ${S(c, i === 1 ? 2.3 : 2.0)}>${path}</g>`);
        o.push(`<text x="${xcur + ICON + GAP}" y="174.5" font-family="${SANS}" font-size="${FS}" font-weight="${i === 1 ? 600 : 500}" fill="${i === 1 ? ac : t.neutralText}">${lab}</text>`);
        xcur += ICON + GAP + widths[lab] + pad;
      });
      o.push(`</g>`);
    }


    // --- world box (stage 3): sim (dashed) and real (solid) in one box
    if (i >= 2) {
      const c = col(2), w = sw(2);
      o.push(`<g${hl(2)}>`);
      const OH = 76, by = bandY + OH / 2;
      // act: build -> world box ; observe: world box -> eye
      o.push(`<line x1="${sx}" y1="${cy + R + 6}" x2="${sx}" y2="${bandY - 4}" stroke="${c}" stroke-width="${w}" stroke-linecap="round" marker-end="url(#${mark(2)})"/>`);
      o.push(`<line x1="${cx}" y1="${bandY - 4}" x2="${cx}" y2="${bot + 28}" stroke="${c}" stroke-width="${w}" stroke-linecap="round" marker-end="url(#${mark(2)})"/>`);
      // outer box
      o.push(`<rect x="${SL}" y="${bandY}" width="${SW}" height="${OH}" rx="18" fill="${tint}" stroke="${c}" stroke-width="${w}"/>`);
      const ih = OH - 20, iy = bandY + 10;
      const simL = SL + 10, simR = SL + 134, realL = SL + 222, realR = SL + SW - 10;
      // sim (dashed, virtual)
      o.push(`<rect x="${simL}" y="${iy}" width="${simR - simL}" height="${ih}" rx="12" fill="${t.nodeFill}" stroke="${c}" stroke-width="2.2" stroke-dasharray="6 5"/>`);
      o.push(`<g transform="translate(${simL + 32} ${by})" ${S(c, 2.3)}><path d="M0 -11 L10 -5.5 V5.5 L0 11 L-10 5.5 V-5.5 Z M0 0 V11 M0 0 L10 -5.5 M0 0 L-10 -5.5"/></g>`);
      o.push(`<text x="${simL + 54}" y="${by + 8}" font-family="${SANS}" font-size="22" font-weight="650" fill="${c}">sim</text>`);
      // real (solid, physical)
      o.push(`<rect x="${realL}" y="${iy}" width="${realR - realL}" height="${ih}" rx="12" fill="${t.nodeFill}" stroke="${c}" stroke-width="2.2"/>`);
      o.push(`<g transform="translate(${realL + 28} ${by})" ${S(c, 2.3)}><rect x="-14" y="-8" width="28" height="19" rx="4"/><path d="M-6 -8 L-3.5 -12 H3.5 L6 -8"/><circle cy="1.5" r="5"/></g>`);
      o.push(`<text x="${(realL + realR) / 2 + 2}" y="${by + 8}" text-anchor="middle" font-family="${SANS}" font-size="22" font-weight="650" fill="${c}">real</text>`);
      o.push(`<g transform="translate(${realR - 30} ${by - 2})" ${S(c, 2.4)}><path d="M-16 18 H10 M-9 18 V11 H3 V18"/><path d="M-3 9 L-10 -7 L7 -13"/><path d="M7 -13 L13 -9 M13 -9 L18 -14 M13 -9 L16 -3"/><circle cx="-3" cy="10" r="2.6" fill="${t.nodeFill}"/><circle cx="-10" cy="-7" r="2.6" fill="${t.nodeFill}"/></g>`);
      // real2sim (top, leftwards) and sim2real (bottom, rightwards)
      o.push(`<line x1="${realL - 10}" y1="${by}" x2="${simR + 10}" y2="${by}" stroke="${c}" stroke-width="2.6" stroke-linecap="round" marker-end="url(#${mark(2)})"/>`);
      // sim ⇢ agent: practice in simulation strengthens the agent (dashed)
      o.push(`<line x1="${ax}" y1="${iy}" x2="${ax}" y2="${cy + R + 6}" stroke="${c}" stroke-width="2.2" stroke-dasharray="6 5" marker-end="url(#${mark(2)})"/>`);
      o.push(`</g>`);
    }

    // --- loop
    const g = 6;
    const ax_ = (R + g) * Math.cos(0.66), ay_ = (R + g) * Math.sin(0.66);
    o.push(`<path d="M${ax + ax_} ${cy - ay_} C${ax + 58} ${top + 14} ${ax + 92} ${top} ${cx - 24} ${top}" ${S(N, 2.4)}/>`);
    o.push(`<path d="M${cx + 24} ${top} C${sx - 92} ${top} ${sx - 58} ${top + 14} ${sx - ax_} ${cy - ay_}" ${S(N, 2.4)} marker-end="url(#ah-n)"/>`);
    const c0 = col(0), w0 = sw(0);
    o.push(`<g${hl(0)}>`);
    o.push(`<path d="M${sx - ax_} ${cy + ay_} C${sx - 58} ${bot - 14} ${sx - 92} ${bot} ${cx + 26} ${bot}" ${S(c0, w0)}/>`);
    o.push(`<path d="M${cx - 26} ${bot} C${ax + 92} ${bot} ${ax + 58} ${bot - 14} ${ax + ax_} ${cy + ay_}" ${S(c0, w0)} marker-end="url(#${mark(0)})"/>`);
    o.push(`<circle cx="${cx}" cy="${bot}" r="23" fill="${i === 0 ? tint : t.chipFill}" stroke="${c0}" stroke-width="${w0}"/>`);
    o.push(`<g transform="translate(${cx} ${bot})"><path d="M-14 0 Q0 -11.5 14 0 Q0 11.5 -14 0 Z" ${S(c0, 2.3)}/><circle r="4" fill="${c0}"/></g>`);
    o.push(`</g>`);
    o.push(`<circle cx="${cx}" cy="${top}" r="21" fill="${t.chipFill}" stroke="${N}" stroke-width="2.4"/>`);
    o.push(`<g transform="translate(${cx} ${top})" ${S(N, 2.3)}><path d="M-5.5 -6 L-11.5 0 L-5.5 6 M5.5 -6 L11.5 0 L5.5 6 M2.2 -8 L-2.2 8"/></g>`);
    o.push(`<text x="${cx}" y="${top + 50}" text-anchor="middle" font-family="${SANS}" font-size="22" fill="${t.neutralText}">code</text>`);
    o.push(`<text x="${cx}" y="${bot - 37}" text-anchor="middle" font-family="${SANS}" font-size="22" font-weight="${i === 0 ? 700 : 400}" fill="${i === 0 ? ac : t.neutralText}">observe</text>`);
    // agent
    o.push(`<circle cx="${ax}" cy="${cy}" r="${R}" fill="${t.nodeFill}" stroke="${N}" stroke-width="2.4"/>`);
    o.push(`<g transform="translate(${ax} ${cy + 3})" ${S(t.neutralText, 2.5)}><rect x="-20" y="-13" width="40" height="29" rx="9"/><path d="M0 -13 V-21"/><circle cx="0" cy="-24" r="3"/><circle cx="-8" cy="1" r="2.6" fill="${t.neutralText}" stroke="none"/><circle cx="8" cy="1" r="2.6" fill="${t.neutralText}" stroke="none"/></g>`);
    o.push(`<text x="${ax}" y="${cy - R - 14}" text-anchor="middle" font-family="${SANS}" font-size="22" fill="${t.neutralText}">agent</text>`);
    // render
    o.push(`<circle cx="${sx}" cy="${cy}" r="${R}" fill="${t.nodeFill}" stroke="${N}" stroke-width="2.4"/>`);
    o.push(`<g transform="translate(${sx} ${cy})" ${S(t.neutralText, 2.5)}><rect x="-23" y="-18" width="46" height="36" rx="6"/><path d="M-23 -8 H23"/><path d="M-12 10 V4 M-3 10 V-1 M6 10 V2 M14 10 V-3"/></g>`);
    o.push(`<text x="${sx}" y="${cy - R - 14}" text-anchor="middle" font-family="${SANS}" font-size="22" fill="${t.neutralText}">build</text>`);
    o.push(`</g>`);

    o.push(`<text x="240" y="${PH - 24}" text-anchor="middle" font-family="${SANS}" font-size="21" fill="${t.sub}">${st.cap}</text>`);
    o.push(`</g>`);
  });

  [545, 1055].forEach((x, k) => {
    o.push(`<circle cx="${x}" cy="${PY + 304}" r="15" fill="${t.bg}" stroke="${t.cardStroke}" stroke-width="1.5"/>`);
    o.push(`<path d="M${x - 6} ${PY + 304} H${x + 6} M${x} ${PY + 298} V${PY + 310}" ${S(t.accents[k + 1], 2.4)}/>`);
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
    await page.waitForTimeout(200);
    await page.screenshot({ path: path.join(OUT, `hero-${key}.png`) });
    await page.close();
  }
  await browser.close();
})();
