"""Freeze and gate the bounded scholar/photographer voice experiment."""
import argparse
import structural_story_pass as prior
RUN=prior.ROOT/'docs/playtest/2026-10-12-TWO-VOICE-SPOILERS'
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['freeze','read','validate','finale','complete']);p.add_argument('--edition',choices=['22','30']);p.add_argument('--trial');p.add_argument('--stage',type=int);a=p.parse_args()
    if a.action=='freeze':
        prior.RUN=RUN;prior.freeze({'22':('03',),'30':('26',)})
        for edition in ('22','30'):
            f=RUN/('cast'+edition)/'READER_INSTRUCTIONS.md'
            f.write_text(f.read_text(encoding='utf-8').replace('scripts/structural_story_pass.py','scripts/two_voice_gate.py'),encoding='utf-8')
    else:
        assert a.edition
        prior.gate.RUN=RUN/('cast'+a.edition);prior.gate.gate(a.trial,a.action,a.stage)
