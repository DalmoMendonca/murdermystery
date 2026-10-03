"""Render EVERY PDF page; map exact visual duplicates to a single review image."""
from pathlib import Path
import json,hashlib,re
import fitz
from PIL import Image,ImageDraw
from build import KIT,ROOT,WORK
def verify():
    out=WORK/'review';out.mkdir(parents=True,exist_ok=True)
    pages=[];unique={};issues=[];files=[]
    chars=json.loads((ROOT/'source/characters.json').read_text(encoding='utf-8'))
    for path in sorted(KIT.rglob('*.pdf')):
        rel=str(path.relative_to(KIT));doc=fitz.open(path);files.append({'file':rel,'pages':len(doc)})
        for n,page in enumerate(doc):
            text=page.get_text();spans=[s for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
            for s in spans:
                box=s['bbox']
                if box[0]<20 or box[1]<20 or box[2]>page.rect.width-20 or box[3]>page.rect.height-15:issues.append(f'{rel} p{n+1} outside safe bounds: {s["text"]}')
                if s['size']<11.9:issues.append(f'{rel} p{n+1} small text {s["size"]}')
                if '\ufffd' in s['text']:issues.append(f'{rel} p{n+1} replacement glyph')
            if not text.strip():issues.append(f'{rel} p{n+1} blank')
            pix=page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
            digest=hashlib.sha256(pix.samples).hexdigest()
            if digest not in unique:
                id=len(unique);image_path=out/f'page-{id:03}.png';pix.save(str(image_path));unique[digest]={'id':id,'label':f'{path.stem} / {n+1}','image':str(image_path),'copies':[]}
            unique[digest]['copies'].append({'file':rel,'page':n+1})
            pages.append({'file':rel,'page':n+1,'review_image':unique[digest]['id'],'sha256':digest})
        if 'PreParty_Individual' in rel:
            assert len(doc)==1,rel
            assert all(s not in doc[0].get_text() for s in ['WHAT YOU ALREADY KNOW','HOW TO PLAY THEM','OPTIONAL QUIPS','Sterling Voss','Page 1','CORE','SECONDARY','TERTIARY']),rel
        if 'Secret_Individual' in rel:assert len(doc)==2,rel
        doc.close()
    for c in chars:
        assert set(c['evidence'])=={'A','B'}
        assert c['private']['innocent_card']!=c['private']['murderer_card']
        assert all(c['private'][key] for key in ['innocent','murderer','final_innocent','final_murderer'])
    values=list(unique.values())
    for start in range(0,len(values),4):
        sheet=Image.new('RGB',(1300,1750),'#cdd7da');draw=ImageDraw.Draw(sheet)
        for i,item in enumerate(values[start:start+4]):
            im=Image.open(item['image']);im.thumbnail((620,815));x=(i%2)*650;y=(i//2)*875
            sheet.paste(im,(x+15+(620-im.width)//2,y+42));draw.text((x+15,y+8),f'{item["id"]:03} '+item['label'][:76],fill='black')
        sheet.save(out/f'sheet-{start//4:02}.jpg',quality=94)
    report={'pdf_count':len(files),'rendered_pages':len(pages),'unique_visual_pages':len(values),'contact_sheets':(len(values)+3)//4,'issues':issues,'files':files,'pages':pages,'visuals':values}
    (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['pdf_count','rendered_pages','unique_visual_pages','contact_sheets','issues']},indent=2))
    assert not issues,'Fix preflight errors before visual review'
if __name__=='__main__':verify()
