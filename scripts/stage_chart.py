"""Render the Section 3.2 build-stage charts from data/site.yaml.

`stage_chart` is the representative chart in the README: who does each step, and what.
`stage_chart_full` is the full chart on stage3/simulator-construction*.md: every 3.2 work,
one row each, with the eleven columns given as a string of kinds (nine build steps, then
verification & revision and variant expansion) and the physics-engine tier
(F full simulator, R sim-ready, S scene only, U engine not stated).

For the representative chart:

Each language gets a light and a dark SVG under assets/stage-chart/. build_readme.py writes
them and `--check` fails when one is out of date, exactly like the engine map.

Every row lists nine cells, one per build step. A cell is `n` (not involved or not stated) or
`[kind, who, what]`. Kind is a (the Agent or VLM does it itself), t (a specialised tool, model
or engine), g (given in advance or by hand), x (no physics engine) or r (sim-ready, not run).
Who and what are plain text or {en, zh, ja}; ` · ` in who starts a new line, as does a newline
in a column name.
"""
import re
from html import escape

from engine_map import FONTS, LANGS, PALETTE as MAP_PALETTE, THEMES, localize, text_width

OUT_DIR = 'assets/stage-chart'
KINDS = ('a', 't', 'g', 'n', 'x', 'r')
TAGS = ('bench', 'S', 'R')
STEPS = 9
FULL_COLS = STEPS + 2
FULL_LANGS = ('en', 'zh')   # the languages stage3/simulator-construction*.md exists in
TIERS = ('F', 'R', 'S', 'U')
ENGINE_KINDS = {'F': 'ta', 'R': 'r', 'S': 'x', 'U': 'n'}   # what column 7 must hold for each tier

PALETTE = {theme: {**pal, 'e': e} for (theme, pal), e in
           zip(MAP_PALETTE.items(), [('#6748B2', '#E7E0F6'), ('#AE98F0', '#241C3A')])}


def _hatches(o, pal):
    for b in 'abcde':
        k, soft = pal[b]
        o(f'<pattern id="hatch-{b}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
          f'<rect width="7" height="7" fill="{soft}"/><rect width="2.2" height="7" fill="{k}"/></pattern>')
    o(f'<pattern id="hatch-legend" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
      f'<rect width="2.2" height="7" fill="{pal["sub"]}"/></pattern>')


# Geometry (SVG user units).
PAD, NAME_W, CELL_W, GAP = 22, 150, 114, 6
ROW_GAP, SEC_H, GROUP_H = 6, 38, 28
FS_WHO, FS_WHAT, FS_HEAD, FS_NAME, FS_TAG, FS_SEC, FS_LEGEND = 13, 12, 13.5, 15, 11.5, 14.5, 13
LH_WHO, LH_WHAT, LH_NAME = 16, 15, 19
NO_LINE_START = set('，、。；：）」』》,.;:)!?・')


def width_of(s, size, bold=False):
    return text_width(s, size) * (1.06 if bold else 1.0)


def _tokens(text):
    return re.findall(r'[⺀-￿]|[^\s⺀-￿]+\s*|\s+', text)


def wrap(text, size, max_w, bold=False):
    """Wrap into as few lines as fit, then narrow the lines as far as that count allows, so they come out balanced."""
    full = max_w
    lines = _greedy(text, size, max_w, full, bold)
    while len(lines) > 1 and max_w > 24:
        trial = _greedy(text, size, max_w - 3, full, bold)
        if len(trial) > len(lines):
            break
        lines, max_w = trial, max_w - 3
    return lines


