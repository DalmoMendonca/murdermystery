"""Bounded timing and post-vote cover continuity experiment; never publish."""
import argparse, json, shutil, yaml
import structural_story_pass as prior

RUN=prior.ROOT/'docs/playtest/2026-10-12-COVER-CONTINUITY-SPOILERS'

def prepare():
    assert not RUN.exists(), 'Never overwrite a frozen candidate.'
    RUN.mkdir()
    old=prior.ROOT/'docs/playtest/2026-10-12-RESIDUAL-COVER-STAGED-SPOILERS/candidate-source'
    dest=RUN/'candidate-source';shutil.copytree(old,dest)
    previous='The bottle looked like another projected shape in that light. I had given production pattern slides, not an inventory of the bench.'
    replacement='The light caught the bottle beside my fabric. I noticed the shape, not what was inside it.'
    for edition in ('all','confirmed'):
        path=dest/(edition+'.yaml');bank=yaml.safe_load(path.read_text(encoding='utf-8'))
        byid={str(c['id']).zfill(2):c for c in bank['characters']}
        for branch in ('innocent','murderer'):
            key='where_'+branch;assert previous in byid['18']['hearings'][key]
            byid['18']['hearings'][key]=byid['18']['hearings'][key].replace(previous,replacement)
        hugh=byid['03']['coming_clean']['innocent']
        needle='I still sold the bowl under a false certificate'
        assert needle in hugh
        byid['03']['coming_clean']['innocent']=hugh.replace(needle,"And I lied to you about the press version. That warning was cut. I let it stay cut. I still sold the bowl under a false certificate")
        penny=byid['28']['coming_clean']['innocent']
        needle='The family settlement pays the difference I withheld;'
        assert needle in penny
        byid['28']['coming_clean']['innocent']=penny.replace(needle,"The comparison wasn't intact like I just told you. The benchmark was damaged. Ours wasn't. I chose it because the number suited me. The family settlement pays the difference I withheld;")
        prior.dump(path,bank)
    manifest=json.loads((dest/'manifest.json').read_text(encoding='utf-8'))
    manifest.update(revision='cover-continuity-2026-10-12',status='UNPUBLISHED',parent_run=old.parent.name,
        limitations='Two targeted staged readings pending. Evidence and all Method answers unchanged. No production promotion on an untested timing change.')
    manifest['sha256']={p.name:prior.sha(p) for p in dest.glob('*.yaml')}
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    prior.RUN=RUN;prior.freeze(('18',))
    for edition in ('22','30'):
        p=RUN/('cast'+edition)/'READER_INSTRUCTIONS.md'
        p.write_text(p.read_text(encoding='utf-8').replace('scripts/structural_story_pass.py','scripts/cover_continuity_pass.py'),encoding='utf-8')
    (RUN/'.gitignore').write_text('layout/\nfull-kit-review/*.png\nfull-kit-review/*.jpg\n',encoding='utf-8')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','read','validate','finale','complete']);p.add_argument('--edition',choices=['22','30']);p.add_argument('--trial');p.add_argument('--stage',type=int);a=p.parse_args()
    if a.action=='prepare':prepare()
    else:
        assert a.edition
        prior.gate.RUN=RUN/('cast'+a.edition)
        prior.gate.gate(a.trial,a.action,a.stage)
