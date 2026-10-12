"""Report released scores for the matched partial-cast diagnostic, without guessing missing results."""
from pathlib import Path
import csv
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/connected-story-01-SPOILERS/balance-slice-01'
manifest = json.loads((OUT/'private-selection.json').read_text())
for relative, expected in manifest['sha256'].items():
    assert hashlib.sha256((OUT/relative).read_bytes()).hexdigest()==expected,relative
names = [r['name'] for r in manifest['cast']]
killer = next(r['name'] for r in manifest['cast'] if r['id']==manifest['killer_id'])
stages = ['Introductions','Initial evidence','Act I statements','Act II evidence',
          'Act II statements','Act III evidence','Act III statements']
results={}
for version in ('old','new'):
    found=[]
    for n in range(1,8):
        path=OUT/version/f'result_{n:02}.json'
        if not path.exists():break
        data=json.loads(path.read_text(encoding='utf-8-sig'))
        assert data['checkpoint']==n,path
        scored={r['name']:r for r in data['scores']}
        assert len(data['scores'])==len(scored)==15 and set(scored)==set(names),path
        assert all(isinstance(r['score'],(float,int)) and not isinstance(r['score'],bool)
                   and 0<=r['score']<=10 for r in scored.values()),path
        data['scores_by_name']=scored
        data['above_five']=sum(r['score']>5 for r in scored.values())
        data['leader_score']=max(r['score'] for r in scored.values())
        data['leaders']=[name for name in names if scored[name]['score']==data['leader_score']]
        data['correct_sole_leader']=data['leaders']==[killer]
        data['alternatives_five_six']=sum(5<=scored[name]['score']<=6 for name in names if name!=killer)
        found.append(data)
    results[version]=found

def midpoint(version):
    found=results[version]
    return found[4]['above_five'] if len(found)>=5 else None

lines=['# Matched fifteen-character balance diagnostic','',
       'Same fifteen characters and one hidden uniform random selection; one fresh independent reader per version. Seven staged releases. Hunt omitted in both. Text and intended visual observations only. This tests a partial core-story slice, not the complete thirty-character or confirmed twenty-two-character kit.','',
       '| Checkpoint | Old >5 | New >5 | Old unique solution | New unique solution |',
       '|---|---:|---:|---|---|']
for n,label in enumerate(stages):
    cells=[]
    for version in ('old','new'):
        cells.append(results[version][n] if len(results[version])>n else None)
    a,b=cells
    lines.append(f'| {label} | {a["above_five"] if a else "Pending"} | {b["above_five"] if b else "Pending"} | {a["unique_solution"] if a else "Pending"} | {b["unique_solution"] if b else "Pending"} |')
lines += ['', 'The one-third midpoint target scales to **5 of 15 strictly above 5** for this diagnostic. It remains **10 of 30** for the actual full-cast gate. A top-ranked suspect is not necessarily a logically unique solution.','',
          '| Final metric | Old | New |','|---|---|---|']
for label,key in [('Correct murderer sole highest scorer','correct_sole_leader'),
                  ('Highest score','leader_score'),('Other suspects scored 5–6','alternatives_five_six')]:
    lines.append('| '+label+' | '+' | '.join(str(results[v][-1][key]) if len(results[v])==7 else 'Pending' for v in ('old','new'))+' |')
for version in ('old','new'):
    if results[version]:
        lines += ['', '## '+version.title()+' reader observations','']
        for n in (2,4,6):
            if len(results[version])>n:
                notes=results[version][n].get('naturalism_notes',[])
                if isinstance(notes,str):notes=[notes]
                lines += [f'- {stages[n]}: '+str(note) for note in notes]
lines += ['', '## Historical context and limits','',
          'Earlier complete-cast midpoints were repair01 4/30 (13.3%) and repair02 2/30 (6.7%). Those involved different selected worlds/readers and the hunt, so they do not form a controlled numerical trend. This matched slice provides a more useful local comparison, but independent reader variance, the reduced cast and omitted hunt still limit interpretation. Initial exhibits are identical; later questions/evidence differ as part of the rewrite. Current clue artwork, final packets and party pacing are not tested.','',
          'Every available result was validated against fifteen unique names and 0–10 scores. Frozen input/source SHA256 checks passed. Pending stages are never treated as results. No production or sent assets changed.']
(OUT/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
summary={v:[{k:d[k] for k in ('checkpoint','above_five','unique_solution','leader_score','correct_sole_leader','alternatives_five_six')} for d in results[v]] for v in results}
(OUT/'metrics.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
with (OUT/'scores.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.writer(f)
    writer.writerow(['name']+[f'{v}_{n}' for v in ('old','new') for n in range(1,8)])
    for name in names:
        writer.writerow([name]+[results[v][n]['scores_by_name'][name]['score'] if len(results[v])>n else '' for v in ('old','new') for n in range(7)])

try:
    regular=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    bold=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',20)
except OSError:
    regular=bold=ImageFont.load_default()
canvas=Image.new('RGB',(1360,720),'#f7f3e9')
draw=ImageDraw.Draw(canvas)
draw.text((22,15),'Matched 15-character diagnostic — old and new',font=bold,fill='#222222')
draw.text((22,45),'Columns: Intro / Initial evidence / Act I / Act II evidence / Act II / Act III evidence / Act III',font=regular,fill='#333333')
for vnum,version in enumerate(('old','new')):
    start=300+vnum*520
    draw.text((start,80),version.upper(),font=bold,fill='#222222')
    for n in range(7):draw.text((start+n*70,110),str(n+1),font=bold,fill='#222222')
for row,name in enumerate(names):
    y=145+row*34
    draw.text((22,y+5),name,font=regular,fill='#222222')
    for vnum,version in enumerate(('old','new')):
        for n in range(7):
            x=300+vnum*520+n*70
            if len(results[version])>n:
                score=results[version][n]['scores_by_name'][name]['score']
                if score<=5:
                    a=score/5
                    rgb=tuple(round(c+(d-c)*a) for c,d in zip((218,234,224),(244,209,119)))
                else:
                    a=(score-5)/5
                    rgb=tuple(round(c+(d-c)*a) for c,d in zip((244,209,119),(143,39,45)))
                text=str(score)
                ink='white' if score>=8 else '#222222'
            else:rgb='#dddddd';text='—';ink='#666666'
            draw.rectangle((x,y,x+62,y+29),fill=rgb)
            draw.text((x+24,y+5),text,font=regular,fill=ink)
draw.text((22,675),'Green = low suspicion; amber = 5; red = high. This is a partial text test, not party vote prediction.',font=regular,fill='#333333')
canvas.save(OUT/'heatmap.png')
print(json.dumps({'released_stages':{v:len(results[v]) for v in results},'midpoint_above_five':{v:midpoint(v) for v in results}},indent=2))