def _greedy(text, size, max_w, full_w, bold=False):
    """Greedy wrap: CJK breaks between characters, Latin between words; a word wider than the
    full width is split at camelCase or hyphens."""
    toks = []
    for tok in _tokens(text):
        if width_of(tok.strip(), size, bold) > full_w and len(tok.strip()) > 1:
            parts = re.split(r'(?<=[a-z0-9])(?=[A-Z])|(?<=-)', tok)
            toks += [p for p in parts if p]
        else:
            toks.append(tok)
    lines, cur = [], ''
    for tok in toks:
        cand = cur + tok
        if cur.strip() and tok.strip() and tok[0] not in NO_LINE_START and width_of(cand.rstrip(), size, bold) > max_w:
            lines.append(cur.rstrip())
            cur = tok.lstrip()
        else:
            cur = cand
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def validate(site, ids=None):
    sc = site.get('stage_chart')
    if not sc:
        return []
    errors = []
    text = sc.get('text') or {}
    localized = [('text.title', text.get('title')), ('text.alt', text.get('alt'))]
    localized += [(f'text.legend.{k}', (text.get('legend') or {}).get(k)) for k in KINDS]
    localized += [(f'text.tags.{k}', (text.get('tags') or {}).get(k)) for k in TAGS]
    localized += [(f'groups[{i}]', g) for i, g in enumerate(sc.get('groups') or [])]
    localized += [(f'columns[{i}]', c) for i, c in enumerate(sc.get('columns') or [])]
    localized += [(f'sections[{i}].title', s.get('title')) for i, s in enumerate(sc.get('sections') or [])]
    for where, value in localized:
        for lang in LANGS:
            if not (value or {}).get(lang):
                errors.append(f'stage_chart: {where} missing {lang}')
    if len(sc.get('columns') or []) != STEPS:
        errors.append(f'stage_chart: expected {STEPS} columns')
    if sum(g.get('span', 1) for g in sc.get('groups') or []) != STEPS:
        errors.append(f'stage_chart: groups must span {STEPS} columns')
    for sec in sc.get('sections') or []:
        for row in sec.get('rows') or []:
            name = row.get('name')
            if ids is not None and row.get('id') not in ids:
                errors.append(f"stage_chart: row {name} links to unknown id {row.get('id')!r}")
            for tag in row.get('tags') or []:
                if tag not in TAGS:
                    errors.append(f'stage_chart: row {name} has unknown tag {tag!r}')
            cells = row.get('cells') or []
            if len(cells) != STEPS:
                errors.append(f'stage_chart: row {name} has {len(cells)} cells, expected {STEPS}')
            for i, cell in enumerate(cells):
                if cell == 'n':
                    continue
                if not isinstance(cell, list) or len(cell) != 3 or cell[0] not in KINDS:
                    errors.append(f'stage_chart: row {name} cell {i + 1} must be n or [kind, who, what]')
                    continue
                for part in cell[1:]:
                    if isinstance(part, dict) and not all(part.get(lang) for lang in LANGS):
                        errors.append(f'stage_chart: row {name} cell {i + 1} missing a language')
    return errors


def _legend(o, pal, legend):
    for lx, ly, k, label in legend:
        sy = ly + 4
        if k == 'a':
            o(f'<rect x="{lx}" y="{sy}" width="26" height="16" rx="3" fill="{pal["sub"]}"/>')
        elif k == 't':
            o(f'<rect x="{lx}" y="{sy}" width="26" height="16" rx="3" fill="url(#hatch-legend)" stroke="{pal["sub"]}"/>')
        elif k == 'g':
            o(f'<rect x="{lx + .75}" y="{sy + .75}" width="24.5" height="14.5" rx="3" fill="none" stroke="{pal["sub"]}" stroke-width="1.5"/>')
        elif k == 'n':
            o(f'<rect x="{lx + .5}" y="{sy + .5}" width="25" height="15" rx="3" fill="none" stroke="{pal["inherit_stroke"]}" stroke-dasharray="3 3"/>')
        elif k == 'x':
            o(f'<rect x="{lx + 1}" y="{sy + 1}" width="24" height="14" rx="3" fill="none" stroke="{pal["d"][0]}" stroke-width="2" stroke-dasharray="4 3"/>')
        else:
            o(f'<rect x="{lx + .75}" y="{sy + .75}" width="24.5" height="14.5" rx="3" fill="none" stroke="{pal["c"][0]}" stroke-width="1.5"/>')
        o(f'<text x="{lx + 34}" y="{sy + 13}" font-size="{FS_LEGEND}" fill="{pal["sub"]}">{escape(label)}</text>')


def legend_layout(labels, width, size):
    """Place legend items left to right, wrapping when a line is full."""
    out, lx, ly = [], PAD, PAD
    for k, label in labels:
        w = 26 + 8 + width_of(label, size) + 20
        if lx + w > width - PAD and lx > PAD:
            lx, ly = PAD, ly + 24
        out.append((lx, ly, k, label))
        lx += w
    return out, ly + 24


