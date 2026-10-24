"""Check proof-bearing facts, cast coverage, immutable inputs and sent-asset lock."""
from pathlib import Path
import json,yaml
from exhaustive_balance import sha,write
from validate_playable_evidence import validate
from public_lock import verify_public_lock
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest/2026-10-24-DEADLINE-FINISH-SPOILERS'
source=RUN/'candidate-source'
load=lambda p:yaml.safe_load(p.read_text(encoding='utf-8'))
e=validate(source/'playable-evidence.yaml');old=load(ROOT/'source/connected_release/playable-evidence.yaml')
assert e['hunt']==old['hunt'] and e['releases'][:2]==old['releases'][:2]
prior={x['id']:x for r in old['releases'] for x in r['exhibits']}
current={x['id']:x for r in e['releases'] for x in r['exhibits']}
assert set(current)==set(prior)
assert e['releases'][-1]['route_checks']==old['releases'][-1]['route_checks']
for ident in current:
    assert current[ident].get('images')==prior[ident].get('images'),ident
    assert current[ident].get('paragraphs')==prior[ident].get('paragraphs'),ident
    assert all(row in prior[ident].get('rows',[]) for row in current[ident].get('rows',[])),ident
for ident in ['original_source','actual_service','original_interview','camera_work','production_originals','visitor_route','governing_papers','collection_working_proof']:
    assert current[ident]==prior[ident],ident
profile=load(ROOT/'source/testing/active-cast.yaml');ledger=[]
for edition,count in [('all',30),('confirmed',22)]:
    bank=load(source/(edition+'.yaml'));assert len(bank['characters'])==count
    ids={c['id'] for c in bank['characters']}
    if count==22:assert ids==set(profile['active_character_ids'])
    for phase in bank['question_rounds']:
        targets=[n for g in phase['groups'] for n in g['targets']]
        assert len(targets)==count and set(targets)=={c['name'] for c in bank['characters']}
    for c in bank['characters']:
        assert set(c['hearings'])=={'motive_'+b for b in ['innocent','murderer']}|{'where_'+b for b in ['innocent','murderer']}|{'evidence_'+b for b in ['innocent','murderer']}
        if count==30:ledger.append({'id':c['id'],'name':c['name'],'murderer_method_claim':c['hearings']['evidence_murderer'],'independent_exhibits':e['releases'][-1]['route_checks'][c['id']]})
manifest=json.loads((RUN/'private-manifest.json').read_text(encoding='utf-8'))
for t in manifest['trials']:
    for name,h in t['inputs'].items():assert sha(RUN/'blind'/t['trial']/name)==h
for name,h in manifest['source_sha256'].items():assert sha(RUN/'frozen-source'/name)==h
verify_public_lock(ROOT)
write(RUN/'continuity-verification.json',{'adult_cast':22,'all_cast':30,'question_coverage_exact':True,'hunt_and_first_two_releases_unchanged':True,'all_physical_observations_and_proof_dependencies_unchanged':True,'sent_assets_locked':True,'frozen_inputs_valid':True,'thirty_world_proof_ledger':ledger,'limits':'Mechanical dependencies and factual comparisons, not thirty independent balance tests. New ordinary-access scenes and personal wrongdoing reviewed for continuity separately.'})
print('PASS: 30 proof routes; 22 attending targets per round; unchanged physical clues; immutable test inputs; sent-asset lock.')
