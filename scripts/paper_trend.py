"""Render the papers-per-stage timeline at the end of the READMEs from data/works.yaml.

One line per stage: the cumulative number of papers (`type: paper`) whose primary section
belongs to that stage, by first-publication month (`date`). Surveys (section SV), resources,
demos and readings are not counted, and papers without a date are left out of the lines and
reported in a note under the chart and in the per-year table.

The localized words live in `paper_trend` in data/site.yaml; the numbers come only from
data/works.yaml, so the chart follows the catalog on every build. Each language gets a light
and a dark SVG under assets/paper-trend/. build_readme.py writes them and `--check` fails when
one is out of date, exactly like the other figures.
"""
import math
from collections import Counter
from html import escape

from engine_map import FONTS, LANGS, PALETTE as MAP_PALETTE, THEMES, localize, text_width

OUT_DIR = 'assets/paper-trend'
TEXT_KEYS = ('heading', 'intro', 'title', 'subtitle', 'undated', 'alt', 'table', 'year', 'total', 'no_date')

# Stage colours keep the hero image's hues (blue, violet, orange), stepped per theme so every
# pair stays apart under colour-vision deficiency on that theme's background.
STAGE_COLORS = {
    'light': ('#0550AE', '#A475F9', '#C4500B'),
    'dark': ('#4C9EF7', '#8050DD', '#E07230'),
}
GRID = {'light': '#EAEEF2', 'dark': '#21262D'}

# Geometry (SVG user units).
WIDTH, PAD, PLOT_H = 1040, 24, 300
FS_TITLE, FS_SUB, FS_LEGEND, FS_TICK, FS_END, FS_NOTE = 18, 13, 13, 12, 13, 12
LABEL_GAP = 18   # minimum vertical distance between two end labels


def month_index(date):
    year, month = str(date).split('.')
    return int(year) * 12 + int(month) - 1


def month_name(index):
    return f'{index // 12}.{index % 12 + 1:02d}'


def stage_of(work):
    section = str(work.get('section') or '')
    return section.split('.')[0] if '.' in section else None


def tally(site, works):
    """Papers per stage and month: ({stage id: Counter(month index -> papers)}, {stage id: undated papers})."""
    stages = [str(st['id']) for st in site['stages']]
    dated = {s: Counter() for s in stages}
    undated = Counter()
    for w in works:
        stage = stage_of(w)
        if w.get('type') != 'paper' or stage not in dated:
            continue
        if w.get('date'):
            dated[stage][month_index(w['date'])] += 1
        else:
            undated[stage] += 1
    return dated, undated


def series(site, works):
    """The plotted months (first, last) and, per stage, (month index, cumulative papers) points."""
    dated, undated = tally(site, works)
    months = [m for c in dated.values() for m in c]
    if not months:
        return None, {}, undated
    # Start one month before the first paper so every line rises from zero.
    first, last = min(months) - 1, max(months)
    lines = {}
    for stage, c in dated.items():
        if not c:
            continue
        start, total, points = max(first, min(c) - 1), 0, []
        for m in range(start, last + 1):
            total += c.get(m, 0)
            points.append((m, total))
        lines[stage] = points
    return (first, last), lines, undated


def nice_ticks(top, count=6):
    """Round tick values from 0 to at least `top`, with at most about `count` intervals."""
    if top <= 0:
        return [0, 1]
    raw = top / count
    mag = 10 ** math.floor(math.log10(raw))
    step = next(s * mag for s in (1, 2, 2.5, 5, 10) if s * mag >= raw)
    n = math.ceil(top / step)
    return [round(i * step, 6) for i in range(n + 1)]


def fmt(value):
    return f'{value:,.0f}' if float(value).is_integer() else f'{value:,}'


def stage_label(site, stage, lang):
    st = next(s for s in site['stages'] if str(s['id']) == stage)
    return f"Stage {stage} · {localize(st['name'], lang)}"


def text(site, key, lang, **values):
    value = localize(site['paper_trend']['text'][key], lang)
    return value.format(**values) if values else value


def validate(site, works):
    pt = site.get('paper_trend')
    if not pt:
        return []
    errors = []
    for key in TEXT_KEYS:
        for lang in LANGS:
            if not ((pt.get('text') or {}).get(key) or {}).get(lang):
                errors.append(f'paper_trend: text.{key} missing {lang}')
    if len(site['stages']) > len(STAGE_COLORS['light']):
        errors.append(f"paper_trend: {len(site['stages'])} stages but only {len(STAGE_COLORS['light'])} stage colours")
    if not series(site, works)[1]:
        errors.append('paper_trend: no dated papers to plot')
    return errors


