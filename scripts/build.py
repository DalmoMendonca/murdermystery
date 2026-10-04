"""Measured museum-gala layouts. Build fonts are never included in downloads."""
from pathlib import Path
import shutil
import json,re,html,zipfile,io,urllib.request,hashlib
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import pdfdoc
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor,white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,SimpleDocTemplate,Table,TableStyle,PageBreak
from pypdf import PdfWriter
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site';WORK=ROOT/'build';SRC=ROOT/'source/v1'
KIT=SITE/'downloads/current/The_Last_Acquisition_Complete_Kit'
INK=HexColor('#132e38');TEAL=HexColor('#057294');RED=HexColor('#8b2636');W,H=612,792
AUDIT=[]
# JPEG colour plus a lossless native alpha mask avoids repeating megabytes of
# uncompressed frame colour in each downloadable player book.
_ImageXObject=pdfdoc.PDFImageXObject
class AlphaJPEGXObject(_ImageXObject):
    def loadImageFromSRC(self,im):
        super().loadImageFromSRC(im)
        if getattr(im,'print_alpha',None) is not None:
            im._dataA=im.print_alpha
            self.mask='auto'
            self._checkTransparency(im)
pdfdoc.PDFImageXObject=AlphaJPEGXObject
GAME=json.loads((ROOT/'source/game.json').read_text(encoding='utf-8'))
def fonts():
    dest=WORK/'fonts';dest.mkdir(parents=True,exist_ok=True)
    if not (dest/'Libron-Regular.ttf').exists():
        data=urllib.request.urlopen('https://github.com/nicoverbruggen/libron/releases/download/v0.25/Libron.zip').read()
        assert hashlib.sha256(data).hexdigest()==(ROOT/'scripts/font.sha256').read_text().strip()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for style in ['Regular','Bold','Italic','BoldItalic']:(dest/f'Libron-{style}.ttf').write_bytes(z.read(f'Libron-{style}.ttf'))
    for name,style in [('Book','Regular'),('BookBold','Bold'),('BookItalic','Italic'),('BookBoldItalic','BoldItalic')]:pdfmetrics.registerFont(TTFont(name,str(dest/f'Libron-{style}.ttf')))
    pdfmetrics.registerFontFamily('Book',normal='Book',bold='BookBold',italic='BookItalic',boldItalic='BookBoldItalic')
def flat(s):return ' '.join(s.split())
def para(s,width,size=14,font='Book',color=INK):
    missing={ord(ch) for ch in s if not ch.isspace() and ord(ch) not in pdfmetrics.getFont(font).face.charToGlyph}
    assert not missing,f'Unsupported glyphs: {sorted(missing)}'
    p=Paragraph(html.escape(s).replace('\n','<br/>'),ParagraphStyle('p',fontName=font,fontSize=size,leading=size*1.25,textColor=color,allowWidows=0,allowOrphans=0))
    _,height=p.wrap(width,10000);return p,height
