"""Review changed packet layouts; inherit bodies changed only by fixed title case."""
from pathlib import Path
import sys,json,fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];RUN=ROOT/'docs/playtest'/sys.argv[1]
report=json.loads((RUN/'full-kit-review/report.json').read_text());kit=Path(report['candidate']);old=ROOT/'build/connected-release-kit'/kit.name
focus=[];inherited=[];title_examples=set()
for row in report['changed_visuals']:
    rel,number=row['label'].rsplit(' / ',1);index=int(number)-1;keep=True
    if 'PRINT_WITHOUT_READING' in rel and index%12 in [3,4,5,6,7,8,9,11] and (old/rel).exists():
        with fitz.open(kit/rel) as newdoc,fitz.open(old/rel) as olddoc:
            new=newdoc[index].get_pixmap(alpha=False);previous=olddoc[index].get_pixmap(alpha=False)
            a=Image.frombytes('RGB',(new.width,new.height),new.samples);b=Image.frombytes('RGB',(previous.width,previous.height),previous.samples)
            for pic in [a,b]:ImageDraw.Draw(pic).rectangle((40,106,574,148),fill='white')
            if a.tobytes()==b.tobytes():
                inherited.append(row['label']);kind={3:'hunt title',4:'question title',5:'answer title',6:'question title',7:'answer title',8:'question title',9:'answer title',11:'finale title'}[index%12]
                keep=kind not in title_examples;title_examples.add(kind)
    if keep:focus.append(row)
out=RUN/'full-kit-review'
for start in range(0,len(focus),6):
    canvas=Image.new('RGB',(1896,1640),'#eee');draw=ImageDraw.Draw(canvas)
    for i,row in enumerate(focus[start:start+6]):
        x=i%3*632;y=i//3*820;draw.text((x+10,y+3),row['label'][-85:],fill='black');canvas.paste(Image.open(row['image']),(x+10,y+20))
    canvas.save(out/f'focus-{start//6+1:02}.jpg',quality=95)
(RUN/'heading-region-verification.json').write_text(json.dumps({'title_only_pages':inherited,'unchanged_outside_title_rectangle':[40,106,574,148],'full_page_visual_reviews':focus,'focus_contacts':(len(focus)+5)//6},indent=2)+'\n')
print(json.dumps({'title_only_unchanged_bodies':len(inherited),'focus_pages':len(focus),'focus_contacts':(len(focus)+5)//6}))
