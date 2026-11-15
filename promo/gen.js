// Promo images for "多模态视角下的 Coding": a cover page and four text pages (3:4, 1080x1440 at 2x).
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

const C = {
  ink: '#1F2328', sub: '#59636E', faint: '#8C959F', card: '#F6F8FA', stroke: '#D8DEE4',
  acc: ['#0969DA', '#8250DF', '#C4500B'], tint: ['#DDF4FF', '#F3EEFF', '#FFF1E5'],
};

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
.pageno{font-size:20px;font-weight:600;color:${C.faint};letter-spacing:1px}
b,strong{font-weight:700}
.grad{background:linear-gradient(90deg,${C.acc[0]} 0%,${C.acc[1]} 52%,${C.acc[2]} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}

/* cover */
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

/* text pages */
.head{margin-top:44px;display:flex;justify-content:space-between;align-items:flex-start;gap:28px}
.chip{display:inline-flex;align-items:center;gap:12px;font-size:20px;font-weight:700;letter-spacing:2.5px;border-radius:999px;padding:9px 18px}
.chip .n{font-size:22px}
.h1{margin-top:22px;font-size:58px;font-weight:900;line-height:1.22;letter-spacing:1px}
.plus{margin-top:16px;font-size:24px;font-weight:600}
.diag{flex:none;width:350px;border-radius:20px;overflow:hidden;position:relative;border:1.5px solid ${C.stroke};background:${C.card}}
.diag img{position:absolute;display:block}
.body{margin-top:34px;font-size:29px;line-height:1.72;color:#2B3137}
.body p+p{margin-top:18px}
.body em{font-style:normal;font-weight:700;color:${C.ink}}
.box{margin-top:22px;border-radius:20px;padding:22px 28px 24px;border:1.5px solid ${C.stroke};background:${C.card}}
.box .k{font-size:22px;font-weight:700;letter-spacing:1px;margin-bottom:8px}
.box .v{font-size:27px;line-height:1.66;color:#2B3137}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:22px}
.pair .box{margin-top:0}
.atoms{display:flex;gap:14px;margin:6px 0 10px}
.atom{flex:1;background:#fff;border-radius:14px;padding:12px 16px;border:1.5px solid ${C.stroke}}
.atom .a{font-size:25px;font-weight:700}.atom .b{font-size:21px;color:${C.sub};margin-top:2px}
.tags{margin-top:22px;display:flex;flex-wrap:wrap;gap:10px}
.tag{font-size:21px;font-weight:500;color:${C.sub};background:${C.card};border:1.5px solid ${C.stroke};border-radius:999px;padding:6px 16px}
.lines .ln{display:grid;grid-template-columns:62px 1fr;gap:6px;margin-top:20px}
.lines .ln .no{font-size:30px;font-weight:800;line-height:1.5}
.lines .ln .tt{font-size:28px;font-weight:800;line-height:1.5}
.lines .ln .tt span{font-size:22px;font-weight:700;letter-spacing:1px;margin-left:10px}
.lines .ln .dd{font-size:26px;line-height:1.64;color:#2B3137;margin-top:4px}
.mini{margin-top:auto;display:flex;align-items:center;justify-content:space-between;padding-top:22px;border-top:1.5px solid ${C.stroke}}
.mini .gh{display:flex;align-items:center;gap:12px;font-size:22px;font-weight:600}
.mini .gh svg{width:26px;height:26px}
.mini .r{font-size:20px;color:${C.faint};font-weight:500}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:26px}
.vs .side{border-radius:22px;padding:26px 28px 28px;border:1.5px solid ${C.stroke}}
.vs .side .lab{font-size:21px;font-weight:700;letter-spacing:2px}
.vs .side .q{font-size:36px;font-weight:900;margin-top:10px;line-height:1.3}
.vs .side .d{font-size:24px;line-height:1.6;color:${C.sub};margin-top:12px}
.road{margin-top:26px;display:flex;flex-direction:column;gap:14px}
.step{display:grid;grid-template-columns:86px 1fr;align-items:center;border-radius:20px;padding:15px 24px;border:1.5px solid ${C.stroke};background:${C.card}}
.step .n{font-size:40px;font-weight:800}
.step .e{font-size:20px;font-weight:700;letter-spacing:1.5px}
.step .z{font-size:28px;font-weight:700;margin-top:4px}
.step .z span{color:${C.sub};font-weight:500;font-size:24px;margin-left:8px}
.close{margin-top:30px;font-size:34px;font-weight:800;line-height:1.4}
.s1 .body,.s2 .body{font-size:31px}.s1 .box,.s2 .box{margin-top:28px}.s1 .box .v,.s2 .box .v{font-size:29px}.s1 .tags,.s2 .tags{margin-top:30px}
.s2 .body{font-size:32px}.s2 .box{margin-top:34px;padding:26px 30px 28px}.s2 .pair{margin-top:34px}.s2 .pair .box{margin-top:0}.s2 .box .v{font-size:30px}.s2 .tags{margin-top:38px}.s2 .tag{font-size:23px;padding:8px 18px}
.why .head{margin-top:36px}.why .body{font-size:28px;margin-top:28px}.why .body p+p{margin-top:14px}.why .vs{margin-top:22px}.why .road{gap:12px;margin-top:22px}.why .step{padding:12px 24px}
.s3 .lines .ln .dd{font-size:28px}.s3 .lines .ln{margin-top:24px}.s3 .box .v{font-size:28px}
`;

const topbar = (right) => `<div class="topbar"><span class="brand"><span class="dots">${C.acc.map((c) => `<i style="background:${c}"></i>`).join('')}</span>Awesome Multimodal Agentic Coding</span>${right}</div>`;
const mini = (n) => `<div class="mini"><span class="gh">${GH}github.com/jiangjin1999/awesome-multimodal-agentic-coding</span><span class="r">${n} / 5</span></div>`;

// Crop helper: show the source rect (x, y, w, h) of the hero PNG inside a box of width boxW.
function crop(cls, x, y, w, h, boxW) {
  const s = boxW / w;
  return `<div class="${cls}" style="width:${boxW}px;height:${Math.round(h * s)}px"><img src="file://${HERO}" style="width:${3200 * s}px;left:${-x * s}px;top:${-y * s}px"></div>`;
}
// Panel i of the hero spans x = 100 + 1020 i .. +960, y = 264 .. 1424 (PNG pixels).
const panelDiagram = (i) => crop('diag', 100 + 1020 * i + 40, 500, 880, 830, 350);

function cover(qrSvg) {
  const cols = [
    ['01', '视觉作为反馈', '看见自己造的东西，<br>模型才能 loop 起来'],
    ['02', '把模型当作工具', '让 Agent 去调生成、<br>感知和动作模型'],
    ['03', '打通数字与物理世界', '用代码搭仿真、控机器人，<br>从屏幕走到真实世界'],
  ];
  return `<div class="page">
  ${topbar('<span class="agi">TOWARD PHYSICAL AGI</span>')}
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

function why() {
  const steps = [
    ['01', 'VISUAL AS FEEDBACK', '视觉作为反馈', '看见自己造的东西'],
    ['02', 'AGENT ORCHESTRATES MODELS', '把模型当作工具', '+ 让 Agent 去调别的模型'],
    ['03', 'BRIDGING DIGITAL &amp; PHYSICAL', '打通数字与物理世界', '+ 从屏幕走到真实世界'],
  ];
  return `<div class="page why">
  ${topbar('<span class="pageno">多模态视角下的 Coding</span>')}
  <div class="head"><div>
    <span class="chip" style="background:${C.card};color:${C.sub};border:1.5px solid ${C.stroke}">我们的出发点</span>
    <div class="h1">不是 Computer Use<br>而是 <span class="grad">Coding</span></div>
  </div></div>
  <div class="body">
    <p>最近和一些大佬交流，感觉我们的角度还挺有意思，分享下我们的思考。</p>
    <p>我们从六月份开始做多模态 coding。GPT-6 发布后，Computer Use Agent 一下子火了，也让我们之前摸着能力边界做的一些研究失去了意义。</p>
    <p>但我们一直是从 <em>coding</em> 而不是 CUA 的角度来看：</p>
  </div>
  <div class="vs">
    <div class="side" style="background:${C.card}"><div class="lab" style="color:${C.faint}">CUA 视角</div><div class="q" style="color:${C.sub}">「用」现成的软件</div><div class="d">让 Agent 像人一样看屏幕、点按钮，去操作已有的软件。</div></div>
    <div class="side" style="background:${C.tint[0]};border-color:#B6E3FF"><div class="lab" style="color:${C.acc[0]}">CODING 视角</div><div class="q">用代码「造」东西</div><div class="d" style="color:#2B3137">让 Agent 用代码把东西造出来，自己看结果，再自己改好。</div></div>
  </div>
  <div class="body" style="margin-top:28px"><p>我们主要从下面<em>三个阶段</em>来理解：</p></div>
  <div class="road">${steps.map(([n, e, z, d], i) => `<div class="step"><div class="n" style="color:${C.acc[i]}">${n}</div><div><div class="e" style="color:${C.acc[i]}">${e}</div><div class="z">${z}<span>${d}</span></div></div></div>`).join('')}</div>
  ${mini(2)}
</div>`;
}

function stage(i, { en, title, plus, body, n }) {
  return `<div class="page s${i + 1}">
  ${topbar('<span class="pageno">多模态视角下的 Coding</span>')}
  <div class="head"><div>
    <span class="chip" style="background:${C.tint[i]};color:${C.acc[i]}"><span class="n">0${i + 1}</span>${en}</span>
    <div class="h1">${title}</div>
    <div class="plus" style="color:${C.acc[i]}">${plus}</div>
  </div>${panelDiagram(i)}</div>
  ${body}
  ${mini(n)}
</div>`;
}

const s1 = stage(0, {
  n: 3, en: 'VISUAL AS FEEDBACK', title: '有了视觉反馈，<br>模型才能<br>loop 起来', plus: '+ sees what it builds',
  body: `<div class="body"><p>相比于一般的 coding agent，多模态 coding agent 的关键就是有<em>视觉反馈</em>，这一点极大地扩展了 agent 的能力边界——只要能跑出来、看得见，就能放进这个 loop 里。</p></div>
  <div class="box"><div class="k" style="color:${C.acc[0]}">基础 · 原子多模态能力</div>
    <div class="atoms"><div class="atom"><div class="a">Perception</div><div class="b">看得准</div></div><div class="atom"><div class="a">Grounding</div><div class="b">找得到</div></div><div class="atom"><div class="a">Diff</div><div class="b">比得出差别</div></div></div>
    <div class="v">反馈够精准，coding loop 才能更好地跑起来。</div></div>
  <div class="box"><div class="k" style="color:${C.acc[0]}">不只是 VQA 了</div>
    <div class="v">在这之前，通过各种 workflow 也能带来 visual feedback；但在 agent 场景下，模型不只是做 VQA 了，它可以<b>自主地去对比</b>，并对整个「多模态 repo」进行优化。</div></div>
  <div class="tags">${['网页与 UI', '图表与科学可视化', '文档 · 幻灯片 · 海报', '3D 与 CAD', '游戏'].map((t) => `<span class="tag">${t}</span>`).join('')}</div>`,
});

const s2 = stage(1, {
  n: 4, en: 'AGENT ORCHESTRATES MODELS', title: '让 Agent<br>去调<br>别的模型', plus: '+ calls models as tools',
  body: `<div class="body"><p>视觉反馈让 agent 拥有了极大的多模态任务空间。但如果 agent 只能自己看、自己做，不仅会有长上下文带来的幻觉，也可能需要极大量的计算——<em>把其他模型当工具来调</em>，就能有效改善。</p></div>
  <div class="pair">
    <div class="box"><div class="k" style="color:${C.acc[1]}">输入 · 帮 Agent 看</div><div class="v">用更擅长的模型，从不同维度给 agent 提供观察，比如检测、分割、深度、重建。</div></div>
    <div class="box"><div class="k" style="color:${C.acc[1]}">输出 · 帮 Agent 做</div><div class="v">调生成模型来做 mask 重绘、基于白模给出构图；调 action model 来操控机械臂。</div></div>
  </div>
  <div class="box" style="background:${C.tint[1]};border-color:#D8CCF8"><div class="v"><b>一句话：</b>Agent 负责想和写代码，专业的「看」和「做」交给更擅长的模型——能力边界更大，效率也更高。</div></div>
  <div class="tags">${['图像生成', '视频生成', '3D 生成', '世界模型', '感知模型', '动作模型'].map((t) => `<span class="tag">${t}</span>`).join('')}</div>`,
});

const s3 = stage(2, {
  n: 5, en: 'BRIDGING DIGITAL &amp; PHYSICAL', title: '把 loop<br>带进<br>物理世界', plus: '+ acts in simulation and reality',
  body: `<div class="body" style="margin-top:28px"><p>前两个阶段扩展的，都还是数字世界里的能力边界。第三个阶段，我们想把 loop 带进物理世界——这也是仓库里最大、涨得最快的一块。</p></div>
  <div class="lines">
    <div class="ln"><div class="no" style="color:${C.acc[2]}">①</div><div><div class="tt">用代码去动手<span style="color:${C.acc[2]}">DIGITAL → PHYSICAL</span></div><div class="dd">让 agent 自己写 Python、调 ROS 控制机器人，看相机画面和力反馈再改下一步。「看结果改代码」变成了「看动作结果改策略」。</div></div></div>
    <div class="ln"><div class="no" style="color:${C.acc[2]}">②</div><div><div class="tt">把真实世界「搬」进仿真<span style="color:${C.acc[2]}">REAL → SIM</span></div><div class="dd">拿一段真实视频，让 agent 把场景、物体、关节、物理参数写成能跑的仿真器，还能和录像对比、改条件再跑一遍。</div></div></div>
    <div class="ln"><div class="no" style="color:${C.acc[2]}">③</div><div><div class="tt">在仿真里练，再回到现实<span style="color:${C.acc[2]}">SIM → REAL</span></div><div class="dd">自己造数据、攒经验和 skills，先在数字孪生里把失败恢复练一遍，甚至只靠仿真轨迹做后训练，再带回真机。</div></div></div>
  </div>
  <div class="box" style="background:${C.tint[2]};border-color:#FFD8B5;margin-top:24px"><div class="v"><b>说到底是同一个 loop：</b>搭能验证的环境 → 收集交互经验 → 让 agent 变强。代码能跑、能查、能改、能组合，刚好把感知、生成、行动和仿真串起来——这条路最终通向物理 AGI。</div></div>`,
});

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const qrSvg = await QRCode.toString(REPO_URL, { type: 'svg', margin: 0, errorCorrectionLevel: 'M', color: { dark: C.ink, light: '#FFFFFF' } });
  const pages = [['00-cover', cover(qrSvg)], ['01-why-coding', why()], ['02-stage1-visual-feedback', s1], ['03-stage2-orchestrate-models', s2], ['04-stage3-digital-physical', s3]];
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'mmac-promo-'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 2 });
  for (const [name, html] of pages) {
    const file = path.join(tmp, `${name}.html`);
    fs.writeFileSync(file, `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">${fontLinks}<style>${css}</style></head><body>${html}</body></html>`);
    await page.goto(`file://${file}`);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    const over = await page.evaluate(() => {
      const p = document.querySelector('.page');
      return [...p.children].some((el) => el.getBoundingClientRect().bottom > p.getBoundingClientRect().bottom - 52 + 0.5);
    });
    if (over) console.warn(`warning: ${name} content overflows the page`);
    await page.screenshot({ path: path.join(OUT, `${name}.png`) });
    console.log(`wrote promo/images/${name}.png`);
  }
  await browser.close();
})();