class Sheet:
    def __init__(self,path,title,size=(W,H)):
        path.parent.mkdir(parents=True,exist_ok=True);self.path=path;self.w,self.h=size;self.page=1
        self.c=canvas.Canvas(str(path),pagesize=size,invariant=1);self.c.setTitle(title);self.c.setAuthor('The Meridian Museum')
    def block(self,s,x,y,width,size=14,font='Book',color=INK,bottom=744):
        p,h=para(s,width,size,font,color);assert y+h<=bottom,f'{self.path.name} p{self.page}: overflow {s[:50]} {y+h:.1f}>{bottom}'
        p.drawOn(self.c,x,self.h-y-h);AUDIT.append(dict(file=str(self.path.relative_to(KIT)),page=self.page,x=x,y=y,width=width,height=h,size=size,text=s));return y+h
    def rect(self,x,y,w,h,fill=None,stroke=INK,dash=None):
        c=self.c;c.saveState();c.setLineWidth(.7);c.setStrokeColor(stroke)
        if dash:c.setDash(dash)
        if fill:c.setFillColor(fill)
        c.rect(x,self.h-y-h,w,h,fill=int(fill is not None),stroke=1);c.restoreState()
    def line(self,x,y,x2,y2):self.c.setStrokeColor(INK);self.c.setLineWidth(.6);self.c.line(x,self.h-y,x2,self.h-y2)
    def image(self,path,x,y,width,height):
        assert path.exists(),f'Missing portrait: {path}'
        # Print derivatives retain the full composition, at >=192 dpi for portraits.
        # The full-resolution generated portrait is preserved in assets and downloads.
        with Image.open(path) as im:
            alpha='A' in im.getbands();im=im.convert('RGBA' if alpha else 'RGB');im.thumbnail((900,900) if 'ornaments' in path.parts else (480,480) if alpha else (900,900))
            stream=io.BytesIO()
            if alpha and 'ornaments' in path.parts:
                im.convert('RGB').save(stream,format='JPEG',quality=88,subsampling=1)
                stream.seek(0);reader=ImageReader(stream)
                reader.print_alpha=ImageReader(im.getchannel('A'))
            elif alpha:im.save(stream,format='PNG',optimize=True)
            else:im.save(stream,format='JPEG',quality=88,subsampling=1)
            stream.seek(0)
            if not (alpha and 'ornaments' in path.parts):reader=ImageReader(stream)
            iw,ih=im.size;scale=min(width/iw,height/ih);w,h=iw*scale,ih*scale
            self.c.drawImage(reader,x+(width-w)/2,self.h-y-(height-h)/2-h,w,h,mask='auto')
    def header(self,label,private=False):
        self.block('MERIDIAN / 2026',42,28,self.w-84,14,'BookBold',TEAL);self.block(label,42,55,self.w-84,14,'BookBold',RED if private else INK);self.line(42,82,self.w-42,82)
    def footer(self,s='The Last Acquisition / Treasures of the World'):self.block(s,42,self.h-32,self.w-84,12,'Book',TEAL,bottom=self.h-10)
    def next(self):self.c.showPage();self.page+=1
    def save(self):self.c.save()
def merge(paths,out):
    writer=PdfWriter()
    for path in paths:writer.append(str(path))
    writer.compress_identical_objects()
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('wb') as f:writer.write(f)
    writer.close()
def load_doc(key):
    p=SRC/f'{key}.md';text=p.read_text(encoding='utf-8') if p.exists() else '\n'.join(p.read_text(encoding='utf-8') for p in sorted((SRC/key).glob('*.md')))
    pairs=json.loads((ROOT/'source/name_map.json').read_text(encoding='utf-8'));lookup=dict(pairs)
    text=re.sub('|'.join(re.escape(k) for k in sorted(lookup,key=len,reverse=True)),lambda m:lookup[m[0]],text)
    return text.replace('VOSS COLLECTION','LARCENY COLLECTION')
def preparty(chars):
    import printable_v2
    return printable_v2.poster(chars,__import__(__name__))

def card_document(path,title,cards,per_page=2):
    s=Sheet(path,title)
    for start in range(0,len(cards),per_page):
        s.header(title);height=620/per_page
        for row,(label,heading,body,kind) in enumerate(cards[start:start+per_page]):
            y=101+row*(height+5);s.rect(42,y,528,height-7,dash=[3,3]);a=s.block(label,60,y+16,492,14,'BookBold',TEAL)+12
            a=s.block(heading,60,a,492,22 if per_page==2 else 20,'BookBold')+12
            s.block(body,60,a,492,16 if per_page==2 else 14,'BookItalic' if kind=='note' else 'Book',bottom=y+height-22)
        s.footer('The Meridian Museum / Cut dashed borders / Print at 100%')
        if start+per_page<len(cards):s.next()
    s.save()
def clues():
    import evidence_design,sys
    evidence_design.build_evidence(sys.modules[__name__])
