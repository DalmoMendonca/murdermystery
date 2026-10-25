"""Presentation-only clue sheets: exact frozen facts, no packet furniture."""
from pathlib import Path
import html, io, copy
from PIL import Image as PILImage
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, SimpleDocTemplate
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor

ACTS={'before_motive':'ACT I: MOTIVE','before_opportunity':'ACT II: OPPORTUNITY','before_method':'ACT III: METHOD'}

def styles(b):
    body=ParagraphStyle('evidence-body',fontName='Book',fontSize=14,leading=17,spaceAfter=7)
    heading=ParagraphStyle('evidence-title',parent=body,fontName='BookBold',fontSize=23,leading=27,textColor=b.RED,spaceAfter=12)
    sub=ParagraphStyle('evidence-agency',parent=body,fontName='BookBold',fontSize=12,leading=15,textColor=b.RED,spaceAfter=7)
    return body,heading,sub

def photo(path,width,height):
    with PILImage.open(path) as im:
        w,h=im.size;data=io.BytesIO();im=im.convert('RGB');im.thumbnail((1600,1600));im.save(data,format='JPEG',quality=88,subsampling=0)
    data.seek(0);scale=min(width/w,height/h)
    out=Image(data,width=w*scale,height=h*scale);out.hAlign='CENTER';return out

def content(b,item,with_title=True):
    body,heading,sub=styles(b)
    def p(t,style=body):return Paragraph(html.escape(str(t)).replace('\n','<br/>'),style)
    out=[]
    if with_title:
        out.extend([p(item.get('department','MERIDIAN MUSEUM'),sub),p(item['title'],heading)])
    if item.get('stamp'):out.append(p(item['stamp'],sub))
    out.extend(p(t) for t in item.get('paragraphs',[]))
    if item.get('rows'):
        table=Table([[p(c) for c in row] for row in item['rows']],colWidths=[155,361],hAlign='LEFT')
        table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(0,-1),b.PALE),('LINEBELOW',(0,0),(-1,-1),.35,b.GOLD),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
        out.append(table)
    return out

def build_pages(b,path,title,sheets):
    """Each planned sheet must fit. Never silently spill to another page."""
    story=[];ledger=[]
    body,heading,sub=styles(b)
    for index,(act,items) in enumerate(sheets):
        if index:story.append(PageBreak())
        marker=Paragraph(html.escape(act),ParagraphStyle('act',parent=sub,fontSize=16,leading=20,spaceAfter=14))
        full=[marker]+items
        height=sum(x.wrap(516,10000)[1] for x in full)
        # Flowable spaceAfter/Before is additional to its wrapped height.
        height+=sum(x.getSpaceBefore()+x.getSpaceAfter() for x in full)
        assert height<=688, f'{path.name}: planned sheet {index+1} {act}: {height:.1f}pt exceeds 688'
        ledger.append({'sheet':index+1,'act':act,'height':round(height,1)})
        story.extend(full)
    path.parent.mkdir(parents=True,exist_ok=True)
    def page(cv,doc):
        cv.setTitle(title);cv.setAuthor('The Meridian Museum')
        cv.setStrokeColor(b.GOLD);cv.setLineWidth(.7);cv.line(48,754,564,754)
    SimpleDocTemplate(str(path),pagesize=(612,792),leftMargin=48,rightMargin=48,topMargin=45,bottomMargin=35,allowSplitting=0).build(story,onFirstPage=page,onLaterPages=page)
    import fitz
    assert len(fitz.open(path))==len(sheets),f'Unexpected spill: {path}'
    return ledger

def hunt(b,path,evidence):
    sheets=[]
    for item in evidence['hunt']:
        art=b.ROOT/'assets/evidence/hunt-2026-10-24'/f"discovery-{item['number']:02}.png"
        assert art.is_file(),art
        items=[photo(art,516,206),Spacer(1,15)]+content(b,item)
        sheets.append((f"DISCOVERY {item['number']:02}",items))
    return build_pages(b,path,'Hunt discoveries',sheets)

def retained(b,item,max_height=200):
    """Inline companions: no repeat exhibit title or near-empty image page."""
    from evidence_views import PHOTO_GROUPS
    body,heading,sub=styles(b);out=[];shown=set()
    for im in item.get('images',[]):
        ident=im['id']
        if ident in shown:continue
        if ident in PHOTO_GROUPS:
            filename,covers,label=PHOTO_GROUPS[ident]
            out.extend([Spacer(1,8),photo(b.ROOT/'assets/evidence/print-2026-10-24'/filename,516,max_height)])
            for other in item['images']:
                if other['id'] in covers:
                    out.append(Paragraph(html.escape(other['observation']),body));shown.add(other['id'])
        else:
            # The exact observation is sufficient alongside its original record;
            # redundant facsimiles are omitted, not their factual contents.
            out.append(Paragraph(html.escape(im['observation']),body));shown.add(ident)
    assert shown=={x['id'] for x in item.get('images',[])}
    return out

def staged(b,path,evidence,bank,confirmed):
    from visible_evidence import exhibits
    sheets=[]
    for release in evidence['releases']:
        act=ACTS[release['key']];items=exhibits(evidence,release,confirmed)
        byid={i['id']:copy.deepcopy(i) for i in items}
        if 'original_interview' in byid:
            byid['original_interview']['paragraphs']=bank['pre_method_press_interview_opening']
            if not bank['pre_method_press_interview_opening']:del byid['original_interview']
        if release['key']!='before_method':
            # The two Opportunity records comfortably share one sheet.
            blocks=[]
            for item in byid.values():blocks.extend(content(b,item)+[Spacer(1,12)])
            sheets.append((act,blocks));continue
        # Keep source records and comparisons together. Related shorter files
        # share one sheet, with no new interpretations or conclusion labels.
        groups=[['original_source'],['actual_service'],['original_interview','camera_work'],['production_originals'],['visitor_route','governing_papers'],['collection_working_proof'],['collector_working_folder'],['press_source_folder','preview_image_custody'],['work_and_settlement']]
        for group in groups:
            blocks=[]
            for ident in group:
                if ident not in byid:continue
                item=byid[ident]
                if blocks:blocks.append(Spacer(1,14))
                if ident=='original_source':
                    # The lengthy source record plus three observations needs
                    # two legible sheets, rather than shrinking its text.
                    sheets.append((act,content(b,item)))
                    body,heading,sub=styles(b)
                    blocks=[Paragraph('The acquired bottle / retained comparisons',heading)]+retained(b,item,250)
                else:blocks.extend(content(b,item)+retained(b,item,160))
            if blocks:sheets.append((act,blocks))
    return build_pages(b,path,'Staged evidence',sheets)
