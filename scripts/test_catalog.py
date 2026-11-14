"""Regression cases from the three-stage migration; no network or publication."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import engine_map
from build_readme import render, validate
from catalog import anchor, canonical_records, check_local_links, load

ROOT = Path(__file__).resolve().parents[1]


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site, cls.works = load(ROOT)

    def test_published_outputs_are_complete_in_three_languages(self):
        self.assertEqual(validate(self.site, self.works, True), ([], []))
        records = []
        for lang, config in self.site['languages'].items():
            actual = (ROOT / config['file']).read_text()
            self.assertEqual(actual, render(self.site, self.works, lang))
            records.append(canonical_records(actual))
        self.assertTrue(all(r == records[0] for r in records))
        self.assertEqual(len(records[0]), len(self.works))
        self.assertEqual(check_local_links(ROOT), [])

    def test_missing_or_fallback_japanese_cannot_publish(self):
        for summary in ('', 'TODO', 'An English fallback is not a translation.'):
            with self.subTest(summary=summary):
                rows = deepcopy(self.works)
                rows[0]['tldr']['ja'] = summary
                self.assertTrue(any('ja' in e or 'Japanese' in e for e in validate(self.site, rows, True)[0]))

    def test_core_verification_and_primary_source_cannot_disappear(self):
        rows = deepcopy(self.works)
        core = next(w for w in rows if w['scope'] == 'core')
        core['verification'] = {}
        core['sources'].remove(core['url'])
        errors = validate(self.site, rows, True)[0]
        self.assertTrue(any('verification' in e for e in errors))
        self.assertTrue(any('primary URL' in e for e in errors))

    def test_report_keeps_stable_id_when_arxiv_alias_arrives(self):
        rows = deepcopy(self.works)
        report = next(w for w in rows if w['id'] == 'system:blenderworld')
        self.assertIn('2610.23986', report['aliases'])
        self.assertEqual(anchor(report['id']), 'paper-system-blenderworld')
        report['aliases'] = []
        self.assertTrue(any('explicit alias' in e for e in validate(self.site, rows, True)[0]))

    def test_revision_and_alias_duplicates_are_rejected(self):
        for ident in ('2610.23986', '2610.23986v2'):
            rows = deepcopy(self.works)
            extra = deepcopy(rows[0]); extra['id'] = ident
            rows.append(extra)
            self.assertTrue(validate(self.site, rows, True)[0])

    def test_resource_cannot_be_counted_as_core_paper(self):
        rows = deepcopy(self.works)
        resource = next(w for w in rows if w['type'] == 'resource')
        resource['scope'] = 'core'
        self.assertTrue(any('nonpapers' in e for e in validate(self.site, rows, True)[0]))

    def test_local_cross_file_fragments_are_checked(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp); (root/'docs').mkdir()
            (root/'README.md').write_text('<a id="new-entry"></a>\n')
            doc = root/'docs/guide.md'
            doc.write_text('[entry](../README.md#old-entry)\n')
            self.assertTrue(any('missing fragment' in e for e in check_local_links(root)))
            with (root/'README.md').open('a') as f: f.write('<a id="old-entry"></a>\n')
            self.assertEqual(check_local_links(root), [])
            doc.write_text('[translation](../CONTRIBUTING.ja.md)\n')
            self.assertTrue(any('missing local target' in e for e in check_local_links(root)))

    def test_engine_map_images_are_current_and_rows_are_complete(self):
        for rel, svg in engine_map.outputs(self.site):
            self.assertEqual((ROOT / rel).read_text(encoding='utf-8'), svg, rel)
        site = deepcopy(self.site)
        row = next(r for r in site['engine_map']['rows'] if r.get('name') == 'MuJoCo')
        row['cells'] = row['cells'][:-1]
        del row['kind']['ja']
        errors = validate(site, self.works, True)[0]
        self.assertTrue(any('covers 7 columns' in e for e in errors))
        self.assertTrue(any('kind missing ja' in e for e in errors))

    def test_compatibility_targets_must_exist(self):
        site = deepcopy(self.site)
        site['anchor_aliases']['old-link'] = 'missing-entry'
        self.assertTrue(any('compatibility anchor' in e for e in validate(site, self.works, True)[0]))


if __name__ == '__main__':
    unittest.main()