def render(site, lang, theme):
    sc = site['stage_chart']
    pal = PALETTE[theme]
    text = sc['text']
    groups, columns = sc['groups'], sc['columns']
    blocks = [g['block'] for g in groups for _ in range(g.get('span', 1))]

    grid_x = PAD + NAME_W
    width = grid_x + STEPS * CELL_W + (STEPS - 1) * GAP + PAD
    col_x = [grid_x + i * (CELL_W + GAP) for i in range(STEPS)]
    inner = CELL_W - 14

    out = []
    o = out.append

    # Legend, wrapped onto as many lines as it needs.
    legend, lx, ly = [], PAD, PAD
    for k in KINDS:
        label = localize(text['legend'][k], lang)
        w = 26 + 8 + width_of(label, FS_LEGEND) + 20
        if lx + w > width - PAD and lx > PAD:
            lx, ly = PAD, ly + 24
        legend.append((lx, ly, k, label))
        lx += w
    y_group = ly + 24 + 12

    # Column heads.
    head_lines = [[ln for part in localize(c, lang).split('\n') for ln in wrap(part, FS_HEAD, CELL_W - 6, bold=True)]
                  for c in columns]
    y_head = y_group + GROUP_H + 8
    y = y_head + 22 + max(len(h) for h in head_lines) * 16 + 4

    # Lay out sections and rows.
    def cell_lines(cell):
        if cell == 'n':
            return [], []
        who = [ln for part in localize(cell[1], lang).split(' · ') for ln in wrap(part, FS_WHO, inner, bold=True)]
        return who, wrap(localize(cell[2], lang), FS_WHAT, inner)

    def block_h(who, what):
        return len(who) * LH_WHO + len(what) * LH_WHAT + (2 if who and what else 0)

    layout = []
    for sec in sc['sections']:
        layout.append(('sec', y, localize(sec['title'], lang)))
        y += SEC_H
        for row in sec['rows']:
            name = wrap(row['name'], FS_NAME, NAME_W - 12, bold=True)
            tags = [localize(text['tags'][t], lang) for t in row.get('tags') or []]
            name_h = len(name) * LH_NAME + (len(tags) * 21 if tags else 0) + 6
            cells = [cell_lines(c) for c in row['cells']]
            h = max([name_h, 54] + [block_h(*c) + 20 for c in cells])
            layout.append(('row', y, (row, name, tags, cells, h)))
            y += h + ROW_GAP
    height = y - ROW_GAP + PAD

    title = localize(text['title'], lang)
    o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height:g}" width="{width}" height="{height:g}" '
      f'role="img" aria-label="{escape(title)}" font-family="{escape(FONTS[lang])}">')
    o(f'<title>{escape(title)}</title>')
    o('<defs>')
    _hatches(o, pal)
    o('</defs>')
    # Opaque card, so the light image stays legible on a dark page and vice versa.
    o(f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1:g}" rx="10" fill="{pal["bg"]}" stroke="{pal["frame"]}"/>')

    _legend(o, pal, legend)

    col = 0
    for g in groups:
        span = g.get('span', 1)
        k, soft = pal[g['block']]
        gx = col_x[col]
        gw = span * CELL_W + (span - 1) * GAP
        o(f'<rect x="{gx}" y="{y_group}" width="{gw}" height="{GROUP_H}" rx="5" fill="{soft}"/>')
        o(f'<text x="{gx + gw / 2:g}" y="{y_group + 19}" text-anchor="middle" font-size="{FS_HEAD + .5}" font-weight="700" fill="{k}">{escape(localize(g, lang))}</text>')
        col += span

    for i, lines in enumerate(head_lines):
        cx = col_x[i] + CELL_W / 2
        o(f'<text x="{cx:g}" y="{y_head + 14}" text-anchor="middle" font-size="{FS_HEAD}" fill="{pal["sub"]}">{chr(0x2460 + i)}</text>')
        for j, line in enumerate(lines):
            o(f'<text x="{cx:g}" y="{y_head + 33 + j * 16}" text-anchor="middle" font-size="{FS_HEAD}" font-weight="600" fill="{pal["ink"]}">{escape(line)}</text>')

    for kind, ry, payload in layout:
        if kind == 'sec':
            ty = ry + SEC_H - 13
            o(f'<text x="{PAD}" y="{ty:g}" font-size="{FS_SEC}" font-weight="700" fill="{pal["ink"]}">{escape(payload)}</text>')
            x1 = PAD + width_of(payload, FS_SEC, bold=True) + 12
            if x1 < width - PAD:
                o(f'<line x1="{x1:g}" y1="{ty - 5:g}" x2="{width - PAD}" y2="{ty - 5:g}" stroke="{pal["line"]}"/>')
            continue
        row, name, tags, cells, h = payload
        top = ry + h / 2 - (len(name) * LH_NAME + len(tags) * 21) / 2
        for j, line in enumerate(name):
            o(f'<text x="{PAD}" y="{top + 14 + j * LH_NAME:g}" font-size="{FS_NAME}" font-weight="700" fill="{pal["ink"]}">{escape(line)}</text>')
        ty = top + len(name) * LH_NAME + 3
        for t, label in zip(row.get('tags') or [], tags):
            tw = width_of(label, FS_TAG) + 14
            if t == 'bench':
                k, soft = pal['e']
                o(f'<rect x="{PAD}" y="{ty:g}" width="{tw:g}" height="17" rx="8.5" fill="{soft}"/>')
                color = k
            elif t == 'S':
                o(f'<rect x="{PAD + .5}" y="{ty + .5:g}" width="{tw - 1:g}" height="16" rx="8" fill="none" stroke="{pal["sub"]}" stroke-dasharray="3 2"/>')
                color = pal['sub']
            else:
                o(f'<rect x="{PAD + .5}" y="{ty + .5:g}" width="{tw - 1:g}" height="16" rx="8" fill="none" stroke="{pal["c"][0]}"/>')
                color = pal['c'][0]
            o(f'<text x="{PAD + 7}" y="{ty + 12.5:g}" font-size="{FS_TAG}" fill="{color}">{escape(label)}</text>')
            ty += 21

        for i, (cell, (who, what)) in enumerate(zip(row['cells'], cells)):
            x = col_x[i]
            k, soft = pal[blocks[i]]
            ck = 'n' if cell == 'n' else cell[0]
            if ck == 'a':
                o(f'<rect x="{x}" y="{ry}" width="{CELL_W}" height="{h}" rx="5" fill="{k}"/>')
                c_who, c_what = pal['on_core'], pal['on_core']
            elif ck == 't':
                o(f'<rect x="{x + .75}" y="{ry + .75}" width="{CELL_W - 1.5}" height="{h - 1.5}" rx="5" fill="url(#hatch-{blocks[i]})" stroke="{k}" stroke-width="1.5"/>')
                c_who, c_what = pal['ink'], pal['sub']
            elif ck == 'g':
                o(f'<rect x="{x + .75}" y="{ry + .75}" width="{CELL_W - 1.5}" height="{h - 1.5}" rx="5" fill="{pal["bg"]}" stroke="{k}" stroke-width="1.5"/>')
                c_who, c_what = k, pal['sub']
            elif ck == 'x':
                d = pal['d'][0]
                o(f'<rect x="{x + 1}" y="{ry + 1}" width="{CELL_W - 2}" height="{h - 2}" rx="5" fill="{pal["bg"]}" stroke="{d}" stroke-width="2" stroke-dasharray="6 4"/>')
                c_who, c_what = d, d
            elif ck == 'r':
                c = pal['c'][0]
                o(f'<rect x="{x + .75}" y="{ry + .75}" width="{CELL_W - 1.5}" height="{h - 1.5}" rx="5" fill="{pal["bg"]}" stroke="{c}" stroke-width="1.5"/>')
                c_who, c_what = c, pal['sub']
            else:
                o(f'<rect x="{x + .5}" y="{ry + .5}" width="{CELL_W - 1}" height="{h - 1}" rx="5" fill="none" stroke="{pal["inherit_stroke"]}" stroke-dasharray="4 4"/>')
                continue
            bh = len(who) * LH_WHO + len(what) * LH_WHAT + (2 if who and what else 0)
            by = ry + h / 2 - bh / 2
            if ck == 't':
                pw = min(CELL_W - 8, max([width_of(s, FS_WHO, True) for s in who] + [width_of(s, FS_WHAT) for s in what]) + 10)
                o(f'<rect x="{x + CELL_W / 2 - pw / 2:g}" y="{by - 4:g}" width="{pw:g}" height="{bh + 8:g}" rx="4" fill="{pal["pill"]}"/>')
            cx = x + CELL_W / 2
            for j, line in enumerate(who):
                o(f'<text x="{cx:g}" y="{by + 11.5 + j * LH_WHO:g}" text-anchor="middle" font-size="{FS_WHO}" font-weight="700" fill="{c_who}">{escape(line)}</text>')
            wy = by + len(who) * LH_WHO + (2 if who else 0)
            for j, line in enumerate(what):
                o(f'<text x="{cx:g}" y="{wy + 10.5 + j * LH_WHAT:g}" text-anchor="middle" font-size="{FS_WHAT}" fill="{c_what}">{escape(line)}</text>')
    o('</svg>')
    return '\n'.join(out) + '\n'


