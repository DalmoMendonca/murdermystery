"""Compare three fifteen-role reads; fail on incomplete or altered frozen inputs."""
from pathlib import Path
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / 'docs/connected-story-01-SPOILERS'
OUT = LAB / 'balance-slice-02'
series = [('Earlier repair', LAB/'balance-slice-01', 'old'),
          ('First connected draft', LAB/'balance-slice-01', 'new'),
          ('Current repaired draft', OUT, 'new')]
results = {}
for label, folder, version in series:
    manifest = json.loads((folder/'private-selection.json').read_text(encoding='utf-8'))
    for relative, expected in manifest['sha256'].items():
        assert hashlib.sha256((folder/relative).read_bytes()).hexdigest() == expected, relative
    names = [r['name'] for r in manifest['cast']]
    killer = next(r['name'] for r in manifest['cast'] if r['id'] == manifest['killer_id'])
    rows = []
    for n in range(1, 8):
        data = json.loads((folder/version/f'result_{n:02}.json').read_text(encoding='utf-8-sig'))
        scores = {r['name']: r['score'] for r in data['scores']}
        assert data['checkpoint'] == n and len(data['scores']) == len(scores) == 15
        assert set(scores) == set(names)
        assert all(isinstance(x,(int,float)) and not isinstance(x,bool) and 0 <= x <= 10 for x in scores.values())
        high = max(scores.values())
        leaders = [name for name in names if scores[name] == high]
        rows.append(dict(checkpoint=n, above_five=sum(x>5 for x in scores.values()),
                         correct_sole_leader=leaders==[killer], leader_score=high,
                         alternatives_five_six=sum(5<=scores[name]<=6 for name in names if name!=killer),
                         unique_solution=data['unique_solution'], scores=scores,
                         observations=data.get('observations',data.get('naturalism_notes',[]))))
    results[label] = rows
(OUT/'metrics.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (OUT/'scores.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['Character']+[f'{label}: stage {n}' for label in results for n in range(1,8)])
    for name in names:
        w.writerow([name]+[r['scores'][name] for rows in results.values() for r in rows])
lines = ['# Current quick balance comparison','',
         'Same fifteen characters and same hidden culprit; one fresh blind reader per version, seven sequential checkpoints. Hunt omitted. This follow-up tests the repaired fifteen-role core, not the five additional market roles, full thirty-role game, finished artwork or live party. Scores from different readers include reader variance.','',
         '| Metric | Earlier repair | First connected draft | Current repaired draft |',
         '|---|---:|---:|---:|']
for label, stage, key in [('Suspects >5 after Act II',4,'above_five'),
                          ('Correct sole final leader',6,'correct_sole_leader'),
                          ('Final highest score',6,'leader_score'),
                          ('Other final suspects at 5–6',6,'alternatives_five_six')]:
    lines.append('| '+label+' | '+' | '.join(str(rows[stage][key]) for rows in results.values())+' |')
lines += ['', 'Target: at least 5/15 above 5 after Act II, correct final leader, and 3–4 final alternatives at 5–6. Full-cast midpoint target remains 10/30.','',
          '## Current reader observations','']
for n in (2,4,6):
    notes = results['Current repaired draft'][n]['observations']
    if isinstance(notes,str): notes = [notes]
    lines += [f'- Stage {n+1}: {note}' for note in notes]
lines += ['', 'Frozen input/source SHA256 checks passed for all three series. Each checkpoint contains all fifteen exact character names and scores within 0–10. Results do not imply statistical significance, full-cast balance, or improvements to the currently published fallback. Historical full-cast repair01 (4/30) and repair02 (2/30) are not directly comparable to these fifteen-role reads.','']
(OUT/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({label:{'act_ii_above_five':rows[4]['above_five'],
                        'correct_final_leader':rows[6]['correct_sole_leader'],
                        'final_alternatives_five_six':rows[6]['alternatives_five_six']}
                  for label,rows in results.items()},indent=2))
