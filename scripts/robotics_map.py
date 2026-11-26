"""Render the robotics branch's taxonomy figure: one Real2Sim2Real loop in a few steps.

`robotics.taxonomy` in data/site.yaml lists the steps in order. Each step names the world it
happens in (`real` or `sim`), a localized `label` and `title`, and the `sections` it groups.
Every section of the robotics branch (the checked-out stage plus the cherry-picked sections)
belongs to exactly one step. Entry counts come from data/works.yaml, so the figure follows the
catalog.

The coding agent spans the top; each step is a card with its sections and counts; a strip
underneath shows which world each step happens in, with the Real2Sim and Sim2Real crossings;
an arrow from the last step back to the first closes the loop.

Each language gets a light and a dark SVG under assets/robotics/. build_readme.py writes them
and `--check` fails when one is out of date.
"""
from collections import Counter
from html import escape

from engine_map import FONTS, LANGS, PALETTE, THEMES, localize, text_width
from stage_chart import wrap

OUT_DIR = 'assets/robotics'
WORLDS = ('real', 'sim')
TEXT_KEYS = ('agent', 'loop', 'back', 'alt', 'picked', 'step_head', 'sections_head')
SEP = {'en': ('. ', ': ', ', ', ' (', ')'), 'zh': ('。', '：', '、', '（', '）'), 'ja': ('。', '：', '、', '（', '）')}

# Geometry (SVG user units).
W, PAD, GX = 1280, 24, 44
AGENT_H, LINK_H = 66, 36
CARD_PAD, PILL_W, PILL_H = 16, 40, 22
FS_AGENT, FS_LOOP, FS_CHIP, FS_TITLE, FS_SEC, FS_NOTE, FS_WORLD = 19, 14, 12.5, 17, 14, 12, 13.5
LH_TITLE, LH_SEC = 22, 18.5
WORLD_H, LOOP_H = 32, 40


def scope(site):
    """The branch's sections in order: the checked-out stage, then the cherry-picked ones."""
    rb = site['robotics']
    stage = next(st for st in site['stages'] if st['id'] == rb['stage'])
    return list(stage['sections']) + list(rb.get('cherry_pick') or [])


def validate(site):
    rb = site.get('robotics')
    if not rb:
        return []
    errors = []
    tx = rb.get('taxonomy') or {}
    steps = tx.get('steps') or []
    if not steps:
        return ['robotics.taxonomy: no steps']
    placed = [sec for step in steps for sec in step.get('sections') or []]
    if sorted(placed) != sorted(scope(site)):
        errors.append(f'robotics.taxonomy: steps must hold each branch section exactly once, got {placed}')
    for i, step in enumerate(steps, 1):
        if step.get('world') not in WORLDS:
            errors.append(f'robotics.taxonomy step {i}: world must be one of {WORLDS}')
        for key in ('label', 'title'):
            if not all((step.get(key) or {}).get(lang) for lang in LANGS):
                errors.append(f'robotics.taxonomy step {i}: {key} needs {", ".join(LANGS)}')
    text = tx.get('text') or {}
    for key in TEXT_KEYS:
        if not all((text.get(key) or {}).get(lang) for lang in LANGS):
            errors.append(f'robotics.taxonomy.text.{key} needs {", ".join(LANGS)}')
    for world in WORLDS:
        if not all(((text.get('worlds') or {}).get(world) or {}).get(lang) for lang in LANGS):
            errors.append(f'robotics.taxonomy.text.worlds.{world} needs {", ".join(LANGS)}')
    labels = (rb.get('hero') or {}).get('labels')
    if labels is not None:
        if sorted(labels) != sorted(scope(site)) or not all(isinstance(v, str) and v.strip() for v in labels.values()):
            errors.append('robotics.hero.labels: give every branch section exactly one short English label')
    return errors


def alt(site, lang):
    """The figure's description, spelled out from the same steps it draws."""
    tx = site['robotics']['taxonomy']
    text = tx['text']
    stop, colon, comma, op, cl = SEP[lang]
    parts = [localize(text['alt'], lang), f"{localize(text['agent'], lang)}{colon}{localize(text['loop'], lang)}"]
    for i, step in enumerate(tx['steps'], 1):
        names = comma.join(f"{sec} {site['sections'][sec][lang]}" for sec in step['sections'])
        world = localize(text['worlds'][step['world']], lang)
        parts.append(f"{i} {localize(step['label'], lang)}{op}{world}{cl}{colon}{names}")
    return stop.join(parts) + stop.strip()


def step_chip(step, i, lang):
    label = localize(step['label'], lang)
    return f'{i} · {label.upper() if lang == "en" else label}'


