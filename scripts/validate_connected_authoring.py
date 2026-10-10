"""Validate authoring coverage/references and immutable sent assets, not mystery balance."""
from pathlib import Path
import hashlib
import json
import yaml
from compile_connected_story import compile_bank

ROOT=Path(__file__).resolve().parents[1]
LAB=ROOT/'docs/connected-story-01-SPOILERS'
full=compile_bank('all')
confirmed=compile_bank('confirmed')
public=yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))
ids=[str(r['id']).zfill(2) for r in public['characters']]
authored=[str(r['id']).zfill(2) for r in full['characters']]
for omitted in ids:
    compile_bank(','.join(i for i in ids if i!=omitted))
for ident in authored:
    compile_bank(ident)
for selected in ('12','27','12,27','01'):
    bank=compile_bank(selected)
    opening='\n'.join(bank['pre_method_press_interview_opening'])
    assert ('ROBIN:' in opening)==('27' in selected)
    assert ('PAIGE:' in opening)==('12' in selected)
    assert bool(opening)==bool(set(selected.split(',')) & {'12','27'})
lock=json.loads((ROOT/'source/public_assets_lock.json').read_text(encoding='utf-8'))
for relative,expected in lock['files'].items():
    assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==expected,relative
prefix='thirty-role' if len(authored)==30 else 'twenty-role'
for filename,bank in [(prefix+'-bank.yaml',full),('confirmed-authoring-bank.yaml',confirmed)]:
    (LAB/filename).write_text(yaml.safe_dump(bank,sort_keys=False,allow_unicode=True,width=110),encoding='utf-8')
record=dict(authored_complete_routes=len(authored),
            act_readings=sum(len(r['hearings']) for r in full['characters']),
            ending_readings=sum(len(r['coming_clean']) for r in full['characters']),
            master_routes_unwritten=full['unwritten_active_ids'],
            confirmed_routes_unwritten=confirmed['unwritten_active_ids'],
            attendance_checks=dict(single_omission_casts=len(ids),single_authored_role_casts=len(authored),
                                   press_recording_combinations=4,
                                   scope='Identity, explicit absent-name substitutions, named question coverage and recording references; not deductive fairness, layout or balance.'),
            sent_asset_files_matching=len(lock['files']),
            named_question_coverage='Every selected character exactly once per round, including all omission/single-role variants.',
            numerical_trial='Published-baseline revision03 same-case checks: all30 Anne, RSVP22 Al. Six correct final9s; E3 7/6/7 and6/6/7; midpoint above5 11/7/11 and9/11/7, four of six meet threshold as before. Final alternatives5-6 4/0/2 and0/3/0, thinner RSVP ending suspicion remains a limitation. Softer Al speech diagnostic22-04 not promoted. See PUBLISHED_BASELINE_REVISION03_RESULTS.md. Not all-world or human acceptance.')
(LAB/(prefix+'-validation.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
files=['five-role-bank.yaml','production-family-scenes.yaml','collection-scenes.yaml','market-scenes.yaml',
       'attendance-edits.yaml','evidence-contracts.yaml','evidence-stage-map.yaml','story-ledger.yaml',
       'reception-events.yaml','late-case-arguments.yaml','remaining-scenes.yaml','question-rounds.yaml',
       'motive-dialogue.yaml','stage-dialogue.yaml','dramatic-dialogue-01.yaml',
       'dramatic-dialogue-02.yaml','dramatic-dialogue-03.yaml','voice-story-bible.yaml',
       'dramatic-fact-contracts.yaml','playable-evidence.yaml',
       prefix+'-bank.yaml','confirmed-authoring-bank.yaml']
hashes={f:hashlib.sha256((LAB/f).read_bytes()).hexdigest() for f in files}
(LAB/'current-authoring-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,indent=2))
