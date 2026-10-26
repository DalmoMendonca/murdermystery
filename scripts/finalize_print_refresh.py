"""Package a visually reviewed print run and stage its existing preview upload."""
from pathlib import Path
import hashlib,json,shutil,sys,zipfile
import yaml
import build as b

run=b.ROOT/'docs/playtest'/sys.argv[1]
kit=Path((run/'candidate-kit-path.txt').read_text().strip())
review=json.loads((run/'full-kit-review/report.json').read_text())
assert review['visual_review_complete'] and not review['issues']
packet=json.loads((run/'packet-verification.json').read_text())
facts=json.loads((run/'fact-verification.json').read_text())
import fitz
with fitz.open(kit/'OPEN_FREELY/05_Staged_Evidence_CONFIRMED_22.pdf') as evidence_pdf:
    actual_counts=[sum(p.get_text().startswith(act) for p in evidence_pdf) for act in ['ACT I: MOTIVE','ACT II: OPPORTUNITY','ACT III: METHOD']]
assert packet.get('verified_spoken_branches',packet.get('unchanged_spoken_branches'))==416 and facts['act_sheet_counts']==actual_counts
manifest=json.loads((b.ROOT/'source/connected_release/manifest.json').read_text())
for name,digest in manifest['sha256'].items():
    assert hashlib.sha256((run/'candidate-source'/name).read_bytes()).hexdigest()==digest
    assert hashlib.sha256((b.ROOT/'source/connected_release'/name).read_bytes()).hexdigest()==digest
e=yaml.safe_load((run/'candidate-source/playable-evidence.yaml').read_text(encoding='utf-8'))
available={x['id'] for r in e['releases'] for x in r['exhibits']}
routes=e['releases'][-1]['route_checks']
assert len(routes)==30 and all(set(deps)<=available for deps in routes.values())
b.WORK=kit.parent.parent;b.KIT=kit;b.SITE=b.WORK/'site'
deploy=b.WORK/'connected-deploy/site'
printdir=kit.parent/'Print_Today_Current_22'
for p in printdir.iterdir():
    shutil.copy2(p,deploy/'downloads'/p.name)
shutil.copy2(kit.parent/'Print_Today_Current_22.zip',deploy/'downloads/Print_Today_Current_22.zip')
# Recreate both archives after the final verification records are saved.
b.package()
for name in ['The_Last_Acquisition_Source.zip','The_Last_Acquisition_Complete_Kit.zip']:
    shutil.copy2(b.SITE/'downloads'/name,deploy/'downloads'/name)
shutil.copytree(kit,deploy/'downloads/current'/kit.name,dirs_exist_ok=True)
for p in [kit.parent/'Print_Today_Current_22.zip',b.SITE/'downloads/The_Last_Acquisition_Complete_Kit.zip',b.SITE/'downloads/The_Last_Acquisition_Source.zip']:
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None,p.name
        assert not any(Path(n).suffix.lower() in {'.ttf','.otf','.woff','.woff2'} for n in z.namelist())
receipt={'story_source_unchanged':manifest['sha256'],'culprit_routes_preserved':len(routes),
         'spoken_branches':416,'evidence_checks':facts['frozen_fact_checks'],
         'rendered_pages':review['rendered_pages'],'visual_review_complete':True,
         'act_sheets':actual_counts,'deploy_dir':str(deploy),
         'downloads':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((deploy/'downloads').iterdir()) if p.is_file()}}
(run/'predeploy-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'deploy_dir':str(deploy),'downloads':len(receipt['downloads']),'routes':30,'zip_integrity':True}))
