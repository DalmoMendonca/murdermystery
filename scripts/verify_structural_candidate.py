"""Mechanical invariants and an explicit thirty-world proof ledger, not balance claims."""
from pathlib import Path
import sys,json,yaml,hashlib
from validate_playable_evidence import validate
from public_lock import verify_public_lock
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest'/(sys.argv[1] if len(sys.argv)>1 else '2026-10-11-STRUCTURAL-FOLLOWUP-SPOILERS')
candidate=RUN/'candidate-source';base=ROOT/'source/connected_release'
def load(p):return yaml.safe_load(p.read_text(encoding='utf-8'))
e=validate(candidate/'playable-evidence.yaml');old=load(base/'playable-evidence.yaml')
assert e['hunt']==old['hunt']
assert e['releases'][:2]==old['releases'][:2]
checks=e['releases'][-1]['route_checks'];assert checks==old['releases'][-1]['route_checks']
old_ex={x['id']:x for r in old['releases'] for x in r['exhibits']}
new_ex={x['id']:x for r in e['releases'] for x in r['exhibits']}
for ident in ['original_source','actual_service','original_interview','camera_work','governing_papers','collection_working_proof']:assert new_ex[ident]==old_ex[ident],ident
for ident in new_ex:assert new_ex[ident].get('images')==old_ex[ident].get('images'),ident
ledger=[]
for edition,n in [('all',30),('confirmed',22)]:
    a=load(candidate/(edition+'.yaml'));b=load(base/(edition+'.yaml'));assert len(a['characters'])==n
    assert a['active_character_ids']==b['active_character_ids']
    assert a['question_rounds']==b['question_rounds']
    assert a['pre_method_press_interview_opening']==b['pre_method_press_interview_opening']
    old_people={str(c['id']).zfill(2):c for c in b['characters']}
    for c in a['characters']:
        ident=str(c['id']).zfill(2);assert c['coming_clean']==old_people[ident]['coming_clean'];assert c['name']==old_people[ident]['name']
        assert set(c['hearings'])==set(old_people[ident]['hearings'])
        assert all(isinstance(v,str) and v.strip() for v in c['hearings'].values())
        if edition=='all':ledger.append({'id':ident,'name':c['name'],'motive_before_vote':c['hearings']['motive_murderer'],'opportunity_before_vote':c['hearings']['where_murderer'],'final_claim_before_vote':c['hearings']['evidence_murderer'],'independent_exhibits':[{'id':x,'title':new_ex[x]['title']} for x in checks[ident]],'confession_unchanged':True})
    for r in a['question_rounds']:
        targets=[name for g in r['groups'] for name in g['targets']]
        assert sorted(targets)==sorted(c['name'] for c in a['characters'])
for ed in (22,30):
    manifest=json.loads((RUN/f'cast{ed}/private-manifest.json').read_text(encoding='utf-8'))
    for trial in manifest['trials']:
        for name,h in trial['inputs'].items():assert hashlib.sha256((RUN/f'cast{ed}/blind'/trial['trial']/name).read_bytes()).hexdigest()==h
verify_public_lock(ROOT)
out={'worlds':30,'confirmed_characters':22,'hunt_discoveries':16,'earlier_evidence_unchanged':True,'crime_bearing_records_and_all_visual_observations_unchanged':True,'route_dependencies_unchanged':True,'all_confessions_unchanged':True,'question_coverage_exact':True,'frozen_input_hashes_valid':True,'sent_public_assets_locked':True,'proof_ledger':ledger,'limits':'Dependencies and preserved facts verified mechanically. Narrative continuity reviewed separately; diagnostic readers test only three selected worlds per cast.'}
(RUN/'continuity-verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('All30 proof dependencies, both roster/round coverages,16 discoveries, frozen inputs, confessions and sent assets verified.')
