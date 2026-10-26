"""Native three-artifact Method folios, paired with the approved photo sheets."""
import copy,html,io,json
from pathlib import Path
import fitz
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader

def render_sources(b,path,spec,bank):
    ROOT=b.ROOT
    data=copy.deepcopy(spec)
    data['pages'][2]['groups'][0]['lines']=bank['pre_method_press_interview_opening']
    INK=HexColor('#202426');RED=HexColor('#741f31');MUTED=HexColor('#596266');LINE=HexColor('#adb2b2');PALE=HexColor('#f1f2ef')
    pdf=path
    c=canvas.Canvas(str(pdf),pagesize=(612,792),invariant=1)
    c.setTitle('Act III: three replacement artifacts');c.setAuthor('The Last Acquisition')
    def rect(x,y,w,h,fill=white,stroke=LINE):
     c.setFillColor(fill);c.setStrokeColor(stroke);c.setLineWidth(.6);c.rect(x,792-y-h,w,h,fill=1,stroke=1)
    def text(s,x,y,w=516,size=16,font='Helvetica',color=INK,leading=None):
     markup=html.escape(s).replace('\n','<br/>')
     p=Paragraph(markup,ParagraphStyle('a',fontName=font,fontSize=size,leading=leading or size*1.2,textColor=color))
     _,h=p.wrap(w,10000);assert y+h<=756,(s[:35],y+h)
     p.drawOn(c,x,792-y-h);return y+h
    def markup(s,x,y,w=516,size=16,font='Helvetica',color=INK,leading=None):
     p=Paragraph(s,ParagraphStyle('a',fontName=font,fontSize=size,leading=leading or size*1.2,textColor=color));_,h=p.wrap(w,10000)
     assert y+h<=756,(s[:35],y+h);p.drawOn(c,x,792-y-h);return y+h
    def rule(y,x=42,w=528):
     c.setStrokeColor(LINE);c.setLineWidth(.7);c.line(x,792-y,x+w,792-y)
    def label(s,y,x=48,w=516):return text(s,x,y,w,10,'Helvetica-Bold',MUTED)+5
    def title(s,y,x=48,w=516,size=20):return text(s,x,y,w,size,'Helvetica-Bold',INK)+8
    def pagehead(page):
     text('ACT III: METHOD',42,22,528,12,'Helvetica-Bold',RED)
     text(page['title'],42,45,528,25,'Helvetica-Bold',INK)
     rule(84)

    # Estate: one private recording, followed by the actual slips, not a narrator's report.
    p=data['pages'][0];pagehead(p);g=p['groups'][0]
    y=label(g['source'],101)
    rect(42,y-2,528,172,PALE)
    vy=y+12
    for para in g['paragraphs']:
     vy=text(para,56,vy,500,16,'Helvetica',leading=19)+5
    assert vy<y+170,('video overflow',vy,y)
    y=y+183;g=p['groups'][3];y=label(g['source'],y);y=text(g['text'],48,y,516,15)+4;y=text(g['status'],48,y,516,12,'Helvetica-Bold',RED)+11;g=p['groups'][1];y=label(g['source'],y);y=text(g['text'],48,y,516,15)+12
    g=p['groups'][2];y=label(g['source'],y);y=title(g['title'],y,size=18)
    for a,z in g['rows']:
     y0=y
     ya=text(a,48,y,180,14,'Helvetica-Bold');yz=text(z,242,y,322,15)
     y=max(ya,yz)+4;rule(y-2,48,516)
    g=p['groups'][4];y=label(g['source'],y+9);y=text(g['text'],48,y,516,15);print('estate bottom',y);c.showPage()

    # Collection file: receiving, correspondence, date slips, and register are separate originals.
    p=data['pages'][1];pagehead(p);y=99
    g=p['groups'][0];y=label(g['source'],y);y=text(g['text'],48,y,516,16)+12;rule(y);y+=13
    g=p['groups'][1];y=label(g['source']+' / DR. ART E. FACT TO INTAKE',y)
    y=text(g['text'],48,y,516,16)+7
    y=markup('<b>Intake reply:</b> '+html.escape(g['reply']),48,y,516,16)+9
    y=text(g['distribution'],48,y,516,13)+9
    y=markup('<b>Press proof:</b> Contents inert. <strike color="#741f31">'+html.escape(g['strike'])+'</strike>',48,y,516,16)+15
    g=p['groups'][2];y=label(g['source'],y);y=title(g['title'],y,size=17)
    ends=[]
    for x,(a,z) in zip([48,315],g['rows']):
     rect(x,y,249,63,PALE);e=text(a,x+10,y+8,230,11,'Helvetica-Bold');ends.append(text(z,x+10,e+5,230,19,'BookBold'))
    y=y+75
    g=p['groups'][3];y=label(g['source'],y)
    for a,z in g['rows']:
     ya=text(a,48,y,165,14,'Helvetica-Bold');yz=text(z,225,y,339,15);y=max(ya,yz)+4;rule(y-2,48,516)
    print('collection bottom',y);c.showPage()

    # Press desk: literal spoken lines, original film frames, import receipt, installed plan.
    p=data['pages'][2];pagehead(p);y=99;g=p['groups'][0]
    y=label(g['source'],y)
    for line in g['lines']:
     speaker,body=line.split(': ',1)
     # Names are speaker labels, not interpretive topic headings.
     y=markup('<b>'+html.escape(speaker)+':</b> '+html.escape(body),48,y,516,15,'Book',leading=17.5)+5
    y+=7;g=p['groups'][1];y=label(g['source'],y)
    with Image.open(ROOT/'assets/evidence/print-2026-10-24/studio_take.png') as im:
     # Crop viewport selects the existing studio-film row; no image content is altered.
     crop=im.crop((0,0,im.width,int(im.height*.49)));buf=io.BytesIO();crop.save(buf,format='JPEG',quality=94);buf.seek(0)
    c.drawImage(ImageReader(buf),48,792-y-94,width=250,height=94,preserveAspectRatio=True,anchor='c')
    end=text(g['text'],315,y,249,14)
    y=max(y+94,end)+12
    g=p['groups'][2];y=label(g['source'],y);y=text(g['text'],48,y,516,14)+6;y=text(g['aside'],48,y,516,14)+12
    g=p['groups'][3];y=label(g['source'],y)
    for a,z in g['rows']:
     ya=text(a,48,y,165,13,'Helvetica-Bold');yz=text(z,225,y,339,14);y=max(ya,yz)+5
    y=text(g['note'],48,y+5,516,14)
    print('press bottom',y);c.save()


def render_all(b,directory,bank):
    import act3_editorial as approved
    spec=json.loads((b.ROOT/'source/act3_artifacts.json').read_text(encoding='utf-8'))
    old=approved.load(b.ROOT)['pages']
    fixed=[next(p for p in old if p['layout']==k) for k in ['bottle','toast','comparisons']]
    paths=[];ledger=[]
    for n,p in enumerate(fixed[:2]):
        dest=directory/f'{n+4:02}-method.pdf';ledger.append(approved.render(b,dest,p,bank));paths.append(dest)
    aggregate=directory/'native-artifacts.pdf';render_sources(b,aggregate,spec,bank)
    with fitz.open(aggregate) as doc:
        assert len(doc)==3
        for i,page in enumerate(doc):
            dest=directory/f'{i+6:02}-method.pdf';one=fitz.open();one.insert_pdf(doc,from_page=i,to_page=i);one.save(dest);one.close();paths.append(dest);ledger.append({'title':spec['pages'][i]['title'],'blocks':[g['id'] for g in spec['pages'][i]['groups']]})
    aggregate.unlink()
    dest=directory/'09-method.pdf';ledger.append(approved.render(b,dest,fixed[2],bank));paths.append(dest)
    return paths,ledger
