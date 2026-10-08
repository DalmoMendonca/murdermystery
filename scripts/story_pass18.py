"""Merge independently authored private dialogue into an isolated trial candidate.

Never touches the canonical kit or already-sent assets. Requires both complete
authoring files, so a partial agent output cannot become a tested story.
"""
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/story-pass-18-SPOILERS'
FIELDS = ('motive_innocent', 'motive_murderer', 'opportunity_innocent',
          'opportunity_murderer', 'method_innocent', 'method_murderer',
          'coming_clean_innocent', 'coming_clean_murderer')


def main():
    assert not (ROOT / 'build/story-pass18/private-manifest.json').exists(), 'Frozen trial must never be rewritten'
    rows = []
    for name in ('core-dialogue.yaml', 'other-dialogue.yaml'):
        data = yaml.safe_load((OUT / name).read_text(encoding='utf-8'))
        rows += data['characters']
    by = {str(r['id']).zfill(2): r for r in rows}
    assert len(rows) == 30 and set(by) == {f'{i:02}' for i in range(1, 31)}, 'Exactly thirty complete roles required'
    for ident, row in by.items():
        for key in FIELDS:
            assert isinstance(row.get(key), str) and row[key].strip(), f'{ident}: missing {key}'
    chars = json.loads((ROOT / 'source/characters.json').read_text(encoding='utf-8'))
    base = yaml.safe_load((ROOT / 'docs/story-pass-17-SPOILERS/investigation_copy.yaml').read_text(encoding='utf-8'))
    records = {r['id']: r for r in base['characters']}
    word_report = []
    for c in chars:
        ident = c['id']; authored = by[ident]; record = records[ident]
        record['hearings'] = {
            'motive_innocent': authored['motive_innocent'],
            'motive_murderer': authored['motive_murderer'],
            'where_innocent': authored['opportunity_innocent'],
            'where_murderer': authored['opportunity_murderer'],
            'evidence_innocent': authored['method_innocent'],
            'evidence_murderer': authored['method_murderer'],
        }
        record['coming_clean'] = {'innocent': authored['coming_clean_innocent'],
                                  'murderer': authored['coming_clean_murderer']}
        # Private setup is provisional until its separate continuity audit.
        # Never silently make the innocent defense everyone's shared history.
        record['authoring_notes'] = {key: value for key, value in authored.items() if key not in FIELDS and key != 'id'}
        word_report.append({'id': ident, 'name': c['name'],
                            'words': {key: len(authored[key].split()) for key in FIELDS}})
    base['status'] = 'Round18 independently authored candidate; continuity and blind acceptance unproven'
    base['characters'] = [records[c['id']] for c in chars]
    (OUT / 'investigation_copy.yaml').write_text(yaml.safe_dump(base, allow_unicode=True, sort_keys=False, width=100), encoding='utf-8')
    (OUT / 'dialogue.yaml').write_text(yaml.safe_dump({'schema_version': 1, 'characters': [dict(by[c['id']], id=c['id']) for c in chars]}, allow_unicode=True, sort_keys=False, width=100), encoding='utf-8')
    (OUT / 'word-counts.json').write_text(json.dumps(word_report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Merged thirty complete private records. Requires human-level continuity review before freezing; public assets untouched.')


if __name__ == '__main__':
    main()
