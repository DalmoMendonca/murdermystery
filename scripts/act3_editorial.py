"""Dinner-readable evidence: edited copy and labeled, full-size comparisons."""
import html,io,json
from PIL import Image as PILImage
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

def load(root):
    return json.loads((root/'source/act3_editorial.json').read_text(encoding='utf-8'))

def record_grid(b,s,page):
    """Eight short record excerpts, with a stable reading order across each row."""
    s.block('ACT III: METHOD',36,20,540,16,'BookBold',b.RED)
    s.block(page['title'],36,46,540,26,'BookBold',b.RED)
    s.line(36,84,576,84)
    body=ParagraphStyle('record-excerpt',fontName='Book',fontSize=16,leading=19,textColor=b.INK,allowWidows=0,allowOrphans=0)
    title=ParagraphStyle('record-label',parent=body,fontName='BookBold',fontSize=16,leading=19,textColor=b.RED)
    y=98;ledger=[]
    for start,item in enumerate(page['blocks']):
        markup=html.escape(item['text'])
        if item.get('strike'):
            phrase=html.escape(item['strike'])
            assert phrase in markup
            markup=markup.replace(phrase,'<strike color="#720f29">'+phrase+'</strike>')
        markup='<font color="#720f29"><b>'+html.escape(item['heading'])+'.</b></font> '+markup
        paragraph=Paragraph(markup,body);_,height=paragraph.wrap(540,10000)
        rowheight=height
        ledger.append(round(rowheight,1))
        assert y+rowheight<=744,(page['title'],'row',start+1,'bottom',y+rowheight,'heights',ledger)
        paragraph.drawOn(s.c,36,792-y-height)
        y+=rowheight+8
        if start+1<len(page['blocks']):s.line(36,y-4,576,y-4)
    s.save()
    return {'title':page['title'],'bottom':y-8,'row_heights':ledger,'blocks':[i['id'] for i in page['blocks']]}