def render(site, works, lang, theme):
    pal = MAP_PALETTE[theme]
    colors = STAGE_COLORS[theme]
    font = FONTS[lang]
    (first, last), lines, undated = series(site, works)
    stages = [str(st['id']) for st in site['stages']]

    out = []
    o = out.append

    # Header: title, subtitle, legend (wrapping to more rows on a narrow width).
    y_title = PAD + FS_TITLE
    y_sub = y_title + 22
    legend, x, y_leg = [], PAD, y_sub + 28
    for i, stage in enumerate(stages):
        label = stage_label(site, stage, lang)
        w = 26 + 8 + text_width(label, FS_LEGEND)
        if x > PAD and x + w > WIDTH - PAD:
            x, y_leg = PAD, y_leg + 24
        legend.append((x, y_leg, colors[i], label))
        x += w + 26

    # Plot area.
    ends = {s: pts[-1][1] for s, pts in lines.items()}
    ticks = nice_ticks(max(ends.values()))
    plot_top = y_leg + 26
    plot_bot = plot_top + PLOT_H
    x0 = PAD + max(text_width(fmt(t), FS_TICK) for t in ticks) + 10
    end_w = max(text_width(fmt(ends[s]), FS_END) * 1.06 + 6 + text_width(f'Stage {s}', FS_END) for s in lines)
    x1 = WIDTH - PAD - 14 - end_w
    span = max(last - first, 1)

    def px(m):
        return x0 + (m - first) / span * (x1 - x0)

    def py(v):
        return plot_bot - v / ticks[-1] * PLOT_H

    y_years = plot_bot + 22
    note = text(site, 'undated', lang, n=sum(undated.values())) if sum(undated.values()) else ''
    y_note = y_years + 30
    height = (y_note if note else y_years) + PAD - 4

    title = text(site, 'title', lang)
    o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height:g}" width="{WIDTH}" height="{height:g}" '
      f'role="img" aria-label="{escape(text(site, "alt", lang))}" font-family="{escape(font)}">')
    o(f'<title>{escape(title)}</title>')
    # Hovering a month (when the SVG is opened on its own) shows a guide line and its numbers.
    o('<style>.m .g{opacity:0}.m:hover .g{opacity:1}</style>')
    # Opaque card, as in the other figures: legible even when GitHub shows the light image on a dark page.
    o(f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1:g}" rx="10" fill="{pal["bg"]}" stroke="{pal["frame"]}"/>')
    o(f'<text x="{PAD}" y="{y_title}" font-size="{FS_TITLE}" font-weight="700" fill="{pal["ink"]}">{escape(title)}</text>')
    o(f'<text x="{PAD}" y="{y_sub}" font-size="{FS_SUB}" fill="{pal["sub"]}">'
      f'{escape(text(site, "subtitle", lang, last=month_name(last)))}</text>')
    for lx, ly, color, label in legend:
        o(f'<line x1="{lx}" y1="{ly - 4.5}" x2="{lx + 26}" y2="{ly - 4.5}" stroke="{color}" stroke-width="2" stroke-linecap="round"/>')
        o(f'<circle cx="{lx + 13}" cy="{ly - 4.5}" r="4" fill="{color}" stroke="{pal["bg"]}" stroke-width="2"/>')
        o(f'<text x="{lx + 34}" y="{ly}" font-size="{FS_LEGEND}" fill="{pal["ink"]}">{escape(label)}</text>')

    # Gridlines and y ticks; the zero line is the baseline.
    for t in ticks:
        y = py(t)
        stroke = pal['line'] if t == 0 else GRID[theme]
        o(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" stroke="{stroke}" stroke-width="1"/>')
        o(f'<text x="{x0 - 8:.1f}" y="{y + 4:.1f}" text-anchor="end" font-size="{FS_TICK}" fill="{pal["sub"]}" '
          f'style="font-variant-numeric:tabular-nums">{fmt(t)}</text>')

    # Year boundaries as ticks under the baseline; each year's label sits in the middle of its months.
    for year in range(first // 12, last // 12 + 1):
        lo, hi = max(first, year * 12 - 0.5), min(last, year * 12 + 11.5)
        if year * 12 - 0.5 > first:
            bx = px(year * 12 - 0.5)
            o(f'<line x1="{bx:.1f}" y1="{plot_bot}" x2="{bx:.1f}" y2="{plot_bot + 6}" stroke="{pal["line"]}" stroke-width="1"/>')
        if px(hi) - px(lo) >= text_width(str(year), FS_TICK) + 8:
            o(f'<text x="{(px(lo) + px(hi)) / 2:.1f}" y="{y_years}" text-anchor="middle" font-size="{FS_TICK}" '
              f'fill="{pal["sub"]}">{year}</text>')

    # Per-month hover targets: a guide line and a native tooltip with every stage's count.
    cum = {s: dict(pts) for s, pts in lines.items()}
    step = (x1 - x0) / span
    for m in range(first, last + 1):
        x = px(m)
        values = ' · '.join(f"Stage {s}: {cum[s].get(m, 0 if m < min(cum[s]) else ends[s])}" for s in lines)
        o(f'<g class="m"><title>{month_name(m)} — {escape(values)}</title>'
          f'<rect x="{x - step / 2:.1f}" y="{plot_top}" width="{step:.1f}" height="{PLOT_H}" fill="transparent"/>'
          f'<line class="g" x1="{x:.1f}" y1="{plot_top}" x2="{x:.1f}" y2="{plot_bot}" stroke="{pal["sub"]}" stroke-width="1"/></g>')

    # Lines, then end dots with a ring in the background colour.
    for i, stage in enumerate(stages):
        if stage not in lines:
            continue
        d = ' '.join(f'{"M" if j == 0 else "L"}{px(m):.1f},{py(v):.1f}' for j, (m, v) in enumerate(lines[stage]))
        o(f'<path d="{d}" fill="none" stroke="{colors[i]}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" '
          f'pointer-events="none"/>')
    for i, stage in enumerate(stages):
        if stage in lines:
            o(f'<circle cx="{px(last):.1f}" cy="{py(ends[stage]):.1f}" r="4" fill="{colors[i]}" stroke="{pal["bg"]}" '
              f'stroke-width="2" pointer-events="none"/>')

    # End labels: total, then the stage number. Labels that would touch are spread apart and
    # tied back to their dot with a leader line.
    order = sorted(lines, key=lambda s: -ends[s])
    placed = {}
    for s in order:
        y = py(ends[s])
        prev = [placed[p] for p in placed]
        if prev and y - max(prev) < LABEL_GAP:
            y = max(prev) + LABEL_GAP
        placed[s] = min(y, plot_bot)
    for s in reversed(order):   # push back up from the baseline if the bottom label was clamped
        below = [placed[p] for p in placed if p != s and placed[p] > placed[s]]
        if below and min(below) - placed[s] < LABEL_GAP:
            placed[s] = min(below) - LABEL_GAP
    lx = x1 + 14
    for s in order:
        dot_y, y = py(ends[s]), placed[s]
        if abs(y - dot_y) > 1:
            o(f'<line x1="{px(last) + 6:.1f}" y1="{dot_y:.1f}" x2="{lx - 3:.1f}" y2="{y:.1f}" stroke="{pal["sub"]}" stroke-width="1"/>')
        o(f'<text x="{lx:.1f}" y="{y + 4.5:.1f}" font-size="{FS_END}" fill="{pal["ink"]}">'
          f'<tspan font-weight="700">{fmt(ends[s])}</tspan><tspan dx="6" fill="{pal["sub"]}">Stage {s}</tspan></text>')

    if note:
        o(f'<text x="{PAD}" y="{y_note}" font-size="{FS_NOTE}" fill="{pal["sub"]}">{escape(note)}</text>')
    o('</svg>')
    return '\n'.join(out) + '\n'


def picture(site, lang):
    """README markup: the light chart, swapped for the dark one under a dark system theme."""
    alt = escape(text(site, 'alt', lang), quote=True)
    base = f'{OUT_DIR}/paper-trend-{lang}'
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{base}-dark.svg">\n'
            f'  <img src="{base}-light.svg" alt="{alt}" width="100%">\n</picture>')


def table(site, works, lang):
    """Markdown table: new papers per year and stage, then undated papers and the totals."""
    dated, undated = tally(site, works)
    stages = list(dated)
    years = sorted({m // 12 for c in dated.values() for m in c})
    per_year = {s: Counter() for s in stages}
    for s, c in dated.items():
        for m, n in c.items():
            per_year[s][m // 12] += n
    head = [text(site, 'year', lang), *(f'Stage {s}' for s in stages), text(site, 'total', lang)]
    rows = [[str(y), *(str(per_year[s][y]) for s in stages), str(sum(per_year[s][y] for s in stages))] for y in years]
    if sum(undated.values()):
        rows.append([text(site, 'no_date', lang), *(str(undated[s]) for s in stages), str(sum(undated.values()))])
    totals = {s: sum(dated[s].values()) + undated[s] for s in stages}
    rows.append([f"**{text(site, 'total', lang)}**", *(f'**{totals[s]}**' for s in stages), f'**{sum(totals.values())}**'])
    lines = ['| ' + ' | '.join(head) + ' |', '| :-- |' + ' --: |' * (len(head) - 1)]
    lines += ['| ' + ' | '.join(r) + ' |' for r in rows]
    return '\n'.join(lines)


def section(site, works, lang):
    """The README block: intro, chart and a collapsible per-year table."""
    return (f"{text(site, 'intro', lang).strip()}\n\n{picture(site, lang)}\n\n"
            f"<details>\n<summary>{escape(text(site, 'table', lang))}</summary>\n\n{table(site, works, lang)}\n\n</details>\n")


def outputs(site, works):
    """Yield (relative path, SVG text) for every language and theme."""
    if not site.get('paper_trend'):
        return
    for lang in LANGS:
        for theme in THEMES:
            yield f'{OUT_DIR}/paper-trend-{lang}-{theme}.svg', render(site, works, lang, theme)