def props(chars):
    parts=[];animals=GAME['animals']
    s=Sheet(KIT/'OPEN_FREELY/Animal_Draw_Cards.pdf','Animal draw cards')
    for n in range(4):
        names=animals[(n%2)*15:(n%2+1)*15];label='PLAYER BOWL A' if n<2 else 'MURDERER BOWL B'
        s.header(label+' / Matching animal set')
        for i,name in enumerate(names):
            x=42+(i%3)*181;y=109+(i//3)*122;s.rect(x,y,166,106,dash=[3,3]);s.block(name,x+10,y+38,146,19,'BookBold',TEAL)
        s.footer('Memorize and return / Remove unused A animals from matching B')
        if n<3:s.next()
    s.save();parts.append(s.path);s=Sheet(KIT/'OPEN_FREELY/Final_Ballots.pdf','Final ballots');s.header('FINAL BALLOTS / Cut dashed borders')
    for top in [100,424]:
        s.rect(42,top,528,305,dash=[3,3]);s.block('The Last Acquisition / Final ballot',58,top+13,496,22,'BookBold',TEAL)
        for j,label in enumerate(['Your character','Accused murderer','Strongest evidence','Motive','Best Actor','Best Costume']):
            y=top+56+j*38;s.block(label,58,y,200,14,'BookBold');s.line(245,y+21,554,y+21)
    s.footer('One ballot per guest / Tally murderer votes first');s.save();parts.append(s.path)
    signs=[('FOUNDERS HALL','Gala floor / Ballots / Evidence table'),('GRAND GALLERY','Treasures of the World'),('SCULPTURE COURT','Buffet & hospitality'),('CONSERVATION LAB','Materials & condition reports'),('MOVING IMAGE GALLERY / ARCHIVES','Press & audiovisual materials'),('SILK ROAD GALLERY','World cultures'),('PATRON LOUNGE','Powder room'),('DONOR SALON','Private donor meetings'),('REGISTRAR & PROVENANCE OFFICE','Shipping & collection records')]
    s=Sheet(KIT/'OPEN_FREELY/Museum_Room_Signs.pdf','Museum room signs',(792,612))
    for i,(name,desc) in enumerate(signs):
        s.rect(36,36,720,540,stroke=TEAL);s.block('MERIDIAN',62,72,668,24,'BookBold',TEAL);s.line(62,135,730,135)
        s.block(name,62,190,668,48,'BookBold',bottom=408);s.block(desc,62,431,668,23,'BookItalic',TEAL,bottom=536)
        if i<len(signs)-1:s.next()
    s.save();parts.append(s.path);merge(parts,KIT/'OPEN_FREELY/04_Host_Safe_Props.pdf')
    import printable_v2
    printable_v2.tents(chars,__import__(__name__))
    return

def invitation():
    s=Sheet(KIT/'OPEN_FREELY/06_Invitation_and_Arrival_Guide.pdf','Invitation & arrival');s.rect(30,30,552,732,stroke=TEAL)
    s.block('Treasures of\nthe World',48,48,516,40,'BookBold',TEAL,bottom=157)
    s.block('The Meridian Museum of Art & World Cultures',48,158,516,18,'BookItalic')
    for x,slug in [(48,'01_Artie_Ficial'),(224,'06_Dada_DiCapo'),(400,'07_Vincent_Van_Faux')]:
        s.rect(x,200,164,212,fill=HexColor('#f6f1e7'),stroke=TEAL)
        s.image(ROOT/'assets/portraits'/slug/'van_gogh.jpg',x+1,201,162,210)
    y=s.block('You are part of the collection.',48,431,516,24,'BookBold',TEAL)+16
    for t,size,font in [('Friday, October 30, 2026 / 6:00 PM',20,'BookBold'),(GAME['address'],18,'Book'),('The Grant Larceny Collection opens with a gala and the unveiling of the thirteenth-century Isfahan Star Bowl.',16,'Book'),('Formal gala attire with art-world flair. Costume suggestions are optional inspiration; make the role your own.',16,'Book'),('Read your character introduction before the party. Your private packet awaits you at the gala.',16,'Book')]:y=s.block(t,48,y,516,size,font,bottom=727)+12
    s.block('Opening night / The Last Acquisition / October 30, 2026',48,742,516,12,'BookItalic',TEAL,bottom=758)
    s.next();s.header('ARRIVAL / Display at check-in');y=s.block('Welcome to the Meridian',42,105,528,32,'BookBold')+24
    rules=['Memorize the animal you draw. Return the slip immediately to the closed return box. Never tell anyone your animal.','Keep phones put away. Everything you need is printed.','Introductions and hunt: read your introduction, try the social tasks and bring discoveries to the Evidence Table.','After the death, follow the three guided hearings. Read your printed answer when your turn comes; acting is optional.','Read only the words inside the speech boxes. Do not invent new locations, events or witnesses.','Your packet includes your ballot and Coming Clean page. Stop before Coming Clean until the host has collected every ballot.']
    for i,t in enumerate(rules):s.block(str(i+1),42,y,32,26,'BookBold',TEAL);y=s.block(t,89,y,481,18)+22
    s.footer('The Last Acquisition / October 30, 2026');s.save()
STYLE=ParagraphStyle('Body',fontName='Book',fontSize=14,leading=18,spaceAfter=9,allowWidows=0,allowOrphans=0,textColor=INK)
HEAD=ParagraphStyle('Head',parent=STYLE,fontName='BookBold',fontSize=20,leading=24,spaceBefore=12,spaceAfter=8,textColor=TEAL,keepWithNext=True)
def P(t,style=STYLE):
    missing={ord(ch) for ch in t if not ch.isspace() and ord(ch) not in pdfmetrics.getFont(style.fontName).face.charToGlyph}
    assert not missing,f'Unsupported glyphs: {sorted(missing)}'
    return Paragraph(html.escape(t),style)
def manual(title,sections,out,page_sections=False,body_style=STYLE):
    out.parent.mkdir(parents=True,exist_ok=True)
    story=[]
    for heading,body in sections:
        if page_sections and story:story.append(PageBreak())
        if heading:story.append(P(heading,HEAD))
        for p in re.split(r'\n\s*\n',body.strip()):
            if flat(p):story.append(P(flat(p),body_style))
    def frame(c,doc):
        c.setFillColor(TEAL);c.setFont('BookBold',14);c.drawString(42,758,'MERIDIAN / 2026');c.setFont('Book',14);c.drawString(42,733,title);c.setStrokeColor(INK);c.line(42,719,570,719);c.setFont('Book',12);c.drawString(42,24,'The Last Acquisition / '+str(doc.page))
    SimpleDocTemplate(str(out),pagesize=(W,H),leftMargin=42,rightMargin=42,topMargin=90,bottomMargin=48,title=title,author='The Meridian Museum',invariant=1).build(story,onFirstPage=frame,onLaterPages=frame)
def exhibits():
    text=load_doc('exhibits_decor').split('LOW-COST STAGING GUIDE')[0].split('THE ISFAHAN STAR BOWL',1)[1]
    text='THE ISFAHAN STAR BOWL'+text
    groups=re.findall(r'(?m)^([A-Z][A-Z &]+)\n([^\n]+)\n+([^\n]+)\n+(.+?)(?=\n[A-Z][A-Z &]+\n|\Z)',text,re.S)
    cards=[('TREASURES OF THE WORLD',name.title(),flat(place)+' / '+flat(material)+'\n\n'+flat(body),'record') for name,place,material,body in groups if name!='TREASURES OF THE WORLD'];assert len(cards)==9,len(cards)
    cards.append(('TREASURES OF THE WORLD','The Larceny Collection','The Meridian Museum of Art & World Cultures\nOpening-night gala / October 30, 2026\n\nAn exhibition of art and culture from around the world. All objects and collection histories in this party kit are fictional.','record'))
    card_document(KIT/'OPEN_FREELY/Exhibit_Placards.pdf','TREASURES OF THE WORLD / Exhibit placards',cards)
    manual('Staging the museum',[(None,load_doc('exhibits_decor').split('LOW-COST STAGING GUIDE')[1])],KIT/'OPEN_FREELY/Staging_Guide.pdf')
    merge([KIT/'OPEN_FREELY/Exhibit_Placards.pdf',KIT/'OPEN_FREELY/Staging_Guide.pdf'],KIT/'OPEN_FREELY/07_Museum_Exhibits_and_Decor.pdf')
def awards():
    s=Sheet(KIT/'OPEN_FREELY/Scavenger_Score_Sheet.pdf','Scavenger scores');s.header('SCAVENGER SCORE SHEET / One point per find');s.block('Guest / Character',42,99,440,18,'BookBold');s.block('Finds',498,99,72,18,'BookBold')
    for i in range(30):y=140+i*19;s.line(42,y,474,y);s.line(498,y,570,y)
    s.footer('Award the Curator’s Eye to the guest with the most discoveries.');s.save()
    captions=[('Best Actor','For committing fully to the role and making everyone else more fun to watch.'),('Best Costume','For arriving as if the Meridian gala had a real red carpet.'),('Curator’s Eye','For finding the most Act I scavenger clues.'),('Master Sleuth','For an innocent guest’s correct accusation supported by evidence and motive.'),('Escaped Justice','For the murderer, if they avoid the three most-accused positions.')]
    s=Sheet(KIT/'OPEN_FREELY/Award_Certificates.pdf','Award certificates')
    for i,(title,desc) in enumerate(captions):
        if i%2==0:s.header('THE MERIDIAN MUSEUM / Gala awards')
        top=100+(i%2)*320;s.rect(42,top,528,299,stroke=TEAL);s.block('TREASURES OF THE WORLD',62,top+22,488,16,'Book',TEAL);s.block(title,62,top+66,488,34,'BookBold');s.block(desc,62,top+121,488,16,'BookItalic');s.block('Awarded to',62,top+204,488,14);s.line(62,top+259,550,top+259)
        if i%2==1:s.footer('Cut each certificate at its border');s.next()
    s.block('Awarding Escaped Justice',42,431,528,22,'BookBold',TEAL);s.block('Collect and lock all ballots first. Tally the top three suspects. The top three suspects read Coming Clean from their packets. If no confession is heard, call the announced animal to stand and confess. Award Escaped Justice if the murderer was outside the top three.',42,476,528,16);s.footer('Cut each certificate at its border');s.save()
    merge([KIT/'OPEN_FREELY/Scavenger_Score_Sheet.pdf',KIT/'OPEN_FREELY/Award_Certificates.pdf'],KIT/'OPEN_FREELY/08_Awards_and_Scoring.pdf')
def readme():
    s=Sheet(KIT/'00_READ_ME_FIRST.pdf','Read me first');s.header('READ ME FIRST / Host-safe');y=s.block('The Last Acquisition',42,103,528,34,'BookBold')+12;y=s.block('October 30, 2026 / Tulsa / 15–30 guests',42,y,528,18,'BookItalic',TEAL)+20
    sections=[('OPEN FREELY','The facilitator guide, pre-party introductions, invitation, animal slips, ballots, museum signs, placards, name cards and awards are safe to inspect.'),('SEND BEFORE THE PARTY','Assign the 15 core roles first, then add optional guests. Send each guest their own single-page PDF or JPEG from PreParty_Individual, plus the invitation. Do not send private packets or the full kit to guests.'),('PRINT WITHOUT READING','Complete private packets and discoveries/reports live in PRINT_WITHOUT_READING. Print single-sided at 100%, face down. Use 10_Blind_Printing_and_Assembly.pdf to assemble complete packets by character name.'),('KEEP SEALED','The spoiler bible and editable source expose every branch. Leave SPOILERS_DO_NOT_OPEN closed if you are playing.'),('AT CHECK-IN','Give each guest their complete named packet and a pencil. Every guest draws from Bowl A, memorizes their animal and returns the slip to the closed box. Remove unused A animals from matching Bowl B before selection.')]
    for heading,body in sections:y=s.block(heading,42,y,528,16,'BookBold',TEAL)+5;y=s.block(body,42,y,528,16)+16
    s.footer('Actual size / Fonts embedded / No font installation needed');s.save()
def facilitator(chars):
    pages=json.loads((ROOT/'source/facilitator.json').read_text(encoding='utf-8'));story=[]
    for page in pages:
        if story:story.append(PageBreak())
        story.append(P(page['title'],HEAD))
        for block in page['blocks']:
            if 'heading' in block:story.append(P(block['heading'],HEAD))
            if 'text' in block:story.append(P(block['text']))
            for t in block.get('bullets',[]):story.append(P('• '+t))
            if 'table' in block:
                t=Table([[P(cell) for cell in row] for row in block['table']],colWidths=block.get('widths',[130,398]),hAlign='LEFT')
                t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.4,HexColor('#a8c4cd')),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]));story.append(t)
    def frame(c,doc):
        c.setFillColor(TEAL);c.setFont('BookBold',14);c.drawString(42,758,'MERIDIAN / 2026');c.setFont('Book',14);c.drawString(42,733,'FACILITATOR GUIDE / Open freely');c.setStrokeColor(INK);c.line(42,719,570,719);c.setFont('Book',12);c.drawString(42,24,'Host-safe / '+str(doc.page))
    SimpleDocTemplate(str(KIT/'OPEN_FREELY/01_Facilitator_Guide_SPOILER_SAFE.pdf'),pagesize=(W,H),leftMargin=42,rightMargin=42,topMargin=90,bottomMargin=48,title='Facilitator guide',invariant=1).build(story,onFirstPage=frame,onLaterPages=frame)
    import fitz
    with fitz.open(KIT/'OPEN_FREELY/01_Facilitator_Guide_SPOILER_SAFE.pdf') as doc:assert len(doc)==len(pages),'Facilitator section spilled onto an unplanned page'
