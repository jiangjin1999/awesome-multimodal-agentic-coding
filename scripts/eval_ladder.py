"""Render the 3.3 simulator-evaluation ladder from `eval_ladder` in data/site.yaml.

One source feeds two outputs: a light and a dark SVG per language under assets/eval-ladder/
(a running example walked through every level, with what each level cannot catch), and the
Markdown table of works under it. build_readme.py writes the SVGs with the READMEs, places
them with the `{eval_ladder}` and `{eval_table}` placeholders in the 3.3 guide, and
`--check` fails when one is stale.

Each level lists its works as `<work id>` or `<work id> †` (an evaluator); the label shown
is `labels.<work id>` when set, else the work's title before the colon.
"""
from html import escape

from engine_map import FONTS, LANGS, PALETTE as MAP_PALETTE, localize, text_width

THEMES = ('light', 'dark')
OUT_DIR = 'assets/eval-ladder'
EVALUATOR = '†'

# One ordinal blue ramp per theme (validated as ordinal: monotone, one hue, clears the surface).
RAMP = {
    'light': ('#86B6EF', '#5598E7', '#2A78D6', '#1C5CAB', '#104281'),
    'dark': ('#184F95', '#256ABF', '#3987E5', '#6DA7EC', '#9EC5F4'),
}

# Geometry (SVG user units).
PAD, GAP = 24, 14
COLS = (112, 170, 330, 240, 110)          # stage, level, example, blind spot, works
FS, FS_HEAD, FS_NAME, FS_CODE, LH = 14, 12.5, 14, 12.5, 20
ROW_PAD, GROUP_GAP, HEAD_H = 12, 8, 32
DOT_R, DOT_PITCH = 4.5, 12

NO_BREAK_BEFORE = set('，。、？！：；）」』”’,.?!:;)%·')
NO_BREAK_AFTER = set('（「『“‘(')


def palette(theme):
    p = MAP_PALETTE[theme]
    return {k: p[k] for k in ('bg', 'frame', 'ink', 'sub', 'line')} | {'tint': p['inherit_fill']}


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


def levels(site):
    for si, stage in enumerate(site['eval_ladder']['stages']):
        for level in stage['levels']:
            yield si, stage, level


def label(site, wid, byid):
    labels = site['eval_ladder'].get('labels') or {}
    if wid in labels:
        return labels[wid]
    return byid[wid]['title'].split(':')[0].strip()


def validate(site, works):
    ladder = site.get('eval_ladder')
    if not ladder:
        return []
    errors = []
    ids = {w['id'] for w in works}
    text = ladder.get('text') or {}
    localized = [(f'text.{k}', text.get(k)) for k in ('title', 'alt', 'example', 'note', 'work', 'evaluator')]
    localized += [(f'text.head[{i}]', h) for i, h in enumerate(text.get('head') or [])]
    localized += [(f'text.table[{i}]', h) for i, h in enumerate(text.get('table') or [])]
    codes = []
    for i, stage in enumerate(ladder.get('stages') or []):
        localized.append((f'stages[{i}].name', stage.get('name')))
        if not stage.get('levels'):
            errors.append(f'eval_ladder: stage {i} has no levels')
        for level in stage.get('levels') or []:
            code = level.get('code')
            codes.append(code)
            for field in ('name', 'question', 'example', 'blind'):
                localized.append((f'{code}.{field}', level.get(field)))
            if not level.get('works'):
                errors.append(f'eval_ladder: {code} lists no works')
            for spec in level.get('works') or []:
                wid, _ = parse_work(spec)
                if wid not in ids:
                    errors.append(f'eval_ladder: {code} work {wid} not found')
    if len(text.get('head') or []) != len(COLS):
        errors.append(f'eval_ladder: text.head needs {len(COLS)} column labels')
    if len(text.get('table') or []) != 3:
        errors.append('eval_ladder: text.table needs 3 column labels')
    for code in {c for c in codes if codes.count(c) > 1}:
        errors.append(f'eval_ladder: duplicate level {code}')
    for where, value in localized:
        for lang in LANGS:
            if not (value or {}).get(lang):
                errors.append(f'eval_ladder: {where} missing {lang}')
    guide = (site.get('sections', {}).get('3.3') or {}).get('guide') or {}
    for lang in LANGS:
        for slot in ('{eval_ladder}', '{eval_table}'):
            if slot not in (guide.get(lang) or ''):
                errors.append(f'eval_ladder: 3.3 guide ({lang}) lacks {slot}')
    return errors


