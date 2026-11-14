"""Render the Stage 3 simulation-tool figures from data/site.yaml: the coverage map
(`engine_map`) and the strengths heatmap (`engine_strengths`).

Each language gets a light and a dark SVG under assets/engine-map/. build_readme.py writes
them and `--check` fails when one is out of date, exactly like the READMEs.

A row lists eight cells, one per simulator step. Each cell is written as
`<level>[*<span>] [<label>]`, where level is core, basic, none or inherit, span merges
columns, and label is a key of `engine_map.labels` (localized) or literal text such as XML.
"""
from html import escape

LANGS = ('en', 'zh', 'ja')
THEMES = ('light', 'dark')
LEVELS = ('core', 'basic', 'none', 'inherit')
OUT_DIR = 'assets/engine-map'

FONTS = {
    'en': "-apple-system, 'Segoe UI', Helvetica, Arial, 'Noto Sans', sans-serif",
    'zh': "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans CJK SC', 'Noto Sans SC', sans-serif",
    'ja': "'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Yu Gothic', Meiryo, 'Noto Sans CJK JP', 'Noto Sans JP', sans-serif",
}

PALETTE = {
    'light': {
        'bg': '#FFFFFF', 'frame': '#D1D9E0',
        'ink': '#1F2328', 'sub': '#59636E', 'line': '#D1D9E0', 'pill': '#FFFFFF', 'on_core': '#FFFFFF',
        'inherit_fill': '#F0F3F6', 'inherit_stroke': '#8C959F',
        'a': ('#A35C0A', '#FBEAD2'), 'b': ('#0B7266', '#D2EEEA'),
        'c': ('#2B57A4', '#DCE5F6'), 'd': ('#A5324D', '#F6DCE2'),
    },
    'dark': {
        'bg': '#0D1117', 'frame': '#3D444D',
        'ink': '#E6EDF3', 'sub': '#9198A1', 'line': '#3D444D', 'pill': '#0D1117', 'on_core': '#0D1117',
        'inherit_fill': '#161B22', 'inherit_stroke': '#6E7681',
        'a': ('#E3A251', '#3A2914'), 'b': ('#45C3B3', '#10302B'),
        'c': ('#8AACEF', '#18243B'), 'd': ('#EA8099', '#3A1A24'),
    },
}

# Geometry (SVG user units).
PAD, NAME_W, CELL_W, GAP = 22, 214, 98, 6
ROW_H, ROW_GAP, SEP_H = 50, 6, 18
LEGEND_H, GROUP_H, HEAD_H = 34, 28, 62
FS_CELL, FS_HEAD, FS_NAME, FS_KIND = 13, 13.5, 15, 12


def text_width(s, size):
    """Rough advance width; generous so layouts survive font substitution."""
    w = 0.0
    for ch in s:
        if ord(ch) >= 0x2E80:
            w += 1.0
        elif ch == ' ':
            w += 0.3
        elif ch.isupper() or ch.isdigit():
            w += 0.64
        else:
            w += 0.56
    return w * size


def parse_cell(spec):
    head, _, label = str(spec).partition(' ')
    level, _, span = head.partition('*')
    return level, int(span or 1), label.strip() or None


def expand(row):
    cells, col = [], 0
    for spec in row.get('cells') or []:
        level, span, label = parse_cell(spec)
        cells.append((col, level, span, label))
        col += span
    return cells, col


def localize(value, lang):
    if isinstance(value, dict):
        return value.get(lang) or value.get('en') or ''
    return '' if value is None else str(value)


def validate(site):
    em = site.get('engine_map')
    if not em:
        return []
    errors = []
    labels = em.get('labels') or {}
    text = em.get('text') or {}
    rows = [r for r in em.get('rows') or [] if not r.get('sep')]
    localized = [('text.title', text.get('title')), ('text.alt', text.get('alt'))]
    localized += [(f'text.legend.{lv}', (text.get('legend') or {}).get(lv)) for lv in LEVELS]
    localized += [(f'groups[{i}]', g) for i, g in enumerate(em.get('groups') or [])]
    localized += [(f'columns[{i}]', c) for i, c in enumerate(em.get('columns') or [])]
    localized += [(f'labels.{k}', v) for k, v in labels.items()]
    localized += [(f"rows.{r.get('name')}.kind", r.get('kind')) for r in rows]
    for where, value in localized:
        for lang in LANGS:
            if not (value or {}).get(lang):
                errors.append(f'engine_map: {where} missing {lang}')
    if len(em.get('columns') or []) != 8:
        errors.append('engine_map: expected 8 columns')
    if sum(g.get('span', 1) for g in em.get('groups') or []) != 8:
        errors.append('engine_map: groups must span 8 columns')
    for row in rows:
        cells, total = expand(row)
        if total != 8:
            errors.append(f"engine_map: row {row.get('name')} covers {total} columns, expected 8")
        for _, level, _, label in cells:
            if level not in LEVELS:
                errors.append(f"engine_map: row {row.get('name')} has unknown level {level!r}")
            if level == 'inherit' and label not in labels:
                errors.append(f"engine_map: row {row.get('name')} needs a localized label for its inherited span")
    return errors


