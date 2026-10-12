"""Gated bounded candidate diagnostic; never touches the completed 110 audit."""
import argparse
import exhaustive_balance as audit

audit.RUN = audit.ROOT / 'docs/playtest/2026-10-11-BOUNDED-STORY-SPOILERS'
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['read', 'validate', 'finale', 'complete'])
    parser.add_argument('--trial', required=True)
    parser.add_argument('--stage', type=int)
    args = parser.parse_args()
    audit.gate(args.trial, args.action, args.stage)
