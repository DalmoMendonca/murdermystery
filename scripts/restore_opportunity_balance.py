"""Preserve published culprit access while strengthening innocent alternatives."""
import argparse
import deadline_balance as candidate
candidate.RUN=candidate.ROOT/'docs/playtest/2026-10-24-RESTORED-OPPORTUNITY-SPOILERS'
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','read','validate','finale','complete']);p.add_argument('--trial');p.add_argument('--stage',type=int);a=p.parse_args()
    if a.action=='prepare':
        candidate.prepare(final_pass=True,preserve_guilty=True)
        instructions=candidate.RUN/'READER_INSTRUCTIONS.md'
        instructions.write_text(instructions.read_text(encoding='utf-8').replace('scripts/deadline_balance.py','scripts/restore_opportunity_balance.py'),encoding='utf-8')
    else:
        candidate.gate.RUN=candidate.RUN
        candidate.gate.gate(a.trial,a.action,a.stage)