def render(site, lang, theme):
    em = site['engine_map']
    pal = PALETTE[theme]
    font = FONTS[lang]
    labels = em.get('labels') or {}
    groups, columns, rows = em['groups'], em['columns'], em['rows']
    blocks = [g['block'] for g in groups for _ in range(g.get('span', 1))]

    grid_x = PAD + NAME_W
    width = grid_x + 8 * CELL_W + 7 * GAP + PAD
    col_x = [grid_x + i * (CELL_W + GAP) for i in range(8)]

    def label_text(key):
        if key is None:
            return ''
        return localize(labels[key], lang) if key in labels else key

    out = []
    o = out.append

    # Legend.
    legend = em['text']['legend']
    x = PAD
    legend_items = []
    for level in LEVELS:
        text = localize(legend[level], lang)
        legend_items.append((x, level, text))
        x += 26 + 8 + text_width(text, FS_CELL) + 22

    # Group bands and column heads.
    y_group = PAD + LEGEND_H
    y_head = y_group + GROUP_H + 6
    y_rows = y_head + HEAD_H

    # Rows.
    row_y, y = [], y_rows
    for row in rows:
        if row.get('sep'):
            row_y.append(('sep', y + SEP_H / 2 - ROW_GAP / 2))
            y += SEP_H
            continue
        row_y.append(('row', y))
        y += ROW_H + ROW_GAP
    height = y - ROW_GAP + PAD

    title = localize(em['text']['title'], lang)
    o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height:g}" width="{width}" height="{height:g}" '
      f'role="img" aria-label="{escape(title)}" font-family="{escape(font)}">')
    o(f'<title>{escape(title)}</title>')
    o('<defs>')
    for b in 'abcd':
        k, soft = pal[b]
        o(f'<pattern id="hatch-{b}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
          f'<rect width="7" height="7" fill="{soft}"/><rect width="2.2" height="7" fill="{k}"/></pattern>')
    o(f'<pattern id="hatch-legend" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
      f'<rect width="2.2" height="7" fill="{pal["sub"]}"/></pattern>')
    o('</defs>')
    # Opaque card: the image stays legible even when a viewer shows the light map on a dark page
    # (GitHub picks the <picture> source from the system theme, not from its own theme setting).
    o(f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1:g}" rx="10" fill="{pal["bg"]}" stroke="{pal["frame"]}"/>')

    # Legend swatches.
    for x, level, text in legend_items:
        sy = PAD + 4
        if level == 'core':
            o(f'<rect x="{x}" y="{sy}" width="26" height="16" rx="3" fill="{pal["sub"]}"/>')
        elif level == 'basic':
            o(f'<rect x="{x}" y="{sy}" width="26" height="16" rx="3" fill="url(#hatch-legend)" stroke="{pal["sub"]}"/>')
        elif level == 'none':
            o(f'<rect x="{x + .5}" y="{sy + .5}" width="25" height="15" rx="3" fill="none" stroke="{pal["inherit_stroke"]}" stroke-dasharray="3 3"/>')
        else:
            o(f'<rect x="{x + .5}" y="{sy + .5}" width="25" height="15" rx="3" fill="{pal["inherit_fill"]}" stroke="{pal["inherit_stroke"]}" stroke-dasharray="3 3"/>')
        o(f'<text x="{x + 34}" y="{sy + 13}" font-size="{FS_CELL}" fill="{pal["sub"]}">{escape(text)}</text>')

    # Group bands.
    col = 0
    for g in groups:
        span = g.get('span', 1)
        k, soft = pal[g['block']]
        gx = col_x[col]
        gw = span * CELL_W + (span - 1) * GAP
        o(f'<rect x="{gx}" y="{y_group}" width="{gw}" height="{GROUP_H}" rx="4" fill="{soft}"/>')
        o(f'<text x="{gx + gw / 2:g}" y="{y_group + 19}" text-anchor="middle" font-size="{FS_HEAD}" font-weight="700" fill="{k}">{escape(localize(g, lang))}</text>')
        col += span

    # Column heads: circled number, then one or two lines of name.
    for i, c in enumerate(columns):
        cx = col_x[i] + CELL_W / 2
        o(f'<text x="{cx:g}" y="{y_head + 14}" text-anchor="middle" font-size="{FS_HEAD}" fill="{pal["ink"]}">{chr(0x2460 + i)}</text>')
        for j, line in enumerate(localize(c, lang).split('\n')):
            o(f'<text x="{cx:g}" y="{y_head + 33 + j * 17}" text-anchor="middle" font-size="{FS_HEAD}" font-weight="600" fill="{pal["ink"]}">{escape(line)}</text>')

    # Rows.
    for (kind, ry), row in zip(row_y, rows):
        if kind == 'sep':
            o(f'<line x1="{PAD}" y1="{ry:g}" x2="{width - PAD}" y2="{ry:g}" stroke="{pal["line"]}"/>')
            continue
        o(f'<text x="{PAD}" y="{ry + 21}" font-size="{FS_NAME}" font-weight="700" fill="{pal["ink"]}">{escape(row["name"])}</text>')
        o(f'<text x="{PAD}" y="{ry + 40}" font-size="{FS_KIND}" fill="{pal["sub"]}">{escape(localize(row["kind"], lang))}</text>')
        cells, _ = expand(row)
        for start, level, span, key in cells:
            x = col_x[start]
            w = span * CELL_W + (span - 1) * GAP
            k, soft = pal[blocks[start]]
            text = label_text(key)
            lines = text.split('\n') if text else []
            if level == 'core':
                o(f'<rect x="{x}" y="{ry}" width="{w}" height="{ROW_H}" rx="4" fill="{k}"/>')
                color, weight = pal['on_core'], ' font-weight="700"'
            elif level == 'basic':
                o(f'<rect x="{x + .75}" y="{ry + .75}" width="{w - 1.5}" height="{ROW_H - 1.5}" rx="4" fill="url(#hatch-{blocks[start]})" stroke="{k}" stroke-width="1.5"/>')
                color, weight = pal['ink'], ''
                if lines:
                    pw = max(text_width(line, FS_CELL) for line in lines) + 10
                    ph = 17 * len(lines) + 3
                    o(f'<rect x="{x + w / 2 - pw / 2:g}" y="{ry + ROW_H / 2 - ph / 2:g}" width="{pw:g}" height="{ph}" rx="3" fill="{pal["pill"]}"/>')
            elif level == 'none':
                o(f'<rect x="{x + .5}" y="{ry + .5}" width="{w - 1}" height="{ROW_H - 1}" rx="4" fill="none" stroke="{pal["inherit_stroke"]}" stroke-dasharray="4 4"/>')
                color, weight = pal['sub'], ''
            else:
                o(f'<rect x="{x + .5}" y="{ry + .5}" width="{w - 1}" height="{ROW_H - 1}" rx="4" fill="{pal["inherit_fill"]}" stroke="{pal["inherit_stroke"]}" stroke-dasharray="4 4"/>')
                color, weight = pal['sub'], ''
            first = ry + ROW_H / 2 + 4.5 - (len(lines) - 1) * 8.5
            for j, line in enumerate(lines):
                o(f'<text x="{x + w / 2:g}" y="{first + j * 17:g}" text-anchor="middle" font-size="{FS_CELL}"{weight} fill="{color}">{escape(line)}</text>')
    o('</svg>')
    return '\n'.join(out) + '\n'


