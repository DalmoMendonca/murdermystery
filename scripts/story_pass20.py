"""Compile a limited physical-story prototype, never the production kit."""
from pathlib import Path
import copy
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/story-pass-20-SPOILERS'
OLD = ROOT / 'docs/story-pass-19-SPOILERS'
MAP = {'motive_innocent': 'motive_innocent', 'motive_murderer': 'motive_murderer',
       'opportunity_innocent': 'where_innocent', 'opportunity_murderer': 'where_murderer',
       'method_innocent': 'evidence_innocent', 'method_murderer': 'evidence_murderer'}

def main():
    assert not (ROOT / 'build/story-pass20/private-manifest.json').exists(), 'Frozen trial cannot be rewritten'
    data = copy.deepcopy(yaml.safe_load((OLD / 'investigation_copy.yaml').read_text(encoding='utf-8')))
    rows = {r['id']: r for r in data['characters']}
    for filename, ids in [('prototype-dialogue.yaml', {'21', '29', '15'}), ('replica-workflow.yaml', {'05', '11', '24'})]:
        edits = yaml.safe_load((OUT / filename).read_text(encoding='utf-8'))
        assert edits['status'].startswith('complete'), filename + ': incomplete'
        assert {r['id'] for r in edits['characters']} == ids, filename + ': coverage mismatch'
        for r in edits['characters']:
            required = ('opportunity_murderer', 'method_murderer', 'coming_clean_murderer') if filename == 'prototype-dialogue.yaml' else ('opportunity_innocent', 'method_innocent')
            assert all(isinstance(r.get(k), str) and r[k].strip() for k in required), filename + ': missing actual speech'
            for source, target in MAP.items():
                if source in r: rows[r['id']]['hearings'][target] = r[source]
            for branch in ('innocent', 'murderer'):
                field = 'coming_clean_' + branch
                if field in r: rows[r['id']]['coming_clean'][branch] = r[field]
    data['status'] = 'Round20 prototype: only Ella/Justin/Elon guilty routes authored; no all-culprit validation'
    data['prototype_guilty_ids'] = ['21', '29', '15']
    evidence = copy.deepcopy(yaml.safe_load((OLD / 'evidence_design.yaml').read_text(encoding='utf-8')))
    reports = {r['id']: r for r in evidence['reports']}
    reports['F3']['title'] = 'A bottle behind reception'
    reports['F3']['text'] = "Jordan West, collections assistant: A dark-blue bottle with visible neck damage was recovered on the staff-returns shelf behind the reception sideboard during the search after Grant's death. Object identification and comparison are pending. This waist-height work shelf stands against a plain wall; gallery and event items await staff collection there. Casey Hart, service manager: Grant's new museum-star glass stood on the reception sideboard from 6:32 to 6:44 while I settled the kitchen's extra-course authorization. Programs, favors and correspondence also used reception. The preparation cabinet and its secondary case were forced at 6:12; the historical original was missing then."
    reports['F3']['rows'][0] = ['Recovered object', 'Dark-blue bottle on staff-returns shelf; identification pending']
    reports['F3']['photo'] = 'returns_shelf20_REQUIRED'
    reports['F4']['title'] = 'The original and its display copy'
    reports['F4']['text'] = "The bottle recovered from the staff-returns shelf is the historical original. It has a closed base and a fresh gap in its neck. The blue fragment recovered in folded favor paper joins that irregular curved neck edge. The receiving record described the original neck as intact. Its display copy has a similar dark-blue body but an open bottom: it cannot hold liquid. The recovered miniature fragrance bottle has an intact neck and body. Service photographs show the donor glass empty when placed at 6:32 and empty when collected at 6:44. Casey filled it with shared punch on the tray at 6:46 and reports keeping it there until the toast. The photographs show moments, not continuous coverage."
    reports['F4']['rows'] = [['Recovered historical original', 'Dark-blue body; closed base; fresh neck gap'],
                           ['Fragment in favor paper', 'Joins the original neck gap'],
                           ['Display copy', 'Similar dark-blue body; open bottom'],
                           ['Recovered miniature', 'Neck and body intact']]
    reports['F4']['photo'] = 'original_replica20_REQUIRED'
    for clue in evidence['discoveries']:
        if clue['number'] == 13:
            clue['paragraphs'].append('Empty handling copy supplied for the planned hands-on display. The historical original is not approved for public handling.')
        if clue['number'] == 14:
            clue['paragraphs'][0] = '5:45: Original secured in locked preparation cabinet and secondary case. Receiving photograph shows the closed case. Condition entry: neck intact. Separate empty display copy supplied for gallery installation.'
    # F2 does not reveal the copy's construction or claim continuous custody.
    reports['F2']['text'] = reports['F2']['text'].replace('Only an empty replica went to the galleries.', 'A separate empty display copy was supplied for gallery installation.')
    for r in rows.values():
        for field, text in r['hearings'].items():
            r['hearings'][field] = text.replace('clear replica', 'display copy').replace('clear display replica', 'display copy')
    for filename, content in [('investigation_copy.yaml', data), ('evidence_design.yaml', evidence)]:
        (OUT / filename).write_text(yaml.safe_dump(content, allow_unicode=True, sort_keys=False, width=100), encoding='utf-8')
    print('Three-world physical prototype compiled. Other guilty variants unvalidated; public assets untouched.')

if __name__ == '__main__': main()
