"""Shared data contract and local-link checks for the three-stage collection."""
from collections import Counter
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit

import yaml

LAYOUT = 'three-stages-v1'
NUMBERED_SECTIONS = {f'{a}.{b}' for a, n in ((1, 7), (2, 6), (3, 6)) for b in range(1, n + 1)}
EXPECTED = NUMBERED_SECTIONS | {'SV'}
LANGS = ('en', 'zh', 'ja')
SCOPES = {'core', 'adjacent', 'resource', 'survey', 'demo', 'reading'}


def anchor(ident):
    return 'paper-' + re.sub(r'[^0-9a-zA-Z]+', '-', ident).strip('-').lower()


def load(root):
    root = Path(root)
    return (yaml.safe_load((root / 'data/site.yaml').read_text(encoding='utf-8')),
            yaml.safe_load((root / 'data/works.yaml').read_text(encoding='utf-8')))


def catalog(site):
    rows = {key: {**{l: value[l] for l in LANGS}, 'anchor': 's' + key.replace('.', '-'),
                  'stage': int(key[0])} for key, value in site['sections'].items()}
    rows['SV'] = {**site['text']['related_title'], 'anchor': 'related', 'stage': None}
    return rows


def metadata(work):
    return {'id': work['id'], 'scope': work['scope'].title(), 'primary': work['section'],
            'stage': int(work['section'][0]) if work['section'] != 'SV' else None,
            'type': work['type']}


def canonical_records(text):
    return [json.loads(m) for m in re.findall(r'<!-- mmac-record: (.*?) -->', text)]


def validate_catalog(site, works, strict_ja=True):
    errors, warnings = [], []
    if site.get('layout') != LAYOUT:
        errors.append('unknown public layout; migrate the data contract explicitly')
    if set(site['sections']) != NUMBERED_SECTIONS:
        errors.append('Expected 19 numbered sections across three stages')
    stage_sections = [sec for stage in site['stages'] for sec in stage['sections']]
    if set(stage_sections) != NUMBERED_SECTIONS or len(stage_sections) != len(set(stage_sections)):
        errors.append('Stages must partition the public sections exactly once')
    for stage in site['stages']:
        if any(not sec.startswith(str(stage['id']) + '.') for sec in stage['sections']):
            errors.append('Stage and section disagree')
    ids = [w['id'] for w in works]
    if len(ids) != len(set(ids)):
        errors.append('duplicate canonical ID')
    anchors = [anchor(i) for i in ids]
    if len(anchors) != len(set(anchors)):
        errors.append('canonical IDs produce colliding anchors')
    aliases = {}
    for w in works:
        ident = w['id']
        if re.fullmatch(r'\d{4}\.\d{4,5}v\d+', ident):
            errors.append(f'{ident}: canonical arXiv IDs must omit version suffixes')
        if w.get('scope') not in SCOPES:
            errors.append(f'{ident}: invalid scope')
        if w.get('type') == 'paper' and w.get('scope') not in ('core', 'adjacent', 'survey'):
            errors.append(f'{ident}: a paper cannot be counted as a resource or demo')
        if w.get('type') != 'paper' and w.get('scope') in ('core', 'survey'):
            errors.append(f'{ident}: nonpapers cannot claim Core or Survey')
        if not w.get('sources') or w.get('url') not in w['sources']:
            errors.append(f'{ident}: primary URL must be retained in sources')
        if len(w.get('sources', [])) != len(set(w.get('sources', []))):
            errors.append(f'{ident}: duplicate sources')
        for url in w.get('sources', []):
            p = urlsplit(url)
            if p.scheme not in ('http', 'https') or not p.netloc:
                errors.append(f'{ident}: invalid source URL')
        for alias in w.get('aliases', []):
            if alias in ids or alias in aliases:
                errors.append(f'{ident}: ambiguous canonical alias {alias}')
            aliases[alias] = ident
        if w.get('scope') == 'core' and not all(w.get('verification', {}).get(l, '').strip() for l in ('en', 'zh')):
            errors.append(f'{ident}: Core requires retained verification evidence in English and Chinese')
        for lang in LANGS:
            value = (w.get('tldr') or {}).get(lang, '').strip()
            if not value:
                (warnings if lang == 'ja' and not strict_ja else errors).append(f'{ident}: missing tldr.{lang}')
            elif re.search(r'\b(?:TODO|TBD|PLACEHOLDER)\b', value, re.I):
                errors.append(f'{ident}: placeholder in tldr.{lang}')
            elif lang == 'ja' and not re.search(r'[\u3040-\u30ff]', value):
                errors.append(f'{ident}: Japanese summary must contain Japanese prose')
        if w.get('section') == 'SV' and w.get('scope') != 'survey':
            errors.append(f'{ident}: survey placement requires Survey scope')
    # Primary arXiv aliases must be explicit; resources may use independent stable IDs.
    for w in works:
        match = re.fullmatch(r'https://arxiv.org/abs/(\d{4}\.\d{4,5})', w['url'])
        if w['type'] == 'paper' and match and match[1] != w['id'] and match[1] not in w.get('aliases', []):
            errors.append(f'{w["id"]}: canonical ID differs from source without an explicit alias')
    destinations = set(anchors) | {'contents', 'related', 'contact', 'citation', 'stage-1', 'stage-2', 'stage-3'}
    destinations |= {'s' + s.replace('.', '-') for s in NUMBERED_SECTIONS}
    for old, target in site.get('anchor_aliases', {}).items():
        if old in destinations or target not in destinations or not re.fullmatch(r'[a-z0-9-]+', old):
            errors.append(f'Invalid compatibility anchor: {old} -> {target}')
    return errors, warnings


def anchors_in(text):
    result = set(re.findall(r'<a\s+id=["\']([^"\']+)', text))
    headings = Counter()
    for h in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        h = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', h)
        h = re.sub(r'<[^>]+>', '', h).lower().strip()
        h = ''.join(c for c in h if c in '-_ ' or unicodedata.category(c)[0] not in ('P', 'S'))
        h = h.replace(' ', '-')
        suffix = f'-{headings[h]}' if headings[h] else ''
        headings[h] += 1
        result.add(h + suffix)
    return result


def check_local_links(root):
    """Check actual targets, including cross-file fragments and HTML images."""
    root = Path(root).resolve()
    files = [p for p in root.rglob('*.md') if '.git' not in p.parts]
    documents = {p: p.read_text(encoding='utf-8') for p in files}
    targets = {p: anchors_in(text) for p, text in documents.items()}
    issues = []
    for path, text in documents.items():
        explicit = re.findall(r'<a\s+id=["\']([^"\']+)', text)
        if len(explicit) != len(set(explicit)):
            issues.append(f'{path.relative_to(root)}: duplicate explicit anchors')
        urls = re.findall(r'\]\(([^)\s]+)(?:\s+"[^"]*")?\)', text)
        urls += re.findall(r'(?:src|srcset|href)="([^"]+)"', text)
        for url in set(urls):
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc:
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not target.is_relative_to(root):
                issues.append(f'{path.relative_to(root)}: local link escapes repository: {url}')
            elif not target.exists():
                issues.append(f'{path.relative_to(root)}: missing local target {url}')
            elif parsed.fragment and target in targets and unquote(parsed.fragment) not in targets[target]:
                issues.append(f'{path.relative_to(root)}: missing fragment {url}')
    return sorted(set(issues))