# ------------------------------------------------------------------ strengths heatmap
# `engine_strengths`: one row per tool with eight scores (1–3) written as a string such as
# "3 1 2 1 2 1 1 3*"; a trailing * marks the column's top pick (exactly one per column).

HEAT = {
    'light': {3: ('#0B7266', '#FFFFFF'), 2: ('#8FCFC6', '#10302B'), 1: ('#E6F3F1', '#59636E'), 'star': '#A35C0A'},
    'dark': {3: ('#45C3B3', '#0D1117'), 2: ('#22645C', '#E6EDF3'), 1: ('#14262A', '#9198A1'), 'star': '#E3A251'},
}
S_ROW_H, S_HEAD_H, GROUP_GAP = 46, 50, 16


def parse_scores(text):
    out = []
    for token in str(text).split():
        star = token.endswith('*')
        out.append((int(token.rstrip('*')), star))
    return out


def validate_strengths(site):
    es = site.get('engine_strengths')
    if not es:
        return []
    errors = []
    text = es.get('text') or {}
    localized = [('text.title', text.get('title')), ('text.alt', text.get('alt'))]
    localized += [(f'text.legend.{k}', (text.get('legend') or {}).get(k)) for k in ('3', '2', '1', 'star')]
    localized += [(f'columns[{i}].name', c.get('name')) for i, c in enumerate(es.get('columns') or [])]
    localized += [(f'columns[{i}].hint', c.get('hint')) for i, c in enumerate(es.get('columns') or [])]
    localized += [(f"rows.{r.get('name')}.note", r.get('note')) for r in es.get('rows') or []]
    for where, value in localized:
        for lang in LANGS:
            if not (value or {}).get(lang):
                errors.append(f'engine_strengths: {where} missing {lang}')
    if len(es.get('columns') or []) != 8:
        errors.append('engine_strengths: expected 8 columns')
    groups = es.get('groups') or []
    if groups and sum(g.get('span', 1) for g in groups) != 8:
        errors.append('engine_strengths: groups must span 8 columns')
    for i, g in enumerate(groups):
        for lang in LANGS:
            if not g.get(lang):
                errors.append(f'engine_strengths: groups[{i}] missing {lang}')
    stars = [0] * 8
    for row in es.get('rows') or []:
        try:
            scores = parse_scores(row.get('scores', ''))
        except ValueError:
            errors.append(f"engine_strengths: row {row.get('name')} has a non-numeric score")
            continue
        if len(scores) != 8 or any(v not in (1, 2, 3) for v, _ in scores):
            errors.append(f"engine_strengths: row {row.get('name')} needs eight scores from 1 to 3")
            continue
        for i, (v, star) in enumerate(scores):
            if star:
                stars[i] += 1
                if v != 3:
                    errors.append(f"engine_strengths: row {row.get('name')} stars a score below 3")
    if any(n != 1 for n in stars):
        errors.append('engine_strengths: each column needs exactly one top pick (*)')
    return errors


