// Promo cover for "多模态视角下的 Coding" (3:4, 1080x1440 at 2x).
// Usage (from the repository root):  node promo/gen.js
// Needs Playwright and the npm packages `qrcode` and `@fontsource/noto-sans-sc` (install them anywhere and
// point NODE_PATH at that node_modules). Without the font package it falls back to system CJK fonts.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('playwright');
const QRCode = require('qrcode');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(__dirname, 'images');
const REPO_URL = 'https://github.com/jiangjin1999/awesome-multimodal-agentic-coding';
const HERO = path.join(ROOT, 'assets/hero/hero-light.png'); // 3200 x 1496

let notoDir = null;
try { notoDir = path.dirname(require.resolve('@fontsource/noto-sans-sc/package.json')); } catch (e) { /* system fonts */ }
const fontLinks = notoDir ? [400, 500, 700, 900].map((w) => `<link rel="stylesheet" href="file://${notoDir}/${w}.css">`).join('') : '';

const C = { ink: '#1F2328', sub: '#59636E', card: '#F6F8FA', stroke: '#D8DEE4', acc: ['#0969DA', '#8250DF', '#C4500B'] };

const GH = `<svg viewBox="0 0 16 16" width="30" height="30" fill="${C.ink}" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>`;

const css = `
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1440px;background:#fff}
body{font-family:'Inter','Noto Sans SC','PingFang SC','Noto Sans CJK SC','Microsoft YaHei',sans-serif;color:${C.ink};
  -webkit-font-smoothing:antialiased;font-feature-settings:'ss01','cv11'}
.page{position:relative;width:1080px;height:1440px;padding:56px 64px 52px;display:flex;flex-direction:column;overflow:hidden}
.page>*{flex-shrink:0}
.topbar{display:flex;justify-content:space-between;align-items:center;font-size:21px;font-weight:600;color:${C.sub}}
.brand{display:flex;align-items:center;gap:12px}
.dots{display:flex;gap:5px}.dots i{width:12px;height:12px;border-radius:50%;display:block}
.agi{color:${C.acc[2]};letter-spacing:3px;font-size:19px;font-weight:700}
b{font-weight:700}
.grad{background:linear-gradient(90deg,${C.acc[0]} 0%,${C.acc[1]} 52%,${C.acc[2]} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.big{margin-top:58px;line-height:1}
.big .l1{display:block;font-size:104px;font-weight:900;letter-spacing:2px}
.big .l2{display:inline-block;font-size:178px;font-weight:800;letter-spacing:-5px;margin-top:6px;padding-bottom:14px}
.sub{margin-top:16px;font-size:40px;font-weight:700;letter-spacing:1px}
.idea{margin-top:20px;font-size:27px;color:${C.sub};font-weight:500}
.idea b{color:${C.ink}}
.heroWrap{margin-top:40px;width:952px;overflow:hidden;position:relative}
.heroWrap img{position:absolute;display:block}
.cols{margin-top:18px;display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.col{padding:2px 6px 0}
.col .t{font-size:27px;font-weight:700;margin-top:2px}
.col .d{font-size:21px;color:${C.sub};margin-top:8px;line-height:1.5}
.foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between;gap:28px;
  background:${C.card};border:1.5px solid ${C.stroke};border-radius:24px;padding:26px 28px 26px 34px}
.foot .gh{display:flex;align-items:center;gap:14px;font-size:27px;font-weight:600;line-height:1.3}
.foot .stats{margin-top:14px;font-size:21px;color:${C.sub};font-weight:500;letter-spacing:.3px}
.qr{width:150px;height:150px;flex:none;background:#fff;border-radius:14px;padding:8px;border:1.5px solid ${C.stroke}}
.qr svg{width:100%;height:100%;display:block}
`;

// Show the source rect (x, y, w, h) of the hero PNG inside a box of width boxW.
function crop(cls, x, y, w, h, boxW) {
  const s = boxW / w;
  return `<div class="${cls}" style="width:${boxW}px;height:${Math.round(h * s)}px"><img src="file://${HERO}" style="width:${3200 * s}px;left:${-x * s}px;top:${-y * s}px"></div>`;
}

function cover(qrSvg) {
  const cols = [
    ['01', '视觉作为反馈', '看见自己造的东西，<br>模型才能 loop 起来'],
    ['02', '把模型当作工具', '让 Agent 去调生成、<br>感知和动作模型'],
    ['03', '打通数字与物理世界', '用代码搭仿真、控机器人，<br>从屏幕走到真实世界'],
  ];
  return `<div class="page">
  <div class="topbar"><span class="brand"><span class="dots">${C.acc.map((c) => `<i style="background:${c}"></i>`).join('')}</span>Awesome Multimodal Agentic Coding</span><span class="agi">TOWARD PHYSICAL AGI</span></div>
  <h1 class="big"><span class="l1">多模态视角下的</span><span class="l2 grad">Coding</span></h1>
  <div class="sub">扩展 Agent 能力边界，最终通向物理 AGI</div>
  <div class="idea">我们从 <b>Coding</b> 而不是 CUA 的角度看：<b>写代码 → 看结果 → 再改</b></div>
  ${crop('heroWrap', 96, 256, 3008, 1176, 952)}
  <div class="cols">${cols.map(([n, t, d], i) => `<div class="col"><div class="t"><span style="color:${C.acc[i]}">${n}</span>&nbsp; ${t}</div><div class="d">${d}</div></div>`).join('')}</div>
  <div class="foot">
    <div><div class="gh">${GH}<span>github.com/jiangjin1999/<br>awesome-multimodal-agentic-coding</span></div>
    <div class="stats">664 项工作 · 3 个阶段 · 19 个方向 · 中 / EN / 日 · 持续更新</div></div>
    <div class="qr">${qrSvg}</div>
  </div>
</div>`;
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const qrSvg = await QRCode.toString(REPO_URL, { type: 'svg', margin: 0, errorCorrectionLevel: 'M', color: { dark: C.ink, light: '#FFFFFF' } });
  const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'mmac-promo-')), 'cover.html');
  fs.writeFileSync(file, `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">${fontLinks}<style>${css}</style></head><body>${cover(qrSvg)}</body></html>`);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 2 });
  await page.goto(`file://${file}`);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(OUT, 'cover.png') });
  await browser.close();
  console.log('wrote promo/images/cover.png');
})();
