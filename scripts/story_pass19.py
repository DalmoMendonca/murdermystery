"""Compile reviewed Round19 private edits without changing released assets."""
from pathlib import Path
import copy
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/story-pass-19-SPOILERS'
FIELDS = ('motive_innocent', 'motive_murderer', 'opportunity_innocent',
          'opportunity_murderer', 'method_innocent', 'method_murderer',
          'coming_clean_innocent', 'coming_clean_murderer')

def main():
    assert not (ROOT / 'build/story-pass19/private-manifest.json').exists(), 'Frozen trial cannot be rewritten'
    previous = ROOT / 'docs/story-pass-18-SPOILERS'
    data = copy.deepcopy(yaml.safe_load((previous / 'dialogue.yaml').read_text(encoding='utf-8')))
    by = {r['id']: r for r in data['characters']}
    chars = json.loads((ROOT / 'source/characters.json').read_text(encoding='utf-8'))
    names = {c['id']: c['name'] for c in chars}
    for filename in ('motive-edits.yaml', 'innocent-edits.yaml', 'guilty-edits.yaml'):
        edits = yaml.safe_load((OUT / filename).read_text(encoding='utf-8'))
        assert edits['status'] == 'complete', f'{filename}: incomplete authoring'
        rows = edits['characters']
        assert len(rows) == 30 and {r['id'] for r in rows} == set(names), filename
        for r in rows:
            assert r['name'] == names[r['id']], filename + ': name mismatch'
            for field in FIELDS:
                if field in r:
                    by[r['id']][field] = r[field]
    continuity = yaml.safe_load((OUT / 'continuity-edits.yaml').read_text(encoding='utf-8'))
    assert continuity['status'] == 'complete', 'Continuity authoring incomplete'
    for row in continuity['characters']:
        assert row['name'] == names[row['id']]
        for key in FIELDS:
            if key in row:
                by[row['id']][key] = row[key]
    compiled = copy.deepcopy(yaml.safe_load((previous / 'investigation_copy.yaml').read_text(encoding='utf-8')))
    records = {r['id']: r for r in compiled['characters']}
    counts = []
    for ident, row in by.items():
        for field in FIELDS:
            assert isinstance(row.get(field), str) and row[field].strip(), ident + ': ' + field
            row[field] = row[field].replace('solicitors', 'attorneys').replace('solicitor', 'attorney')
        record = records[ident]
        record['hearings'] = {key: row[source] for key, source in (
            ('motive_innocent', 'motive_innocent'), ('motive_murderer', 'motive_murderer'),
            ('where_innocent', 'opportunity_innocent'), ('where_murderer', 'opportunity_murderer'),
            ('evidence_innocent', 'method_innocent'), ('evidence_murderer', 'method_murderer'))}
        record['coming_clean'] = {'innocent': row['coming_clean_innocent'], 'murderer': row['coming_clean_murderer']}
        record['authoring_notes'] = {'status': 'Round19 candidate; briefing inherited and requires separate audit before kit integration'}
        counts.append({'id': ident, 'name': names[ident], 'words': {f: len(row[f].split()) for f in FIELDS}})
    compiled['status'] = 'Round19 private candidate; blind acceptance and full packet integration unproven'
    compiled['characters'] = [records[c['id']] for c in chars]
    data = {'schema_version': 1, 'status': compiled['status'], 'characters': [by[c['id']] for c in chars]}
    for filename, content in (('dialogue.yaml', data), ('investigation_copy.yaml', compiled)):
        (OUT / filename).write_text(yaml.safe_dump(content, allow_unicode=True, sort_keys=False, width=100), encoding='utf-8')
    (OUT / 'word-counts.json').write_text(json.dumps(counts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Compiled thirty reviewed private characters. Briefings remain provisional; public assets untouched.')

if __name__ == '__main__':
    main()