def star_points(cx, cy, r):
    import math
    pts = []
    for k in range(10):
        rad = r if k % 2 == 0 else r * 0.45
        a = -math.pi / 2 + k * math.pi / 5
        pts.append(f'{cx + rad * math.cos(a):.1f},{cy + rad * math.sin(a):.1f}')
    return ' '.join(pts)


def dots(o, cx, cy, value, color, r=4.6, step=14):
    for k in range(3):
        x = cx + (k - 1) * step
        if k < value:
            o(f'<circle cx="{x:g}" cy="{cy:g}" r="{r}" fill="{color}"/>')
        else:
            o(f'<circle cx="{x:g}" cy="{cy:g}" r="{r - .7:g}" fill="none" stroke="{color}" stroke-width="1.4"/>')


def render_strengths(site, lang, theme):
    es = site['engine_strengths']
    pal, heat = PALETTE[theme], HEAT[theme]
    columns, rows, groups = es['columns'], es['rows'], es.get('groups') or []
    grid_x = PAD + NAME_W
    # Columns follow the coverage map's blocks; a wider gap separates one block from the next.
    starts = {sum(g.get('span', 1) for g in groups[:k]) for k in range(1, len(groups))}
    col_x, x = [], grid_x
    for i in range(8):
        if i in starts:
            x += GROUP_GAP - GAP
        col_x.append(x)
        x += CELL_W + GAP
    width = col_x[-1] + CELL_W + PAD
    y_group = PAD + LEGEND_H
    y_head = y_group + (GROUP_H + 8 if groups else 0)
    y_rows = y_head + S_HEAD_H + 8
    height = y_rows + len(rows) * (S_ROW_H + ROW_GAP) - ROW_GAP + PAD
    title = localize(es['text']['title'], lang)
    out = []
    o = out.append
    o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
      f'role="img" aria-label="{escape(title)}" font-family="{escape(FONTS[lang])}">')
    o(f'<title>{escape(title)}</title>')
    o(f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" fill="{pal["bg"]}" stroke="{pal["frame"]}"/>')

    # Legend: three score samples, then the top-pick star.
    legend = es['text']['legend']
    x, ly = PAD, PAD + 12
    for v in (3, 2, 1):
        fill, ink = heat[v]
        o(f'<rect x="{x}" y="{ly - 11}" width="52" height="22" rx="4" fill="{fill}"/>')
        dots(o, x + 26, ly, v, ink, r=3.6, step=11)
        text = localize(legend[str(v)], lang)
        o(f'<text x="{x + 60}" y="{ly + 4.5}" font-size="{FS_CELL}" fill="{pal["sub"]}">{escape(text)}</text>')
        x += 60 + text_width(text, FS_CELL) + 22
    o(f'<polygon points="{star_points(x + 9, ly, 8)}" fill="{heat["star"]}"/>')
    o(f'<text x="{x + 24}" y="{ly + 4.5}" font-size="{FS_CELL}" fill="{pal["sub"]}">{escape(localize(legend["star"], lang))}</text>')

    # Group bands, coloured like the coverage map's blocks.
    col = 0
    for g in groups:
        span = g.get('span', 1)
        k, soft = pal[g['block']]
        gx, gw = col_x[col], col_x[col + span - 1] + CELL_W - col_x[col]
        o(f'<rect x="{gx}" y="{y_group}" width="{gw}" height="{GROUP_H}" rx="4" fill="{soft}"/>')
        o(f'<text x="{gx + gw / 2:g}" y="{y_group + 19}" text-anchor="middle" font-size="{FS_HEAD}" font-weight="700" fill="{k}">{escape(localize(g, lang))}</text>')
        col += span

    # Column heads: dimension, then a short hint.
    for i, c in enumerate(columns):
        cx = col_x[i] + CELL_W / 2
        o(f'<text x="{cx:g}" y="{y_head + 18}" text-anchor="middle" font-size="{FS_HEAD}" font-weight="700" fill="{pal["ink"]}">{escape(localize(c["name"], lang))}</text>')
        o(f'<text x="{cx:g}" y="{y_head + 37}" text-anchor="middle" font-size="{FS_KIND}" fill="{pal["sub"]}">{escape(localize(c["hint"], lang))}</text>')

    for r, row in enumerate(rows):
        ry = y_rows + r * (S_ROW_H + ROW_GAP)
        o(f'<text x="{PAD}" y="{ry + 19}" font-size="{FS_NAME}" font-weight="700" fill="{pal["ink"]}">{escape(row["name"])}</text>')
        o(f'<text x="{PAD}" y="{ry + 37}" font-size="{FS_KIND}" fill="{pal["sub"]}">{escape(localize(row["note"], lang))}</text>')
        for i, (v, star) in enumerate(parse_scores(row['scores'])):
            x = col_x[i]
            fill, ink = heat[v]
            o(f'<rect x="{x}" y="{ry}" width="{CELL_W}" height="{S_ROW_H}" rx="4" fill="{fill}"/>')
            dots(o, x + CELL_W / 2, ry + S_ROW_H / 2, v, ink)
            if star:
                sc = heat['star']
                o(f'<rect x="{x + 1.25}" y="{ry + 1.25}" width="{CELL_W - 2.5}" height="{S_ROW_H - 2.5}" rx="3.5" fill="none" stroke="{sc}" stroke-width="2.5"/>')
                o(f'<circle cx="{x + CELL_W - 12}" cy="{ry + 12}" r="9" fill="{pal["bg"]}"/>')
                o(f'<polygon points="{star_points(x + CELL_W - 12, ry + 12.5, 7.5)}" fill="{sc}"/>')
    o('</svg>')
    return '\n'.join(out) + '\n'


# ------------------------------------------------------------------ README hooks
FIGURES = (('engine_map', 'engine-map', render), ('engine_strengths', 'engine-strengths', render_strengths))


def picture(site, lang, key='engine_map'):
    """README markup: the light figure, swapped for the dark one under a dark system theme."""
    name = dict((k, n) for k, n, _ in FIGURES)[key]
    alt = escape(localize(site[key]['text']['alt'], lang), quote=True)
    base = f'{OUT_DIR}/{name}-{lang}'
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{base}-dark.svg">\n'
            f'  <img src="{base}-light.svg" alt="{alt}" width="100%">\n</picture>')


def fill_placeholders(site, lang, body):
    """Replace {engine_map} and {engine_strengths} in an extras body with their figures."""
    for key, _, _ in FIGURES:
        token = '{' + key + '}'
        if token in body and site.get(key):
            body = body.replace(token, picture(site, lang, key))
    return body


def validate_all(site):
    return validate(site) + validate_strengths(site)


def outputs(site):
    """Yield (relative path, SVG text) for every figure, language and theme."""
    for key, name, fn in FIGURES:
        if not site.get(key):
            continue
        for lang in LANGS:
            for theme in THEMES:
                yield f'{OUT_DIR}/{name}-{lang}-{theme}.svg', fn(site, lang, theme)