def render(b,path,page,bank):
    s=b.Sheet(path,page['title']);blocks={x['id']:x for x in page['blocks']}
    if page['layout'] in ['record-grid','museum-grid']:return record_grid(b,s,page)
    def text(value,y,size=17,x=48,w=516,font='Book',color=None):
        return s.block(value,x,y,w,size,font,color or b.INK,bottom=744)
    def heading(value,y):return text(value,y,19,font='BookBold',color=b.RED)+7
    def block(ident,y,show_heading=True,size=17):
        item=blocks[ident]
        if show_heading and item.get('heading'):y=heading(item['heading'],y)
        return text(item['text'],y,size)+11
    def panel(filename,rect,x,y,w,h):
        # PDF viewport, not an edited raster: source pixels and proportions stay intact.
        path=b.ROOT/'assets/evidence/print-2026-10-24'/filename
        with PILImage.open(path) as im:
            iw,ih=im.size;data=io.BytesIO();im.convert('RGB').save(data,format='JPEG',quality=93,subsampling=0)
        data.seek(0);u0,v0,u1,v1=rect
        scale=min(w/((u1-u0)*iw),h/((v1-v0)*ih))
        dw,dh=(u1-u0)*iw*scale,(v1-v0)*ih*scale
        px,py=x+(w-dw)/2,y+(h-dh)/2
        c=s.c;c.saveState();clip=c.beginPath();clip.rect(px,792-py-dh,dw,dh);c.clipPath(clip,stroke=0,fill=0)
        c.drawImage(ImageReader(data),px-u0*iw*scale,792-py-dh-(1-v1)*ih*scale,width=iw*scale,height=ih*scale)
        c.restoreState()
    def label(value,x,y,w=246):return text(value,y,15,x,w,'BookBold',b.RED)
    text('ACT III: METHOD',26,16,font='BookBold',color=b.RED)
    y=text(page['title'],70,30,font='BookBold',color=b.RED)+6
    if page['layout']=='plans':y+=1
    else:y=text(page['subtitle'],y,13,font='BookItalic')+13
    s.line(48,y,564,y);y+=18
    kind=page['layout']
    if kind=='bottle':
        y=block('bottle-preview',y)
        label('Front of Bottle',48,y);label('Back of Seal',318,y)
        y+=25
        panel('bottle_closure.png',(0,0,.492,.492),48,y,246,137)
        panel('bottle_closure.png',(.508,0,1,.492),318,y,246,137)
        y+=148;y=block('seal',y,False)
        label('Unused Sealing Paper',48,y);label('Scrap from Grant’s Glass',318,y)
        y+=24
        panel('bottle_closure.png',(0,.508,.492,1),48,y,246,133)
        panel('bottle_closure.png',(.508,.508,1,1),318,y,246,133)
        y+=146;y=block('paper-match',y,False)
    elif kind=='toast':
        y=block('flavoring',y)
        # A readable comparison, with explicit analyte names and no slash shorthand.
        cols=[(48,230),(288,122),(426,138)]
        for (x,w),name in zip(cols,['Sample','Cyanide','Flavoring']):text(name,y,15,x,w,'BookBold',b.RED)
        y+=29
        for row in page['results']:
            for (x,w),value in zip(cols,[row['sample'],row['cyanide'],row['flavoring']]):text(value,y,16,x,w)
            s.line(48,y+24,564,y+24);y+=30
        y+=10
        label('Before the Toast',48,y);label('Grant Drinking',318,y);y+=24
        panel('glass_service.png',(0,0,.493,1),48,y,246,110)
        panel('glass_service.png',(.507,0,1,1),318,y,246,110)
        y+=121;y=block('glass',y,False)
        y=block('camera',y);y=block('demo',y,False,16)
    elif kind=='recordings':
        # Explicitly a recorder's log, not invented verbatim dialogue.
        original='\n'.join(bank['pre_method_press_interview_opening'])
        assert all(name in original for name in ['PAIGE:','ROBIN:']), 'Re-edit log for a changed attendance edition'
        y=heading(blocks['interview']['heading'],y)
        for entry in blocks['interview']['text'].split('\n\n'):
            y=text(entry,y,16)+4
        y+=7
        for ident in ['film','podcast','photo-files']:y=block(ident,y,size=16)
    elif kind=='paperwork':
        y=block('purchase',y)
        y=block('keys',y,False,16)
        top=y
        # Actual correspondence, with the named sender and the literal removed sentence.
        y=heading(blocks['query']['heading'],y+10)
        y=text(blocks['query']['text'],y,16)+10
        y=text('Museum’s Reply: '+blocks['reply']['text'],y,17,font='BookBold',color=b.RED)+13
        y=text(blocks['deletion']['heading'],y,16,font='BookBold',color=b.RED)+6
        deleted=blocks['deletion']['text'];baseline=y
        y=text(deleted,y,16)+9
        from reportlab.pdfbase.pdfmetrics import stringWidth
        s.c.setStrokeColor(b.RED);s.c.setLineWidth(1.1)
        s.c.line(48,792-baseline-10,48+stringWidth(deleted,'Book',16),792-baseline-10)
        y=block('copies',y,False,16)
        s.line(48,y,564,y);y+=15
        heights=[]
        for x,date in zip([48,318],page['dates']):
            end=text(date['label'],y,15,x,246,'BookBold',b.RED)+7
            heights.append(text(date['date'],end,20,x,246,'BookBold'))
        y=max(heights)+10;y=block('dates',y,False,16)
    elif kind=='plans':
        ends=[]
        for x,ids in [(48,['gift','announcement-copies','family-seat']),(318,['ownership','old-policy'])]:
            cy=y
            for ident in ids:
                item=blocks[ident]
                if item.get('heading'):cy=text(item['heading'],cy,19,x,246,'BookBold',b.RED)+7
                cy=text(item['text'],cy,16,x,246)+9
            ends.append(cy)
        y=max(ends)+14;s.line(48,y,564,y);y+=18
        y=block('final-plans',y,size=16);y=block('tour',y,size=16)
    elif kind=='accounts':
        for ident in ['sales','valuation','sculpture','payments','school-budget','gallery-photo']:y=block(ident,y,size=16)
    elif kind=='comparisons':
        y=heading('The Artist’s Reference',y)
        label('Painted Wooden Model',48,y);label('Historic Glass Bottle',318,y);y+=24
        panel('artist_reference.png',(0,0,.496,1),48,y,246,164)
        panel('artist_reference.png',(.504,0,1,1),318,y,246,164)
        y+=176;y=block('model',y,False,16)
        y=heading(blocks['frame']['heading'],y+7)
        label('Before Delivery: Intact',48,y);label('On Arrival: New Crack',318,y);y+=24
        panel('frame_condition_pair.png',(0,0,.496,1),48,y,246,164)
        panel('frame_condition_pair.png',(.504,0,1,1),318,y,246,164)
        y+=176;y=block('frame',y,False,16)
    assert y<=755,(page['title'],'bottom',y)
    s.save()
    return {'title':page['title'],'bottom':y,'blocks':[x['id'] for x in page['blocks']]}

def render_all(b,directory,bank):
    pages=load(b.ROOT)['pages'];paths=[];ledger=[]
    for n,page in enumerate(pages):
        dest=directory/f'{n+4:02}-method.pdf'
        ledger.append(render(b,dest,page,bank));paths.append(dest)
    return paths,ledger
