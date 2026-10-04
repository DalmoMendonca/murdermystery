"""Measured museum-gala layouts. Build fonts are never included in downloads."""
from pathlib import Path
import json,re,html,zipfile,io,urllib.request,hashlib
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor,white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,SimpleDocTemplate,Table,TableStyle,PageBreak
from pypdf import PdfWriter
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site';WORK=ROOT/'build';SRC=ROOT/'source/v1'
KIT=SITE/'downloads/current/The_Last_Acquisition_Complete_Kit'
INK=HexColor('#132e38');TEAL=HexColor('#057294');RED=HexColor('#8b2636');W,H=612,792
AUDIT=[]
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
            alpha='A' in im.getbands();im=im.convert('RGBA' if alpha else 'RGB');im.thumbnail((480,480) if alpha else (900,900))
            stream=io.BytesIO()
            if alpha:im.save(stream,format='PNG',optimize=True)
            else:im.save(stream,format='JPEG',quality=92,subsampling=0)
            stream.seek(0)
            iw,ih=im.size;scale=min(width/iw,height/ih);w,h=iw*scale,ih*scale
            self.c.drawImage(ImageReader(stream),x+(width-w)/2,self.h-y-(height-h)/2-h,w,h,mask='auto')
    def header(self,label,private=False):
        self.block('MERIDIAN / 2026',42,28,self.w-84,14,'BookBold',TEAL);self.block(label,42,55,self.w-84,14,'BookBold',RED if private else INK);self.line(42,82,self.w-42,82)
    def footer(self,s='The Last Acquisition / Treasures of the World'):self.block(s,42,self.h-32,self.w-84,12,'Book',TEAL,bottom=self.h-10)
    def next(self):self.c.showPage();self.page+=1
    def save(self):self.c.save()
def merge(paths,out):
    writer=PdfWriter()
    for path in paths:writer.append(str(path))
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('wb') as f:writer.write(f)
    writer.close()
def load_doc(key):
    p=SRC/f'{key}.md';text=p.read_text(encoding='utf-8') if p.exists() else '\n'.join(p.read_text(encoding='utf-8') for p in sorted((SRC/key).glob('*.md')))
    pairs=json.loads((ROOT/'source/name_map.json').read_text(encoding='utf-8'));lookup=dict(pairs)
    text=re.sub('|'.join(re.escape(k) for k in sorted(lookup,key=len,reverse=True)),lambda m:lookup[m[0]],text)
    return text.replace('VOSS COLLECTION','LARCENY COLLECTION')