def short_name(level, lang):
    """The figure groups L3 under its stage, so drop the shared 'Dynamics:' prefix there."""
    return localize(level.get('short') or level['name'], lang)


def render(site, lang, theme):
    ladder = site['eval_ladder']
    text = ladder['text']
    pal, ramp, font = palette(theme), RAMP[theme], FONTS[lang]
    width = PAD * 2 + sum(COLS) + GAP * (len(COLS) - 1)
    xs, x = [], PAD
    for w in COLS:
        xs.append(x)
        x += w + GAP
    x_stage, x_level, x_example, x_blind, x_works = xs

    out = []
    o = out.append

    def lines_at(x, y, lines, size=FS, fill=pal['ink'], weight=''):
        for j, line in enumerate(lines):
            o(f'<text x="{x:g}" y="{y + j * LH:g}" font-size="{size}"{weight} fill="{fill}">{escape(line)}</text>')

    # Running example, set as a lead line above the table.
    example = wrap(localize(text['example'], lang), width - 2 * PAD - 24, FS)
    y = PAD
    box_h = 20 + LH * len(example)
    body = []
    body.append(f'<rect x="{PAD}" y="{y}" width="{width - 2 * PAD}" height="{box_h}" rx="6" fill="{pal["tint"]}"/>')
    body_lines_y = y + 10 + 15
    y += box_h + 14

    # Column heads.
    y_head = y
    y += HEAD_H

    # Rows: measure first, so the stage rail can span its rows.
    rows, stage_spans = [], []
    for si, stage in enumerate(ladder['stages']):
        top = y
        for li, level in enumerate(stage['levels']):
            name = wrap(short_name(level, lang), COLS[1], FS_NAME)
            ex = wrap(localize(level['example'], lang), COLS[2], FS)
            blind = wrap(localize(level['blind'], lang), COLS[3], FS)
            n = max(len(name) + 1, len(ex), len(blind))
            h = ROW_PAD * 2 + LH * n
            rows.append((si, li, level, y, h, name, ex, blind))
            y += h
        stage_spans.append((top, y))
        y += GROUP_GAP
    y_end = y - GROUP_GAP

    # Note and legend.
    legend = [('work', localize(text['work'], lang)), ('evaluator', localize(text['evaluator'], lang))]
    legend_w = sum(16 + text_width(t, FS_HEAD) + 16 for _, t in legend)
    note = wrap(localize(text['note'], lang), width - 2 * PAD - legend_w - 24, FS_HEAD)
    y_note = y_end + 26
    height = y_note + LH * (len(note) - 1) + PAD

    title = localize(text['title'], lang)
    o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height:g}" width="{width}" height="{height:g}" '
      f'role="img" aria-label="{escape(title)}" font-family="{escape(font)}">')
    o(f'<title>{escape(title)}</title>')
    o('<defs>')
    for i, c in enumerate(ramp):
        o(f'<marker id="arrow-{i}" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
          f'<path d="M1 1 L9 5 L1 9 Z" fill="{c}"/></marker>')
    o('</defs>')
    # Opaque card, as with the engine map, so either variant stays legible on any page theme.
    o(f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1:g}" rx="10" fill="{pal["bg"]}" stroke="{pal["frame"]}"/>')
    out.extend(body)
    lines_at(PAD + 12, body_lines_y, example)

    for x, head in zip(xs, text['head']):
        o(f'<text x="{x}" y="{y_head + 18}" font-size="{FS_HEAD}" font-weight="600" fill="{pal["sub"]}">{escape(localize(head, lang))}</text>')
    o(f'<line x1="{PAD}" y1="{y_head + HEAD_H - 4}" x2="{width - PAD}" y2="{y_head + HEAD_H - 4}" stroke="{pal["frame"]}"/>')

    # Stage rail: a dot per stage, joined by arrows pointing to the next stage.
    cx = x_stage + 7
    dot_y = [top + ROW_PAD + 10 for top, _ in stage_spans]
    for si in range(len(dot_y) - 1):
        o(f'<line x1="{cx}" y1="{dot_y[si] + 11:g}" x2="{cx}" y2="{dot_y[si + 1] - 14:g}" stroke="{ramp[si]}" '
          f'stroke-width="2" marker-end="url(#arrow-{si})"/>')
    for si, stage in enumerate(ladder['stages']):
        o(f'<circle cx="{cx}" cy="{dot_y[si]:g}" r="7" fill="{ramp[si]}"/>')
        name = wrap(localize(stage['name'], lang), COLS[0] - 22, FS_NAME)
        lines_at(x_stage + 22, dot_y[si] + 5, name, FS_NAME, weight=' font-weight="700"')

    # Rows.
    for si, li, level, top, h, name, ex, blind in rows:
        if li:
            o(f'<line x1="{x_level}" y1="{top:g}" x2="{width - PAD}" y2="{top:g}" stroke="{pal["line"]}" stroke-dasharray="3 3"/>')
        elif si:
            o(f'<line x1="{PAD}" y1="{top - GROUP_GAP / 2:g}" x2="{width - PAD}" y2="{top - GROUP_GAP / 2:g}" stroke="{pal["line"]}"/>')
        base = top + ROW_PAD + 15
        code = level['code']
        cw = text_width(code, FS_CODE) + 14
        o(f'<rect x="{x_level + .75}" y="{base - 14.25:g}" width="{cw:g}" height="19.5" rx="4" fill="{pal["bg"]}" '
          f'stroke="{ramp[si]}" stroke-width="1.5"/>')
        o(f'<text x="{x_level + 7.75:g}" y="{base:g}" font-size="{FS_CODE}" font-weight="700" fill="{pal["ink"]}">{escape(code)}</text>')
        lines_at(x_level, base + LH, name, FS_NAME, weight=' font-weight="600"')
        lines_at(x_example, base, ex)
        lines_at(x_blind, base, blind, fill=pal['sub'])
        works = [parse_work(spec) for spec in level['works']]
        for k, (_, is_eval) in enumerate(works):
            dx = x_works + DOT_R + k * DOT_PITCH
            if is_eval:
                o(f'<circle cx="{dx:g}" cy="{base - 5:g}" r="{DOT_R - .75:g}" fill="none" stroke="{pal["sub"]}" stroke-width="1.5"/>')
            else:
                o(f'<circle cx="{dx:g}" cy="{base - 5:g}" r="{DOT_R}" fill="{pal["sub"]}"/>')
        o(f'<text x="{x_works + len(works) * DOT_PITCH + 4:g}" y="{base:g}" font-size="{FS_HEAD}" fill="{pal["sub"]}">{len(works)}</text>')

    # Bottom: reading note on the left, dot legend on the right.
    lines_at(PAD, y_note, note, FS_HEAD, fill=pal['sub'])
    lx = width - PAD - legend_w
    for kind, t in legend:
        if kind == 'evaluator':
            o(f'<circle cx="{lx + DOT_R:g}" cy="{y_note - 4.5:g}" r="{DOT_R - .75:g}" fill="none" stroke="{pal["sub"]}" stroke-width="1.5"/>')
        else:
            o(f'<circle cx="{lx + DOT_R:g}" cy="{y_note - 4.5:g}" r="{DOT_R}" fill="{pal["sub"]}"/>')
        o(f'<text x="{lx + 16:g}" y="{y_note:g}" font-size="{FS_HEAD}" fill="{pal["sub"]}">{escape(t)}</text>')
        lx += 16 + text_width(t, FS_HEAD) + 16
    o('</svg>')
    return '\n'.join(out) + '\n'


