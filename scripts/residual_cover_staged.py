"""Freeze and gate the residual-cover diagnostic without changing production."""
import argparse, shutil
import structural_story_pass as prior

RUN=prior.ROOT/'docs/playtest/2026-10-12-RESIDUAL-COVER-STAGED-SPOILERS'

def prepare():
    assert not RUN.exists(), 'Never overwrite frozen trials.'
    RUN.mkdir()
    shutil.copytree(prior.ROOT/'docs/playtest/2026-10-11-RESIDUAL-COVER-PROBE-SPOILERS/candidate-source', RUN/'candidate-source')
    prior.RUN=RUN
    prior.freeze(('03','28','18'))
    for edition in ('22','30'):
        path=RUN/('cast'+edition)/'READER_INSTRUCTIONS.md'
        path.write_text(path.read_text(encoding='utf-8').replace('scripts/structural_story_pass.py','scripts/residual_cover_staged.py'),encoding='utf-8')
    (RUN/'.gitignore').write_text('layout/\nfull-kit-review/*.png\nfull-kit-review/*.jpg\n',encoding='utf-8')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','read','validate','finale','complete']);p.add_argument('--edition',choices=['22','30']);p.add_argument('--trial');p.add_argument('--stage',type=int);a=p.parse_args()
    if a.action=='prepare':prepare()
    else:
        assert a.edition
        prior.gate.RUN=RUN/('cast'+a.edition)
        prior.gate.gate(a.trial,a.action,a.stage)
