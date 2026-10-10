"""Render all changed paired speaking pages using the production layout."""
from pathlib import Path
import sys,json
import fitz
from PIL import Image,ImageDraw
import build as b
from compile_connected_story import compile_bank
from printable_v2 import pagehead,pagefoot,speech

out=b.WORK/'revision03-layout';out.mkdir(exist_ok=True)
b.KIT=out;b.fonts()
sheet=b.Sheet(out/'Changed_Speaking_Pages.pdf','Revision03 private speaking-page review')
rows=compile_bank('all')['characters'];number=0
for row in rows:
    fields=['where']+(['evidence'] if row['id'] in ('08','20') else [])+(['motive'] if row['id']=='25' else [])
    for phase in fields:
        number+=1
        pagehead(sheet,b,row,{'where':'ACT II: OPPORTUNITY','evidence':'ACT III: METHOD','motive':'ACT I: MOTIVE'}[phase])
        y=sheet.block('Your answer / read your role only',42,109,528,26,'BookBold',b.TEAL)+16
        words=[row['hearings'][phase+'_'+branch] for branch in ('innocent','murderer')]
        size=next((size for size in (16,15) if y+sum(b.para(t,492,size)[1]+61 for t in words)<=659),None)
        assert size,(row['name'],phase)
        for branch,text in zip(('innocent','murderer'),words):y=speech(sheet,'IF '+branch.upper(),text,y,b,size)+6
        pagefoot(sheet,b)
        sheet.next()
sheet.save()
(out/'ledger.json').write_text(json.dumps(b.AUDIT,indent=2),encoding='utf-8')
doc=fitz.open(sheet.path);assert len(doc)==number
for start in range(0,len(doc),9):
    montage=Image.new('RGB',(3*410,3*565),'#ddd8ce');draw=ImageDraw.Draw(montage)
    for j,index in enumerate(range(start,min(start+9,len(doc)))):
        pix=doc[index].get_pixmap(matrix=fitz.Matrix(.65,.65),alpha=False)
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((390,515))
        x=(j%3)*410+10;y=(j//3)*565+25;montage.paste(im,(x,y));draw.text((x,y-18),f'Paired speaking page {index+1}',fill='black')
    montage.save(out/f'proof_{start//9:02}.jpg')
print(f'{number} paired pages rendered; production fit assertions passed.')
