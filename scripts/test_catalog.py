"""Regression cases from the three-stage migration; no network or publication."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import engine_map
import eval_ladder
import triage
import stage_chart
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

    def test_walkthrough_links_need_a_page_and_three_languages(self):
        guides = self.site['sections']['3.4']['guides']
        self.assertTrue(guides)
        for lang in self.site['languages']:
            text = render(self.site, self.works, lang)
            self.assertIn(f"]({guides[0]['url']})", text.split('## ', 3)[2])  # listed in the contents
        for broken in ({'page': 'stage3/missing/index.html'}, {'page': 'https://example.com/page'},
                       {'url': 'https://example.com/elsewhere/'}, {'note': {'en': 'x'}}):
            with self.subTest(broken=broken):
                site = deepcopy(self.site)
                site['sections']['3.4']['guides'][0].update(broken)
                self.assertTrue(any('guide' in e for e in validate(site, self.works, True)[0]))

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
        site = deepcopy(self.site)
        site['engine_strengths']['rows'][0]['scores'] = '3 1 2 1 2 1 1 3'  # drops the only star in its column
        self.assertTrue(any('exactly one top pick' in e for e in validate(site, self.works, True)[0]))

    def test_eval_ladder_images_are_current_and_levels_are_complete(self):
        for rel, svg in eval_ladder.outputs(self.site):
            self.assertEqual((ROOT / rel).read_text(encoding='utf-8'), svg, rel)
        site = deepcopy(self.site)
        level = site['eval_ladder']['stages'][0]['levels'][0]
        level['works'].append('9999.99999')
        level['pic'] = 'unknown'
        del level['fake']['zh']
        errors = validate(site, self.works, True)[0]
        self.assertTrue(any('work 9999.99999 not found' in e for e in errors))
        self.assertTrue(any('unknown pictogram' in e for e in errors))
        self.assertTrue(any('L0a.fake missing zh' in e for e in errors))

    def test_setup_renders_sim_and_real_groups_and_rejects_bad_names(self):
        rows = deepcopy(self.works)
        work = next(w for w in rows if w['section'].startswith('3') and w['type'] == 'paper')
        work['setup'] = {'engines': ['MuJoCo', 'Blender'], 'sim_robots': ['Franka Panda'],
                         'real_robots': ['UR5e', 'AgileX Piper']}
        self.assertEqual(validate(self.site, rows, True)[0], [])
        zh = render(self.site, rows, 'zh')
        self.assertIn('🖥️ **仿真** MuJoCo + Blender（Franka Panda） · 🦾 **真机** UR5e、AgileX Piper', zh)
        work['setup'] = {'real_robots': ['UR5e']}
        self.assertIn('<br>\n  > 🦾 **Real** UR5e\n', render(self.site, rows, 'en'))
        for bad in ({'engines': []}, {'robots': ['UR5e']}, {'engines': ['Mu*JoCo']}, {'sim_robots': ['UR5e', 'UR5e']}):
            work['setup'] = bad
            self.assertTrue(any('setup' in e for e in validate(self.site, rows, True)[0]), bad)

    def test_contents_subgroups_and_subgroup_links_are_checked(self):
        zh = render(self.site, self.works, 'zh')
        count = sum(1 for w in self.works if (w['section'], w.get('sub')) == ('3.6', 'experiments'))
        self.assertIn(f'    - [科学实验（AI4Science）](#s3-6-experiments) ({count})', zh)
        self.assertIn('<a id="s3-6-experiments"></a>\n\n#### 科学实验（AI4Science）', zh)
        self.assertIn('[ChemAutoAgent](#paper-chemautoagent)', zh.split('#### 物理设计')[0].split('#### 科学实验')[-1])
        site = deepcopy(self.site)
        meta = site['sections']['3.6']
        meta['contents_subs'].append('unknown-sub')
        meta['sub_see_also']['experiments'] += ['9999.99999', '2610.23826']  # missing, and already primary there
        errors = validate(site, self.works, True)[0]
        self.assertTrue(any("contents_subs 'unknown-sub'" in e for e in errors))
        self.assertTrue(any('9999.99999 not found' in e for e in errors))
        self.assertTrue(any('2610.23826 is already listed there' in e for e in errors))

    def test_stage_chart_images_are_current_and_rows_are_complete(self):
        for rel, svg in stage_chart.outputs(self.site):
            self.assertEqual((ROOT / rel).read_text(encoding='utf-8'), svg, rel)
        site = deepcopy(self.site)
        row = site['stage_chart']['sections'][1]['rows'][0]
        row['cells'] = row['cells'][:-1]
        row['id'] = 'missing-entry'
        del site['stage_chart']['columns'][0]['ja']
        errors = validate(site, self.works, True)[0]
        self.assertTrue(any('has 8 cells, expected 9' in e for e in errors))
        self.assertTrue(any('unknown id' in e for e in errors))
        self.assertTrue(any('columns[0] missing ja' in e for e in errors))

    def test_full_stage_chart_rows_match_their_tier(self):
        site = deepcopy(self.site)
        rows = [r for s in site['stage_chart_full']['sections'] for r in s['rows']]
        dycraft = next(r for r in rows if r['name'] == 'DyCraft')
        dycraft['tier'] = 'F'
        rows[-1]['steps'] = rows[-1]['steps'][:-1]
        errors = validate(site, self.works, True)[0]
        self.assertTrue(any('DyCraft is tier F' in e for e in errors))
        self.assertTrue(any('steps must be 11' in e for e in errors))

    def test_compatibility_targets_must_exist(self):
        site = deepcopy(self.site)
        site['anchor_aliases']['old-link'] = 'missing-entry'
        self.assertTrue(any('compatibility anchor' in e for e in validate(site, self.works, True)[0]))

    def test_triage_log_agrees_with_catalog(self):
        log = triage.load(ROOT)
        self.assertIsNotNone(log)
        self.assertEqual(triage.validate(self.works, log), [])

    def test_triage_decisions_cannot_drift_from_catalog(self):
        log = deepcopy(triage.load(ROOT))
        pending = next(c for c in log['candidates'] if c['decision'] == 'pending')
        added = next(c for c in log['candidates'] if c['decision'] == 'added')
        rows = deepcopy(self.works)
        extra = deepcopy(rows[0]); extra['id'] = pending['id']
        rows = [w for w in rows if w['id'] != added['id']] + [extra]
        errors = triage.validate(rows, log)
        self.assertTrue(any('mark it added or updated' in e for e in errors))
        self.assertTrue(any('is not in data/works.yaml' in e for e in errors))
        pending.update(decision='excluded', decided=pending['found'])
        self.assertTrue(any('requires a reason' in e for e in triage.validate(self.works, log)))


if __name__ == '__main__':
    unittest.main()
