"""Check all-route proof preservation and the actual frozen attendance edition."""
from pathlib import Path
import json,yaml,sys
from exhaustive_balance import sha,write
from public_lock import verify_public_lock
from validate_playable_evidence import validate
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest'/(sys.argv[1] if len(sys.argv)>1 else '2026-10-24-PRINT-FINAL-SPOILERS')
load=lambda p:yaml.safe_load(p.read_text(encoding='utf-8'))
old=ROOT/'source/connected_release';new=RUN/'candidate-source'
e=validate(new/'playable-evidence.yaml');before=load(old/'playable-evidence.yaml')
prior={x['id']:x for r in before['releases'] for x in r['exhibits']}
current={x['id']:x for r in e['releases'] for x in r['exhibits']}
assert e['hunt'][:12]==before['hunt'][:12] and e['hunt'][13:]==before['hunt'][13:]
assert e['hunt'][12]['rows'][:-1]==before['hunt'][12]['rows']
assert e['releases'][:2]==before['releases'][:2]
assert set(prior)==set(current)
for ident in current:
    assert current[ident].get('images')==prior[ident].get('images'),ident
    assert current[ident].get('paragraphs')==prior[ident].get('paragraphs'),ident
for ident in ['original_source','actual_service','original_interview','camera_work','production_originals','visitor_route','governing_papers','collection_working_proof']:
    assert current[ident]==prior[ident],ident
assert e['releases'][-1]['route_checks']==before['releases'][-1]['route_checks']
profile=load(ROOT/'source/testing/active-cast.yaml');changes=[]
for edition,count in [('all',30),('confirmed',22)]:
    bank=load(new/(edition+'.yaml'));baseline=load(old/(edition+'.yaml'))
    rows={c['id']:c for c in bank['characters']};orig={c['id']:c for c in baseline['characters']}
    assert len(rows)==count
    if count==22:assert set(rows)==set(profile['active_character_ids'])
    for rd in bank['question_rounds']:
        targets=[n for g in rd['groups'] for n in g['targets']]
        assert len(targets)==count and set(targets)=={c['name'] for c in rows.values()}
    for ident,c in rows.items():
        assert len(c['hearings'])==6 and len(c['coming_clean'])==2
        for field,value in c['hearings'].items():
            if field.endswith('_murderer') and value!=orig[ident]['hearings'][field]:
                changes.append({'edition':edition,'id':ident,'field':field})
                assert (ident,field) in [('24','where_murderer'),('27','evidence_murderer'),('09','where_murderer')]
    assert 'before the preview' in rows['04']['hearings']['evidence_murderer']
    assert bank['pre_method_press_interview_opening']==baseline['pre_method_press_interview_opening']
manifest=json.loads((RUN/'private-manifest.json').read_text())
assert len(manifest['trials'])==22 and len({t['murderer_id'] for t in manifest['trials']})==22
for t in manifest['trials']:
    for name,h in t['inputs'].items():assert sha(RUN/'blind'/t['trial']/name)==h
for name,h in manifest['source_sha256'].items():assert sha(RUN/'frozen-source'/name)==h
verify_public_lock(ROOT)
write(RUN/'continuity-verification.json',{'all30_proof_dependencies_preserved':True,'current22_targets_exact':True,'all22_unique_worlds_frozen':True,'every_physical_comparison_and_recording_preserved':True,'Monet_deliberate_early_lie_preserved':True,'sent_assets_locked':True,'guilty_statement_changes':changes,'limits':'Dependency and source fidelity checks, not independent solve or balance certification. Suspicious innocent access does not establish physical elimination.'})
print('PASS: all30 proof dependencies, current22 coverage, frozen inputs and public asset lock.')
