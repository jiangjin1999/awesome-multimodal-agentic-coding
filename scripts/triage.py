"""Decision log for update runs (data/triage.yaml); the rules are in docs/AUTO_UPDATE.md."""
from pathlib import Path
import re
from urllib.parse import urlsplit

import yaml

DECISIONS = ('pending', 'added', 'updated', 'excluded', 'deferred')
TRIGGERS = ('sweep', 'report', 'citations', 'issue')
RUN_FIELDS = {'date', 'trigger', 'covered', 'note'}
FIELDS = {'id', 'title', 'url', 'found', 'via', 'decision', 'decided', 'entry', 'precedent', 'reason', 'note'}
DATE = re.compile(r'\d{4}-\d{2}-\d{2}')


def load(root):
    path = Path(root) / 'data/triage.yaml'
    return yaml.safe_load(path.read_text(encoding='utf-8')) if path.exists() else None


def validate(works, log):
    """Every candidate has one decision, and that decision agrees with data/works.yaml."""
    if log is None:
        return []
    if not isinstance(log, dict) or set(log) - {'runs', 'candidates'}:
        return ['triage: the top level holds only runs and candidates']
    known = {w['id'] for w in works} | {a for w in works for a in w.get('aliases', [])}
    errors = []
    for n, run in enumerate(log.get('runs') or [], 1):
        where = f'triage run {n}'
        if set(run) - RUN_FIELDS:
            errors.append(f'{where}: unknown fields {sorted(set(run) - RUN_FIELDS)}')
        if not DATE.fullmatch(str(run.get('date', ''))):
            errors.append(f'{where}: date must be YYYY-MM-DD')
        if run.get('trigger') not in TRIGGERS:
            errors.append(f'{where}: trigger must be one of {", ".join(TRIGGERS)}')
        if not str(run.get('covered', '')).strip():
            errors.append(f'{where}: covered must say what the run searched')
    seen = set()
    for c in log.get('candidates') or []:
        ident = str(c.get('id', '')).strip()
        if not ident:
            errors.append('triage: a candidate has no id')
            continue
        where = f'triage {ident}'
        if ident in seen:
            errors.append(f'{where}: duplicate candidate')
        seen.add(ident)
        if set(c) - FIELDS:
            errors.append(f'{where}: unknown fields {sorted(set(c) - FIELDS)}')
        if re.fullmatch(r'\d{4}\.\d{4,5}v\d+', ident):
            errors.append(f'{where}: omit the arXiv version suffix')
        for field in ('title', 'via'):
            if not str(c.get(field, '')).strip():
                errors.append(f'{where}: {field} is required')
        url = urlsplit(str(c.get('url', '')))
        if url.scheme not in ('http', 'https') or not url.netloc:
            errors.append(f'{where}: url must be http(s)')
        found = str(c.get('found', ''))
        if not DATE.fullmatch(found):
            errors.append(f'{where}: found must be YYYY-MM-DD')
        decision = c.get('decision')
        if decision not in DECISIONS:
            errors.append(f'{where}: decision must be one of {", ".join(DECISIONS)}')
            continue
        if decision == 'pending':
            if 'decided' in c:
                errors.append(f'{where}: a pending candidate has no decided date')
        else:
            decided = str(c.get('decided', ''))
            if not DATE.fullmatch(decided):
                errors.append(f'{where}: decided must be YYYY-MM-DD')
            elif DATE.fullmatch(found) and decided < found:
                errors.append(f'{where}: decided before it was found')
        entry = str(c.get('entry', ident))
        if decision in ('added', 'updated'):
            if entry not in known:
                errors.append(f'{where}: marked {decision}, but {entry} is not in data/works.yaml')
        elif entry in known:
            errors.append(f'{where}: {entry} is in data/works.yaml; mark it added or updated')
        if decision in ('excluded', 'deferred') and not str(c.get('reason', '')).strip():
            errors.append(f'{where}: {decision} requires a reason')
        for precedent in c.get('precedent') or []:
            if precedent not in known:
                errors.append(f'{where}: precedent {precedent} is not in data/works.yaml')
    return errors
