"""Printable visuals for the frozen retained observations; no new clue facts."""
from reportlab.platypus import Image,Paragraph,Spacer,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.shapes import Drawing,Rect,String,Line,Circle
from reportlab.lib.colors import HexColor
from PIL import Image as PILImage
import html
import io

PHOTO_GROUPS={
 'wide_preview':('bottle_closure.png',{'wide_preview','closure_comparison'},'Open preview / rear split / retained stock / glass scrap'),
 'prepared_place':('glass_service.png',{'prepared_place','consumed_toast'},'Prepared place / delivered toast'),
 'frame_condition_pair':('frame_condition_pair.png',{'frame_condition_pair'},'Before delivery / receiving photograph'),
 'studio_take':('studio_take.png',{'studio_take'},'Studio film frames / textile slide contact sheet'),
 'artist_reference':('artist_reference.png',{'artist_reference'},'Joined studio model / historical glass bottle'),
}

def condition_record(b):
    """Facsimiles implement the exact two dates and same signed treatment."""
    d=Drawing(512,230)
    for x,label,date in [(0,'ORIGINAL RECORD','October 30, 2026'),(264,'INSURANCE COPY','October 29, 2026')]:
        d.add(Rect(x,0,248,226,fillColor=b.PALE,strokeColor=b.GOLD,strokeWidth=.7))
        for yy,text,size,font,color in [(201,'MERIDIAN / CONSERVATION',12,'BookBold',b.RED),(176,label,16,'BookBold',b.INK),(144,'Closure-band treatment',14,'Book',b.INK),(111,date,20,'BookBold',b.RED),(75,'Red foil-backed paper',14,'Book',b.INK),(52,'Across the stopper',14,'Book',b.INK),(21,'Signed: Chip Patina',14,'BookItalic',b.INK)]:
            d.add(String(x+13,yy,text,fontName=font,fontSize=size,fillColor=color))
    return d

def camera_order(b):
    """A technician's diagram, not an invented camera photograph or model."""
    d=Drawing(512,220)
    d.add(Rect(160,74,214,126,fillColor=HexColor('#eeeae4'),strokeColor=b.INK))
    d.add(String(178,172,'PRIVATE-ROOM CAMERA',fontName='BookBold',fontSize=15,fillColor=b.INK))
    d.add(String(182,130,'POWER',fontName='BookBold',fontSize=13,fillColor=b.RED))
    d.add(String(274,130,'NETWORK',fontName='BookBold',fontSize=13,fillColor=b.INK))
    d.add(Circle(209,95,7,strokeColor=b.INK,fillColor=None))
    d.add(Rect(290,88,23,15,strokeColor=b.INK,fillColor=None))
    # Visible gap between barrel plug and empty power socket.
    d.add(Line(30,40,140,40,strokeColor=b.RED,strokeWidth=3))
    d.add(Line(140,40,164,65,strokeColor=b.RED,strokeWidth=3))
    d.add(Rect(160,60,18,10,strokeColor=b.RED,fillColor=b.RED))
    d.add(Line(178,65,187,65,strokeColor=b.RED,strokeWidth=2))
    d.add(Line(301,88,301,40,strokeColor=b.INK,strokeWidth=3))
    d.add(Line(301,40,485,40,strokeColor=b.INK,strokeWidth=3))
    d.add(String(12,12,'Power adapter: unplugged',fontName='BookBold',fontSize=14,fillColor=b.RED))
    d.add(String(285,12,'Network lead: attached',fontName='BookBold',fontSize=14,fillColor=b.INK))
    return d

def marked_proof(b):
    d=Drawing(512,330)
    d.add(Rect(0,0,512,328,fillColor=b.PALE,strokeColor=b.GOLD,strokeWidth=.7))
    def line(y,text,size=14,font='Book',color=None):
        d.add(String(18,y,text,fontName=font,fontSize=size,fillColor=color or b.INK))
    line(302,'CATALOG / WORKING PROOF',20,'BookBold',b.RED)
    line(274,'October 29, 2026 / Dr. Art E. Fact',15,'BookBold')
    line(243,'Seller requires original contents. Lender calls contents inert.',15)
    line(222,'Please clarify before opening.',15)
    line(189,'INTAKE REPLY: Unresolved. Keep closed.',16,'BookBold',b.RED)
    line(147,'Reed DeLabel / PRESS MARKUP',15,'BookBold')
    line(116,'Purchase condition requires original contents to remain.',15)
    d.add(Line(17,121,463,121,strokeColor=b.RED,strokeWidth=1.3))
    line(73,'STAFF COPY: full query and seller attachment retained',14)
    line(43,'PRESS COPY: shortened inert caption',14)
    return d

def pages(b,section,heading,sub,body):
    """One self-contained, readable exhibit view per page/group."""
    images=section['images'];byid={x['id']:x for x in images};shown=set();story=[]
    def p(text,style=body):return Paragraph(html.escape(str(text)),style)
    for image in images:
        ident=image['id']
        if ident in shown:continue
        if story and ident not in PHOTO_GROUPS and ident not in {'insurance_comparison','unplugged_camera','marked_catalog_proof'}:
            # A short agency caption belongs beside its companion comparison,
            # not alone on a nearly empty extra sheet.
            story.extend([Spacer(1,18),p('Retained observation / '+ident.replace('_',' '),sub),p(image['observation'])]);shown.add(ident)
            continue
        story.extend([PageBreak(),p(section.get('department','MERIDIAN MUSEUM / 2026'),sub),p(section['title']+' / retained views',heading)])
        group=PHOTO_GROUPS.get(ident)
        if group:
            filename,covers,label=group;path=b.ROOT/'assets/evidence/print-2026-10-24'/filename
            assert path.is_file(),path
            # Export encoding only; preserve original generated PNGs in assets.
            # Full-resolution JPEG inside PDF avoids enormous repeated Flate
            # image streams without resizing or altering the exhibit geometry.
            with PILImage.open(path) as im:
                w,h=im.size;encoded=io.BytesIO();im.convert('RGB').save(encoded,format='JPEG',quality=93,subsampling=0)
            encoded.seek(0)
            scale=min(512/w,386/h)
            photo=Image(encoded,width=w*scale,height=h*scale);photo.hAlign='CENTER'
            story.extend([photo,Spacer(1,12),p(label,sub),Spacer(1,5)])
            for key in [x['id'] for x in images if x['id'] in covers]:
                story.append(p(byid[key]['observation']));shown.add(key)
        elif ident=='insurance_comparison':
            story.extend([condition_record(b),Spacer(1,18),p(image['observation'])]);shown.add(ident)
        elif ident=='unplugged_camera':
            story.extend([p('Technician\'s connection diagram',sub),camera_order(b),Spacer(1,18),p(image['observation'])]);shown.add(ident)
        elif ident=='marked_catalog_proof':
            story.extend([marked_proof(b),Spacer(1,18),p(image['observation'])]);shown.add(ident)
        else:
            # Secondary absent-role references retain their exact observations;
            # they are not mislabeled as generated photographic proof.
            story.extend([p('Retained observation / '+ident.replace('_',' '),sub),p(image['observation'])]);shown.add(ident)
    assert shown==set(byid)
    return story
