"""Report a frozen eight-stage blind diagnostic without changing its inputs."""
from pathlib import Path
import csv
import hashlib
import html
import json

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / 'docs/connected-story-01-SPOILERS'
OUT = LAB / 'balance-full-03'
manifest = json.loads((OUT/'private-selection.json').read_text(encoding='utf-8'))
for relative, expected in manifest['sha256'].items():
    assert hashlib.sha256((OUT/relative).read_bytes()).hexdigest() == expected, relative
names = [r['name'] for r in manifest['cast']]
killer = next(r['name'] for r in manifest['cast'] if r['id'] == manifest['killer_id'])
data = json.loads((OUT/'reader-scores.json').read_text(encoding='utf-8-sig'))
assert len(data['checkpoints']) == 8
metrics = []
for stage, row in enumerate(data['checkpoints'], 1):
    assert row['stage'] == stage
    scores = row['scores']
    assert set(scores) == set(names)
    assert all(isinstance(v,(int,float)) and not isinstance(v,bool) and 0<=v<=10 for v in scores.values())
    high = max(scores.values())
    leaders = [name for name in names if scores[name] == high]
    metrics.append(dict(stage=stage, above_five=sum(v>5 for v in scores.values()),
        leaders=leaders, high=high, culprit_score=scores[killer], correct_sole_leader=leaders==[killer],
        alternatives_five_six=sum(5<=scores[name]<=6 for name in names if name!=killer)))
(OUT/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n',encoding='utf-8')
with (OUT/'scores.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['Character']+[f'Stage {n}' for n in range(1,9)])
    for name in names: w.writerow([name]+[r['scores'][name] for r in data['checkpoints']])
prior=json.loads((LAB/'balance-slice-02/metrics.json').read_text(encoding='utf-8'))
lines=['# Quick balance check: current thirty-role draft','',
       '**Spoilers. Preliminary diagnostic.** One fresh blind reader; eight sequential checkpoints, all sixteen hunt clues and named questions. Same hidden culprit as the preceding fifteen-role diagnostics. Intended image observations are text, not rendered artwork. Larger cast and changed evidence mean the latest column is not a controlled comparison.','',
       '**Test-export defect:** unquoted YAML clock times were parsed as sexagesimal integers (392/424/426/429) in checkpoint 5. The reader could not reliably evaluate the timeline. Authoring source now uses quoted clock strings, but frozen inputs and scores remain unchanged. These scores must not be treated as a clean chronology or acceptance test.','',
       '| Metric | Earlier repair (15) | Connected draft (15) | Repaired draft (15) | Current draft (30) |',
       '|---|---:|---:|---:|---:|']
old=list(prior.values())
lines.append('| Suspects >5 after Act II | '+' | '.join(f"{r[4]['above_five']}/15" for r in old)+f" | {metrics[5]['above_five']}/30 |")
lines.append('| Correct sole final leader | '+' | '.join(str(r[6]['correct_sole_leader']) for r in old)+f" | {metrics[7]['correct_sole_leader']} |")
lines.append('| Final leader score | '+' | '.join(str(r[6]['leader_score']) for r in old)+f" | {metrics[7]['high']} |")
lines.append('| Other final suspects at 5–6 | '+' | '.join(str(r[6]['alternatives_five_six']) for r in old)+f" | {metrics[7]['alternatives_five_six']} |")
lines += ['', f"Selected culprit: **{killer}**. Target: ≥10/30 strictly above 5 after Act II, correct final leader only after Act III, 3–4 final alternatives at 5–6.", '',
          '| Checkpoint | Suspects >5 | Leader(s) | Highest | Culprit score |', '|---|---:|---|---:|---:|']
labels=['Introductions','Hunt clues','First evidence','Act I statements','Act II evidence','Act II statements','Act III evidence','Act III statements']
for label,r in zip(labels,metrics):
    lines.append(f"| {label} | {r['above_five']} | {', '.join(r['leaders'])} | {r['high']} | {r['culprit_score']} |")
lines+=['','## Reader observations','']
for row,label in zip(data['checkpoints'],labels):
    lines += [f"### {label}", '', row.get('top_reasoning',''), '', row.get('naturalness',''), '']
lines += ['## Overall feedback','',data.get('final_feedback',''),'',
          'All frozen hashes and 240 score entries validated. One reader and one selected culprit cannot validate all thirty culprit routes or live-party difficulty. Sent public assets and the published fallback are unchanged.','']
(OUT/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Balance diagnostic — spoilers</title><style>body{font:16px system-ui;background:#faf8f3;color:#222;margin:24px}table{border-collapse:collapse}th,td{padding:9px;border:1px solid #ddd;text-align:center}th:first-child{text-align:left;position:sticky;left:0;background:#faf8f3}td{font-weight:700}.scroll{overflow:auto}p{max-width:850px}</style><h1>Current balance diagnostic · spoilers</h1><p>Fresh blind reader. Thirty roles, sixteen hunt clues. Scores 0–10; darker red means more suspicion. Preliminary: clock labels were corrupted by YAML parsing in this frozen test; chronology was not properly assessed. One culprit route tested; intended image observations only.</p><div class="scroll"><table><tr><th>Character</th>']
parts += [f'<th>{html.escape(label)}</th>' for label in labels]
parts.append('</tr>')
for name in names:
    parts.append('<tr><th>'+html.escape(name)+(' · selected culprit' if name==killer else '')+'</th>')
    for row in data['checkpoints']:
        v=row['scores'][name]; light=97-v*5
        parts.append(f'<td style="background:hsl(2 65% {light}%);color:{"white" if v>=7 else "#222"}">{v:g}</td>')
    parts.append('</tr>')
parts.append('</table></div></html>')
(OUT/'heatmap.html').write_text(''.join(parts),encoding='utf-8')
print(json.dumps({'act_ii':metrics[5],'final':metrics[7]},indent=2))
