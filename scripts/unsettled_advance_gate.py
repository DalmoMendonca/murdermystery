"""Sequential blind gate for deferred nonmurder repayment disclosure."""
import argparse
import structural_story_pass as prior
RUN=prior.ROOT/'docs/playtest/2026-10-12-UNSETTLED-ADVANCE-SPOILERS'
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['read','validate','finale','complete']);p.add_argument('--edition',choices=['22','30'],required=True);p.add_argument('--trial',required=True);p.add_argument('--stage',type=int);a=p.parse_args()
    prior.gate.RUN=RUN/('cast'+a.edition);prior.gate.gate(a.trial,a.action,a.stage)
