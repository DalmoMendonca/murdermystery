"""Render every changed answer page with production layout and check minimum type."""
import json, yaml, sys
from pathlib import Path
import build as b
from printable_v2 import pagehead,pagefoot,speech
import fitz
from PIL import Image,ImageDraw

run=b.ROOT/'docs/playtest'/(sys.argv[1] if len(sys.argv)>1 else '2026-10-11-STRUCTURAL-STORY-SPOILERS')
b.fonts();b.KIT=run/'layout';b.KIT.mkdir(exist_ok=True)
bank=yaml.safe_load((run/'candidate-source/all.yaml').read_text(encoding='utf-8'))
original=yaml.safe_load((b.ROOT/'source/connected_release/all.yaml').read_text(encoding='utf-8'))
old={str(c['id']).zfill(2):c for c in original['characters']}
rows=[]
for c in bank['characters']:
    ident=str(c['id']).zfill(2)
    for field,phase,number in [('motive','ACT I: MOTIVE',6),('where','ACT II: OPPORTUNITY',8),('evidence','ACT III: METHOD',10)]:
        words=[c['hearings'][field+'_'+br] for br in ['innocent','murderer']]
        if words==[old[ident]['hearings'][field+'_'+br] for br in ['innocent','murderer']]:continue
        s=b.Sheet(b.KIT/f'{ident}_{field}.pdf',c['name']+' / candidate');s.page=number;pagehead(s,b,c,phase)
        y=s.block('Your answer',42,109,528,27,'BookBold',b.TEAL)+12
        y=s.block('Read only the bordered words when asked. Keep your packet facing you. After answering, ask an unheard guest their question from the previous page.',42,y,528,14)+18
        size=next((sz for sz in [16,15] if y+sum(b.para(t,492,sz)[1]+61 for t in words)<=659),None)
        assert size,(c['name'],field,'No fit at 15pt')
        for br,t in zip(['innocent','murderer'],words):y=speech(s,'IF '+br.upper(),t,y,b,size)+6
        if field=='evidence' and y<620:s.block('The shared discoveries and reports remain at the Evidence Table.',42,y+13,528,14,'BookItalic',bottom=675)
        pagefoot(s,b);s.save();doc=fitz.open(s.path);assert len(doc)==1
        doc[0].get_pixmap(matrix=fitz.Matrix(1,1)).save(str(s.path.with_suffix('.png')))
        rows.append({'id':ident,'character':c['name'],'field':field,'font_size':size,'bottom':y,'pages':len(doc)})
(run/'layout-check.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
paths=sorted(b.KIT.glob('*.png'))
for start in range(0,len(paths),6):
    contact=Image.new('RGB',(1896,1640),'#eeeeee');draw=ImageDraw.Draw(contact)
    for index,path in enumerate(paths[start:start+6]):
        x=(index%3)*632;y=(index//3)*820;draw.text((x+10,y+3),path.stem,fill='black')
        contact.paste(Image.open(path).convert('RGB'),(x+10,y+20))
    contact.save(b.KIT/f'contact-{start//6+1:02}.jpg',quality=93)
print(json.dumps({'changed_pages':len(rows),'minimum_font':min(r['font_size'] for r in rows),'maximum_bottom':max(r['bottom'] for r in rows)}))
