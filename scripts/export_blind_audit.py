"""Preserve completed blind trials and draw their actual eight-stage scores."""
from pathlib import Path
import json, shutil, hashlib, argparse
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'docs/playtest/2026-10-07-NATURALISM-SPOILERS'
LABELS = ['Intros', 'Hunt', 'Evidence 1–2', 'Motive', 'Evidence 3', 'Opportunity', 'Evidence 4–5', 'Method']

def export(version):
    src = ROOT / 'build' / f'naturalism-v{version}'
    batches = [json.loads((src/'blind'/f'result_{i:02}.json').read_text(encoding='utf-8')) for i in range(1,9)]
    private = json.loads((src/'blind/run_private.json').read_text(encoding='utf-8'))
    name_source=src/'tested-source/characters.json'
    # Names/IDs are locked public copy; v9 has transcripts but no source snapshot.
    if not name_source.exists(): name_source=ROOT/'source/characters.json'
    chars = json.loads(name_source.read_text(encoding='utf-8'))
    assert all(len(b['scores']) == 30 for b in batches)
    # Readers preserve released character order. Raw Unicode and wording are retained.
    assert all(b['scores'][0]['name'].startswith('Artie') for b in batches)
    target = DEST / f'v{version}'
    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src/'blind', target/'blind', dirs_exist_ok=True)
    if (src/'tested-source').exists():
        shutil.copytree(src/'tested-source', target/'tested-source', dirs_exist_ok=True)
    hashes = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (target/'tested-source').iterdir() if p.is_file()} if (target/'tested-source').exists() else {}
    killer_index = next(i for i,c in enumerate(chars) if c['id'] == private['killer_id'])
    last = batches[-1]['scores']; maximum = max(s['score'] for s in last)
    summary = {'trial':version, 'selected_character':chars[killer_index]['name'],
        'after_opportunity_above_5':sum(s['score']>5 for s in batches[5]['scores']),
        'final_selected_score':last[killer_index]['score'],
        'selected_highest':last[killer_index]['score']==maximum,
        'final_alternatives_5_to_6':sum(5<=s['score']<=6 for i,s in enumerate(last) if i!=killer_index),
        'source_sha256':hashes, 'limitation':'One AI reader, full transcript; not a human solve rate. Frozen trial source, not subsequent patches.'}
    (target/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    im=Image.new('RGB',(1740,1410),'#f5f0e6'); draw=ImageDraw.Draw(im)
    fontpath='C:/Windows/Fonts/georgia.ttf'
    f=ImageFont.truetype(fontpath,24); small=ImageFont.truetype(fontpath,19); title=ImageFont.truetype(fontpath,34)
    draw.text((40,25),f'Blind trial {version} / SPOILERS',font=title,fill='#6d1730')
    draw.text((40,78),'Actual suspicion scores, 0–10. One reader; eight sequential releases; no finale available.',font=f,fill='#282323')
    x0=390; cw=159; y0=205; rh=35
    for j,label in enumerate(LABELS): draw.text((x0+j*cw+cw/2,150),label,font=small,anchor='mm',fill='#282323')
    for i,c in enumerate(chars):
        y=y0+i*rh; label=c['name']+(' *' if i==killer_index else '')
        draw.text((40,y+rh/2),label,font=f,anchor='lm',fill='#6d1730' if i==killer_index else '#282323')
        for j,b in enumerate(batches):
            score=b['scores'][i]['score']; assert 0<=score<=10
            a=score/10; color=tuple(round(lo+(hi-lo)*a) for lo,hi in zip((244,237,222),(112,14,39)))
            x=x0+j*cw;draw.rectangle((x+2,y+2,x+cw-2,y+rh-2),fill=color)
            draw.text((x+cw/2,y+rh/2),str(score),font=f,anchor='mm',fill='white' if score>=6 else '#302326')
    draw.text((40,1280),'* Hidden selected murderer (revealed here only after scores were saved).',font=small,fill='#6d1730')
    draw.text((40,1320),f"Act II >5: {summary['after_opportunity_above_5']}/30. Final selected score: {summary['final_selected_score']}. Alternatives 5–6: {summary['final_alternatives_5_to_6']}.",font=f,fill='#282323')
    im.save(target/'heatmap.png')
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('versions',type=int,nargs='+');a=p.parse_args()
    for version in a.versions: export(version)
