"""Promote only the tested five-speech Act III refinement, preserving revision03."""
from pathlib import Path
import hashlib,json,shutil,yaml
from compile_connected_story import ROOT,LAB,compile_bank
from public_lock import verify_public_lock
from validate_playable_evidence import validate

cases=[LAB/'balance-act3-30-04',LAB/'balance-act3-22-04']
metrics=[m for case in cases for m in json.loads((case/'metrics.json').read_text(encoding='utf-8')).values()]
assert len(metrics)==6
assert all(m['correct_final_leader'] and m['final_culprit_score']>=9 and m['e3_culprit_score']>=5
           and not m['early_obvious_culprit'] and not m['early_large_lead'] for m in metrics)
assert sum(m['final_alternatives_five_six']>=3 for m in metrics)>=4,'Ending breadth not consistently improved'
dest=ROOT/'source/connected_release'
old=yaml.safe_load((dest/'all.yaml').read_text(encoding='utf-8'))
baseline={r['id']:r for r in old['characters']}
banks={active:compile_bank(active) for active in ('all','confirmed')}
allowed={'03','05','11','16','23'}
changed=[]
for row in banks['all']['characters']:
    for field,text in row['hearings'].items():
        if text!=baseline[row['id']]['hearings'][field]:
            assert row['id'] in allowed and field=='evidence_innocent',(row['id'],field)
            changed.append(row['id'])
    assert row['coming_clean']==baseline[row['id']]['coming_clean']
assert set(changed)==allowed
for case,active,previous in zip(cases,('all','confirmed'),('balance-dramatic-30-03','balance-dramatic-22-03')):
    manifest=json.loads((case/'private-selection.json').read_text(encoding='utf-8'))
    for relative,expected in manifest['sha256'].items():
        assert hashlib.sha256((case/relative).read_bytes()).hexdigest()==expected,relative
    frozen=yaml.safe_load((case/'frozen-source/compiled-bank.yaml').read_text(encoding='utf-8'))
    assert banks[active]==frozen
    for number in range(1,8):
        filename=f'checkpoint_{number:02}.txt'
        assert (case/filename).read_bytes()==(LAB/previous/filename).read_bytes()
    assert (case/'frozen-source/playable-evidence.yaml').read_bytes()==(dest/'playable-evidence.yaml').read_bytes()
validate();verify_public_lock(ROOT)
archive=LAB/'published-revision03-source'
assert not archive.exists()
shutil.copytree(dest,archive)
before=ROOT/'build/act3-revision04-before';before.mkdir(exist_ok=False)
kit=ROOT/'build/connected-release-kit/The_Last_Acquisition_Complete_Kit'
for p in kit.rglob('*.pdf'):
    target=before/p.relative_to(kit);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
for active in ('all','confirmed'):
    banks[active]['status']='tested_act3_refinement_revision04'
    (dest/(active+'.yaml')).write_text(yaml.safe_dump(banks[active],sort_keys=False,allow_unicode=True),encoding='utf-8')
record={'revision':'act3-five-speech-refinement-2026-10-10','baseline_commit':'fc15ebd',
        'tests':[str(p.relative_to(ROOT)) for p in cases],
        'changed':sorted(i+'/evidence_innocent' for i in allowed),
        'limitations':'Two same-case text worlds, not all murderer worlds or human solve rates. Unchanged first seven inputs permit comparison but fresh-reader variation persists. Physical attribution is circumstantial.',
        'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.iterdir() if p.is_file() and p.name!='manifest.json'}}
(dest/'manifest.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('Tested five-speech revision promoted locally; revision03 sources and PDFs archived.')
