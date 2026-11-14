#!/usr/bin/env python3
"""Generate README.md, README.zh-CN.md and README.ja.md from data/site.yaml and data/works.yaml.

Usage:
  python scripts/build_readme.py           # write the three READMEs
  python scripts/build_readme.py --check   # validate data and fail if a README is out of date
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

import yaml

import engine_map
import eval_ladder
from catalog import LAYOUT, validate_catalog, check_local_links

ROOT = Path(__file__).resolve().parent.parent
LANGS = ['en', 'zh', 'ja']


def load():
    site = yaml.safe_load((ROOT / 'data/site.yaml').read_text(encoding='utf-8'))
    works = yaml.safe_load((ROOT / 'data/works.yaml').read_text(encoding='utf-8'))
    return site, works


# ------------------------------------------------------------------ validation
def validate(site, works, strict_ja):
    errors, warnings = validate_catalog(site, works, strict_ja=strict_ja)
    ids = Counter(w['id'] for w in works)
    for k, n in ids.items():
        if n > 1:
            errors.append(f'duplicate id: {k}')
    byid = {w['id']: w for w in works}
    secs = site['sections']
    for w in works:
        where = f"{w.get('id')}"
        for f in ('id', 'title', 'url', 'section', 'type', 'tldr'):
            if not w.get(f):
                errors.append(f'{where}: missing {f}')
        if w.get('section') not in secs and w.get('section') != 'SV':
            errors.append(f"{where}: unknown section {w.get('section')}")
        elif w.get('section') in secs and w.get('sub') not in secs[w['section']]['subs']:
            errors.append(f"{where}: sub {w.get('sub')!r} not allowed in {w['section']}")
        if w.get('type') not in ('paper', 'resource', 'demo', 'reading'):
            errors.append(f"{where}: bad type {w.get('type')}")
        if not re.match(r'^https?://', w.get('url', '')):
            errors.append(f'{where}: url is not http(s)')
        if w.get('date') and not re.match(r'^20\d\d\.(0[1-9]|1[0-2])$', str(w['date'])):
            errors.append(f"{where}: date must be YYYY.MM, got {w['date']}")
        for s in w.get('see_also') or []:
            if s not in secs:
                errors.append(f'{where}: see_also section {s} unknown')
    for st in site['stages']:
        for k in st['start_with']:
            if k not in byid:
                errors.append(f"stage {st['id']}: start_with id {k} not found")
        for extra in st.get('extras') or []:
            if not re.fullmatch(r'[a-z0-9-]+', extra.get('anchor') or '') or extra['anchor'] in {sec_anchor(s) for s in secs}:
                errors.append(f"stage {st['id']}: invalid extra anchor {extra.get('anchor')!r}")
            for lang in LANGS:
                if not (extra.get('title') or {}).get(lang) or not (extra.get('body') or {}).get(lang, '').strip():
                    errors.append(f"stage {st['id']}: extra {extra.get('anchor')} missing title/body for {lang}")
    for sec, ks in (site.get('see_also') or {}).items():
        for k in ks:
            if k not in byid:
                errors.append(f'see_also {sec}: id {k} not found')
    errors += engine_map.validate(site)
    errors += eval_ladder.validate(site, works)
    return errors, warnings


# ------------------------------------------------------------------ helpers
def anchor(wid):
    return 'paper-' + re.sub(r'[^0-9a-zA-Z]+', '-', wid).strip('-').lower()


def sec_anchor(sec):
    return 's' + sec.replace('.', '-')


def short_title(title):
    head = title.split(':')[0].strip()
    if len(head) > 48:
        head = ' '.join(head.split()[:6]) + '…'
    return head


def t(site, key, lang):
    v = site['text'][key]
    return v.get(lang) or v.get('en')


def sort_key(w):
    d = str(w.get('date') or '0000.00')
    return (-int(d.replace('.', '')), w['title'].lower())


def source_kind(url, site, demo_url=None):
    override = site.get('source_kind_overrides', {}).get(url)
    if override:
        return override
    parsed = urlsplit(url)
    host = parsed.hostname
    path = parsed.path.lower().rstrip('/')
    if host == 'arxiv.org' or path.endswith('.pdf') or host in {
        'aclanthology.org', 'doi.org', 'journals.aps.org', 'openaccess.thecvf.com',
        'openreview.net', 'pmc.ncbi.nlm.nih.gov', 'proceedings.neurips.cc',
        'www.cambridge.org', 'www.mdpi.com', 'www.nature.com', 'www.repository.cam.ac.uk',
    }:
        return 'paper'
    if host == 'huggingface.co':
        if path.startswith('/datasets/'):
            return 'dataset'
        if path.startswith('/collections/'):
            return 'collection'
        if path.startswith('/papers/'):
            return 'paper'
        if path.startswith('/spaces/'):
            return 'demo'
        return 'model'
    if '/docs/' in path or path.endswith('/skill.md'):
        return 'docs'
    if '/blog/' in path or '/news/' in path or path.startswith('/index/'):
        return 'article'
    if path.endswith('/leaderboard'):
        return 'leaderboard'
    if host == 'github.com':
        if '/awesome-' in path:
            return 'collection'
        return 'code' if path.count('/') >= 2 else 'repository'
    if url == demo_url or host in {'youtube.com', 'www.youtube.com', 'youtu.be'}:
        return 'demo'
    return 'project'


def paper_key(url, site):
    """Identify interchangeable entry points while retaining deep links."""
    if urlsplit(url).fragment:
        return None
    canonical = site.get('paper_url_aliases', {}).get(url, url)
    parsed = urlsplit(canonical)
    path = parsed.path.rstrip('/')
    if parsed.hostname == 'arxiv.org':
        match = re.fullmatch(r'/(?:abs|html|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?(?:\.pdf)?', path)
        if match:
            return 'arxiv:' + match[1]
    if source_kind(canonical, site) == 'paper':
        return parsed.netloc.lower(), path
    return None


def unique_paper_links(urls, site):
    seen = set()
    for url in urls:
        key = paper_key(url, site)
        if key is not None:
            if key in seen:
                continue
            seen.add(key)
        yield url


def entry(w, lang, site):
    date = f"`{w['date']}` " if w.get('date') else ''
    tl = (w['tldr'].get(lang) or w['tldr']['en']).strip()
    target = anchor(w['id'])
    aliases = ''.join(f'<a id="{a}"></a>\n' for a, dest in site.get('anchor_aliases', {}).items() if dest == target)
    metadata = {'id': w['id'], 'scope': w['scope'].title(), 'primary': w['section'],
                'stage': int(w['section'][0]) if w['section'] != 'SV' else None, 'type': w['type']}
    urls = dict.fromkeys([w['url'], w.get('demo'), *w.get('sources', [])])
    sources = unique_paper_links((url for url in urls if url), site)
    next(sources)  # The title already links to the first destination.
    labels = site['source_labels']
    extra = ''.join(
        f' [[{labels[source_kind(url, site, w.get("demo"))][lang]}]]({url})'
        for url in sources
    )
    return (f'{aliases}<!-- mmac-record: {json.dumps(metadata, ensure_ascii=False)} -->\n\n'
            f'- <a id="{target}"></a>{date}**[{w["title"]}]({w["url"]})**{extra}\n'
            f'  > {tl}\n')


def link_list(ids, byid):
    return ' · '.join(f'[{short_title(byid[k]["title"])}](#{anchor(k)})' for k in ids if k in byid)


# ------------------------------------------------------------------ render
def render(site, works, lang):
    byid = {w['id']: w for w in works}
    groups = defaultdict(list)
    for w in works:
        groups[(w['section'], w.get('sub'))].append(w)
    for g in groups.values():
        g.sort(key=sort_key)
    sec_count = Counter(w['section'] for w in works)
    stage_see = defaultdict(list)          # stage-3 sections pointing back to Plan-B works
    for w in works:
        for s in w.get('see_also') or []:
            stage_see[s].append(w['id'])
    for s in stage_see:
        stage_see[s].sort(key=lambda k: sort_key(byid[k]))

    L = site['languages']
    out = []
    o = out.append
    def named_anchor(target):
        for old, dest in site.get('anchor_aliases', {}).items():
            if dest == target:
                o(f'<a id="{old}"></a>')
        o(f'<a id="{target}"></a>\n')
    repo = site['repo']
    n_total = len(works)

    # header
    o(f'<!-- Generated by scripts/build_readme.py from data/*.yaml — edit the data, not this file. -->\n')
    o(f'<!-- mmac-layout: {LAYOUT} -->\n')
    o('<div align="center">\n')
    o('# Awesome Multimodal Agentic Coding\n')
    h = site['hero']
    o(f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{h["dark"]}">\n'
      f'  <img src="{h["light"]}" alt="{h["alt"]}" width="100%">\n</picture>\n')
    o(f"{t(site, 'tagline', lang)}\n")
    upd = site['updated']
    o(f'[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) '
      f'[![Works](https://img.shields.io/badge/works-{n_total}-blue.svg)](#contents) '
      f'[![Last updated](https://img.shields.io/badge/updated-{upd.replace("-", "--")}-brightgreen.svg)](https://github.com/{repo}/commits/main) '
      f'[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)\n')
    langs = ' · '.join((f'**{L[x]["label"]}**' if x == lang else f'[{L[x]["label"]}](./{L[x]["file"]})') for x in LANGS)
    o(f'{langs}\n')
    o('</div>\n')
    if lang == 'ja':
        o(f"> [!NOTE]\n> {t(site, 'machine_note', lang)}\n")

    # vision
    o(f"## {t(site, 'vision_title', lang)}\n")
    o(t(site, 'vision', lang).strip() + '\n')

    # contents
    named_anchor('contents')
    o(f'## {t(site, "contents", lang)}\n')
    for st in site['stages']:
        o(f"- [Stage {st['id']} · {st['name'][lang]}](#stage-{st['id']})")
        for sec in st['sections']:
            o(f"  - [{sec} {site['sections'][sec][lang]}](#{sec_anchor(sec)}) ({sec_count.get(sec, 0)})")
        for extra in st.get('extras') or []:
            o(f"  - [{extra['title'][lang]}](#{extra['anchor']})")
    o(f"- [{t(site, 'related_title', lang)}](#related)")
    o(f"- [{t(site, 'contact_title', lang)}](#contact) · [{t(site, 'citation_title', lang)}](#citation)\n")

    # stages
    for st in site['stages']:
        named_anchor(f'stage-{st["id"]}')
        o(f'## Stage {st["id"]} · {st["name"][lang]}\n')
        o(st['intro'][lang].strip() + '\n')
        o(f"**{t(site, 'start_with', lang)}:** {link_list(st['start_with'], byid)}\n")
        for sec in st['sections']:
            meta = site['sections'][sec]
            named_anchor(sec_anchor(sec))
            o(f'### {sec} {meta[lang]}\n')
            if meta.get('engines'):
                eng = ' · '.join(f'[{e}]({site["engines"][e]})' for e in meta['engines'])
                o(f"*{t(site, 'engines', lang)}:* {eng}\n")
            if meta.get('guide'):
                o(eval_ladder.fill(site, works, lang, anchor, meta['guide'][lang].strip()) + '\n')
            for sub in meta['subs']:
                items = groups.get((sec, sub), [])
                if not items:
                    continue
                if sub:
                    o(f"#### {site['text']['subs'][sub][lang]}\n")
                o('\n'.join(entry(w, lang, site) for w in items))
            see = list((site.get('see_also') or {}).get(sec, [])) + stage_see.get(sec, [])
            if see:
                o(f"*{t(site, 'see_also', lang)}:* {link_list(see, byid)}\n")
            o(f"[↑ {t(site, 'back_to_contents', lang)}](#contents)\n")
        # Unnumbered reference blocks: listed in the contents, but hold no entries.
        for extra in st.get('extras') or []:
            named_anchor(extra['anchor'])
            o(f"### {extra['title'][lang]}\n")
            body = extra['body'][lang].strip()
            if '{engine_map}' in body:
                body = body.replace('{engine_map}', engine_map.picture(site, lang))
            o(body + '\n')
            o(f"[↑ {t(site, 'back_to_contents', lang)}](#contents)\n")

    # surveys & related
    named_anchor('related')
    o(f'## {t(site, "related_title", lang)}\n')
    o('\n'.join(entry(w, lang, site) for w in sorted(groups.get(('SV', None), []), key=sort_key)))
    o(f"\n**{t(site, 'related_lists', lang)}**\n")
    for r in site['related_lists']:
        o(f"- [{r['name']}]({r['url']}) — {r.get(lang) or r['en']}")
    o('')

    # contact, citation, license
    named_anchor('contact')
    o(f'## {t(site, "contact_title", lang)}\n')
    o(t(site, 'contact', lang).strip() + '\n')
    o(f'<img src="{site["contact"]["wechat_image"]}" alt="WeChat QR code" width="200">\n')
    named_anchor('citation')
    o(f'## {t(site, "citation_title", lang)}\n')
    o(f"{t(site, 'citation', lang)}:\n\n```bibtex\n{site['citation'].rstrip()}\n```\n")
    o(f"## {t(site, 'license_title', lang)}\n")
    o(t(site, 'license', lang) + ' ' + t(site, 'hero_credit', lang) + '\n')
    o(f"## {t(site, 'acknowledgments_title', lang)}\n")
    o(t(site, 'acknowledgments', lang) + '\n')
    text = '\n'.join(out)
    text = re.sub(r'\n{3,}', '\n\n', text).rstrip() + '\n'
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='validate and verify the READMEs are up to date')
    ap.add_argument('--allow-missing-ja', action='store_true', help='do not fail on empty Japanese summaries')
    args = ap.parse_args()
    site, works = load()
    errors, warnings = validate(site, works, strict_ja=not args.allow_missing_ja)
    for w in warnings[:10]:
        print('warning:', w)
    if len(warnings) > 10:
        print(f'warning: … {len(warnings) - 10} more')
    if errors:
        for e in errors:
            print('error:', e)
        sys.exit(1)
    stale = []
    generated = [(ROOT / site['languages'][lang]['file'], render(site, works, lang)) for lang in LANGS]
    generated += [(ROOT / rel, svg) for rel, svg in engine_map.outputs(site)]
    generated += [(ROOT / rel, svg) for rel, svg in eval_ladder.outputs(site)]
    for path, text in generated:
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != text:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
            print(f'wrote {path.relative_to(ROOT)} ({len(text) // 1024} KB)')
    if stale:
        print('error: out of date, run `python scripts/build_readme.py`:', ', '.join(stale))
        sys.exit(1)
    if args.check:
        links = check_local_links(ROOT)
        if links:
            for issue in links:
                print('error:', issue)
            sys.exit(1)
        print(f'ok: {len(works)} works, READMEs up to date')


if __name__ == '__main__':
    main()
