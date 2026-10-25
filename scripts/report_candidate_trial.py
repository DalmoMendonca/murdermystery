"""Validate saved stages and summarize an immutable sequential transcript trial."""
from pathlib import Path
import argparse,csv,hashlib,json

parser=argparse.ArgumentParser()
parser.add_argument('trial',type=Path)
args=parser.parse_args()
p=args.trial
m=json.loads((p/'private-selection.json').read_text(encoding='utf-8'))
cast=m['cast'];names={c['name'] for c in cast}
for name,digest in m['input_sha256'].items():
    assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest
for name,digest in m['source_sha256'].items():
    assert hashlib.sha256((p/'frozen-source'/name).read_bytes()).hexdigest()==digest
results=[]
for stage in range(1,9):
    path=p/f'result_{stage:02}.json'
    if not path.exists():break
    r=json.loads(path.read_text(encoding='utf-8'))
    assert r['checkpoint']==stage
    scores=r['scores']
    assert len(scores)==len(names)==len({v['name'] for v in scores})
    assert {v['name'] for v in scores}==names
    assert all(isinstance(v['score'],(int,float)) and 0<=v['score']<=10 and v['reason'] for v in scores)
    results.append(r)
assert len(list(p.glob('result_*.json')))==len(results),'Nonsequential result file'
summary={'stages_measured':len(results),'input_and_source_hashes_verified':True,
         'counts_above_five':[sum(v['score']>5 for v in r['scores']) for r in results],
         'unique_solution':[r['unique_solution'] for r in results],
         'result_sha256':{f'result_{r["checkpoint"]:02}.json':hashlib.sha256((p/f'result_{r["checkpoint"]:02}.json').read_bytes()).hexdigest() for r in results}}
if len(results)>=6:
    summary['midpoint_required']=10
    summary['midpoint_pass']=summary['counts_above_five'][5]>=10 and not results[5]['unique_solution']
if len(results)==8:
    killer=next(c['name'] for c in cast if c['id']==m['killer_id'])
    last={v['name']:v['score'] for v in results[-1]['scores']}
    summary['correct_unique_final_leader']=last[killer]>max(v for k,v in last.items() if k!=killer)
    summary['final_alternatives_five_to_six']=sum(5<=v<=6 for k,v in last.items() if k!=killer)
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
with (p/'scores.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['Character']+[f'Stage {n}' for n in range(1,9)])
    for c in cast:w.writerow([c['name']]+[next(v['score'] for v in r['scores'] if v['name']==c['name']) for r in results]+['NOT RELEASED']*(8-len(results)))
if results:
    from PIL import Image,ImageDraw,ImageFont
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
    small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
    title=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',28)
    labels=['Intros','Hunt','Evidence I','Act I','Evidence II','Act II','Evidence III','Act III']
    image=Image.new('RGB',(1470,1480),'white');draw=ImageDraw.Draw(image)
    draw.text((35,20),'Baseline repair 02: one blind transcript reader',fill='#222222',font=title)
    draw.text((35,62),'Gray = not released. Scores are not human difficulty measurements.',fill='#555555',font=font)
    left,top,width,height=350,155,132,42
    for col,label in enumerate(labels):draw.text((left+col*width,115),label,fill='#222222',font=small)
    for row,c in enumerate(cast):
        y=top+row*height
        draw.text((28,y+9),c['name'],fill='#222222',font=font)
        for col in range(8):
            v=next((v['score'] for v in results[col]['scores'] if v['name']==c['name']),None) if col<len(results) else None
            if v is None:color=(220,220,220);text='—'
            else:
                fraction=v/10
                color=(255,int(250-200*fraction),int(205-175*fraction));text=f'{v:g}'
            x=left+col*width
            draw.rectangle((x,y,x+width-2,y+height-2),fill=color)
            draw.text((x+width/2,y+height/2),text,anchor='mm',fill='#222222',font=font)
    image.save(p/'heatmap.png')
print(json.dumps({k:v for k,v in summary.items() if k!='result_sha256'},indent=2))
