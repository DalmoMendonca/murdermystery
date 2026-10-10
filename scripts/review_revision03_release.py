"""Compare every rebuilt PDF page with the reviewed fallback; render every changed page."""
from pathlib import Path
import hashlib,json
import fitz
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
kit=ROOT/'build/connected-release-kit/The_Last_Acquisition_Complete_Kit'
before=ROOT/'build/revision03-before'
out=ROOT/'build/revision03-release-review';out.mkdir(exist_ok=True)
seen=set();changed=[];same=0;pages=0;files=0
for path in sorted(kit.rglob('*.pdf')):
    rel=path.relative_to(kit);oldpath=before/rel;doc=fitz.open(path)
    assert oldpath.exists(),rel
    old=fitz.open(oldpath);assert len(doc)==len(old),(rel,len(doc),len(old))
    files+=1
    for index in range(len(doc)):
        pages+=1
        a=doc[index].get_pixmap(matrix=fitz.Matrix(.5,.5),alpha=False)
        b=old[index].get_pixmap(matrix=fitz.Matrix(.5,.5),alpha=False)
        digest=hashlib.sha256(a.samples).hexdigest()
        if a.samples==b.samples:
            same+=1;continue
        if digest in seen:continue
        seen.add(digest)
        pix=doc[index].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
        image=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        name=f'page_{len(changed):03}.png';image.save(out/name)
        changed.append({'pdf':str(rel),'page':index+1,'raster':name})
    doc.close();old.close()
for start in range(0,len(changed),9):
    montage=Image.new('RGB',(1260,1725),'#ddd8ce');draw=ImageDraw.Draw(montage)
    for j,item in enumerate(changed[start:start+9]):
        image=Image.open(out/item['raster']);image.thumbnail((390,520))
        x=j%3*420+12;y=j//3*575+34;montage.paste(image,(x,y))
        draw.text((x,y-24),f"Changed page {start+j+1} / source p{item['page']}",fill='black')
    montage.save(out/f'montage_{start//9:02}.jpg')
(out/'coverage.json').write_text(json.dumps({'pdf_files':files,'pages_compared':pages,'pages_pixel_identical_to_reviewed_fallback':same,'unique_changed_pages':len(changed),'changed':changed},indent=2),encoding='utf-8')
print(json.dumps({'pdf_files':files,'pages_compared':pages,'pixel_identical_pages':same,'unique_changed_pages':len(changed)}))
