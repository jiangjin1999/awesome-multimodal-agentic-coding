"""Render the simulator-evaluation overview figure from `eval_ladder` in data/site.yaml.

The figure opens stage3/simulator-evaluation.md and its Chinese translation: one kitchen
simulation walked through every level, each card showing how the level checks it, the
question it asks and the fake simulation it exposes. build_readme.py writes a light and a
dark SVG per guide language under assets/eval-ladder/, and `--check` fails when one is stale.

Each level lists its works as `<work id>` or `<work id> †` (an evaluator); the figure only
counts them, so keep the lists in step with the guide's tables.
"""
import math
from html import escape

from engine_map import FONTS, PALETTE as MAP_PALETTE, localize, text_width

LANGS = ('en', 'zh')            # the languages stage3/simulator-evaluation*.md exists in
THEMES = ('light', 'dark')
OUT_DIR = 'assets/eval-ladder'
EVALUATOR = '†'
PICTOGRAMS = ('checklist', 'photo', 'floating', 'door', 'film', 'ramps', 'predict', 'rank')

# Ordinal blue ramp, one step per stage (validated as ordinal against each surface).
RAMP = {
    'light': ('#86B6EF', '#5598E7', '#2A78D6', '#1C5CAB', '#104281'),
    'dark': ('#3987E5', '#4E95E8', '#6DA7EC', '#86B6EF', '#9EC5F4'),
}
BAD = {'light': '#CF222E', 'dark': '#F85149'}

# Geometry (SVG user units).
M, CW, GX = 28, 248, 24          # margin, card width, gap between cards
PW, PH = 220, 104                 # pictogram panel
FS_Q, FS_F, LH = 14, 13, 20

NO_BREAK_BEFORE = set('，。、？！：；）」』”’,.?!:;)%·')
NO_BREAK_AFTER = set('（「『“‘(')


def palette(theme):
    p = MAP_PALETTE[theme]
    return {
        'bg': p['bg'], 'frame': p['frame'], 'ink': p['ink'], 'sub': p['sub'], 'line': p['line'],
        'panel': p['inherit_fill'], 'fill': '#EAEEF2' if theme == 'light' else '#262C36',
        'bad': BAD[theme], 'ramp': RAMP[theme],
    }


def tokens(text):
    """Latin words stay whole; CJK breaks between characters."""
    out, word = [], ''
    for ch in text:
        if ord(ch) >= 0x2E80:
            if word:
                out.append(word)
                word = ''
            out.append(ch)
        elif ch == ' ':
            out.append(word + ' ')
            word = ''
        else:
            word += ch
    if word:
        out.append(word)
    return [t for t in out if t]


def wrap(text, width, size):
    lines = []
    for para in str(text).split('\n'):
        line = ''
        for tok in tokens(para):
            if line and text_width((line + tok).rstrip(), size) > width:
                # Keep closing punctuation on this line and opening punctuation on the next.
                if tok[0] in NO_BREAK_BEFORE:
                    line, tok = line + tok, ''
                elif line[-1] in NO_BREAK_AFTER:
                    line, tok = line[:-1], line[-1] + tok
                lines.append(line.rstrip())
                line = tok
            else:
                line += tok
        if line.strip() or not lines:
            lines.append(line.rstrip())
    return lines


def parse_work(spec):
    wid, _, mark = str(spec).partition(' ')
    return wid, mark.strip() == EVALUATOR


def cards(site):
    """Levels in reading order, each with the index of its stage."""
    return [(si, level) for si, stage in enumerate(site['eval_ladder']['stages']) for level in stage['levels']]


def validate(site, works):
    ladder = site.get('eval_ladder')
    if not ladder:
        return []
    errors = []
    ids = {w['id'] for w in works}
    localized = [(f'text.{k}', v) for k, v in (ladder.get('text') or {}).items()]
    localized += [(f'pic.{k}', v) for k, v in (ladder.get('pic') or {}).items()]
    for key in ('title', 'alt', 'lead', 'note', 'fake', 'or', 'work', 'evaluator', 'count'):
        if key not in (ladder.get('text') or {}):
            errors.append(f'eval_ladder: text.{key} missing')
    for i, stage in enumerate(ladder.get('stages') or []):
        localized.append((f'stages[{i}].name', stage.get('name')))
        if not stage.get('levels'):
            errors.append(f'eval_ladder: stage {i} has no levels')
    all_cards = [lv for st in ladder.get('stages') or [] for lv in st.get('levels') or []]
    if len(all_cards) != 8:
        errors.append(f'eval_ladder: expected 8 levels (two rows of four cards), found {len(all_cards)}')
    for level in all_cards:
        code = level.get('code')
        for field in ('name', 'question', 'fake'):
            localized.append((f'{code}.{field}', level.get(field)))
        if level.get('pic') not in PICTOGRAMS:
            errors.append(f"eval_ladder: {code} has unknown pictogram {level.get('pic')!r}")
        if not level.get('works'):
            errors.append(f'eval_ladder: {code} lists no works')
        for spec in level.get('works') or []:
            wid, _ = parse_work(spec)
            if wid not in ids:
                errors.append(f'eval_ladder: {code} work {wid} not found')
    for where, value in localized:
        for lang in LANGS:
            if not (value or {}).get(lang):
                errors.append(f'eval_ladder: {where} missing {lang}')
    return errors


