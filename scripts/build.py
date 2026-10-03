"""Measured museum-gala layouts. Build fonts are never included in downloads."""
from pathlib import Path
import json,re,html,zipfile,io,urllib.request,hashlib
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
        s.rect(30,30,552,732,stroke=TEAL);s.rect(30,30,552,151,fill=TEAL,stroke=TEAL)
        s.block('The Living Collection / Treasures of the World',48,46,516,16,'BookItalic',white);s.block(c['name'],48,76,516,36,'BookBold',white)
        s.block(c['role'],48,131,516,16,'Book',white,bottom=177)
        p=c['preparty']
        def measure(size):
            y=200+para(p['description'],516,size)[1]+12
            for item in p['relationships']:y+=para('• '+item,516,size)[1]+5
            y+=26
            for heading,key in [('ACTING TIPS','acting'),('COSTUME SUGGESTIONS','costume')]:y+=20+6+para(p[key],516,size)[1]+17
            return y-17
        size=next(n for n in [20,19,18,17,16] if measure(n)<=729)
        y=s.block(p['description'],48,200,516,size)+12
        for item in p['relationships']:y=s.block('• '+item,48,y,516,size)+5
        y+=10;s.line(48,y,564,y);y+=16
        for heading,key in [('ACTING TIPS','acting'),('COSTUME SUGGESTIONS','costume')]:
            y=s.block(heading,48,y,516,16,'BookBold',TEAL)+6;y=s.block(p[key],48,y,516,size,bottom=730)+17
        s.block('October 30, 2026 / Meridian Museum Gala',48,739,516,12,'Book',TEAL,bottom=758);s.save();paths.append(path)
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
    text=load_doc('clues_forensics');cards=[]
    for m in re.finditer(r'(?m)^(\d+)\. ([^\n]+)\n+(.+?)(?=\n\d+\. |\nFixed Forensic Evidence)',text,re.S):cards.append((f'ACT I / Discovery {int(m[1]):02}',m[2],flat(m[3]),'note' if m[1] in ['3','6'] else 'record'))
    for r in json.loads((ROOT/'source/investigation.json').read_text(encoding='utf-8')):cards.append((f'{"ACT III" if r["id"] in ["F4","F5"] else "ACT II"} / {r["id"]} / Staged release',r['title'],r['text'],'record'))
    assert len(cards)==21
    cards.append(('EVIDENCE TABLE / Release order','Three releases, three rounds','Read F1–F2 before Motive. Read F3 before Opportunity. Read F4–F5 before Method. Guests select their assigned A/B preparation receipt only when Method begins. Ask their named question, hear their answer, then read their receipt. Compare all the records before voting.','record'))
    card_document(KIT/'PRINT_WITHOUT_READING/04B_Clues_and_Forensics_PRINT_DO_NOT_READ.pdf','PRINT WITHOUT READING / Clues & forensics',cards)