def preparty(chars):
    paths=[]
    for c in chars:
        path=KIT/'OPEN_FREELY/PreParty_Individual'/f'{c["slug"]}.pdf';s=Sheet(path,c['name'])
        s.rect(30,30,552,732,stroke=TEAL)
        s.block(c['name'],42,44,528,34,'BookBold',TEAL)
        s.block(c['role'],42,93,528,16,'Book',bottom=139);s.line(42,141,570,141)
        p=c['preparty']
        def measure(size):
            right=158+para(p['description'],324,size)[1]+12
            for item in p['relationships']:right+=para('• '+item,324,size)[1]+6
            left=414+20+6+para(p['acting'],180,size)[1]
            return max(left,right)+18+20+6+para(p['costume'],528,size)[1]
        size=next(n for n in [18,17,16] if measure(n)<=732)
        s.rect(42,158,180,230,fill=HexColor('#f6f1e7'),stroke=TEAL)
        s.image(ROOT/'assets/portraits'/c['slug']/'van_gogh.jpg',43,159,178,228)
        s.block('The Living Collection / 2026',42,394,180,12,'BookItalic',TEAL)
        y=s.block(p['description'],246,158,324,size)+12
        for item in p['relationships']:y=s.block('• '+item,246,y,324,size)+6
        a=s.block('ACTING TIPS',42,414,180,16,'BookBold',TEAL)+6
        a=s.block(p['acting'],42,a,180,size)
        y=max(y,a)+18;s.line(42,y-8,570,y-8)
        y=s.block('COSTUME SUGGESTIONS',42,y,528,16,'BookBold',TEAL)+6
        s.block(p['costume'],42,y,528,size,bottom=732)
        s.block('October 30, 2026 / Meridian Museum Gala',42,742,528,12,'Book',TEAL,bottom=758);s.save();paths.append(path)
    merge(paths,KIT/'OPEN_FREELY/02_PreParty_Character_Sheets_ALL.pdf')
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
    s=Sheet(KIT/'OPEN_FREELY/09_Host_Safe_Name_Cards.pdf','Guest name cards')
    for start in range(0,len(chars),4):
        s.header('GUEST NAME CARDS / Cut dashed borders')
        for i,c in enumerate(chars[start:start+4]):
            x=42+(i%2)*276;y=104+(i//2)*318;s.rect(x,y,252,302,dash=[3,3])
            s.block(c['card_name']['first_middle'],x+13,y+15,226,24,'BookBold',TEAL,bottom=y+47)
            s.block(c['card_name']['last'],x+13,y+48,226,29,'BookBold',TEAL,bottom=y+88)
            s.image(ROOT/'assets/portraits'/c['slug']/'chibi.webp',x+10,y+97,110,189)
            s.block(c['role'],x+133,y+105,106,14,bottom=y+268)

        s.footer('Host-safe / Display flat or attach to a place-card stand')
        if start+4<len(chars):s.next()
    s.save()
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
    rules=['Memorize the animal you draw. Return the slip immediately to the closed return box. Never tell anyone your animal.','Keep phones put away. Everything you need is printed.','Act I: introduce yourself, try the three social tasks and bring discoveries to the Evidence Table.','After the death, follow the three guided hearings. Read your printed answer when your turn comes; acting is optional.','Read only the words inside the speech boxes. Do not invent new locations, events or witnesses.','Your packet includes your ballot and Coming Clean page. Stop before Coming Clean until the host has collected every ballot.']
    for i,t in enumerate(rules):s.block(str(i+1),42,y,32,26,'BookBold',TEAL);y=s.block(t,89,y,481,18)+22
    s.footer('The Last Acquisition / October 30, 2026');s.save()
STYLE=ParagraphStyle('Body',fontName='Book',fontSize=14,leading=18,spaceAfter=9,allowWidows=0,allowOrphans=0,textColor=INK)
HEAD=ParagraphStyle('Head',parent=STYLE,fontName='BookBold',fontSize=20,leading=24,spaceBefore=12,spaceAfter=8,textColor=TEAL,keepWithNext=True)
def P(t,style=STYLE):
    missing={ord(ch) for ch in t if not ch.isspace() and ord(ch) not in pdfmetrics.getFont(style.fontName).face.charToGlyph}
    assert not missing,f'Unsupported glyphs: {sorted(missing)}'
    return Paragraph(html.escape(t),style)
def manual(title,sections,out,page_sections=False):
    out.parent.mkdir(parents=True,exist_ok=True)
    story=[]
    for heading,body in sections:
        if page_sections and story:story.append(PageBreak())
        if heading:story.append(P(heading,HEAD))
        for p in re.split(r'\n\s*\n',body.strip()):
            if flat(p):story.append(P(flat(p)))
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
    captions=[('Best Actor','For committing fully to the role and making everyone else more fun to watch.'),('Best Costume','For arriving as if the Meridian gala had a real red carpet.'),('Curator’s Eye','For finding the most Act I scavenger clues.'),('Master Sleuth','For a correct accusation supported by the strongest evidence and motive.'),('Escaped Justice','For the murderer, if they avoid the three most-accused positions.')]
    s=Sheet(KIT/'OPEN_FREELY/Award_Certificates.pdf','Award certificates')
    for i,(title,desc) in enumerate(captions):
        if i%2==0:s.header('THE MERIDIAN MUSEUM / Gala awards')
        top=100+(i%2)*320;s.rect(42,top,528,299,stroke=TEAL);s.block('TREASURES OF THE WORLD',62,top+22,488,16,'Book',TEAL);s.block(title,62,top+66,488,34,'BookBold');s.block(desc,62,top+121,488,16,'BookItalic');s.block('Awarded to',62,top+204,488,14);s.line(62,top+259,550,top+259)
        if i%2==1:s.footer('Cut each certificate at its border');s.next()
    s.block('Awarding Escaped Justice',42,431,528,22,'BookBold',TEAL);s.block('Collect and lock all ballots first. Tally the top three suspects. The top three suspects read Coming Clean from their packets. If no confession is heard, call the announced animal to stand and confess. Award Escaped Justice if the murderer was outside the top three.',42,476,528,16);s.footer('Cut each certificate at its border');s.save()
    merge([KIT/'OPEN_FREELY/Scavenger_Score_Sheet.pdf',KIT/'OPEN_FREELY/Award_Certificates.pdf'],KIT/'OPEN_FREELY/08_Awards_and_Scoring.pdf')
def readme():
    s=Sheet(KIT/'00_READ_ME_FIRST.pdf','Read me first');s.header('READ ME FIRST / Host-safe');y=s.block('The Last Acquisition',42,103,528,34,'BookBold')+12;y=s.block('October 30, 2026 / Tulsa / 15–30 guests',42,y,528,18,'BookItalic',TEAL)+20
    sections=[('OPEN FREELY','The facilitator guide, pre-party introductions, invitation, animal slips, ballots, museum signs, placards, name cards and awards are safe to inspect.'),('SEND BEFORE THE PARTY','Assign the 15 core roles first, then add optional guests. Send each guest their own single-page PDF or PNG from PreParty_Individual, plus the invitation. Do not send private packets or the full kit to guests.'),('PRINT WITHOUT READING','Complete private packets and discoveries/reports live in PRINT_WITHOUT_READING. Print single-sided at 100%, face down. Use 10_Blind_Printing_and_Assembly.pdf to assemble complete packets by character name.'),('KEEP SEALED','The spoiler bible and editable source expose every branch. Leave SPOILERS_DO_NOT_OPEN closed if you are playing.'),('AT CHECK-IN','Give each guest their complete named packet and a pencil. Every guest draws from Bowl A, memorizes their animal and returns the slip to the closed box. Remove unused A animals from matching Bowl B before selection.')]
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
    sections=[('Canonical murder facts','Grant Larceny dies from a botanical cardiac toxin applied inside his silver coupe and on its rim using toxin-dampened gold-seamed linen. The glass was clean at 6:40; he drank at 6:49. One attending guest is selected through the memorized animal draw. Every role has a working murderer branch. Only the murderer matches all three: salon entry after 6:40, cabinet key loan during setup and gold-seamed linen possession. No keys, samples or linen changed hands.\n\nAll questions, answers, preparation records, the ballot and both Coming Clean statements are in each twelve-page packet. No separate letter cards, question catalog or finale envelope. Coming Clean is the final page and remains unread until all votes are locked. The top three suspects read their appropriate statements; if none confesses, call the murderer animal to stand and confess.')]
    for c in chars:
        p=c['private'];body=[label+': '+p[key] for label,key in [('Victim relationship','history'),('Hidden complication','secret'),('Innocent route','innocent'),('Murderer route','murderer'),('Innocent Coming Clean','final_innocent'),('Murderer Coming Clean','final_murderer')]]
        body += ['Innocent preparation record: '+c['preparation_record']['innocent'],'Murderer preparation record: '+c['preparation_record']['murderer']]
        sections.append((c['name'],'\n\n'.join(body)))
    manual('SPOILER BIBLE / Do not open if playing',sections,KIT/'SPOILERS_DO_NOT_OPEN/99_SPOILER_BIBLE_DO_NOT_OPEN.pdf')

def archive_entry(z,p,name):
    data=p.read_bytes()
    if p.suffix in ['.md','.json','.py','.html','.css','.toml','.txt','.sha256'] or p.name in ['.gitignore','.gitattributes']:data=data.replace(b'\r\n',b'\n')
    entry=zipfile.ZipInfo(name,(2026,1,1,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;entry.create_system=3;entry.external_attr=0o100644<<16
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
                if old.suffix in ['.pdf','.png']:old.unlink()
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
                else:im.save(dest/(style+ext),quality=92,subsampling=0,comment=('impeccable:prompt\0'+origin).encode('utf-8'))
    import fitz
    for path in sorted((KIT/'OPEN_FREELY/PreParty_Individual').glob('*.pdf')):
        with fitz.open(path) as doc:
            assert len(doc)==1,path;doc[0].get_pixmap(matrix=fitz.Matrix(2,2)).save(str(path.with_suffix('.png')))
        png=path.with_suffix('.png');metadata=PngInfo()
        metadata.add_text('impeccable:prompt','Origin: rendered from '+path.name+' by scripts/build.py; incorporates the built-in image_gen Van Gogh portrait from assets/portraits/'+path.stem+'/van_gogh.jpg. Exact portrait prompt is in source/art_direction.json.')
        with Image.open(png) as im:im.save(png,pnginfo=metadata,dpi=(144,144))
    (WORK/'layout-ledger.json').write_text(json.dumps(AUDIT,ensure_ascii=False,indent=2),encoding='utf-8');(KIT/'README.txt').write_text('Start with 00_READ_ME_FIRST.pdf. Print at 100%, single-sided. Handle private files face down. OPEN_FREELY is host-safe; all other folders contain spoilers. Fonts are embedded.\n',encoding='utf-8')
    package();print(f'Built {len(list(KIT.rglob("*.pdf")))} PDFs and 30 character PNGs')
def speech(s,title,words,y=176,size=16):
    y=s.block(title,55,y,502,16,'BookBold',TEAL)+9
    p,h=para(words,480,size);s.rect(42,y-2,528,h+30,stroke=TEAL)
    s.block(words,66,y+10,480,size,bottom=730)
    return y+h+45

def question_pages(s,c,round_data):
    for half in range(2):
        s.header(c['name']+' / '+round_data['title']);s.block('Questions to ask',42,104,528,27,'BookBold',TEAL)
        instruction='Choose one guest named below who has not answered this round. Read the question aloud. Ignore absent guests. After answering, that guest chooses the next person. Your own answer is on the following answer page.'
        s.block(instruction,42,146,528,14);y=218
        for row in round_data['groups'][half*5:half*5+5]:
            y=s.block('ASK: '+' / '.join(row['targets']),42,y,528,14,'BookBold',TEAL)+5
            y=s.block(row['question'],42,y,528,16)+14;s.line(42,y-6,570,y-6)
        s.footer('Choose by name / Everyone answers once / Turn only within this round');s.next()

def secret_packets(chars):
    rounds=json.loads((ROOT/'source/question_rounds.json').read_text(encoding='utf-8'));paths=[]
    for c in chars:
        p=c['private'];h=c['hearing'];s=Sheet(KIT/'PRINT_WITHOUT_READING/Secret_Individual'/f'{c["slug"]}_SECRET.pdf',c['name']+' / complete packet')
        s.header(c['name']+' / Private background');y=s.block(c['name'],42,100,528,30,'BookBold')+16
        portrait_top=y;s.rect(42,y,144,216,fill=HexColor('#f6f1e7'),stroke=TEAL);s.image(ROOT/'assets/portraits'/c['slug']/'picasso.jpg',43,y+1,142,214)
        for label,key in [('Your grievance with Grant','history'),('Your other secret','secret')]:
            y=s.block(label,210,y,360,16,'BookBold',TEAL)+5;y=s.block(p[key],210,y,360,14)+13
        y=max(y,portrait_top+216)+19
        y=s.block('Three things to try before dinner',42,y,528,18,'BookBold',TEAL)+8
        for n,t in enumerate(['Introduce yourself by your character name.']+p['objectives'][:2]):y=s.block(str(n+1)+'. '+t,42,y,528,14)+9
        y=s.block('If a named guest is absent, discuss that subject with anyone. These social tasks do not block the investigation.',42,y+5,528,14,'BookItalic')+15
        s.block('Everything you need is here: questions, answers, preparation records, ballot and Coming Clean. Memorize your animal and return its slip. After the host announces the murderer animal, read IF MURDERER only if it is yours; otherwise read IF INNOCENT.',42,y,528,14)
        s.footer('STOP / Wait for the host to open Motive');s.next()
        for round_data in rounds:
            question_pages(s,c,round_data);key=round_data['key']
            s.header(c['name']+' / '+round_data['title']);s.block('Your answer',42,104,528,27,'BookBold',TEAL)
            y=s.block('Read the box for your role when questioned. Keep its label private. Acting is optional; these printed facts are enough.',42,148,528,14)+17
            if key=='motive':
                y=speech(s,'READ ALOUD / INNOCENT OR MURDERER',h['motive'],y)
            else:
                for branch in ['innocent','murderer']:
                    words=h[('where_' if key=='opportunity' else 'evidence_')+branch]
                    if key=='method':words+='\n\nPreparation record:\n'+'\n'.join(c['preparation_record'][branch].splitlines()[1:4])
                    y=speech(s,'IF '+branch.upper(),words,y,size=14 if key=='method' else 16)+6
            y=s.block('Then choose another guest',42,y+9,528,18,'BookBold',TEAL)+8
            s.block('Choose a guest who has not answered this round from either Questions to ask page. Ask one question addressed to that name. The host keeps track so everybody is heard.',42,y,528,14)
            y+=para('Choose a guest who has not answered this round from either Questions to ask page. Ask one question addressed to that name. The host keeps track so everybody is heard.',528,14)[1]+22
            if y<635:
                y=s.block('Notes from this round',42,y,528,16,'BookBold',TEAL)+20
                while y<710:s.line(42,y,570,y);y+=31
            s.footer('STOP / Wait for the host before the next round');s.next()
        s.header(c['name']+' / Voting');s.block('Your ballot',42,105,528,30,'BookBold',TEAL)
        y=s.block('Complete privately after Method. Name one suspect and explain the motive and evidence. Tear out this page or hand your closed packet to the host opened only here. Once all ballots are collected, no votes change.',42,153,528,16)+26
        for label in ['Your character name','I accuse','Motive','Evidence connecting the salon, key and linen','Best Actor','Best Costume']:
            y=s.block(label,42,y,528,16,'BookBold',TEAL)+34;s.line(42,y,570,y);y+=28
        s.footer('STOP / Do not turn to Coming Clean until all ballots are locked');s.next()
        s.header(c['name']+' / Coming Clean');s.block('Coming Clean',42,105,528,30,'BookBold',TEAL)
        y=s.block('STOP: Read only after voting, when the host calls your character among the top three suspects. If no suspect confesses, the host will call the murderer animal. Everyone else keeps this page private.',42,150,528,14,'BookBold',RED)+20
        for branch in ['innocent','murderer']:
            y=s.block('IF '+branch.upper()+' / READ ALOUD WHEN CALLED',42,y,528,16,'BookBold',TEAL)+7
            words=p['final_'+branch];paragraph,height=para(words,500,14);s.rect(42,y-2,528,height+24,stroke=TEAL)
            y=s.block(words,56,y+9,500,14)+26
        s.footer('Top three suspects first / If nobody confesses, the murderer stands');s.save();paths.append(s.path)
    merge(paths,KIT/'PRINT_WITHOUT_READING/03_Secret_Player_Packets_PRINT_DO_NOT_READ.pdf')

def play_aids(chars):
    s=Sheet(KIT/'OPEN_FREELY/12_Attendance_and_Hearing_Roster.pdf','Host name checklist');s.header('FACILITATOR / Host-safe')
    s.block('Hear every guest, every round',42,100,528,24,'BookBold');s.block('Character name',42,143,320,14,'BookBold');s.block('Here / Motive / Opp. / Method',350,143,220,12,'BookBold')
    for i,c in enumerate(chars):
        y=176+i*18;s.block(c['name'],42,y,310,12)
        for x in [365,425,485,545]:s.rect(x,y+1,11,11)
    s.footer('Choose by name / Tick each answer / All votes locked before Coming Clean');s.save()
    s=Sheet(KIT/'OPEN_FREELY/10_Blind_Printing_and_Assembly.pdf','Complete packet assembly');s.header('OPEN FREELY / Packet assembly')
    y=s.block('One guest. One complete packet.',42,101,528,28,'BookBold')+18
    for t in ['Print one named twelve-page SECRET packet per attending guest: single-sided, 100%, face down. A non-playing helper can handle exposed text.',
              'Staple pages in order at the left edge. Questions, answers, records, ballot and Coming Clean are all inside.',
              'Give the guest their named packet and a pencil at arrival. Keep the public introduction separate for sending before the party.',
              'If using the combined packet file, each consecutive twelve-page block belongs to the next character name listed below. Do not read private pages while assembling.',
              'Print one host guide and name checklist. Hide Discoveries 1–16. Stage reports: F1–F2 before Motive, F3 before Opportunity, F4–F5 before Method.']:
        y=s.block(t,42,y,528,14)+12
    y=s.block('Packet order / character names',42,y,528,18,'BookBold',TEAL)+9
    for row in range(15):
        for i,x in [(row,42),(row+15,318)]:s.block(chars[i]['name'],x,y,252,12)
        y+=18
    s.footer('The complete packet includes its ballot and Coming Clean page');s.save()

if __name__=='__main__':build_kit()