def picture(site, lang):
    """README markup: the light figure, swapped for the dark one under a dark theme."""
    alt = escape(localize(site['eval_ladder']['text']['alt'], lang), quote=True)
    base = f'{OUT_DIR}/eval-ladder-{lang}'
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{base}-dark.svg">\n'
            f'  <img src="{base}-light.svg" alt="{alt}" width="100%">\n</picture>')


def table(site, works, lang, anchor):
    """Markdown index of the works per level; the figure above carries the explanation."""
    byid = {w['id']: w for w in works}
    head = [localize(h, lang) for h in site['eval_ladder']['text']['table']]
    rows = [f'| {" | ".join(head)} |', '|---|---|---|']
    for _, _, level in levels(site):
        links = []
        for wid, is_eval in map(parse_work, level['works']):
            link = f'[{label(site, wid, byid)}](#{anchor(wid)})'
            links.append(f'{link} {EVALUATOR}' if is_eval else link)
        rows.append(f"| {level['code']} {localize(level['name'], lang)} | {localize(level['question'], lang)} | {' · '.join(links)} |")
    return '\n'.join(rows)


def fill(site, works, lang, anchor, body):
    if not site.get('eval_ladder'):
        return body
    return (body.replace('{eval_ladder}', picture(site, lang))
                .replace('{eval_table}', table(site, works, lang, anchor)))


def outputs(site):
    """Yield (relative path, SVG text) for every language and theme."""
    if not site.get('eval_ladder'):
        return
    for lang in LANGS:
        for theme in THEMES:
            yield f'{OUT_DIR}/eval-ladder-{lang}-{theme}.svg', render(site, lang, theme)
