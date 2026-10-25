"""Public, image-first gala materials; private packet layouts stay independent."""
import html
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase.pdfmetrics import stringWidth

NIGHT = HexColor('#061415')
CREAM = HexColor('#fff1d5')
GOLD = HexColor('#edc189')
WINE = HexColor('#620e21')

def ground(s):
    cv=s.c;cv.setFillColor(NIGHT);cv.rect(0,0,s.w,s.h,fill=1,stroke=0)

def rule(s,y,x=42,width=528,color=GOLD):
    cv=s.c;cv.saveState();cv.setStrokeColor(color);cv.setLineWidth(.55)
    cv.line(x,s.h-y,x+width,s.h-y);cv.restoreState()

def text(s,b,words,x,y,width,size=17,font='Book',color=CREAM,center=False,leading=1.2):
    p=Paragraph(html.escape(words).replace('\n','<br/>'),ParagraphStyle('gala',
        fontName=font,fontSize=size,leading=size*leading,textColor=color,
        alignment=1 if center else 0,allowWidows=0,allowOrphans=0))
    _,height=p.wrap(width,10000)
    assert y+height<=774,(s.path.name,words[:40],y+height)
    p.drawOn(s.c,x,s.h-y-height)
    if s.path.is_relative_to(b.KIT):
        b.AUDIT.append(dict(file=str(s.path.relative_to(b.KIT)),page=s.page,x=x,y=y,
                            width=width,height=height,size=size,text=words))
    return y+height

def height(b,words,width,size,font='Book'):
    p=Paragraph(html.escape(words),ParagraphStyle('measure',fontName=font,
        fontSize=size,leading=size*1.2))
    return p.wrap(width,10000)[1]

def portrait(s,b,path,x,y,w,h):
    # Restore the same native-alpha gilded frame used on the private covers.
    from printable_v2 import framed
    framed(s,b,path,x,y,w,h)

def poster(chars,b,print_mode=False,output_dir=None,merged_path=None):
    paths=[]
    output_dir=output_dir or b.KIT/'OPEN_FREELY/PreParty_Individual'
    ink=b.INK if print_mode else CREAM
    accent=b.RED if print_mode else GOLD
    gilt=b.GOLD if print_mode else GOLD
    for c in chars:
        s=b.Sheet(output_dir/f'{c["slug"]}.pdf',c['name'])
        if not print_mode:ground(s)
        p=c['preparty']
        size_name=next(v for v in range(43,27,-1) if stringWidth(c['name'],'BookBold',v)<=528)
        text(s,b,c['name'],42,36,528,size_name,'BookBold',ink)
        role_end=text(s,b,c['role'],42,94,528,17,'BookItalic',accent)
        hero_y=max(141,role_end+18)
        def measure(size,portrait_width=196,gap=18):
            hero=max(portrait_width*1.16,height(b,p['description'],528-portrait_width-24,size))
            y=hero_y+hero+gap
            y+=sum(height(b,'• '+t,528,size)+5 for t in p['relationships'])
            y+=16+18+5+height(b,p['acting'],528,size)
            y+=19+18+5+height(b,p['costume'],500,size)+22
            return y,hero
        choice=next(((size,*measure(size)) for size in [17,16.5,16] if measure(size)[0]<=736),None)
        assert choice,(c['name'],measure(16))
        size,end,hero=choice
        portrait_width=196
        for candidate in [250,230]:
            proposed,new_hero=measure(size,candidate)
            if proposed<=736:
                portrait_width=candidate;end=proposed;hero=new_hero;break
        gap=18+min(24,max(0,710-end))
        portrait(s,b,c.get('portrait_path',b.ROOT/'assets/portraits'/c['slug']/'van_gogh.jpg'),42,hero_y,portrait_width,hero)
        text(s,b,p['description'],66+portrait_width,hero_y+3,528-portrait_width-24,size,color=ink)
        y=hero_y+hero+gap
        for rel in p['relationships']:
            y=text(s,b,'• '+rel,42,y,528,size,color=ink)+5
        rule(s,y+7,color=gilt)
        y=text(s,b,'ACTING TIPS',42,y+16,528,15,'BookBold',accent)+5
        y=text(s,b,p['acting'],42,y,528,size,color=ink)
        box_y=y+19
        box_h=18+5+height(b,p['costume'],500,size)+22
        s.c.setFillColor(b.PALE if print_mode else WINE);s.c.rect(28,s.h-box_y-box_h,556,box_h,fill=1,stroke=0)
        y=text(s,b,'COSTUME SUGGESTIONS',42,box_y+9,528,15,'BookBold',accent)+5
        text(s,b,p['costume'],42,y,500,size,color=ink)
        rule(s,747,color=gilt)
        text(s,b,'The Last Acquisition  /  October 30, 2026',42,756,528,12,'BookItalic',accent)
        s.save();paths.append(s.path)
    b.merge(paths,merged_path or b.KIT/'OPEN_FREELY/02_PreParty_Character_Sheets_ALL.pdf')

def invitation_front(s,b,print_mode=False):
    if not print_mode:ground(s)
    else:
        s.c.setFillColor(NIGHT);s.c.rect(0,s.h-383,612,383,fill=1,stroke=0)
    ink=b.INK if print_mode else CREAM
    accent=b.RED if print_mode else GOLD
    # Reuse the exact commissioned art that establishes the live site's world.
    s.image(b.ROOT/'site/art/museum-after-hours.webp',0,0,612,383)
    cv=s.c;cv.saveState();cv.setFillColor(NIGHT);cv.setFillAlpha(.62)
    cv.rect(0,s.h-383,306,383,fill=1,stroke=0);cv.restoreState()
    text(s,b,'The Last\nAcquisition',38,72,375,51,'BookBold',leading=.98)
    text(s,b,'A museum gala\nmurder mystery',42,238,320,23,'BookItalic')
    text(s,b,'The Meridian Museum',42,321,400,18,'Book',GOLD)
    rule(s,388,color=b.GOLD if print_mode else GOLD)
    text(s,b,'You are part of the collection.',42,407,528,25,'BookItalic',accent)
    cv.setFillColor(b.PALE if print_mode else WINE);cv.rect(0,s.h-555,612,102,fill=1,stroke=0)
    text(s,b,'Friday, October 30, 2026',42,469,528,27,'BookBold',ink)
    text(s,b,'6:00 PM  /  Tulsa, Oklahoma',42,505,528,21,'Book',accent)
    text(s,b,b.GAME['address'],42,576,528,19,'BookBold',ink)
    text(s,b,'The Grant Larceny Collection opens with a gala and the unveiling of the thirteenth-century Isfahan Star Bowl.',42,619,528,16,color=ink)
    text(s,b,'Formal gala attire with art-world flair. Make the role your own.',42,678,528,16,color=ink)
    text(s,b,'Read your character sheet before the party. Your private packet awaits you at the gala.',42,723,528,16,'BookItalic',accent)
