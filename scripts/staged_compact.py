"""Readable artifact folios: same evidence, same reveal gates, fewer sheets."""
import copy
import html
import json
from pathlib import Path
from reportlab.platypus import Paragraph, Spacer, Image, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader

ACTS = {'before_motive': 'ACT I: MOTIVE', 'before_opportunity': 'ACT II: OPPORTUNITY', 'before_method': 'ACT III: METHOD'}

def flow_height(items, width=516):
    return sum(i.wrap(width,10000)[1]+i.getSpaceBefore()+i.getSpaceAfter() for i in items)

def record(b,item,photo_height=0):
    """A wide ledger line uses space that a narrow label column wastes."""
    body=ParagraphStyle('folio-body',fontName='Book',fontSize=14,leading=17,spaceAfter=3)
    title=ParagraphStyle('folio-title',parent=body,fontName='BookBold',fontSize=18,leading=21,spaceBefore=2,spaceAfter=5,textColor=b.RED)
    agency=ParagraphStyle('folio-agency',parent=body,fontName='BookBold',fontSize=10.5,leading=13,spaceAfter=2,textColor=b.RED)
    p=lambda t,style=body:Paragraph(html.escape(str(t)),style)
    out=[p(item['department'],agency),p(item['title'],title)]
    if item.get('stamp'):out.append(p(item['stamp'],agency))
    for text in item.get('paragraphs',[]):out.append(p(text))
    rows=item.get('rows',[])
    for start in range(0,len(rows),2):
        out.append(Paragraph(' &nbsp; / &nbsp; '.join('<b>'+html.escape(label)+':</b> '+html.escape(value) for label,value in rows[start:start+2]),body))
    if photo_height:
        from loose_evidence import photo
        from evidence_views import PHOTO_GROUPS
        used=set()
        for im in item.get('images',[]):
            if im['id'] in used:continue
            if im['id'] in PHOTO_GROUPS:
                filename,covers,_=PHOTO_GROUPS[im['id']]
                out.extend([Spacer(1,5),photo(b.ROOT/'assets/evidence/print-2026-10-24'/filename,516,photo_height)])
                used.update(covers)
    for im in item.get('images',[]):out.append(p(im['observation']))
    return out

def notice(b,path,act,item):
    s=b.Sheet(path,'Board secretary notice')
    s.block(act,42,26,528,17,'BookBold',b.RED)
    s.image(b.ROOT/'assets/evidence/staged-artifacts-2026-10-24/board-notice.png',30,66,552,688)
    s.block(item['department'],92,206,428,13,'BookBold',b.RED)
    s.block("Board Secretary's Notice",92,242,428,32,'BookBold',b.RED)
    s.block('Grant Larceny has died at the gala after his private toast.',92,326,428,24,bottom=439)
    s.block('The proposed gift remains\nunsigned and unaccepted.',92,453,428,26,'BookBold',b.RED,bottom=535)
    s.block("The naming terms, donor control and director's resignation are proposals, not completed decisions.",92,561,428,20,bottom=666)
    s.save()

def lab(b,path,act,item):
    s=b.Sheet(path,'Initial laboratory findings')
    s.block(act,42,26,528,17,'BookBold',b.RED)
    s.image(b.ROOT/'assets/evidence/staged-artifacts-2026-10-24/lab-report.png',30,62,552,696)
    s.block('SAINT FRANCIS HOSPITAL',78,121,440,23,'BookBold',b.RED)
    s.block('Tulsa, Oklahoma / Laboratory Services',78,157,440,14)
    s.line(78,193,534,193)
    s.block(item['title'],78,215,456,27,'BookBold',b.RED)
    s.block(item['department'],78,255,456,12,'BookBold')
    for y,(sample,result) in zip([303,390,477],item['rows']):
        s.block(sample,78,y,456,17,'BookBold')
        s.block(result,78,y+29,456,21,'BookBold',b.RED)
        s.line(78,y+65,534,y+65)
    s.block('Specimen / scene note',78,579,456,14,'BookBold',b.RED)
    s.block(item['paragraphs'][0],78,605,456,16,bottom=690)
    s.block('FICTIONAL CASE / THE LAST ACQUISITION',78,716,456,10,'BookItalic',b.RED)
    s.save()