def spoiler(chars):
    sections=[('Canonical murder facts','Grant Larceny dies from a botanical cardiac toxin wiped inside his silver coupe and along its rim using toxin-dampened gold-seamed linen. The empty coupe was delivered at 6:40. The murderer contaminated it between 6:40 and 6:44, before the first pour at 6:46; Grant drank at 6:49. One attending guest is selected through the memorized animal draw. Every role has a working murderer branch, and access to setup materials is widespread.\n\nThe murderer invents a late interior alcove task to cover the poisoning interval. That story relies on two obsolete assumptions: the programme’s 6:48 closure and the abandoned enclosed-cabinet proposal. In reality the alcove locked at 6:38 and the installed display was an open steel cradle with exposed padded forks, a side label rail and an external spotlight. It had no sliding glass front, brass corner posts, velvet shelf or internal lamp. The gallery’s decorative brass clock is ten minutes fast; independent watches, phones and service, camera and security records are synchronized.\n\nDishonesty alone does not identify the murderer. Eight innocent routes also invent late interior times to conceal their scandals, while describing real earlier work on the actual installation. Eight other innocent routes invent earlier cabinet errands, but their late whereabouts remain outside the alcove. Other guests refer to old proposals, legitimate early visits or the fast gallery clock. Innocent Coming Clean speeches explain their particular deceptions and resolve their private scandals. Compare the claimed time, physical work, salon access and motive against the documents. The laboratory identifies contamination, not a person; the accusation is a reasoned reconstruction rather than a laboratory certificate of guilt.\n\nAll questions, answers, hunt hints, the ballot and both Coming Clean statements are in each twelve-page packet. The cover is safe to display; page 11 is a loose ballot and page 12 is Coming Clean. All ballots lock before any Coming Clean speech. Hear all three highest-voted attending suspects, even if a confession occurs early. Only if none confesses, announce the retained murderer animal and ask its owner to stand and read the IF MURDERER confession.')]
    for c in chars:
        p=c['private'];body=[label+': '+p[key] for label,key in [('Victim relationship','history'),('Hidden complication','secret'),('Innocent route','innocent'),('Murderer route','murderer'),('Innocent Coming Clean','final_innocent'),('Murderer Coming Clean','final_murderer')]]
        body += [label+': '+c['hearing'][key] for label,key in [('Motive speech','motive'),('Opportunity / innocent','where_innocent'),('Opportunity / murderer','where_murderer'),('Method speech / both branches','evidence_innocent')]]
        sections.append((c['name'],'\n\n'.join(body)))
    bible_style=ParagraphStyle('BibleBody',parent=STYLE,spaceAfter=7)
    manual('SPOILER BIBLE / Do not open if playing',sections,KIT/'SPOILERS_DO_NOT_OPEN/99_SPOILER_BIBLE_DO_NOT_OPEN.pdf',body_style=bible_style)

