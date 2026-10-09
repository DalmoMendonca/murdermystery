"""Compile an unfrozen private scene experiment; never modify public assets."""
from pathlib import Path
import copy
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/story-pass-21-SPOILERS'
OLD = ROOT / 'docs/story-pass-20-SPOILERS'
MAP = {'motive_innocent': 'motive_innocent',
       'opportunity_innocent': 'where_innocent',
       'method_innocent': 'evidence_innocent'}

def main():
    assert not (ROOT / 'build/story-pass21/private-manifest.json').exists(), 'Cannot rewrite frozen trial'
    data = copy.deepcopy(yaml.safe_load((OLD / 'investigation_copy.yaml').read_text(encoding='utf-8')))
    rows = {r['id']: r for r in data['characters']}
    counts = []
    coverage = set()
    for filename in ('scene-edits.yaml', 'method-edits.yaml', 'ending-edits.yaml'):
        edits = yaml.safe_load((OUT / filename).read_text(encoding='utf-8'))
        assert len({r['id'] for r in edits['characters']}) == len(edits['characters'])
        for edit in edits['characters']:
            assert edit['id'] in rows
            if 'coming_clean_innocent' in edit:
                rows[edit['id']]['coming_clean']['innocent'] = edit['coming_clean_innocent']
            for field, target in MAP.items():
                if field not in edit:
                    continue
                text = edit[field]
                assert isinstance(text, str) and text.strip()
                words = len(text.split())
                assert words <= 100, (edit['id'], field, words)
                rows[edit['id']]['hearings'][target] = text
                counts.append({'id': edit['id'], 'field': field, 'words': words})
                if field == 'opportunity_innocent':
                    coverage.add(edit['id'])
    assert coverage == set(rows), 'All thirty innocent Opportunity scenes required'
    data['status'] = 'Round21 limited three-world transcript candidate; production and all30 branch audits pending'
    (OUT / 'investigation_copy.yaml').write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100), encoding='utf-8')
    evidence = yaml.safe_load((OLD / 'evidence_design.yaml').read_text(encoding='utf-8'))
    (OUT / 'evidence_design.yaml').write_text(yaml.safe_dump(evidence, allow_unicode=True, sort_keys=False, width=100), encoding='utf-8')
    (OUT / 'word-counts.json').write_text(json.dumps(counts, indent=2) + '\n', encoding='utf-8')
    print(f'Compiled {len(counts)} private speeches; all 30 innocent Opportunity scenes. No tests frozen.')

if __name__ == '__main__':
    main()
