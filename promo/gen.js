// Promo images for "多模态视角下的 Coding": the cover and four pages of the post text (3:4, 1080x1440 at 2x).
// The page text follows section 三 of promo/post.zh-CN.md word for word; only the emphasis is added here.
// Usage (from the repository root):  node promo/gen.js
// Needs Playwright and the npm package `@fontsource/noto-sans-sc` (install it anywhere and point NODE_PATH at
// that node_modules). Without the font package it falls back to system CJK fonts.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(__dirname, 'images');
const HERO = path.join(ROOT, 'assets/hero/hero-light.png'); // 3200 x 1496

let notoDir = null;
try { notoDir = path.dirname(require.resolve('@fontsource/noto-sans-sc/package.json')); } catch (e) { /* system fonts */ }
const fontLinks = notoDir ? [400, 500, 700, 900].map((w) => `<link rel="stylesheet" href="file://${notoDir}/${w}.css">`).join('') : '';

const C = {
  ink: '#1F2328', sub: '#59636E', faint: '#8C959F', card: '#F6F8FA', stroke: '#D8DEE4', text: '#2B3137',
  acc: ['#0969DA', '#8250DF', '#C4500B'], tint: ['#DDF4FF', '#F3EEFF', '#FFF1E5'], mark: ['#CFE6FF', '#E5DAFF', '#FFDCBC'],
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
b{font-weight:700}
.grad{background:linear-gradient(90deg,${C.acc[0]} 0%,${C.acc[1]} 52%,${C.acc[2]} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.big{margin-top:96px;line-height:1}
.big .l1{display:block;font-size:104px;font-weight:900;letter-spacing:2px}
.big .l2{display:inline-block;font-size:178px;font-weight:800;letter-spacing:-5px;margin-top:6px;padding-bottom:14px}
.sub{margin-top:26px;font-size:40px;font-weight:700;letter-spacing:1px}
.heroWrap{margin-top:92px;width:952px;overflow:hidden;position:relative}
.heroWrap img{position:absolute;display:block}
.cols{margin-top:30px;display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.col{padding:2px 6px 0}
.col .t{font-size:27px;font-weight:700;margin-top:2px}
.col .d{font-size:22px;color:${C.sub};margin-top:8px;line-height:1.5}
.link{margin-top:auto;display:flex;align-items:center;justify-content:center;gap:12px;padding-top:26px;
  border-top:1.5px solid ${C.stroke};font-size:25px;font-weight:600}
.link svg{width:28px;height:28px}

/* post pages */
.prog{font-size:20px;font-weight:600;color:${C.faint};letter-spacing:.5px}
.ttl{margin-top:64px;font-size:74px;font-weight:900;line-height:1.15;letter-spacing:1px}
.tsub{margin-top:18px;font-size:32px;font-weight:700;color:${C.sub}}
.txt p{margin-top:22px;font-size:28px;line-height:1.78;color:${C.text}}
.txt b{color:${C.ink}}
.hl{font-weight:700;color:${C.ink};background:linear-gradient(transparent 58%,var(--mark) 58%);padding:0 2px}
.lead{margin-top:34px;padding-left:24px;border-left:6px solid var(--acc);font-size:33px;font-weight:800;line-height:1.5;color:${C.ink}}
.hd{margin-top:46px;display:flex;justify-content:space-between;align-items:flex-start;gap:28px}
.chip{display:inline-flex;align-items:center;gap:10px;font-size:20px;font-weight:700;letter-spacing:2.5px;border-radius:999px;padding:9px 18px;background:var(--tint);color:var(--acc)}
.h2{margin-top:22px;font-size:54px;font-weight:900;line-height:1.25;letter-spacing:.5px}
.diag{flex:none;border-radius:20px;overflow:hidden;position:relative;border:1.5px solid ${C.stroke};background:${C.card}}
.diag img{position:absolute;display:block}
.intro3{margin-top:30px;font-size:28px;font-weight:700}
.stages{margin-top:18px;display:flex;flex-direction:column;gap:12px}
.srow{display:grid;grid-template-columns:80px 1fr;align-items:center;border-radius:20px;padding:14px 24px;border:1.5px solid ${C.stroke};background:${C.card}}
.srow .n{font-size:38px;font-weight:800}
.srow .e{font-size:19px;font-weight:700;letter-spacing:1.5px}
.srow .z{font-size:26px;font-weight:600;margin-top:3px;color:${C.ink}}
.io{margin-top:20px;display:grid;grid-template-columns:1fr 1fr;gap:20px}
.box{border-radius:20px;padding:22px 26px 24px;border:1.5px solid ${C.stroke};background:${C.card}}
.box .k{font-size:22px;font-weight:800;letter-spacing:1px;color:var(--acc);margin-bottom:6px}
.box .v{font-size:27px;line-height:1.66;color:${C.text}}
.box .v b{color:${C.ink}}
.bridge{margin-top:auto;background:${C.tint[2]};border-color:#FFD8B5}
.pull{margin-top:28px;font-size:44px;font-weight:900;line-height:1.3}
.h2{text-wrap:balance}.lead{text-wrap:pretty}.txt p,.box .v{text-wrap:pretty}
.pp1 .ttl{font-size:78px;margin-top:76px}.pp1 .tsub{margin-top:22px}.pp1 .txt p{font-size:30px;margin-top:28px}.pp1 .intro3{margin-top:44px}.pp1 .stages{margin-top:22px;gap:16px}.pp1 .srow .z{font-size:27px}
.pp2 .txt p{font-size:32px;margin-top:26px}.pp2 .lead{font-size:37px;margin-top:40px}
.pp3 .txt p{font-size:30px}.pp3 .lead{font-size:33px;text-wrap:wrap}.pp3 .box .v{font-size:28px}
.pp4 .txt p{font-size:30px}.pp4 .pull{font-size:48px}.pp4 .box .v{font-size:28px}
.endbox{margin-top:auto;background:linear-gradient(90deg,${C.tint[0]},${C.tint[1]} 55%,${C.tint[2]});border-color:#E3DDF3}
`;

// Show the source rect (x, y, w, h) of the hero PNG inside a box of width boxW.
function crop(cls, x, y, w, h, boxW) {
  const s = boxW / w;
  return `<div class="${cls}" style="width:${boxW}px;height:${Math.round(h * s)}px"><img src="file://${HERO}" style="width:${3200 * s}px;left:${-x * s}px;top:${-y * s}px"></div>`;
}

function cover() {
  const cols = [
    ['01', '视觉作为反馈', '看见自己造的东西，<br>模型才能 loop 起来'],
    ['02', '把模型当作工具', '让 Agent 去调生成、<br>感知和动作模型'],
    ['03', '打通数字与物理世界', '用代码搭仿真、控机器人，<br>从屏幕走到真实世界'],
  ];
  return `<div class="page">
  <div class="topbar"><span class="brand"><span class="dots">${C.acc.map((c) => `<i style="background:${c}"></i>`).join('')}</span>Awesome Multimodal Agentic Coding</span><span class="agi">TOWARD PHYSICAL AGI</span></div>
  <h1 class="big"><span class="l1">多模态视角下的</span><span class="l2 grad">Coding</span></h1>
  <div class="sub">扩展 Agent 能力边界，最终通向物理 AGI</div>
  ${crop('heroWrap', 96, 256, 3008, 1176, 952)}
  <div class="cols">${cols.map(([n, t, d], i) => `<div class="col"><div class="t"><span style="color:${C.acc[i]}">${n}</span>&nbsp; ${t}</div><div class="d">${d}</div></div>`).join('')}</div>
  <div class="link">${GH}github.com/jiangjin1999/awesome-multimodal-agentic-coding</div>
</div>`;
}

const vars = (i) => `--acc:${C.acc[i]};--tint:${C.tint[i]};--mark:${C.mark[i]}`;
const topbar = (n) => `<div class="topbar"><span class="brand"><span class="dots">${C.acc.map((c) => `<i style="background:${c}"></i>`).join('')}</span>Awesome Multimodal Agentic Coding</span><span class="prog">多模态视角下的 Coding · ${n} / 4</span></div>`;
// Panel i of the hero spans x = 100 + 1020 i .. +960 (PNG pixels); this crop keeps its loop diagram.
const diagram = (i, w = 300) => crop('diag', 100 + 1020 * i + 40, 500, 880, 830, w);
const hl = (t) => `<span class="hl">${t}</span>`;
const head = (i, chip, title, w) => `<div class="hd"><div><span class="chip">${chip}</span><div class="h2">${title}</div></div>${diagram(i, w)}</div>`;

function intro() {
  const rows = [
    ['Visual as Feedback', '有了视觉反馈，模型才能真正 loop 起来'],
    ['Agent Orchestrates Models', '让 Agent 去调生成、感知、动作模型，能力边界进一步扩展'],
    ['Bridging Digital &amp; Physical', '用代码搭仿真、控机器人，从屏幕走到真实世界'],
  ];
  return `<div class="page pp1" style="${vars(1)}">
  ${topbar(1)}
  <div class="ttl">多模态视角下的 <span class="grad">Coding</span></div>
  <div class="tsub">扩展 Agent 能力边界，最终通向物理 AGI</div>
  <div class="txt">
    <p>最近和一些同学交流，感觉我们的角度还挺有意思的，所以分享下我们的思考。</p>
    <p>我们从六月份开始做多模态 agentic coding 相关的任务。GPT-6 发布后，Computer Use Agent 一下子火了，也让我们之前摸着能力边界做的一些研究显得不那么前沿了（一个人做也确实比较慢）。</p>
    <p>但我们一直是从 ${hl('coding 的角度、而不是 CUA 的角度')}来看这件事。最近 <b>Robot Use Agent</b> 也越来越多：让 Agent 直接写代码控制机器人，再加上 <b>Real2Sim2Real</b>，这些都是${hl('多模态 coding 这条线往物理世界的延伸')}。其实从 coding 的角度来看，这个发展是很自然的。</p>
  </div>
  <div class="intro3">我们主要从下面三个阶段来理解：</div>
  <div class="stages">${rows.map(([e, z], i) => `<div class="srow"><div class="n" style="color:${C.acc[i]}">0${i + 1}</div><div><div class="e" style="color:${C.acc[i]}">${e.toUpperCase()}</div><div class="z">${z}</div></div></div>`).join('')}</div>
</div>`;
}

function stage1() {
  return `<div class="page pp2" style="${vars(0)}">
  ${topbar(2)}
  ${head(0, '01 · VISUAL AS FEEDBACK', '有了视觉反馈，<br>模型才能<br>loop 起来', 340)}
  <div class="lead">视觉反馈和 perception 能力的提升，让模型可以真正 loop 起来。</div>
  <div class="txt">
    <p>相比于一般的 coding agent，多模态 coding agent 的关键就是有${hl('视觉反馈')}，这一点<b>极大地扩展了 agent 的能力边界</b>。网页、图表、PPT、3D/CAD、游戏……${hl('只要能跑出来、看得见，就能放进这个 loop 里')}。</p>
    <p>其中，<b>perception、grounding 以及 diff</b> 这些原子多模态能力是基础：看得准、找得到、比得出差别。${hl('反馈够精准，coding loop 才能更好地跑起来')}。</p>
    <p>当然，在这之前通过各种 workflow 也能带来 visual feedback；但在 agent 场景下，${hl('模型不只是做 VQA 了')}，它可以自主地去对比，并且对整个<b>「多模态 repo」</b>进行优化。</p>
  </div>
</div>`;
}

function stage2() {
  return `<div class="page pp3" style="${vars(1)}">
  ${topbar(3)}
  ${head(1, '02 · AGENT ORCHESTRATES MODELS', '让 Agent<br>去调<br>别的模型')}
  <div class="lead">Agent 去 orchestrate 各种模型（其他 VLM、生成模型、action model 等），进一步扩展了能力边界，也提高了效率。</div>
  <div class="txt">
    <p>视觉反馈让 agent 拥有了极大的多模态任务空间。但如果 agent 只能自己看、自己做，不仅会有<b>长上下文带来的幻觉</b>，也可能需要<b>极大量的计算</b>；${hl('把其他模型当作工具来调，就能有效改善效率和效果')}。</p>
    <p>orchestration 既体现在输入，也体现在输出：</p>
  </div>
  <div class="io">
    <div class="box"><div class="k">输入</div><div class="v">用更擅长的模型，从不同维度给 agent 提供观察，比如检测、分割、深度、重建；</div></div>
    <div class="box"><div class="k">输出</div><div class="v">调生成模型来做 mask 重绘、基于白模给出构图；也可以调 action model 来操控机械臂。</div></div>
  </div>
  <div class="box bridge"><div class="k" style="color:${C.acc[2]}">→ 03</div><div class="v">上面两个阶段为第三个阶段打下了扎实的基础：视觉反馈让 agent 能看清每一步的结果，把模型当工具来调，又让它能借用感知、生成和动作模型的能力。<b>走进物理世界，靠的正是这两样。</b></div></div>
</div>`;
}

function stage3() {
  return `<div class="page pp4" style="${vars(2)}">
  ${topbar(4)}
  ${head(2, '03 · BRIDGING DIGITAL &amp; PHYSICAL', '把 loop<br>带进<br>物理世界')}
  <div class="txt">
    <p>前两个阶段不断扩展着 coding agent 的能力边界，但都还在 digital world 里。很自然地，我们想把这个 loop 带进 physical world。这也是我们仓库里现在最大、涨得最快的一块。</p>
  </div>
  <div class="pull grad">Agentic Loop 是一切想法的开始。</div>
  <div class="txt">
    <p style="margin-top:12px">coding控制的就是一台机器人，${hl('「看结果改代码」变成了「看动作结果改策略」')}。最近的 <b>Robot Use Agent</b> 做的正是这件事：不用专门训练一个策略，只给现成的 coding agent 一个终端和机器人的感知、运动接口，它就能自己写 Python 让机器人干活，看相机画面和执行结果，失败了就改代码再试。但真机上的 loop <b>又慢又贵</b>，于是很自然地想先把真实世界「搬」进代码里，而前两个阶段的发展为 <b>Real2Sim</b> 提供了可能；再在仿真里把 loop 转得又快又多，造数据、攒经验，最后把能力带回真机。${hl('这一切又是基模的故事了')}</p>
  </div>
  <div class="box endbox"><div class="k" style="color:${C.ink}">最后</div><div class="v">三个阶段是层层叠上去的。我们相信，沿着「写代码 → 看结果 → 再改」这条路，agent 会一步步从屏幕走进真实世界，<b>最终通向物理 AGI</b>。</div></div>
</div>`;
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const pages = [
    ['cover', cover()],
    ['post-1-intro', intro()],
    ['post-2-visual-feedback', stage1()],
    ['post-3-orchestrate-models', stage2()],
    ['post-4-digital-physical', stage3()],
  ];
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'mmac-promo-'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 2 });
  for (const [name, html] of pages) {
    const file = path.join(dir, `${name}.html`);
    fs.writeFileSync(file, `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">${fontLinks}<style>${css}</style></head><body>${html}</body></html>`);
    await page.goto(`file://${file}`);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    const spare = await page.evaluate(() => {
      const p = document.querySelector('.page');
      const kids = [...p.children];
      const last = kids[kids.length - 1].getBoundingClientRect();
      const prev = kids.length > 1 ? kids[kids.length - 2].getBoundingClientRect().bottom : last.top;
      const overflow = Math.round(p.getBoundingClientRect().bottom - 52 - last.bottom);
      return overflow < 0 ? overflow : Math.round(last.top - prev);
    });
    if (spare < 0) console.warn(`warning: ${name} overflows by ${-spare}px`);
    await page.screenshot({ path: path.join(OUT, `${name}.png`) });
    console.log(`wrote promo/images/${name}.png (gap before last block ${spare}px)`);
  }
  await browser.close();
})();
