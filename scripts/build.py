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
    p=SRC/f'{key}.md';return p.read_text(encoding='utf-8') if p.exists() else '\n'.join(p.read_text(encoding='utf-8') for p in sorted((SRC/key).glob('*.md')))
def preparty(chars):
    paths=[]
    for c in chars:
        path=KIT/'OPEN_FREELY/PreParty_Individual'/f'{c["slug"]}.pdf';s=Sheet(path,c['name'])
        s.rect(30,30,552,732,stroke=TEAL);s.rect(30,30,552,151,fill=TEAL,stroke=TEAL)
        s.block('Treasures of the World',48,46,516,18,'BookItalic',white);s.block(c['name'],48,76,516,36,'BookBold',white)
        s.block(c['role']+f' / Age {c["age"]}',48,131,516,16,'Book',white,bottom=177)
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
def secret_packets(chars):
    paths=[]
    for c in chars:
        path=KIT/'PRINT_WITHOUT_READING/Secret_Individual'/f'{c["slug"]}_SECRET.pdf';s=Sheet(path,c['name']+' / private packet');p=c['private'];s.header('PRIVATE / Open at the gala',True)
        y=s.block(c['name'],42,96,528,30,'BookBold')+5;y=s.block('ACT I / Before the murder',42,y,528,18,'BookBold',TEAL)+15
        for title,key in [('Your history with Sterling','history'),('What you are hiding','secret')]:
            y=s.block(title,42,y,528,16,'BookBold')+5;y=s.block(p[key],42,y,528,14)+12
        for title,key in [('Your objectives','objectives'),('What you know about other guests','knowledge')]:
            y=s.block(title,42,y,528,16,'BookBold')+5
            for item in p[key]:y=s.block('• '+item,42,y,528,14)+5
            y+=7
        if y<650:
            y=s.block('Notes / Who will you speak to first?',42,y+8,528,14,'BookItalic',TEAL)+18
            while y<725:s.line(42,y,570,y);y+=25
        s.footer('STOP / Turn over only after the murder announcement');s.next();s.header(c['name']+' / PRIVATE',True)
        y=s.block('ACT II / After Sterling dies',42,97,528,22,'BookBold',TEAL)+8
        y=s.block('Follow your assigned branch. Keep it private. If you are the murderer, the innocent branch is a cover story you may claim.',42,y,528,14)+12
        tops=[]
        for x,key,title in [(42,'innocent','IF INNOCENT'),(318,'murderer','IF MURDERER')]:
            a=s.block(title,x,y,252,16,'BookBold',TEAL)+7;tops.append(s.block(p[key],x,a,252,14)+16)
        y=max(tops);s.line(42,y,570,y);y+=13;y=s.block('ACT III / Evidence update',42,y,528,18,'BookBold',TEAL)+5
        y=s.block(p['evidence_instruction'],42,y,528,14)+15;y=s.block('FINAL STATEMENT / Read only if called',42,y,528,16,'BookBold')+8
        end=[]
        for x,key,title in [(42,'final_innocent','IF INNOCENT'),(318,'final_murderer','IF MURDERER')]:
            a=s.block(title,x,y,252,14,'BookBold',TEAL)+5;end.append(s.block(p[key],x,a,252,14,bottom=739))
        if max(end)<655:
            y=s.block('Investigation notes',42,max(end)+18,528,14,'BookItalic',TEAL)+22
            while y<726:s.line(42,y,570,y);y+=25
        s.footer('Keep this packet and the unused evidence card private.');s.save();paths.append(path)
    merge(paths,KIT/'PRINT_WITHOUT_READING/03_Secret_Player_Packets_PRINT_DO_NOT_READ.pdf')
def evidence(chars):
    s=Sheet(KIT/'PRINT_WITHOUT_READING/05_Character_Evidence_Cards_PRINT_DO_NOT_READ.pdf','Character evidence / print without reading')
    for i in range(0,30,2):
        s.header(f'PRINT FACE DOWN / Evidence pairs {i+1:02}-{i+2:02}',True)
        for row,c in enumerate(chars[i:i+2]):
            top=100+row*323;s.block(f'{c["id"]} / {c["name"]} / Pack BOTH cards together',42,top,528,14,'BookBold')
            for x,letter in [(42,'A'),(318,'B')]:
                y=top+29;s.rect(x,y,252,272,dash=[3,3]);a=s.block(f'{c["name"]} / Card {letter}',x+13,y+13,226,15,'BookBold',TEAL)
                a=s.block('EVIDENCE UPDATE',x+13,a+5,226,14,'BookBold')+13;s.block(c['evidence'][letter],x+13,a,226,14,bottom=y+225)
                s.block('Submit face down only when your packet tells you to.',x+13,y+229,226,12,bottom=y+270)
        s.footer('Cut dashed borders / One A/B pair per labeled envelope')
        if i<28:s.next()
    s.save()
    safe=Sheet(KIT/'OPEN_FREELY/10_Blind_Printing_and_Assembly.pdf','Blind printing and assembly');safe.header('Host-safe assembly guide');y=safe.block('Print. Cut. Seal.',42,98,528,32,'BookBold')+14
    for t in ['Print single-sided at Actual size (100%). Do not use booklet mode or two pages per sheet. Print private files face down; keep the output tray covered. If your printer outputs face up, ask a non-playing helper to handle exposed text.','Each guest gets two consecutive private pages and both A/B cards. Seal them in a labeled envelope. Each individual PDF has the same two private pages.','Evidence: 15 sheets, two guests per sheet. Cut each dashed rectangle. The two cards in each row belong together. A/B assignments vary by guest; letters do not identify guilt.','Clues: hide 1–16 by the safe placement table. Keep F1–F5 face down until Act III.']:
        y=safe.block(t,42,y,528,14)+12
    y=safe.block('Evidence sheet / envelope names',42,y,528,18,'BookBold',TEAL)+8
    for i in range(0,30,2):y=safe.block(f'{i//2+1:02}   {chars[i]["name"]} + {chars[i+1]["name"]}',42,y,528,14)+2
    safe.footer('OPEN FREELY / No evidence or branch assignments');safe.save()
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
    for m in re.finditer(r'(?m)^(F\d) - ([^\n]+)\n+(.+?)(?=\nF\d - |\Z)',text,re.S):cards.append((f'ACT III / {m[1]} / Release together',m[2].title(),flat(m[3]),'record'))
    assert len(cards)==21
    cards.append(('ACT III / Evidence table','Read the five reports together','Release F1–F5 at the start of Act III. Compare timing, access and each character’s evidence update. Keep unused A/B evidence cards private.','record'))
    card_document(KIT/'PRINT_WITHOUT_READING/04B_Clues_and_Forensics_PRINT_DO_NOT_READ.pdf','PRINT WITHOUT READING / Clues & forensics',cards)
