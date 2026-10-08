"""Archive all three completed pass-12 trials; reveal selections only after completion."""
from pathlib import Path
import json, shutil, hashlib, math, argparse
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'build/story-pass12'
DEST=ROOT/'docs/story-pass-12-SPOILERS/tests'
LABELS=['Intros','Hunt','Evidence 1–2','Motive','Evidence 3','Opportunity','Evidence 4–5','Method']

def normalized(name):
    return name.replace('’',"'").strip().casefold()

def export(version=12):
    global SRC,DEST
    SRC=ROOT/f'build/story-pass{version}'
    DEST=ROOT/f'docs/story-pass-{version}-SPOILERS/tests'
    for label in 'ABC':
        for n in range(1,9):
            if not (SRC/label/f'result_{n:02}.json').exists():
                raise SystemExit(f'Incomplete {label}, stage {n}; no selections revealed.')
    chars=json.loads((ROOT/'source/characters.json').read_text(encoding='utf-8'))
    manifest=json.loads((SRC/'private-manifest.json').read_text(encoding='utf-8'))
    frozen=SRC/'tested-source'
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in frozen.glob('*.yaml')}
    assert hashes==manifest['source_sha256'], 'Frozen sources changed'
    DEST.mkdir(parents=True,exist_ok=True)
    shutil.copytree(frozen,DEST/'tested-source',dirs_exist_ok=True)
    shutil.copy2(SRC/'private-manifest.json',DEST/'manifest.json')
    summaries=[]
    for label in 'ABC':
        target=DEST/label
        shutil.copytree(SRC/label,target,dirs_exist_ok=True)
        selection=json.loads((target/'private-selection.json').read_text(encoding='utf-8'))
        cast=[c for c in chars if c['id'] in selection['cast_ids']]
        killer=next(c for c in cast if c['id']==selection['killer_id'])
        stages=[]
        protocol_notes=[]
        for n in range(1,9):
            result=json.loads((target/f'result_{n:02}.json').read_text(encoding='utf-8-sig'))
            protocol_notes.extend(note for note in result.get('plausibility_notes',[]) if 'write failed' in note.lower() or 'procedural exception' in note.lower())
            scores={normalized(s['name']):s['score'] for s in result['scores']}
            assert len(scores)==len(cast)
            assert set(scores)=={normalized(c['name']) for c in cast}
            assert all(0<=s<=10 for s in scores.values())
            stages.append(scores)
        kn=normalized(killer['name']);last=stages[-1]
        summary={'trial':label,'cast_size':len(cast),'selected_character':killer['name'],
            'act_II_above_5':sum(s>5 for s in stages[5].values()),
            'act_II_target':math.ceil(len(cast)/3),'final_selected_score':last[kn],
            'selected_highest':last[kn]==max(last.values()),
            'selected_unique_highest':sum(s>=last[kn] for s in last.values())==1,
            'final_alternatives_5_to_6':sum(5<=s<=6 for name,s in last.items() if name!=kn),
            'selected_scores':[stage[kn] for stage in stages],
            'protocol_notes':protocol_notes,
            'limitation':'One independent AI reader per trial, full transcripts. Not a human solve rate or all-culprit validation.'}
        (target/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        summaries.append(summary)
        rows=len(cast);height=270+rows*36
        im=Image.new('RGB',(1740,height),'#f5f0e6');d=ImageDraw.Draw(im)
        path='C:/Windows/Fonts/georgia.ttf'
        font=ImageFont.truetype(path,23);small=ImageFont.truetype(path,18);title=ImageFont.truetype(path,32)
        d.text((30,20),f'Pass {version} / trial {label} / SPOILERS',font=title,fill='#6d1730')
        d.text((30,70),'Actual independent scores; selected identity revealed only after all eight saved releases.',font=font,fill='#302326')
        x0=400;cw=160;y0=155;rh=36
        for j,s in enumerate(LABELS):d.text((x0+j*cw+cw/2,120),s,font=small,anchor='mm',fill='#302326')
        for i,c in enumerate(cast):
            y=y0+i*rh;name=normalized(c['name'])
            d.text((30,y+rh/2),c['name']+(' *' if name==kn else ''),font=font,anchor='lm',fill='#6d1730' if name==kn else '#302326')
            for j,stage in enumerate(stages):
                s=stage[name];a=s/10;x=x0+j*cw
                color=tuple(round(lo+(hi-lo)*a) for lo,hi in zip((244,237,222),(112,14,39)))
                d.rectangle((x+2,y+2,x+cw-2,y+rh-2),fill=color)
                d.text((x+cw/2,y+rh/2),str(s),font=font,anchor='mm',fill='white' if s>=6 else '#302326')
        d.text((30,height-90),f"Act II >5: {summary['act_II_above_5']}/{rows} (target {summary['act_II_target']}). Final culprit: {last[kn]}. Alternatives 5–6: {summary['final_alternatives_5_to_6']}.",font=font,fill='#302326')
        d.text((30,height-48),'* Selected murderer. Three blind draws; no human difficulty estimate.',font=small,fill='#6d1730')
        im.save(target/'heatmap.png')
    (DEST/'summaries.json').write_text(json.dumps(summaries,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(summaries,indent=2,ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--version',type=int,default=12)
    export(p.parse_args().version)
