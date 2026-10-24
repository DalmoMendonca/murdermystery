"""Verify every proof route and every actual printed branch, without guessing scores."""
from pathlib import Path
import json,re,sys,yaml,fitz
from exhaustive_balance import sha,write
from public_lock import verify_public_lock
from validate_playable_evidence import validate
from visible_evidence import exhibits
from american_copy import american
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest'/(sys.argv[1] if len(sys.argv)>1 else '2026-10-24-SHARED-PREVIEW-PRINT-SPOILERS')
PARENT=ROOT/'docs/playtest/2026-10-24-CONCEALED-STAKES-SPOILERS/candidate-source'
load=lambda p:yaml.safe_load(p.read_text(encoding='utf-8'))
e=validate(RUN/'candidate-source/playable-evidence.yaml');old=load(PARENT/'playable-evidence.yaml')
assert e['hunt']==old['hunt']
prior={x['id']:x for r in old['releases'] for x in r['exhibits']};now={x['id']:x for r in e['releases'] for x in r['exhibits']}
for ident,x in now.items():
    assert x.get('images')==prior[ident].get('images'),ident
    if ident not in ('initial_samples','service_account'):assert x==prior[ident],ident
    else:
        assert x.get('rows',[])[:len(prior[ident].get('rows',[]))]==prior[ident].get('rows',[])
        assert x.get('paragraphs',[])[:len(prior[ident].get('paragraphs',[]))]==prior[ident].get('paragraphs',[])
assert e['releases'][-1]['route_checks']==old['releases'][-1]['route_checks']
active=set(load(ROOT/'source/testing/active-cast.yaml')['active_character_ids'])
available={x['id'] for r in e['releases'] for x in exhibits(e,r,True)}
assert all(set(e['releases'][-1]['route_checks'][i])<=available for i in active)
checks=0
kitpath=RUN/'candidate-kit-path.txt'
def norm(t):return re.sub(r'\s+',' ',american(t)).strip()
for edition,count in [('all',30),('confirmed',22)]:
    b=load(RUN/'candidate-source'/(edition+'.yaml'));p=load(PARENT/(edition+'.yaml'));oldrows={c['id']:c for c in p['characters']}
    assert len(b['characters'])==count
    if count==22:assert {c['id'] for c in b['characters']}==active
    for c in b['characters']:
        for k,text in c['hearings'].items():
            if k.endswith('_murderer'):assert text==oldrows[c['id']]['hearings'][k]
        assert c['coming_clean']==oldrows[c['id']]['coming_clean']
    for rd in b['question_rounds']:
        targets=[n for g in rd['groups'] for n in g['targets']];assert len(targets)==count and set(targets)=={c['name'] for c in b['characters']}
    if kitpath.exists():
        kit=Path(kitpath.read_text().strip());pdf=kit/'PRINT_WITHOUT_READING'/('03_Secret_Player_Packets_PRINT_DO_NOT_READ.pdf' if count==30 else '03A_Confirmed_22_Guest_Packets_PRINT_DO_NOT_READ.pdf')
        with fitz.open(pdf) as doc:
            assert len(doc)==count*12
            for index,c in enumerate(b['characters']):
                for key,page in [('motive',6),('where',8),('evidence',10)]:
                    text=norm(doc[index*12+page-1].get_text())
                    for branch in ('innocent','murderer'):
                        assert norm(c['hearings'][key+'_'+branch]) in text,(c['name'],key,branch);checks+=1
                text=norm(doc[index*12+11].get_text())
                for branch in ('innocent','murderer'):
                    assert norm(c['coming_clean'][branch]) in text,(c['name'],'finale',branch);checks+=1
                assert norm(b['player_briefing']) in norm(doc[index*12+2].get_text())
manifest=json.loads((RUN/'private-manifest.json').read_text())
for t in manifest['trials']:
    for name,h in t['inputs'].items():assert sha(RUN/'blind'/t['trial']/name)==h
for name,h in manifest['source_sha256'].items():assert sha(RUN/'frozen-source'/name)==h
verify_public_lock(ROOT)
write(RUN/'continuity-verification.json',{'all30_guilty_accounts_and_finales_identical_to_parent':True,'all_physical_observations_and_recorded_comparisons_preserved':True,'every_current22_proof_dependency_survives_attendance_filter':True,'hunt_and_late_personal_proof_unchanged_from_parent':True,'added_context':'Shared invitation-only preview and staff source access beforeActII; service entrance to donor office.','current22_names_per_round_exact':True,'actual_printed_branch_checks':checks,'sent_assets_locked':True,'frozen_inputs_valid':True,'limits':'Mechanical fidelity and proof checks, not balance scores or human solve-rate certification.'})
print('PASS:30 guilty routes unchanged; current22 proof dependencies; public lock; printed branches:',checks)
