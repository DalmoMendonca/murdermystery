"""Render every candidate PDF page and identify changes from the published kit."""
from pathlib import Path
import hashlib,json,fitz,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest'/(sys.argv[1] if len(sys.argv)>1 else '2026-10-11-STRUCTURAL-FOLLOWUP-SPOILERS')
KIT=Path((RUN/'candidate-kit-path.txt').read_text(encoding='utf-8').strip())
BASE=ROOT/'build/connected-release-kit'/KIT.name
OUT=RUN/'full-kit-review';OUT.mkdir(exist_ok=True)
pages=[];changed={};issues=[];count=0
for path in sorted(KIT.rglob('*.pdf')):
    relative=path.relative_to(KIT);doc=fitz.open(path)
    original=fitz.open(BASE/relative) if (BASE/relative).exists() else None
    for n,page in enumerate(doc):
        count+=1;pix=page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
        digest=hashlib.sha256(pix.samples).hexdigest()
        oldhash=hashlib.sha256(original[n].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples).hexdigest() if original and n<len(original) else None
        row={'file':str(relative),'page':n+1,'sha256':digest,'changed':digest!=oldhash}
        if row['changed'] and digest not in changed:
            image=OUT/f'changed-{len(changed):03}.png';pix.save(str(image));changed[digest]={'image':str(image),'label':str(relative)+f' / {n+1}'}
        if not page.get_text().strip():issues.append(str(relative)+f' / {n+1}: blank text')
        if '\ufffd' in page.get_text():issues.append(str(relative)+f' / {n+1}: replacement glyph')
        pages.append(row)
    doc.close()
    if original:original.close()
values=list(changed.values())
for start in range(0,len(values),6):
    out=Image.new('RGB',(1896,1640),'#eee');d=ImageDraw.Draw(out)
    for i,row in enumerate(values[start:start+6]):
        x=i%3*632;y=i//3*820;d.text((x+10,y+3),f'{start+i:03} '+row['label'][-80:],fill='black')
        out.paste(Image.open(row['image']).convert('RGB'),(x+10,y+20))
    out.save(OUT/f'contact-{start//6+1:02}.jpg',quality=94)
report={'pdf_count':len(list(KIT.rglob('*.pdf'))),'rendered_pages':count,'changed_unique_pages':len(values),'contact_sheets':(len(values)+5)//6,'issues':issues,'pages':pages,'changed_visuals':values,'visual_review_complete':False,'baseline':str(BASE),'candidate':str(KIT)}
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['pdf_count','rendered_pages','changed_unique_pages','contact_sheets','issues']}))