def props(chars):
    parts=[];core='ANTELOPE BADGER COUGAR DOLPHIN EGRET FOX GAZELLE HERON IBIS JAGUAR KOALA LYNX MARMOT OTTER RABBIT'.split();optional=['NEWT','PANDA','QUAIL','SEAL','TIGER','URCHIN','VIPER','WOLF','X-RAY TETRA','YAK','ZEBRA','MOOSE','PENGUIN','SHARK','TURTLE']
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
    s.block('Treasures\nof the World',52,145,508,44,'BookBold',white,bottom=293);y=s.block('The Sterling Voss Collection',52,327,508,22,'BookItalic',TEAL)+23
    for t,size,font in [('Friday, October 30, 2026 / 6:00 PM',20,'BookBold'),('Tulsa, Oklahoma',18,'Book'),('Location: __________________________________',16,'Book'),('An opening-night gala celebrating art and culture from around the world, culminating in the unveiling of the thirteenth-century Isfahan Star Bowl.',18,'Book'),('Formal gala attire with art-world flair. Your character’s costume suggestions are optional inspiration; make the role your own.',16,'Book'),('Read your separate character introduction before the party. Your private packet awaits you at the gala.',16,'Book')]:y=s.block(t,52,y,508,size,font,bottom=732)+16
    s.next();s.header('ARRIVAL / Display at check-in');y=s.block('Welcome to the Meridian',42,105,528,32,'BookBold')+24
    rules=['Draw one animal from the appropriate bowl. Memorize it; never tell anyone which animal you drew.','Keep phones put away. Everything you need for the game is physical.','During Act I, bring each discovered clue to the Evidence Table. You earn one point; the clue becomes public.','Stay in character as much as you enjoy. You never have to perform a speech on demand.','After the murder, innocents may evade, omit, or deflect but may not invent false facts. The murderer may lie.','Open each part of your private packet only when the game tells you to use it.']
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
    cards.append(('TREASURES OF THE WORLD','The Voss Collection','The Meridian Museum of Art & World Cultures\nOpening-night gala / October 30, 2026\n\nAn exhibition of art and culture from around the world. All objects and collection histories in this party kit are fictional.','record'))
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
    s.block('Awarding Escaped Justice',42,431,528,22,'BookBold',TEAL);s.block('Tally accusations first. If the actual murderer is outside the top three, award Escaped Justice; then ask the murderer animal to identify themselves and read their final statement.',42,476,528,16);s.footer('Cut each certificate at its border');s.save()
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
def spoiler(chars):
    sections=[('Canonical murder facts',load_doc('spoiler_bible').split('Canonical murder facts')[1].split('Character branch matrix')[0])]
    for c in chars:
        p=c['private'];body=[label+': '+p[key] for label,key in [('Victim relationship','history'),('Hidden complication','secret'),('Innocent route','innocent'),('Murderer route','murderer')]]
        body+=[f'Innocent evidence / Card {p["innocent_card"]}: '+c['evidence'][p['innocent_card']],f'Murderer evidence / Card {p["murderer_card"]}: '+c['evidence'][p['murderer_card']]];sections.append((c['id']+' / '+c['name'],'\n\n'.join(body)))
    sections.append(('Difficulty & continuity',load_doc('spoiler_bible').split('Difficulty tuning rationale',1)[1]))
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
    preparty(chars);secret_packets(chars);evidence(chars);clues();props(chars);invitation();exhibits();awards();readme();facilitator(chars);spoiler(chars)
    import fitz
    for path in sorted((KIT/'OPEN_FREELY/PreParty_Individual').glob('*.pdf')):
        with fitz.open(path) as doc:
            assert len(doc)==1,path;doc[0].get_pixmap(matrix=fitz.Matrix(2,2)).save(str(path.with_suffix('.png')))
    (WORK/'layout-ledger.json').write_text(json.dumps(AUDIT,ensure_ascii=False,indent=2),encoding='utf-8');(KIT/'README.txt').write_text('Start with 00_READ_ME_FIRST.pdf. Print at 100%, single-sided. Handle private files face down. OPEN_FREELY is host-safe; all other folders contain spoilers. Fonts are embedded.\n',encoding='utf-8')
    package();print(f'Built {len(list(KIT.rglob("*.pdf")))} PDFs and 30 character PNGs')
if __name__=='__main__':build_kit()