def props(chars):
    parts=[];core=GAME['core_animals'];optional=GAME['optional_animals']
    s=Sheet(KIT/'OPEN_FREELY/Animal_Draw_Cards.pdf','Animal draw cards')
    for n,(names,label) in enumerate([(core,'PLAYER BOWL A / 15 core animals'),(core,'MURDERER BOWL B / Matching 15 animals'),(optional,'OPTIONAL BOWL / Never add these to Bowl B')]):
        s.header(label)
        for i,name in enumerate(names):
            x=42+(i%3)*181;y=109+(i//3)*122;s.rect(x,y,166,106,dash=[3,3]);s.block(name,x+10,y+38,146,19,'BookBold',TEAL)
        s.footer('Cut separately / A and B must match / Remove absent core animals')
        if n<2:s.next()
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
    for start in range(0,30,6):
        s.header('GUEST NAME CARDS / Cut dashed borders')
        for i,c in enumerate(chars[start:start+6]):
            x=42+(i%2)*276;y=104+(i//2)*211;s.rect(x,y,252,196,dash=[3,3]);s.block('MERIDIAN / GALA',x+13,y+14,226,14,'BookBold',TEAL)
            a=s.block(c['name'],x+13,y+48,226,26,'BookBold')+12;s.block(c['role'],x+13,a,226,14,bottom=y+183)
        s.footer('Host-safe / Display flat or attach to a place-card stand')
        if start<24:s.next()
    s.save()
def invitation():
    s=Sheet(KIT/'OPEN_FREELY/06_Invitation_and_Arrival_Guide.pdf','Invitation & arrival');s.rect(30,30,552,732,stroke=TEAL);s.rect(30,30,552,270,fill=TEAL,stroke=TEAL)
    s.block('The Meridian Museum',52,55,508,24,'BookBold',white);s.block('of Art & World Cultures',52,89,508,18,'Book',white)
    s.block('Treasures\nof the World',52,145,508,44,'BookBold',white,bottom=293);y=s.block('The Grant Larceny Collection',52,327,508,22,'BookItalic',TEAL)+23
    for t,size,font in [('Friday, October 30, 2026 / 6:00 PM',20,'BookBold'),(GAME['address'],18,'Book'),('An opening-night gala celebrating art and culture from around the world, culminating in the unveiling of the thirteenth-century Isfahan Star Bowl.',18,'Book'),('Formal gala attire with art-world flair. Your character’s costume suggestions are optional inspiration; make the role your own.',16,'Book'),('Read your separate character introduction before the party. Your private packet awaits you at the gala.',16,'Book')]:y=s.block(t,52,y,508,size,font,bottom=732)+16
    s.next();s.header('ARRIVAL / Display at check-in');y=s.block('Welcome to the Meridian',42,105,528,32,'BookBold')+24
    rules=['Memorize the animal you draw. Return the slip immediately to the closed return box. Never tell anyone your animal.','Keep phones put away. Everything you need is printed.','Act I: introduce yourself, try the three social tasks and bring discoveries to the Evidence Table.','After the death, follow the three guided hearings. Read your printed answer when your turn comes; acting is optional.','Read only the words inside the speech boxes. Do not invent new locations, events or witnesses.','FINALE envelopes stay with the host until every ballot is collected.']
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
    s.block('Awarding Escaped Justice',42,431,528,22,'BookBold',TEAL);s.block('Collect and lock all ballots first. Tally the top three suspects. Then ask the murderer animal to identify themselves and open their separate finale envelope. If outside the top three, award Escaped Justice.',42,476,528,16);s.footer('Cut each certificate at its border');s.save()
    merge([KIT/'OPEN_FREELY/Scavenger_Score_Sheet.pdf',KIT/'OPEN_FREELY/Award_Certificates.pdf'],KIT/'OPEN_FREELY/08_Awards_and_Scoring.pdf')
def readme():
    s=Sheet(KIT/'00_READ_ME_FIRST.pdf','Read me first');s.header('READ ME FIRST / Host-safe');y=s.block('The Last Acquisition',42,103,528,34,'BookBold')+12;y=s.block('October 30, 2026 / Tulsa / 15–30 guests',42,y,528,18,'BookItalic',TEAL)+20
    sections=[('OPEN FREELY','The facilitator guide, pre-party introductions, invitation, animal slips, ballots, museum signs, placards, name cards and awards are safe to inspect.'),('SEND BEFORE THE PARTY','Assign the 15 core roles first, then add optional guests. Send each guest their own single-page PDF or PNG from PreParty_Individual, plus the invitation. Do not send private packets or the full kit to guests.'),('PRINT WITHOUT READING','Private packets, clues/forensics and A/B pairs live in PRINT_WITHOUT_READING. Print single-sided at 100%, face down. Use 10_Blind_Printing_and_Assembly.pdf to cut and seal by names and numbers.'),('KEEP SEALED','The spoiler bible and editable source expose every branch. Leave SPOILERS_DO_NOT_OPEN closed if you are playing.'),('AT CHECK-IN','Give each guest their labeled private envelope. Use separate core and optional animal bowls. The facilitator guide explains how to remove absent core animals from the murderer draw.')]
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
    sections=[('Canonical murder facts','Grant Larceny dies from a botanical cardiac toxin applied inside his private silver coupe and on its rim using toxin-dampened gold-seamed linen. It was introduced in the Donor Salon, 6:40–6:49. One of the attending 15 core roles is selected through the blind animal draw. Optional roles cannot be selected.\n\nAll essential facts are heard in the three mandatory hearings. Three overlapping suspect groups emerge: guests who entered the salon during the poisoning window, guests who borrowed the cabinet key during setup, and guests who carried the matching linen. Only the murderer belongs to all three. No record names a person seen committing the crime. The lone culprit did not exchange keys, badges, samples or linen with another guest.\n\nThe actual murder narrative and confession are never printed in the four active-play pages. The separate named FINALE envelope opens only after ballots are collected. All fixed clues work for every eligible murderer. Warning notes and flickering lights are human-made; no curse causes the death.')]
    for c in chars:
        p=c['private'];body=[label+': '+p[key] for label,key in [('Victim relationship','history'),('Hidden complication','secret'),('Innocent route','innocent'),('Murderer route','murderer')]]
        body+=[f'Innocent evidence / Card {p["innocent_card"]}: '+c['evidence'][p['innocent_card']],f'Murderer evidence / Card {p["murderer_card"]}: '+c['evidence'][p['murderer_card']]];sections.append((c['id']+' / '+c['name'],'\n\n'.join(body)))
    sections.append(('Difficulty & continuity','Motive reveals grievances. Opportunity establishes salon visits and setup errands. Method reveals the significance of the key and linen, then compares the original receipts. Each individual clue matches many innocent guests. Only the murderer matches the combined salon-entry, cabinet-key and gold-seamed-linen records. No essential evidence may be withheld. Optional guests do not certify another guest’s movements. Scavenger discoveries add atmosphere but cannot block solving.'))
    manual('SPOILER BIBLE / Do not open if playing',sections,KIT/'SPOILERS_DO_NOT_OPEN/99_SPOILER_BIBLE_DO_NOT_OPEN.pdf')
def package():
    with zipfile.ZipFile(SITE/'downloads/The_Last_Acquisition_Complete_Kit.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(KIT.rglob('*')):
            if p.is_file():z.write(p,Path(KIT.name)/p.relative_to(KIT))
    with zipfile.ZipFile(SITE/'downloads/The_Last_Acquisition_Source.zip','w',zipfile.ZIP_DEFLATED) as z:
        for base in ['source','docs','scripts','site','.impeccable']:
            for p in sorted((ROOT/base).rglob('*')):
                if p.is_file() and 'downloads' not in p.parts and p.suffix not in ['.ttf','.woff','.woff2','.pyc']:z.write(p,p.relative_to(ROOT))
        for name in ['README.md','PRODUCT.md','CHANGELOG.md','requirements.txt','netlify.toml','.gitignore']:z.write(ROOT/name,name)
def build_kit():
    fonts();KIT.mkdir(parents=True,exist_ok=True);chars=json.loads((ROOT/'source/characters.json').read_text(encoding='utf-8'))
    # Clear superseded character filenames, keeping only current canonical exports.
    for folder in ['OPEN_FREELY/PreParty_Individual','PRINT_WITHOUT_READING/Secret_Individual','PRINT_WITHOUT_READING/Finale_Individual']:
        dest=KIT/folder
        if dest.exists():
            for old in dest.iterdir():
                if old.suffix in ['.pdf','.png']:old.unlink()
    preparty(chars);secret_packets(chars);evidence(chars);play_aids(chars);clues();props(chars);invitation();exhibits();awards();readme();facilitator(chars);spoiler(chars)
    import fitz
    for path in sorted((KIT/'OPEN_FREELY/PreParty_Individual').glob('*.pdf')):
        with fitz.open(path) as doc:
            assert len(doc)==1,path;doc[0].get_pixmap(matrix=fitz.Matrix(2,2)).save(str(path.with_suffix('.png')))
    (WORK/'layout-ledger.json').write_text(json.dumps(AUDIT,ensure_ascii=False,indent=2),encoding='utf-8');(KIT/'README.txt').write_text('Start with 00_READ_ME_FIRST.pdf. Print at 100%, single-sided. Handle private files face down. OPEN_FREELY is host-safe; all other folders contain spoilers. Fonts are embedded.\n',encoding='utf-8')
    package();print(f'Built {len(list(KIT.rglob("*.pdf")))} PDFs and 30 character PNGs')
def speech(s,title,words,y=176):
    y=s.block(title,55,y,502,16,'BookBold',TEAL)+9
    p,h=para(words,480,16);s.rect(42,y-2,528,h+30,stroke=TEAL)
    s.block(words,66,y+10,480,16,bottom=730)
    return y+h+45

def secret_packets(chars):
    paths=[];finals=[]
    for c in chars:
        p=c['private'];h=c['hearing'];s=Sheet(KIT/'PRINT_WITHOUT_READING/Secret_Individual'/f'{c["slug"]}_SECRET.pdf',c['name']+' / play packet')
        s.header('ACT I / Private background');y=s.block(c['name'],42,100,528,30,'BookBold')+16
        for label,key in [('Your grievance with Grant','history'),('Your other secret','secret')]:
            y=s.block(label,42,y,528,16,'BookBold',TEAL)+5;y=s.block(p[key],42,y,528,14)+13
        y=s.block('Three things to try before dinner',42,y,528,18,'BookBold',TEAL)+8
        tasks=['Introduce yourself to someone you do not already know. Your role and pre-party sheet are enough.']+p['objectives'][:2]
        for n,t in enumerate(tasks):y=s.block(str(n+1)+'. '+t,42,y,528,14)+9
        y=s.block('When a named contact is absent, discuss that issue with any guest. No task blocks the investigation.',42,y+5,528,14,'BookItalic')+15
        s.block('Private background can be shared or withheld. Later hearings tell you exactly what must be said. No crime confession is printed in these four play pages.',42,y,528,14)
        s.footer('STOP / Turn to Hearing 1 only when announced');s.next()
        s.header(c['name']+' / ACT II');s.block('Round 1 / Motive',42,101,528,26,'BookBold')
        y=s.block('When questioned, read your answer. It is the same whether you are innocent or the murderer.',42,143,528,14)+17
        y=speech(s,'READ ALOUD / YOUR ANSWER',h['motive'],y)
        y=s.block('Your next action',42,y+15,528,18,'BookBold',TEAL)+8
        y=s.block('Ask the next seated guest their named Motive question in the question catalog. Note one grievance that might matter. Wait for the host before turning the page.',42,y,528,16)+20
        for z in range(3):s.line(42,y+z*32,570,y+z*32)
        s.footer('STOP / Wait for Hearing 2');s.next()
        s.header(c['name']+' / ACT II');s.block('Round 2 / Opportunity',42,101,528,26,'BookBold')
        y=s.block('When questioned, read the answer for your role. Keep the section labels to yourself.',42,143,528,14)+18
        y=speech(s,'IF INNOCENT',h['where_innocent'],y)
        y=speech(s,'IF MURDERER',h['where_murderer'],y+12)
        s.block('After answering, ask the next seated guest their named Opportunity question in the catalog. Wait for the host before turning the page.',42,y+8,528,14)
        s.footer('STOP / Wait for Hearing 3 and the evidence collection');s.next()
        s.header(c['name']+' / ACT III');s.block('Round 3 / Method',42,101,528,26,'BookBold')
        y=s.block(f'Open your EVIDENCE envelope. Choose privately: IF INNOCENT = Card {p["innocent_card"]}; IF MURDERER = Card {p["murderer_card"]}. Submit only that letter. Keep the unused card hidden. Do not choose according to what looks safer.',42,142,528,14)+14
        y=s.block('When questioned, read your answer below, then your selected receipt. Leave the unused card hidden.',42,y,528,14)+14
        y=speech(s,'IF INNOCENT',h['evidence_innocent'],y)
        y=speech(s,'IF MURDERER',h['evidence_murderer'],y+10)
        s.block('Put the read receipt on the Evidence Table. Discuss, then vote privately. The host will distribute FINALE envelopes only after collecting all ballots.',42,y+5,528,14)
        s.footer('FINALE IS SEPARATE / Open only after ballots are locked');s.save();paths.append(s.path)
        f=Sheet(KIT/'PRINT_WITHOUT_READING/Finale_Individual'/f'{c["slug"]}_FINALE.pdf',c['name']+' / sealed finale');f.header('FINALE / Seal in a separate named envelope',True)
        y=f.block(c['name'],42,102,528,30,'BookBold')+20;y=f.block('Do not open before all ballots are collected.',42,y,528,20,'BookBold',RED)+15
        y=f.block('Only the guest who memorized the announced murderer animal reads a confession. Everyone else keeps this envelope closed. If opened by mistake, stop before reading the next section aloud.',42,y,528,16)+25
        y=f.block('CONFESSION / Read only after identifying yourself',42,y,528,18,'BookBold',RED)+10
        f.block(p['final_murderer'] if c['tier']=='CORE' else 'This role cannot be selected in the standard draw. There is no confession to read.',42,y,528,16)
        f.footer('SPOILER / Keep separately sealed until the finale');f.save();finals.append(f.path)
    merge(paths,KIT/'PRINT_WITHOUT_READING/03_Secret_Player_Packets_PRINT_DO_NOT_READ.pdf')
    merge(finals,KIT/'PRINT_WITHOUT_READING/03B_Sealed_Finales_PRINT_DO_NOT_READ.pdf')

def evidence(chars):
    s=Sheet(KIT/'PRINT_WITHOUT_READING/05_Character_Evidence_Cards_PRINT_DO_NOT_READ.pdf','Evidence pairs / one guest per sheet')
    for i,c in enumerate(chars):
        s.header(f'PRINT FACE DOWN / Pair {c["id"]} / Pack BOTH together',True)
        for row,letter in enumerate(['A','B']):
            y=106+row*319;s.rect(42,y,528,293,dash=[3,3]);a=s.block(c['id']+' / '+c['name']+' / Card '+letter,58,y+15,496,20,'BookBold',TEAL)+14
            s.block(c['evidence'][letter],58,a,496,14,bottom=y+257)
            s.block('Select privately at Hearing 3 / Keep unused card hidden',58,y+267,496,12,'Book',TEAL,bottom=y+286)
        s.footer('Cut each dashed rectangle / Same-name A and B stay together')
        if i<29:s.next()
    s.save()

def play_aids(chars):
    s=Sheet(KIT/'OPEN_FREELY/11_Questions_and_Notes.pdf','Questions and deduction notes');s.header('ONE COPY PER SEATING PAIR / Host-safe')
    y=s.block('Questions for the gala',42,104,528,30,'BookBold')+16
    y=s.block('Find the next guest by ID and name in the following catalog pages. Ask their question for the current round. They answer, then ask the next occupied seat. The last seated guest asks the first. Skip absent IDs.',42,y,528,16)+18
    y=s.block('Follow the case',42,y,528,20,'BookBold',TEAL)+8
    for label in ['Motive / what would the suspect lose?','Opportunity / who entered the salon after 6:40?','Access / who borrowed the cabinet key during setup?','Method / who carried the matching linen?']:
        y=s.block(label,42,y,528,16,'BookBold')+38;s.line(42,y,570,y);y+=17
    s.footer('Read one named question per round / Wait for the host’s next release');s.next()
    y=100
    for c in chars:
        q=c['questions'];items=[('1 / Motive',q['motive']),('2 / Opportunity',q['opportunity']),('3 / Method',q['method'])]
        height=23+sum(para(label+': '+words,528,14)[1]+5 for label,words in items)+13
        if y+height>730:
            s.footer('Question catalog / ID order / Skip absent guests');s.next();y=100
        if y==100:s.header('QUESTION CATALOG / Ask only the current round')
        y=s.block(c['id']+' / '+c['name'],42,y,528,18,'BookBold',TEAL)+5
        for label,words in items:y=s.block(label+': '+words,42,y,528,14)+5
        s.line(42,y+2,570,y+2);y+=13
    s.footer('Question catalog / ID order / Skip absent guests');s.save()
    s=Sheet(KIT/'OPEN_FREELY/12_Attendance_and_Hearing_Roster.pdf','Attendance and hearing ticks');s.header('FACILITATOR / Host-safe')
    s.block('Tick every guest, every hearing',42,100,528,24,'BookBold');s.block('ID / Name',42,143,330,14,'BookBold');s.block('Here / R1 / R2 / R3',362,143,208,12,'BookBold')
    for i,c in enumerate(chars):
        y=176+i*18;s.block(c['id']+' / '+c['name'],42,y,310,12)
        for x in [378,430,482,534]:s.rect(x,y+1,11,11)
    s.footer('Skip absent IDs / Count cards before Hearing 3 / Lock ballots before finale');s.save()
    s=Sheet(KIT/'OPEN_FREELY/10_Blind_Printing_and_Assembly.pdf','Blind printing and assembly');s.header('OPEN FREELY / Blind assembly')
    y=s.block('Print. Cut. Seal separately.',42,101,528,28,'BookBold')+18
    for t in ['Print single-sided at 100%, face down. Cover exposed pages. Ask a non-playing helper if your printer exposes text.','Each guest: four consecutive play pages, their same-name A/B pair in a closed EVIDENCE envelope, and one FINALE page sealed in a separate named envelope. The host keeps FINALE envelopes on a tray until all ballots are collected.','Evidence sheet 01 belongs to character 01, through sheet 30 for character 30. Cut both full-width rectangles. Keep A and B together. Letters do not identify guilt.','The combined finale file is for blind printing only. Seal each page separately by name and ID. Do not send the whole file to guests.','Hide discoveries 1–16. Keep F1–F5 in order. Release F1–F2 before Motive, F3 before Opportunity, F4–F5 before Method.']:
        y=s.block(t,42,y,528,14)+12
    y=s.block('Sheet / play packet / finale ID',42,y,528,18,'BookBold',TEAL)+9
    for row in range(15):
        for i,x in [(row,42),(row+15,318)]:s.block(chars[i]['id']+' / '+chars[i]['name'],x,y,252,12)
        y+=18
    s.footer('OPEN FREELY / Branch letters and evidence text are not shown');s.save()

if __name__=='__main__':build_kit()
