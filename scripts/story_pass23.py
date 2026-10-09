"""Compile an unfrozen scene-and-material-account prototype; public assets untouched."""
from pathlib import Path
import copy
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'docs/story-pass-22-SPOILERS'
OUT = ROOT / 'docs/story-pass-23-SPOILERS'

def main():
    assert not (ROOT / 'build/story-pass23/private-manifest.json').exists(), 'Frozen trial cannot be rewritten'
    story = copy.deepcopy(yaml.safe_load((OLD / 'investigation_copy.yaml').read_text(encoding='utf-8')))
    by = {r['id']: r for r in story['characters']}
    fieldmap = {'opportunity_innocent': 'where_innocent', 'opportunity_murderer': 'where_murderer',
                'method_innocent': 'evidence_innocent', 'method_murderer': 'evidence_murderer'}
    changes = []
    for filename in ('scene-edits.yaml', 'prototype-edits.yaml'):
        edits = yaml.safe_load((OUT / filename).read_text(encoding='utf-8'))
        for edit in edits['characters']:
            row = by[edit['id']]
            for field, target in fieldmap.items():
                if field not in edit:
                    continue
                text = edit[field]
                assert len(text.split()) <= 100, (edit['id'], field, len(text.split()))
                row['hearings'][target] = text
                changes.append({'id': edit['id'], 'field': field, 'words': len(text.split())})
            if 'coming_clean_murderer' in edit:
                row['coming_clean']['murderer'] = edit['coming_clean_murderer']
            if 'coming_clean_innocent' in edit:
                row['coming_clean']['innocent'] = edit['coming_clean_innocent']
    # A single originally selected world is the initial feasibility experiment.
    # Inherited routes are deliberately NOT eligible for selection or production.
    story['prototype_guilty_ids'] = ['29']
    story['status'] = 'Round23 Justin-only structural prototype; other29 guilty routes ineligible'
    evidence = copy.deepcopy(yaml.safe_load((OLD / 'evidence_design.yaml').read_text(encoding='utf-8')))
    reports = {r['id']: r for r in evidence['reports']}
    reports['F3']['title'] = 'Returns and interrupted service'
    reports['F3']['text'] = (
        "Jordan West: During clearing after the death, I found the damaged dark-blue bottle among abandoned packing on the staff-returns shelf. "
        "Nobody handed it to me. I also retained the reception waste: a miniature fragrance bottle, folded papers and broken glass. Comparisons are pending. "
        "Casey Hart: I placed Grant's new star glass at 6:32 and collected it at 6:44. "
        "The kitchen argument left reception without its usual cover. I filled it from shared punch on my tray at 6:46 and kept the tray through the toast. "
        "The photographs show separate moments, not everything between them.")
    records = yaml.safe_load((OUT / 'scene-records.yaml').read_text(encoding='utf-8'))['observations']
    assert len({r['id'] for r in records}) == len(records)
    reports['F3']['rows'] = [[r['display_label'], r['display_text']] for r in records]
    reports['F3']['layout'] = 'scene_records23_REQUIRED'
    reports['F3']['photo'] = 'returns_scene23_REQUIRED'
    reports['F4']['text'] = reports['F4']['text'].replace('folded favor paper', 'folded reception paper')
    for record in reports['F4']['rows']:
        record[0] = record[0].replace('favor paper', 'reception paper')
    reports['F4']['text'] += (
        " Examination of the collected glass finds dark-blue bottle-neck pieces and flat clear screen-protector pieces. "
        "Every examined dark-blue neck piece joins the historical original's fresh gap. "
        "Their curvature is too broad for any of the supplied miniature favors. The flat clear pieces do not join a bottle. "
        "The papers and pieces were collected as mixed reception waste; their recovery does not identify their last holder.")
    reports['F4']['rows'].append(['Collected glass', 'Dark-blue neck pieces join original; too broad for miniature necks. Flat clear protector pieces separate.'])
    # Extend the early receiving plant; physical examination still comes in Method.
    receiving = next(d for d in evidence['discoveries'] if d['number'] == 14)
    receiving['paragraphs'].append(
        "Collections refused Grant's request for the original in private photographs. Installation tools remained on the adjoining bench. "
        "After the alarm, collections asked that damaged packing and reception returns be held for examination.")
    (OUT / 'investigation_copy.yaml').write_text(yaml.safe_dump(story, allow_unicode=True, sort_keys=False, width=100), encoding='utf-8')
    (OUT / 'evidence_design.yaml').write_text(yaml.safe_dump(evidence, allow_unicode=True, sort_keys=False, width=100), encoding='utf-8')
    (OUT / 'change-audit.json').write_text(json.dumps({'speeches': changes, 'eligible_guilty_ids': ['29'],
        'shared_evidence_selection_dependent': False, 'public_assets_modified': False,
        'scope': 'One originally selected 22-person world; fresh repeat; not all-culprit validation'}, indent=2) + '\n', encoding='utf-8')
    print(f'Compiled {len(changes)} speeches; only Justin prototype eligible. Not frozen or accepted.')

if __name__ == '__main__':
    main()