def archive_entry(z,p,name):
    data=p.read_bytes()
    if p.suffix in ['.md','.json','.py','.html','.css','.toml','.txt','.csv','.sha256'] or p.name in ['.gitignore','.gitattributes']:data=data.replace(b'\r\n',b'\n')
    entry=zipfile.ZipInfo(name,(2026,1,1,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;entry._compresslevel=9;entry.create_system=3;entry.external_attr=0o100644<<16
    z.writestr(entry,data)

def package():
    with zipfile.ZipFile(SITE/'downloads/The_Last_Acquisition_Complete_Kit.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(KIT.rglob('*'),key=lambda p:p.as_posix()):
            if p.is_file():archive_entry(z,p,(Path(KIT.name)/p.relative_to(KIT)).as_posix())
    with zipfile.ZipFile(SITE/'downloads/The_Last_Acquisition_Source.zip','w',zipfile.ZIP_DEFLATED) as z:
        for base in ['source','docs','scripts','site','.impeccable','assets']:
            for p in sorted((ROOT/base).rglob('*'),key=lambda p:p.as_posix()):
                if p.is_file() and 'downloads' not in p.parts and p.suffix not in ['.ttf','.otf','.woff','.woff2','.pyc']:archive_entry(z,p,p.relative_to(ROOT).as_posix())
        for name in ['README.md','PRODUCT.md','CHANGELOG.md','requirements.txt','netlify.toml','.gitignore','.gitattributes']:archive_entry(z,ROOT/name,name)
def build_kit():
    fonts();KIT.mkdir(parents=True,exist_ok=True);chars=json.loads((ROOT/'source/characters.json').read_text(encoding='utf-8'))
    for relative in ['PRINT_WITHOUT_READING/05_Character_Evidence_Cards_PRINT_DO_NOT_READ.pdf','PRINT_WITHOUT_READING/03B_Sealed_Finales_PRINT_DO_NOT_READ.pdf','OPEN_FREELY/11_Questions_and_Notes.pdf']:
        obsolete=KIT/relative
        assert obsolete.resolve().is_relative_to(KIT.resolve())
        obsolete.unlink(missing_ok=True)
    # Clear superseded character filenames, keeping only current canonical exports.
    for folder in ['OPEN_FREELY/PreParty_Individual','PRINT_WITHOUT_READING/Secret_Individual','PRINT_WITHOUT_READING/Finale_Individual']:
        dest=KIT/folder
        if dest.exists():
            for old in dest.iterdir():
                if old.suffix in ['.pdf','.png','.jpg']:old.unlink()
            if folder.endswith('Finale_Individual'):dest.rmdir()
    preparty(chars);secret_packets(chars);play_aids(chars);clues();props(chars);invitation();exhibits();awards();readme();facilitator(chars);spoiler(chars)
    for c in chars:
        dest=KIT/'OPEN_FREELY/Portraits'/c['slug'];dest.mkdir(parents=True,exist_ok=True)
        (dest/'chibi.jpg').unlink(missing_ok=True)
        for style in ['van_gogh','picasso','chibi']:
            ext='.webp' if style=='chibi' else '.jpg'
            with Image.open(ROOT/'assets/portraits'/c['slug']/(style+ext)) as im:
                origin='Origin: fictional '+c['name']+' '+style+' portrait; built-in image_gen. Full prompt in organizer source archive.'
                im.thumbnail((900,900))
                if style=='chibi':
                    exif=Image.Exif();exif[270]='impeccable:prompt '+origin
                    im.save(dest/(style+ext),lossless=True,exif=exif)
                else:im.save(dest/(style+ext),quality=88,subsampling=1,comment=('impeccable:prompt\0'+origin).encode('utf-8'))
    import fitz
    for path in sorted((KIT/'OPEN_FREELY/PreParty_Individual').glob('*.pdf')):
        with fitz.open(path) as doc:
            assert len(doc)==1,path
            pix=doc[0].get_pixmap(matrix=fitz.Matrix(2,2))
            im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
            origin='impeccable:prompt Origin: rendered from '+path.name+' by scripts/build.py; exact portrait prompt in source/art_direction.json.'
            im.save(path.with_suffix('.jpg'),quality=90,subsampling=0,dpi=(144,144),comment=origin.encode('utf-8'))
    (WORK/'layout-ledger.json').write_text(json.dumps(AUDIT,ensure_ascii=False,indent=2),encoding='utf-8');(KIT/'README.txt').write_text('Start with 00_READ_ME_FIRST.pdf. Print at 100%, single-sided. Handle private files face down. OPEN_FREELY is host-safe; all other folders contain spoilers. Fonts are embedded.\n',encoding='utf-8')
    sync_playtest_records();package();print(f'Built {len(list(KIT.rglob("*.pdf")))} PDFs and 30 character JPEG posters')

def sync_playtest_records():
    summary=ROOT/'docs/PLAYTEST_SUMMARY.md'
    if summary.exists():shutil.copy2(summary,KIT/'OPEN_FREELY/PLAYTEST_SUMMARY.md')
    reports=ROOT/'docs/playtest'
    if reports.exists():shutil.copytree(reports,KIT/'SPOILERS_DO_NOT_OPEN/Playtest',dirs_exist_ok=True)
def secret_packets(chars):
    import printable_v2
    return printable_v2.packets(chars,__import__(__name__))

def play_aids(chars):
    s=Sheet(KIT/'OPEN_FREELY/12_Attendance_and_Hearing_Roster.pdf','Host name checklist');s.header('FACILITATOR / Host-safe')
    for half in range(2):
        if half:s.header('FACILITATOR / Host-safe')
        s.block('Hear every guest, every round',42,100,528,24,'BookBold')
        s.block('Tick Here at check-in. Use a fresh round column for every answer. Say the speaker’s full name. A guest can repeat an answer without getting a second turn.',42,145,528,14)
        for label,x,width in [('Character name',42,220),('Here',270,45),('Motive',320,65),('Opp.',400,55),('Method',470,85)]:s.block(label,x,220,width,14,'BookBold')
        for i,c in enumerate(chars[half*15:half*15+15]):
            y=257+i*28;s.block(c['name'],42,y,220,14)
            for x in [277,337,417,497]:s.rect(x,y+2,12,12)
            s.line(42,y+23,570,y+23)
        s.footer('Choose by name / Everyone answers once / All votes locked before Coming Clean');s.next()
    s.header('FACILITATOR / Ballot tally');s.block('Lock votes. Then reveal.',42,100,528,26,'BookBold')
    s.block('Attending: ______    Ballots collected: ______    Counts match: ______',42,148,528,14,'BookBold')
    s.block('After counts match, tally only attending names. Rank all their totals, including zero. Break ties alphabetically by full character name. Call the top three.',42,184,528,14)
    for half in range(2):
        x=42+half*276
        for i,c in enumerate(chars[half*15:half*15+15]):
            y=252+i*25;s.block(c['name'],x,y,198,14);s.rect(x+202,y,48,20)
    for i in range(3):s.block(f'Suspect {i+1}: _______________________   Votes: ______',42,641+i*28,528,14)
    s.block('Read every selected statement. Animal fallback only if no confession is heard.',42,725,528,12,'BookBold',TEAL)
    s.footer('Keep collected ballots folded / Guests retain packets for Coming Clean');s.save()
    s=Sheet(KIT/'OPEN_FREELY/10_Blind_Printing_and_Assembly.pdf','Complete packet assembly');s.header('OPEN FREELY / Packet assembly')
    y=s.block('One guest. One complete packet.',42,101,528,28,'BookBold')+18
    for t in ['Print one named twelve-page SECRET packet per attending guest: single-sided, 100%, face down. A non-playing helper can handle exposed text.',
              'Leave ballot page 11 loose inside. Staple other pages in order at the upper left. Orientation, hunt hints, questions, answers and Coming Clean stay with the guest.',
              'Place the covered packet facing up at the guest’s named seat, with a pencil. Keep the public introduction separate for sending before the party.',
              'If using the combined file, each consecutive twelve-page block belongs to the next name listed below. Do not read private pages while assembling.',
              'Print one host guide and name checklist. Hide Discoveries 1–16, then display any missed at hunt end. Stage reports: F1–F2 before Motive, F3 before Opportunity, F4–F5 before Method.']:
        y=s.block(t,42,y,528,14)+12
    y=s.block('Packet order / character names',42,y,528,18,'BookBold',TEAL)+9
    for row in range(15):
        for i,x in [(row,42),(row+15,318)]:s.block(chars[i]['name'],x,y,252,12)
        y+=18
    s.footer('The complete packet includes its ballot and Coming Clean page');s.save()

if __name__=='__main__':build_kit()
