"""Compact orchestration state; does not expose culprits or ratings."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest/2026-10-26-DRAMATURGICAL-01-BLIND-SPOILERS'
rows=[]
for number in range(1,23):
    token=f't{number:03}';folder=RUN/'blind'/token;journal=folder/'journal.json'
    events=json.loads(journal.read_text(encoding='utf-8-sig')) if journal.exists() else []
    complete=(folder/'complete.json').exists()
    started=bool(events) or (folder/'checkpoint_01.txt').exists()
    if complete:action='complete'
    elif events and 'score_sha256' not in events[-1]:action=f'finish or validate released stage{len(events)}'
    elif len(events)==8:
        action='post-vote review and complete gate' if (folder/'accusation-lock.json').exists() else 'save accusation, finale gate, post-vote, complete'
    else:action=f'next release stage{len(events)+1}'
    rows.append({'trial':token,'agent':'/root/dram01_'+token,'locked_stages':sum('score_sha256' in e for e in events),'released_stages':len(events),'started':started,'complete':complete,'next':action})
payload={'completed':sum(r['complete'] for r in rows),'total':22,'status':'complete' if all(r['complete'] for r in rows) else 'running','readers':rows}
(RUN/'progress.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload))