def render(site, works, lang, theme):
    rb = site['robotics']
    tx = rb['taxonomy']
    text = tx['text']
    steps = tx['steps']
    picked = set(rb.get('cherry_pick') or [])
    count = Counter(w['section'] for w in works)
    pal = PALETTE[theme]
    n = len(steps)
    card_w = (W - 2 * PAD - (n - 1) * GX) / n
    inner = card_w - 2 * CARD_PAD
    accents = [pal['abcd'[i % 4]] for i in range(n)]

    # Lay out each card's text first, so every card gets the height of the tallest.
    cards = []
    for step in steps:
        title = wrap(localize(step['title'], lang), FS_TITLE, inner, bold=True)
        rows = []
        for sec in step['sections']:
            name = wrap(f"{sec} {site['sections'][sec][lang]}", FS_SEC, inner - PILL_W - 8)
            note = localize(text['picked'], lang) if sec in picked else ''
            rows.append((name, note, count.get(sec, 0)))
        head_h = 34 + len(title) * LH_TITLE + 12
        body_h = sum(len(name) * LH_SEC + (17 if note else 0) + 14 for name, note, _ in rows) + 12
        cards.append((title, rows, head_h, body_h))
    head_h = max(c[2] for c in cards)
    card_h = head_h + max(c[3] for c in cards)

    card_y = PAD + AGENT_H + LINK_H
    world_y = card_y + card_h + 18
    loop_y = world_y + WORLD_H + LOOP_H - 12
    height = loop_y + 14 + PAD
    xs = [PAD + i * (card_w + GX) for i in range(n)]

    out = []
    o = out.append
    description = alt(site, lang)
    o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height:g}" width="{W}" height="{height:g}" '
      f'role="img" aria-label="{escape(description)}" font-family="{escape(FONTS[lang])}">')
    o(f'<title>{escape(description)}</title>')
    o('<defs>')
    o(f'<marker id="arr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
      f'<path d="M1 1 L9 5 L1 9 Z" fill="{pal["sub"]}"/></marker>')
    o('</defs>')
    # Opaque card, so either variant stays legible on any page theme.
    o(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{height - 1:g}" rx="12" fill="{pal["bg"]}" stroke="{pal["frame"]}"/>')

    # The coding agent, above every step.
    o(f'<rect x="{PAD}" y="{PAD}" width="{W - 2 * PAD}" height="{AGENT_H}" rx="12" '
      f'fill="{pal["inherit_fill"]}" stroke="{pal["frame"]}"/>')
    o(f'<text x="{W / 2:g}" y="{PAD + 28}" text-anchor="middle" font-size="{FS_AGENT}" font-weight="700" fill="{pal["ink"]}">'
      f'<tspan font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" fill="{pal["sub"]}">&lt;/&gt;</tspan> '
      f'{escape(localize(text["agent"], lang))}</text>')
    o(f'<text x="{W / 2:g}" y="{PAD + 51}" text-anchor="middle" font-size="{FS_LOOP}" fill="{pal["sub"]}">'
      f'{escape(localize(text["loop"], lang))}</text>')

    for i, (x, (title, rows, _, _), step) in enumerate(zip(xs, cards, steps)):
        k, soft = accents[i]
        mid = x + card_w / 2
        # Code goes down to the step; observations come back up.
        y0, y1 = PAD + AGENT_H + 4, card_y - 4
        o(f'<line x1="{mid - 9:g}" y1="{y0}" x2="{mid - 9:g}" y2="{y1}" stroke="{pal["sub"]}" stroke-width="1.6" marker-end="url(#arr)"/>')
        o(f'<line x1="{mid + 9:g}" y1="{y1}" x2="{mid + 9:g}" y2="{y0}" stroke="{pal["sub"]}" stroke-width="1.6" marker-end="url(#arr)"/>')
        # Card with a tinted head.
        o(f'<rect x="{x:g}" y="{card_y}" width="{card_w:g}" height="{card_h:g}" rx="12" fill="{pal["bg"]}" stroke="{k}" stroke-width="1.6"/>')
        o(f'<path d="M{x + 0.8:g} {card_y + head_h} V{card_y + 12} a11.2 11.2 0 0 1 11.2 -11.2 H{x + card_w - 12:g} '
          f'a11.2 11.2 0 0 1 11.2 11.2 V{card_y + head_h} Z" fill="{soft}"/>')
        o(f'<line x1="{x:g}" y1="{card_y + head_h}" x2="{x + card_w:g}" y2="{card_y + head_h}" stroke="{k}" stroke-opacity="0.35"/>')
        o(f'<text x="{x + CARD_PAD:g}" y="{card_y + 25}" font-size="{FS_CHIP}" font-weight="700" letter-spacing="0.6" fill="{k}">'
          f'{escape(step_chip(step, i + 1, lang))}</text>')
        for j, line in enumerate(title):
            o(f'<text x="{x + CARD_PAD:g}" y="{card_y + 50 + j * LH_TITLE}" font-size="{FS_TITLE}" font-weight="700" '
              f'fill="{pal["ink"]}">{escape(line)}</text>')
        y = card_y + head_h + 16
        for name, note, num in rows:
            px = x + card_w - CARD_PAD - PILL_W
            o(f'<rect x="{px:g}" y="{y:g}" width="{PILL_W}" height="{PILL_H}" rx="11" fill="{soft}"/>')
            o(f'<text x="{px + PILL_W / 2:g}" y="{y + 15.5:g}" text-anchor="middle" font-size="13" font-weight="700" '
              f'fill="{k}">{num}</text>')
            for j, line in enumerate(name):
                o(f'<text x="{x + CARD_PAD:g}" y="{y + 15 + j * LH_SEC:g}" font-size="{FS_SEC}" fill="{pal["ink"]}">{escape(line)}</text>')
            y += len(name) * LH_SEC
            if note:
                o(f'<text x="{x + CARD_PAD:g}" y="{y + 13:g}" font-size="{FS_NOTE}" font-style="italic" fill="{pal["sub"]}">'
                  f'⤴ {escape(note)}</text>')
                y += 17
            y += 14
        # The next step follows from this one.
        if i < n - 1:
            ya = card_y + head_h / 2
            o(f'<line x1="{x + card_w + 6:g}" y1="{ya:g}" x2="{x + card_w + GX - 8:g}" y2="{ya:g}" stroke="{pal["sub"]}" '
              f'stroke-width="1.8" marker-end="url(#arr)"/>')

    # Where each step happens: runs of the same world merge into one band.
    runs = []
    for i, step in enumerate(steps):
        if runs and runs[-1][0] == step['world']:
            runs[-1][2] = i
        else:
            runs.append([step['world'], i, i])
    for world, a, b in runs:
        x0, x1 = xs[a], xs[b] + card_w
        dash = ' stroke-dasharray="6 4"' if world == 'sim' else ''
        fill = pal['inherit_fill'] if world == 'real' else pal['bg']
        o(f'<rect x="{x0:g}" y="{world_y:g}" width="{x1 - x0:g}" height="{WORLD_H}" rx="{WORLD_H / 2:g}" fill="{fill}" '
          f'stroke="{pal["inherit_stroke"]}" stroke-width="1.3"{dash}/>')
        o(f'<text x="{(x0 + x1) / 2:g}" y="{world_y + 21:g}" text-anchor="middle" font-size="{FS_WORLD}" font-weight="600" '
          f'fill="{pal["ink"]}">{escape(localize(text["worlds"][world], lang))}</text>')
    for (w0, _, b), (w1, a, _) in zip(runs, runs[1:]):
        label = 'Real2Sim' if (w0, w1) == ('real', 'sim') else 'Sim2Real'
        cx = (xs[b] + card_w + xs[a]) / 2
        cw = text_width(label, 12) * 1.08 + 20
        o(f'<rect x="{cx - cw / 2:g}" y="{world_y + 5:g}" width="{cw:g}" height="{WORLD_H - 10}" rx="{(WORLD_H - 10) / 2:g}" '
          f'fill="{pal["ink"]}"/>')
        o(f'<text x="{cx:g}" y="{world_y + 20.5:g}" text-anchor="middle" font-size="12" font-weight="700" '
          f'fill="{pal["bg"]}">{label}</text>')

    # Back from the last step to the first.
    xa, xb = xs[0] + card_w / 2, xs[-1] + card_w / 2
    yb = world_y + WORLD_H
    o(f'<path d="M{xb:g} {yb + 4:g} V{loop_y - 10:g} a10 10 0 0 1 -10 10 H{xa + 10:g} a10 10 0 0 1 -10 -10 V{yb + 6:g}" '
      f'fill="none" stroke="{pal["sub"]}" stroke-width="1.6" marker-end="url(#arr)"/>')
    back = localize(text['back'], lang)
    bw = text_width(back, 13) + 24
    o(f'<rect x="{W / 2 - bw / 2:g}" y="{loop_y - 11:g}" width="{bw:g}" height="22" fill="{pal["bg"]}"/>')
    o(f'<text x="{W / 2:g}" y="{loop_y + 4.5:g}" text-anchor="middle" font-size="13" fill="{pal["sub"]}">{escape(back)}</text>')
    o('</svg>')
    return '\n'.join(out) + '\n'


def picture(site, lang):
    """README markup: the light figure, swapped for the dark one under a dark system theme."""
    description = escape(alt(site, lang), quote=True)
    base = f'{OUT_DIR}/robotics-map-{lang}'
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{base}-dark.svg">\n'
            f'  <img src="{base}-light.svg" alt="{description}" width="100%">\n</picture>')


def outputs(site, works):
    """Yield (relative path, SVG text) for every language and theme."""
    if not site.get('robotics'):
        return
    for lang in LANGS:
        for theme in THEMES:
            yield f'{OUT_DIR}/robotics-map-{lang}-{theme}.svg', render(site, works, lang, theme)