# ------------------------------------------------------------------ full chart (stage3 page)
F_NAME_W, F_CW, F_GAP, F_SPLIT, F_HOW_W = 222, 54, 4, 16, 360
F_ROW_GAP, F_LH_HOW, FS_F_HEAD, FS_F_NAME, FS_F_HOW, FS_F_SUM = 4, 15, 11, 13, 12, 10.5


def validate_full(site, ids=None):
    sf = site.get('stage_chart_full')
    if not sf:
        return []
    errors = []
    text = sf.get('text') or {}
    localized = [(f'text.{k}', text.get(k)) for k in ('title', 'alt', 'extra_band', 'how', 'totals', 'count')]
    localized += [(f'text.sum.{k}', (text.get('sum') or {}).get(k)) for k in ('a', 't', 'engine', 'x', 'r')]
    localized += [(f'text.tiers.{k}', (text.get('tiers') or {}).get(k)) for k in TIERS]
    localized += [(f'text.columns[{i}]', c) for i, c in enumerate(text.get('columns') or [])]
    localized += [(f'sections[{i}].title', s.get('title')) for i, s in enumerate(sf.get('sections') or [])]
    for where, value in localized:
        for lang in FULL_LANGS:
            if not (value or {}).get(lang):
                errors.append(f'stage_chart_full: {where} missing {lang}')
    if len(text.get('columns') or []) != FULL_COLS:
        errors.append(f'stage_chart_full: expected {FULL_COLS} columns')
    seen = set()
    for sec in sf.get('sections') or []:
        for row in sec.get('rows') or []:
            name, steps, tier = row.get('name'), str(row.get('steps') or ''), row.get('tier')
            if ids is not None and row.get('id') not in ids:
                errors.append(f"stage_chart_full: row {name} links to unknown id {row.get('id')!r}")
            if row.get('id') in seen:
                errors.append(f'stage_chart_full: row {name} appears twice')
            seen.add(row.get('id'))
            if len(steps) != FULL_COLS or any(k not in KINDS for k in steps):
                errors.append(f'stage_chart_full: row {name} steps must be {FULL_COLS} of {"".join(KINDS)}')
            elif tier not in TIERS:
                errors.append(f'stage_chart_full: row {name} has unknown tier {tier!r}')
            elif steps[6] not in ENGINE_KINDS[tier]:
                errors.append(f'stage_chart_full: row {name} is tier {tier} but its physics-engine cell is {steps[6]!r}')
            if not all((row.get('how') or {}).get(lang) for lang in FULL_LANGS):
                errors.append(f'stage_chart_full: row {name} how missing a language')
    return errors