def service_docket(b,path,act,item):
    s=b.Sheet(path,"Private service docket")
    s.block(act,42,26,528,17,'BookBold',b.RED)
    s.block(item['department'],48,99,516,13,'BookBold',b.RED)
    s.block(item['title'],48,132,516,29,'BookBold',b.RED)
    s.block(item['paragraphs'][0],48,190,516,17,bottom=295)
    s.line(134,315,134,670)
    for n,(time,event) in enumerate(item['rows']):
        y=321+n*74
        s.c.setFillColor(b.RED);s.c.circle(134,792-y-8,4,fill=1,stroke=0)
        s.block(time,48,y,74,15,'BookBold',b.RED,bottom=y+63)
        s.block(event,156,y,408,17,bottom=y+63)
    s.save()

def proof_document(b):
    """The actual markup, with every evidentiary line at least 14 points."""
    from reportlab.graphics.shapes import Drawing,Rect,String,Line
    d=Drawing(512,268)
    d.add(Rect(0,0,512,266,fillColor=b.PALE,strokeColor=b.GOLD,strokeWidth=.7))
    def line(y,text,size=14,font='Book',color=None):
        d.add(String(16,y,text,fontName=font,fontSize=size,fillColor=color or b.INK))
    line(242,'CATALOG / WORKING PROOF',18,'BookBold',b.RED)
    line(218,'October 29, 2026 / Dr. Art E. Fact',14,'BookBold')
    line(192,'Seller requires original contents. Lender calls contents inert.')
    line(174,'Please clarify before opening.')
    line(147,'INTAKE REPLY: Unresolved. Keep closed.',15,'BookBold',b.RED)
    line(116,'Reed DeLabel / PRESS MARKUP',14,'BookBold')
    line(91,'Purchase condition requires original contents to remain.')
    d.add(Line(15,96,463,96,strokeColor=b.RED,strokeWidth=1.3))
    line(54,'STAFF COPY: full query and seller attachment retained')
    line(28,'PRESS COPY: shortened inert caption')
    return d

def staged(b,path,evidence,bank,confirmed):
    from visible_evidence import exhibits
    from loose_evidence import build_pages
    from pypdf import PdfWriter
    tmp=path.parent/('_'+path.stem);tmp.mkdir(parents=True,exist_ok=True)
    byrelease={r['key']:{i['id']:copy.deepcopy(i) for i in exhibits(evidence,r,confirmed)} for r in evidence['releases']}
    late=byrelease['before_method']
    if 'original_interview' in late:
        late['original_interview']['paragraphs']=bank['pre_method_press_interview_opening']
        if not late['original_interview']['paragraphs']:del late['original_interview']
    # Repair paragraph boundaries in presentation only. Frozen story source stays untouched.
    late['original_source']['paragraphs']=[', '.join(late['original_source']['paragraphs'])]
    ledger=[];paths=[]
    first=tmp/'01-notice.pdf';notice(b,first,ACTS['before_motive'],byrelease['before_motive']['gift_status']);paths.append(first)
    service=tmp/'02-service.pdf'
    service_docket(b,service,ACTS['before_opportunity'],byrelease['before_opportunity']['service_account']);paths.append(service)
    result=tmp/'03-lab.pdf';lab(b,result,ACTS['before_opportunity'],byrelease['before_opportunity']['initial_samples']);paths.append(result)
    if (b.ROOT/'source/act3_artifacts.json').exists():
        from act3_artifacts import render_all
    else:
        from act3_editorial import render_all
    method_paths,ledger=render_all(b,tmp,bank)
    paths.extend(method_paths)
    writer=PdfWriter()
    for p in paths:writer.append(str(p))
    with path.open('wb') as f:writer.write(f)
    writer.close()
    for p in paths:p.unlink()
    tmp.rmdir()
    (b.WORK/f'staged-folios-{path.stem}.json').write_text(json.dumps({'act_sheets':[1,2,len(method_paths)],'folios':ledger},indent=2)+'\n',encoding='utf-8')
    return ledger