def pictogram(kind, p, accent, words):
    """One small scene per level, in a 220 x 104 box."""
    ink, sub, fill, bad, panel = p['ink'], p['sub'], p['fill'], p['bad'], p['panel']
    s = []
    a = s.append
    stroke = f'stroke="{ink}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"'

    def arrow(color):
        return f'marker-end="url(#arr-{color[1:]})"'

    def table(x, y, w, floor=96):
        a(f'<rect x="{x}" y="{y}" width="{w}" height="6" rx="1.5" fill="{fill}" {stroke}/>')
        a(f'<line x1="{x + 7}" y1="{y + 6}" x2="{x + 7}" y2="{floor}" {stroke}/>')
        a(f'<line x1="{x + w - 7}" y1="{y + 6}" x2="{x + w - 7}" y2="{floor}" {stroke}/>')

    def cup(x, yb, color=None, dash='', rot=0, opacity=1):
        c = color or ink
        t = f' transform="rotate({rot:g} {x:g} {yb - 9:g})"' if rot else ''
        o = f' opacity="{opacity}"' if opacity != 1 else ''
        d = f' stroke-dasharray="{dash}"' if dash else ''
        a(f'<g{t}{o}><path d="M{x - 8:g} {yb - 18:g} L{x + 8:g} {yb - 18:g} L{x + 6:g} {yb:g} L{x - 6:g} {yb:g} Z" fill="{panel}" '
          f'stroke="{c}" stroke-width="1.6" stroke-linejoin="round"{d}/>'
          f'<path d="M{x + 7.5:g} {yb - 14:g} q7 1 5 7 q-1 3 -6 3" fill="none" stroke="{c}" stroke-width="1.6"{d}/></g>')

    def cabinet(x, y, w, h):
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{fill}" {stroke}/>')
        a(f'<line x1="{x + w - 8}" y1="{y + h / 2 - 6:g}" x2="{x + w - 8}" y2="{y + h / 2 + 6:g}" {stroke}/>')

    def floor(x1=8, x2=212, y=96):
        a(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{sub}" stroke-width="1.2"/>')

    def label(x, y, t, color=None, anchor='middle', size=11, bold=False):
        w = ' font-weight="700"' if bold else ''
        a(f'<text x="{x:g}" y="{y:g}" text-anchor="{anchor}" font-size="{size}"{w} fill="{color or sub}">{escape(t)}</text>')

    def tick(x, y, ok):
        if ok:
            a(f'<path d="M{x - 4} {y} l3 3.5 l6 -7" fill="none" stroke="{ink}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
        else:
            a(f'<path d="M{x - 4} {y - 4} l8 8 M{x + 4} {y - 4} l-8 8" stroke="{bad}" stroke-width="1.8" stroke-linecap="round"/>')

    if kind == 'checklist':                       # L0a: tick the requirements off a list
        a(f'<rect x="12" y="10" width="76" height="86" rx="4" fill="{panel}" {stroke}/>')
        a(f'<rect x="37" y="5" width="26" height="9" rx="2" fill="{fill}" {stroke}/>')
        for i, (key, ok) in enumerate((('table', True), ('cabinet', True), ('cup', False))):
            y = 34 + i * 22
            tick(25, y - 3, ok)
            label(36, y + 1, words[key], ink, 'start', 11.5)
        floor(98, 212)
        table(102, 58, 68)
        cabinet(178, 26, 32, 70)
        cup(136, 58, accent, '3 2.5')
        label(136, 32, '?', accent, size=15, bold=True)
    elif kind == 'photo':                         # L0b: compare with a reference photo
        a(f'<rect x="10" y="12" width="84" height="70" rx="3" fill="{panel}" {stroke}/>')
        a(f'<rect x="16" y="18" width="72" height="58" fill="{fill}"/>')
        a(f'<line x1="20" y1="70" x2="84" y2="70" stroke="{sub}" stroke-width="1"/>')
        a(f'<rect x="24" y="46" width="32" height="3" fill="{ink}"/>'
          f'<line x1="27" y1="49" x2="27" y2="70" stroke="{ink}" stroke-width="1.2"/>'
          f'<line x1="53" y1="49" x2="53" y2="70" stroke="{ink}" stroke-width="1.2"/>')
        a(f'<rect x="62" y="30" width="18" height="40" fill="none" stroke="{ink}" stroke-width="1.2"/>')
        a(f'<path d="M36 46 l8 0 l-1 -8 l-6 0 Z" fill="none" stroke="{ink}" stroke-width="1.2"/>')
        label(52, 97, words['reference'])
        label(112, 54, '≈?', accent, size=16, bold=True)
        floor(130, 214, 80)
        table(134, 50, 42, 80)
        cabinet(182, 22, 26, 58)
        cup(153, 50)
        label(172, 97, words['built'])
    elif kind == 'floating':                      # L1: inspect contacts while nothing moves
        floor()
        table(40, 64, 132)
        cabinet(178, 26, 32, 70)
        cup(100, 50)
        a(f'<line x1="90" y1="57" x2="110" y2="57" stroke="{bad}" stroke-width="1.4" stroke-dasharray="2.5 2"/>')
        a(f'<circle cx="100" cy="56" r="21" fill="none" stroke="{accent}" stroke-width="2.4"/>')
        a(f'<line x1="115" y1="71" x2="128" y2="84" stroke="{accent}" stroke-width="4" stroke-linecap="round"/>')
        label(74, 40, words['floating'], bad, 'end', 12, True)
    elif kind == 'door':                          # L2: pull the cabinet door
        floor()
        a(f'<rect x="84" y="14" width="78" height="82" rx="2" fill="{fill}" {stroke}/>')
        a(f'<line x1="88" y1="56" x2="158" y2="56" {stroke}/>')
        cup(123, 56)
        a(f'<path d="M84 16 L46 26 L46 86 L84 94 Z" fill="{panel}" {stroke}/>')
        a(f'<line x1="52" y1="52" x2="52" y2="62" {stroke}/>')
        for y in (28, 82):
            a(f'<circle cx="84" cy="{y}" r="2.6" fill="{accent}"/>')
        a(f'<path d="M154 30 A 64 34 0 0 0 54 20" fill="none" stroke="{accent}" stroke-width="2.2" {arrow(accent)}/>')
        label(25, 48, words['pull'], accent, 'middle', 12.5, True)
        a(f'<line x1="42" y1="57" x2="12" y2="57" stroke="{accent}" stroke-width="2.2" {arrow(accent)}/>')
    elif kind == 'film':                          # L3a: compare the fall with footage
        floor(6, 130)
        table(8, 40, 64)
        cup(58, 40, None, '', 0, .45)
        a(f'<path d="M68 30 Q 96 26 100 76" fill="none" stroke="{accent}" stroke-width="1.8" stroke-dasharray="3 3" {arrow(accent)}/>')
        cup(104, 96, accent, '', 90)
        a(f'<rect x="152" y="8" width="58" height="84" rx="3" fill="{ink}"/>')
        for i in range(6):
            a(f'<rect x="155" y="{12 + i * 13.5:g}" width="5" height="7" rx="1" fill="{panel}"/>'
              f'<rect x="202" y="{12 + i * 13.5:g}" width="5" height="7" rx="1" fill="{panel}"/>')
        for i in range(3):
            a(f'<rect x="163" y="{12 + i * 26.5:g}" width="36" height="22" rx="1" fill="{panel}"/>')
            cx, cy = 172 + i * 9, 26 + i * 28.5
            a(f'<rect x="{cx - 3}" y="{cy - 6:g}" width="6" height="7" fill="{sub}" transform="rotate({i * 45} {cx} {cy:g})"/>')
        label(181, 103, words['footage'])
        label(132, 52, '≈?', accent, size=15, bold=True)
    elif kind == 'ramps':                         # L3b: change the conditions and rerun
        floor()
        for x0, h, run, land, col, key in ((10, 26, 78, 102, sub, 'before'), (116, 52, 64, 204, accent, 'after')):
            a(f'<path d="M{x0} 96 L{x0} {96 - h} L{x0 + run} 96 Z" fill="{fill}" {stroke}/>')
            along = run * .42
            cup(x0 + along, 96 - h + h * along / run - 1, accent if col == accent else None, '',
                math.degrees(math.atan2(h, run)))
            a(f'<path d="M{x0 + run - 4} 92 Q {x0 + run + 6} 92 {land} 95" fill="none" stroke="{col}" stroke-width="1.8" '
              f'stroke-dasharray="3 3" {arrow(col)}/>')
            label(x0, 96 - h - 12, words[key], col, 'start', 11.5, col == accent)
    elif kind == 'predict':                       # L3c: from the first seconds, predict the rest
        a(f'<line x1="16" y1="84" x2="208" y2="84" stroke="{sub}" stroke-width="1.2" {arrow(sub)}/>')
        a(f'<line x1="16" y1="84" x2="16" y2="10" stroke="{sub}" stroke-width="1.2"/>')
        a(f'<path d="M16 78 C 40 74, 60 40, 84 34" fill="none" stroke="{ink}" stroke-width="2.2"/>')
        a(f'<path d="M84 34 C 108 28, 130 46, 150 56 S 188 66, 204 64" fill="none" stroke="{accent}" stroke-width="2.2" stroke-dasharray="5 4"/>')
        a(f'<line x1="84" y1="12" x2="84" y2="84" stroke="{sub}" stroke-width="1" stroke-dasharray="2 3"/>')
        label(50, 98, words['given'])
        label(146, 98, words['predicted'], accent, bold=True)
        x = 212
        for key in ('friction', 'mass'):
            w = text_width(words[key], 10.5) + 12
            x -= w
            a(f'<rect x="{x:g}" y="8" width="{w:g}" height="18" rx="9" fill="{panel}" stroke="{accent}" stroke-width="1.4"/>')
            label(x + w / 2, 21, words[key], ink, size=10.5)
            x -= 6
    elif kind == 'rank':                          # L4: does the ranking carry over to the real world?
        label(48, 13, words['in_sim'], ink, size=11.5, bold=True)
        label(172, 13, words['in_real'], ink, size=11.5, bold=True)
        ys = (34, 60, 86)
        order = {'A': (0, 0), 'B': (1, 2), 'C': (2, 1)}
        for k, (left, right) in order.items():
            col = accent if k == 'A' else sub
            a(f'<line x1="60" y1="{ys[left]}" x2="160" y2="{ys[right]}" stroke="{col}" stroke-width="{2.4 if k == "A" else 1.6}"/>')
        for k, (left, right) in order.items():
            col = accent if k == 'A' else sub
            for x, y in ((48, ys[left]), (172, ys[right])):
                a(f'<circle cx="{x}" cy="{y}" r="10" fill="{panel}" stroke="{col}" stroke-width="1.8"/>')
                label(x, y + 4, k, ink, size=11.5, bold=True)
        for i, y in enumerate(ys):
            label(19, y + 4, words['rank'].format(n=i + 1), sub, 'middle', 10.5)
        label(110, 26, words['same'], accent, 'middle', 11, True)
    return '\n'.join(s)


def render(site, lang, theme):
    ladder = site['eval_ladder']
    text = {k: localize(v, lang) for k, v in ladder['text'].items()}
    words = {k: localize(v, lang) for k, v in ladder['pic'].items()}
    stages = ladder['stages']
    deck = cards(site)
    p = palette(theme)
    ramp = p['ramp']
    width = M * 2 + CW * 4 + GX * 3
    out = []
    o = out.append

    # Card text, measured first so every card shares one height.
    name_avail = CW - 74
    names = [localize(lv['name'], lang) for _, lv in deck]
    fs_name = next((s for s in (16, 15, 14) if all(text_width(n, s) <= name_avail for n in names)), 13)
    qs = [wrap(localize(lv['question'], lang), CW - 28, FS_Q) for _, lv in deck]
    fakes = [wrap(localize(lv['fake'], lang), CW - 46, FS_F) for _, lv in deck]
    y_q = 46 + PH + 26
    y_f = y_q + LH * (max(map(len, qs)) - 1) + 30
    card_h = y_f + 26 + LH * (max(map(len, fakes)) - 1) + 40

    lead = wrap(text['lead'], width - 2 * M, 14.5)
    y = M + 40 + 22 * len(lead) + 16
    rows_y = []
    for _ in range(2):
        rows_y.append(y + 30)                     # stage bracket band above each row
        y += 30 + card_h + 26
    legend = [(False, text['work']), (True, text['evaluator'])]
    legend_w = sum(18 + text_width(t, 12.5) + 14 for _, t in legend)
    note = wrap(text['note'], width - 2 * M - legend_w - 24, 12.5)
    y_note = y + 8
    height = y_note + 18 * (len(note) - 1) + M

    def cx(i):
        return M + (i % 4) * (CW + GX)

    def cy(i):
        return rows_y[i // 4]

    o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height:g}" width="{width}" height="{height:g}" '
      f'role="img" aria-label="{escape(text["title"])}" font-family="{escape(FONTS[lang])}">')
    o(f'<title>{escape(text["title"])}</title>')
    o('<defs>')
    for c in sorted(set(ramp) | {p['sub']}):
        o(f'<marker id="arr-{c[1:]}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
          f'<path d="M1 1 L9 5 L1 9 Z" fill="{c}"/></marker>')
    for i in range(len(deck)):
        o(f'<clipPath id="card-{i}"><rect x="{cx(i)}" y="{cy(i):g}" width="{CW}" height="{card_h:g}" rx="10"/></clipPath>')
    o('</defs>')
    # Opaque card, so either variant stays legible on any page theme.
    o(f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1:g}" rx="12" fill="{p["bg"]}" stroke="{p["frame"]}"/>')
    o(f'<text x="{M}" y="{M + 24}" font-size="22" font-weight="700" fill="{p["ink"]}">{escape(text["title"])}</text>')
    for i, line in enumerate(lead):
        o(f'<text x="{M}" y="{M + 56 + i * 22}" font-size="14.5" fill="{p["sub"]}">{escape(line)}</text>')

    # Stage brackets above the cards.
    first = 0
    for si, stage in enumerate(stages):
        a, b = first, first + len(stage['levels']) - 1
        first = b + 1
        x1, x2, yb = cx(a), cx(b) + CW, cy(a) - 14
        name = localize(stage['name'], lang)
        tw, mx = text_width(name, 13) + 20, (cx(a) + cx(b) + CW) / 2
        o(f'<path d="M{x1 + 1} {yb + 6:g} V{yb:g} H{x2 - 1} V{yb + 6:g}" fill="none" stroke="{ramp[si]}" stroke-width="2"/>')
        o(f'<rect x="{mx - tw / 2:g}" y="{yb - 11:g}" width="{tw:g}" height="22" rx="11" fill="{p["bg"]}" stroke="{ramp[si]}" stroke-width="2"/>')
        o(f'<text x="{mx:g}" y="{yb + 4.5:g}" text-anchor="middle" font-size="13" font-weight="700" fill="{p["ink"]}">{escape(name)}</text>')

    # Flow: L0a and L0b are parallel starting points; arrows elsewhere; a turn between rows.
    for i in range(len(deck) - 1):
        if i == 3:
            continue
        x1, x2, ym = cx(i) + CW + 4, cx(i + 1) - 4, cy(i) + 26
        if deck[i][0] == deck[i + 1][0] == 0:
            mx = (x1 + x2) / 2
            o(f'<circle cx="{mx:g}" cy="{ym:g}" r="11" fill="{p["bg"]}" stroke="{p["sub"]}" stroke-width="1.2"/>')
            o(f'<text x="{mx:g}" y="{ym + 4:g}" text-anchor="middle" font-size="11.5" fill="{p["sub"]}">{escape(text["or"])}</text>')
        else:
            o(f'<line x1="{x1}" y1="{ym:g}" x2="{x2 - 2}" y2="{ym:g}" stroke="{p["sub"]}" stroke-width="1.6" marker-end="url(#arr-{p["sub"][1:]})"/>')
    yt = cy(3) + card_h + 13
    o(f'<path d="M{cx(3) + CW / 2:g} {cy(3) + card_h + 2:g} V{yt:g} H{cx(4) + 60} V{cy(4) - 22:g}" fill="none" stroke="{p["sub"]}" '
      f'stroke-width="1.6" stroke-linejoin="round" marker-end="url(#arr-{p["sub"][1:]})"/>')

    for i, (si, level) in enumerate(deck):
        x, y0 = cx(i), cy(i)
        col = ramp[si]
        # The lightest light-theme step is too faint for line art; draw that stage's pictograms one step darker.
        accent = ramp[1] if theme == 'light' and si == 0 else col
        o(f'<rect x="{x + .5}" y="{y0 + .5:g}" width="{CW - 1}" height="{card_h - 1:g}" rx="10" fill="{p["bg"]}" stroke="{p["frame"]}"/>')
        o(f'<rect x="{x}" y="{y0:g}" width="{CW}" height="5" fill="{col}" clip-path="url(#card-{i})"/>')
        cw = text_width(level['code'], 13) + 14
        o(f'<rect x="{x + 14}" y="{y0 + 16:g}" width="{cw:g}" height="21" rx="4" fill="none" stroke="{accent}" stroke-width="1.8"/>')
        o(f'<text x="{x + 21}" y="{y0 + 31:g}" font-size="13" font-weight="700" fill="{p["ink"]}">{escape(level["code"])}</text>')
        o(f'<text x="{x + 22 + cw:g}" y="{y0 + 32:g}" font-size="{fs_name}" font-weight="700" fill="{p["ink"]}">{escape(names[i])}</text>')
        px, py = x + (CW - PW) / 2, y0 + 46
        o(f'<rect x="{px:g}" y="{py:g}" width="{PW}" height="{PH}" rx="6" fill="{p["panel"]}"/>')
        o(f'<g transform="translate({px:g} {py:g})">\n{pictogram(level["pic"], p, accent, words)}\n</g>')
        for j, line in enumerate(qs[i]):
            o(f'<text x="{x + 14}" y="{y0 + y_q + j * LH:g}" font-size="{FS_Q}" font-weight="600" fill="{p["ink"]}">{escape(line)}</text>')
        o(f'<line x1="{x + 14}" y1="{y0 + y_f - 20:g}" x2="{x + CW - 14}" y2="{y0 + y_f - 20:g}" stroke="{p["line"]}" stroke-dasharray="3 3"/>')
        o(f'<text x="{x + 14}" y="{y0 + y_f - 2:g}" font-size="11.5" fill="{p["sub"]}">{escape(text["fake"])}</text>')
        for j, line in enumerate(fakes[i]):
            yy = y0 + y_f + 18 + j * LH
            if j == 0:
                o(f'<path d="M{x + 16} {yy - 9:g} l8 8 M{x + 24} {yy - 9:g} l-8 8" stroke="{p["bad"]}" stroke-width="2" stroke-linecap="round"/>')
            o(f'<text x="{x + 32}" y="{yy:g}" font-size="{FS_F}" fill="{p["ink"]}">{escape(line)}</text>')
        works = [parse_work(spec) for spec in level['works']]
        yd = y0 + card_h - 18
        for k, (_, is_eval) in enumerate(works):
            dx = x + 18 + k * 12
            if is_eval:
                o(f'<circle cx="{dx}" cy="{yd:g}" r="3.8" fill="none" stroke="{p["sub"]}" stroke-width="1.4"/>')
            else:
                o(f'<circle cx="{dx}" cy="{yd:g}" r="4.5" fill="{p["sub"]}"/>')
        count = text['count'].format(n=len(works))
        o(f'<text x="{x + 18 + len(works) * 12 + 2}" y="{yd + 4:g}" font-size="11.5" fill="{p["sub"]}">{escape(count)}</text>')

    # Bottom: reading note on the left, dot legend on the right.
    for j, line in enumerate(note):
        o(f'<text x="{M}" y="{y_note + 8 + j * 18:g}" font-size="12.5" fill="{p["sub"]}">{escape(line)}</text>')
    lx = width - M - legend_w
    for is_eval, t in legend:
        if is_eval:
            o(f'<circle cx="{lx + 4.5:g}" cy="{y_note + 4:g}" r="3.8" fill="none" stroke="{p["sub"]}" stroke-width="1.4"/>')
        else:
            o(f'<circle cx="{lx + 4.5:g}" cy="{y_note + 4:g}" r="4.5" fill="{p["sub"]}"/>')
        o(f'<text x="{lx + 15:g}" y="{y_note + 8:g}" font-size="12.5" fill="{p["sub"]}">{escape(t)}</text>')
        lx += 18 + text_width(t, 12.5) + 14
    o('</svg>')
    return '\n'.join(out) + '\n'


def outputs(site):
    """Yield (relative path, SVG text) for every guide language and theme."""
    if not site.get('eval_ladder'):
        return
    for lang in LANGS:
        for theme in THEMES:
            yield f'{OUT_DIR}/eval-ladder-{lang}-{theme}.svg', render(site, lang, theme)