def _tag(o, pal, x, y, kind, label, size):
    """A rounded pill for a physics-engine tier or the Bench mark; returns its width."""
    tw = width_of(label, size) + 14
    if kind == 'bench':
        k, soft = pal['e']
        o(f'<rect x="{x:g}" y="{y:g}" width="{tw:g}" height="17" rx="8.5" fill="{soft}"/>')
        color = k
    elif kind == 'F':
        k, soft = pal['b']
        o(f'<rect x="{x:g}" y="{y:g}" width="{tw:g}" height="17" rx="8.5" fill="{soft}"/>')
        color = k
    elif kind == 'S':
        o(f'<rect x="{x + .5:g}" y="{y + .5:g}" width="{tw - 1:g}" height="16" rx="8" fill="none" stroke="{pal["sub"]}" stroke-dasharray="3 2"/>')
        color = pal['sub']
    elif kind == 'R':
        o(f'<rect x="{x + .5:g}" y="{y + .5:g}" width="{tw - 1:g}" height="16" rx="8" fill="none" stroke="{pal["c"][0]}"/>')
        color = pal['c'][0]
    else:
        o(f'<rect x="{x + .5:g}" y="{y + .5:g}" width="{tw - 1:g}" height="16" rx="8" fill="none" stroke="{pal["line"]}"/>')
        color = pal['sub']
    o(f'<text x="{x + 7:g}" y="{y + 12.5:g}" font-size="{size}" fill="{color}">{escape(label)}</text>')
    return tw


def render_full(site, lang, theme):
    sf = site['stage_chart_full']
    sc = site['stage_chart']
    pal = PALETTE[theme]
    text = sf['text']
    groups = sc['groups']
    blocks = [g['block'] for g in groups for _ in range(g.get('span', 1))] + ['e', 'e']

    grid_x = PAD + F_NAME_W
    col_x = [grid_x + i * (F_CW + F_GAP) for i in range(STEPS)]
    ex = col_x[-1] + F_CW + F_SPLIT
    col_x += [ex, ex + F_CW + F_GAP]
    how_x = col_x[-1] + F_CW + F_SPLIT
    width = how_x + F_HOW_W + PAD

    out = []
    o = out.append
    legend, y_group = legend_layout([(k, localize(sc['text']['legend'][k], lang)) for k in KINDS], width, FS_LEGEND)
    y_group += 12
    heads = [wrap(localize(c, lang), FS_F_HEAD, F_CW - 2, bold=True) for c in text['columns']]
    y_head = y_group + GROUP_H + 8
    y_sum = y_head + 20 + max(len(h) for h in heads) * 14 + 6
    counted = [r for s in sf['sections'] if not s.get('reference') for r in s['rows']]
    n = len(counted)

    def counts(i):
        c = {k: 0 for k in KINDS}
        for r in counted:
            c[r['steps'][i]] += 1
        return c

    sum_lines = []
    for i in range(FULL_COLS):
        c = counts(i)
        lab = text['sum']
        if i == 6:
            sum_lines.append((c, [(localize(lab['engine'], lang), c['t'] + c['a']), (localize(lab['x'], lang), c['x']), (localize(lab['r'], lang), c['r'])]))
        else:
            sum_lines.append((c, [(localize(lab['a'], lang), c['a']), (localize(lab['t'], lang), c['t'])]))
    y = y_sum + 12 + max(len(l) for _, l in sum_lines) * 13 + 10

    layout = []
    for sec in sf['sections']:
        layout.append(('sec', y, sec))
        y += 34
        for row in sec['rows']:
            name = wrap(row['name'], FS_F_NAME, F_NAME_W - 10, bold=True)
            tags = (['bench'] if 'bench' in (row.get('tags') or []) else []) + [row['tier']]
            labels = [(t, localize(text['tiers'][t], lang) if t in TIERS else localize(sc['text']['tags'][t], lang)) for t in tags]
            tags_w = sum(width_of(l, FS_TAG) + 14 + 5 for _, l in labels)
            inline = len(name) == 1 and width_of(name[0], FS_F_NAME, True) + 8 + tags_w <= F_NAME_W - 4
            name_h = len(name) * 17 + (0 if inline else 20)
            how = wrap(localize(row['how'], lang), FS_F_HOW, F_HOW_W)
            h = max(26, name_h + 6, len(how) * F_LH_HOW + 8)
            layout.append(('row', y, (row, name, labels, inline, how, h)))
            y += h + F_ROW_GAP
    height = y - F_ROW_GAP + PAD

    title = localize(text['title'], lang)
    o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height:g}" width="{width}" height="{height:g}" '
      f'role="img" aria-label="{escape(title)}" font-family="{escape(FONTS[lang])}">')
    o(f'<title>{escape(title)}</title>')
    o('<defs>')
    _hatches(o, pal)
    o('</defs>')
    o(f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1:g}" rx="10" fill="{pal["bg"]}" stroke="{pal["frame"]}"/>')
    _legend(o, pal, legend)

    def band(x, w, block, label):
        """Group band; a label too wide for one line drops to a smaller size on two."""
        k, soft = pal[block]
        o(f'<rect x="{x}" y="{y_group}" width="{w}" height="{GROUP_H}" rx="5" fill="{soft}"/>')
        lines = wrap(label, 12, w - 8, bold=True)
        size, ys = (12, [y_group + 18]) if len(lines) == 1 else (10.5, [y_group + 12.5, y_group + 24])
        if len(lines) > 1:
            lines = wrap(label, size, w - 6, bold=True)[:2]
        for line, ly in zip(lines, ys):
            o(f'<text x="{x + w / 2:g}" y="{ly}" text-anchor="middle" font-size="{size}" font-weight="700" fill="{k}">{escape(line)}</text>')

    col = 0
    for g in groups:
        span = g.get('span', 1)
        band(col_x[col], span * F_CW + (span - 1) * F_GAP, g['block'], localize(g, lang))
        col += span
    band(col_x[9], 2 * F_CW + F_GAP, 'e', localize(text['extra_band'], lang))

    for i, lines in enumerate(heads):
        cx = col_x[i] + F_CW / 2
        mark = chr(0x2460 + i) if i < STEPS else ''
        if mark:
            o(f'<text x="{cx:g}" y="{y_head + 13}" text-anchor="middle" font-size="{FS_HEAD}" fill="{pal["sub"]}">{mark}</text>')
        for j, line in enumerate(lines):
            o(f'<text x="{cx:g}" y="{y_head + 30 + j * 14}" text-anchor="middle" font-size="{FS_F_HEAD}" font-weight="600" fill="{pal["ink"]}">{escape(line)}</text>')
    o(f'<text x="{how_x}" y="{y_head + 30}" font-size="{FS_F_HEAD}" font-weight="600" fill="{pal["ink"]}">{escape(localize(text["how"], lang))}</text>')

    # Totals row: a bar split by kind, then the counts that matter for the column.
    o(f'<text x="{PAD}" y="{y_sum + 14}" font-size="{FS_F_HEAD + 1}" fill="{pal["sub"]}">{escape(localize(text["totals"], lang).format(n=n))}</text>')
    for i, (c, lines) in enumerate(sum_lines):
        x, b = col_x[i], blocks[i]
        k, soft = pal[b]
        o(f'<rect x="{x}" y="{y_sum}" width="{F_CW}" height="8" rx="3" fill="{pal["inherit_fill"]}"/>')
        bx = x
        for kind in ('a', 't', 'g', 'r', 'x'):
            if not c[kind]:
                continue
            w = F_CW * c[kind] / n
            fill = {'a': k, 't': f'url(#hatch-{b})', 'g': soft, 'r': pal['c'][1], 'x': pal['d'][0]}[kind]
            o(f'<rect x="{bx:g}" y="{y_sum}" width="{w:g}" height="8" fill="{fill}"/>')
            bx += w
        for j, (label, v) in enumerate(lines):
            o(f'<text x="{x + F_CW / 2:g}" y="{y_sum + 21 + j * 13}" text-anchor="middle" font-size="{FS_F_SUM}" fill="{pal["sub"]}">'
              f'{escape(label)} <tspan font-weight="700" fill="{pal["ink"]}">{v}</tspan></text>')
    ly = y_sum + 12 + max(len(l) for _, l in sum_lines) * 13 + 4
    o(f'<line x1="{PAD}" y1="{ly}" x2="{width - PAD}" y2="{ly}" stroke="{pal["line"]}"/>')

    for kind, ry, payload in layout:
        if kind == 'sec':
            sec = payload
            label = localize(sec['title'], lang)
            ty = ry + 23
            o(f'<text x="{PAD}" y="{ty}" font-size="{FS_SEC - .5}" font-weight="700" fill="{pal["ink"]}">{escape(label)}'
              f'<tspan font-weight="400" fill="{pal["sub"]}" dx="10">{escape(localize(text["count"], lang).format(n=len(sec["rows"])))}</tspan></text>')
            x1 = PAD + width_of(label, FS_SEC - .5, True) + 22 + width_of(localize(text['count'], lang), FS_SEC - .5) + 12
            if x1 < width - PAD:
                o(f'<line x1="{x1:g}" y1="{ty - 5}" x2="{width - PAD}" y2="{ty - 5}" stroke="{pal["line"]}"/>')
            continue
        row, name, labels, inline, how, h = payload
        top = ry + h / 2 - (len(name) * 17 + (0 if inline else 20)) / 2
        for j, line in enumerate(name):
            o(f'<text x="{PAD}" y="{top + 13 + j * 17:g}" font-size="{FS_F_NAME}" font-weight="700" fill="{pal["ink"]}">{escape(line)}</text>')
        tx = PAD + width_of(name[0], FS_F_NAME, True) + 8 if inline else PAD
        ty = top - 0.5 if inline else top + len(name) * 17 + 2
        for t, label in labels:
            tx += _tag(o, pal, tx, ty, t, label, FS_TAG) + 5
        for i, kind in enumerate(row['steps']):
            x, b = col_x[i], blocks[i]
            k, soft = pal[b]
            if kind == 'a':
                o(f'<rect x="{x}" y="{ry}" width="{F_CW}" height="{h}" rx="4" fill="{k}"/>')
            elif kind == 't':
                o(f'<rect x="{x + .75}" y="{ry + .75}" width="{F_CW - 1.5}" height="{h - 1.5}" rx="4" fill="url(#hatch-{b})" stroke="{k}" stroke-width="1.5"/>')
            elif kind == 'g':
                o(f'<rect x="{x + .75}" y="{ry + .75}" width="{F_CW - 1.5}" height="{h - 1.5}" rx="4" fill="{pal["bg"]}" stroke="{k}" stroke-width="1.5"/>')
            elif kind == 'x':
                o(f'<rect x="{x + 1}" y="{ry + 1}" width="{F_CW - 2}" height="{h - 2}" rx="4" fill="{pal["bg"]}" stroke="{pal["d"][0]}" stroke-width="2" stroke-dasharray="5 3"/>')
            elif kind == 'r':
                o(f'<rect x="{x + .75}" y="{ry + .75}" width="{F_CW - 1.5}" height="{h - 1.5}" rx="4" fill="{pal["bg"]}" stroke="{pal["c"][0]}" stroke-width="1.5"/>')
            else:
                o(f'<rect x="{x + .5}" y="{ry + .5}" width="{F_CW - 1}" height="{h - 1}" rx="4" fill="none" stroke="{pal["inherit_stroke"]}" stroke-dasharray="3 3"/>')
        hy = ry + h / 2 - len(how) * F_LH_HOW / 2
        for j, line in enumerate(how):
            o(f'<text x="{how_x}" y="{hy + 11.5 + j * F_LH_HOW:g}" font-size="{FS_F_HOW}" fill="{pal["sub"]}">{escape(line)}</text>')
    o('</svg>')
    return '\n'.join(out) + '\n'


def picture(site, lang):
    """README markup: the light chart, swapped for the dark one under a dark system theme."""
    alt = escape(localize(site['stage_chart']['text']['alt'], lang), quote=True)
    base = f'{OUT_DIR}/stage-chart-{lang}'
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{base}-dark.svg">\n'
            f'  <img src="{base}-light.svg" alt="{alt}" width="100%">\n</picture>')


def outputs(site):
    """Yield (relative path, SVG text) for every chart, language and theme."""
    if not site.get('stage_chart'):
        return
    for lang in LANGS:
        for theme in THEMES:
            yield f'{OUT_DIR}/stage-chart-{lang}-{theme}.svg', render(site, lang, theme)
    if not site.get('stage_chart_full'):
        return
    for lang in FULL_LANGS:
        for theme in THEMES:
            yield f'{OUT_DIR}/stage-full-{lang}-{theme}.svg', render_full(site, lang, theme)
