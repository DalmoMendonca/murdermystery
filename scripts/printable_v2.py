"""Gala posters and self-contained, paced twelve-page player books."""
import json, html, re, math
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph

from print_identity import GOLD

def ornament(s):
    s.rect(28,28,556,736,stroke=GOLD)
    s.rect(33,33,546,726,stroke=GOLD)
    for x,y in [(33,33),(579,33),(33,759),(579,759)]:
        c=s.c;c.saveState();c.setStrokeColor(GOLD);c.setLineWidth(.7)
        c.circle(x,s.h-y,7,stroke=1,fill=0)
        c.line(x-12,s.h-y,x+12,s.h-y);c.line(x,s.h-y-12,x,s.h-y+12)
        c.restoreState()

def framed(s,b,path,x,y,w,h):
    # Native alpha in the generated frame preserves the painted portrait underneath.
    fw=min(w,h*2/3);fh=fw*1.5;x+=(w-fw)/2;y+=(h-fh)/2
    ax,ay,aw,ah=x+fw*.18,y+fh*.14,fw*.64,fh*.72
    s.c.saveState();clip=s.c.beginPath();clip.rect(ax,s.h-ay-ah,aw,ah);s.c.clipPath(clip,stroke=0,fill=0)
    pw=max(aw,ah*2/3);ph=pw*1.5
    s.image(path,ax+(aw-pw)/2,ay+(ah-ph)/2,pw,ph)
    s.c.restoreState()
    s.image(b.ROOT/'assets/ornaments/gilt_frame.png',x,y,fw,fh)

def pagehead(s,b,c,phase):
    from print_identity import museum_mark
    s.block(phase,42,30,528,16,'BookBold',b.TEAL)
    s.block(c['name'],42,62,528,14,'BookBold')
    s.line(42,89,570,89)
    museum_mark(s.c,542,28,s.h,22)
    s.c.saveState();s.c.setStrokeColor(GOLD);s.c.setLineWidth(.4);s.c.line(42,s.h-92,570,s.h-92);s.c.restoreState()

def pagefoot(s,b,stop=True,extra=None):
    if stop:
        s.rect(42,686,528,61,fill=b.PALE,stroke=b.RED)
        cv=s.c;cv.saveState();cv.setFillColor(b.RED);cv.setStrokeColor(b.RED)
        p=cv.beginPath();cx,cy=66,s.h-716;radius=20
        for i in range(8):
            a=math.pi/8+i*math.pi/4;xx=cx+radius*math.cos(a);yy=cy+radius*math.sin(a)
            if i:p.lineTo(xx,yy)
            else:p.moveTo(xx,yy)
        p.close();cv.drawPath(p,fill=1,stroke=1);cv.setFillColor(white);cv.setFont('BookBold',12);cv.drawCentredString(cx,cy-4,'STOP');cv.restoreState()
        s.block('STOP! Do not turn the page yet.\nWait for the host to announce the next round.',96,700,457,14,'BookBold',b.RED,bottom=743)
    elif extra:s.block(extra,42,708,528,14,'BookItalic',b.TEAL)
    s.footer(f'Murder Mystery Dinner Party 2026 / {s.page} of 12')

def relationship_paragraph(b,text,w,size,names):
    aliases=set(names)|{n.split()[0] for n in names if not n.startswith('Dr.')}
    if 'Dr. Art E. Fact' in names:aliases.add('Art')
    pattern=r'\b(?:'+'|'.join(re.escape(n) for n in sorted(aliases,key=len,reverse=True))+r')\b'
    pieces=[];end=0
    for m in re.finditer(pattern,text):
        pieces.append(html.escape(text[end:m.start()]));pieces.append('<font backColor="#fff099"><b>'+html.escape(m[0])+'</b></font>');end=m.end()
    pieces.append(html.escape(text[end:]));markup=''.join(pieces)
    p=Paragraph(markup,ParagraphStyle('relationships',fontName='Book',fontSize=size,leading=size*1.25,textColor=b.INK,allowWidows=0,allowOrphans=0))
    _,h=p.wrap(w,10000)
    return p,h

def rich(s,b,text,x,y,w,size,names):
    p,h=relationship_paragraph(b,text,w,size,names)
    assert y+h<=675,(s.path.name,y+h,text)
    p.drawOn(s.c,x,s.h-y-h);b.AUDIT.append(dict(file=str(s.path.relative_to(b.KIT)),page=s.page,x=x,y=y,width=w,height=h,size=size,text=text));return y+h

def poster(chars,b):
    paths=[]
    for c in chars:
        s=b.Sheet(b.KIT/'OPEN_FREELY/PreParty_Individual'/f'{c["slug"]}.pdf',c['name'])
        ornament(s);p=c['preparty']
        s.block(c['name'],48,49,516,34,'BookBold',b.TEAL)
        s.block(c['role'],48,98,516,16,'BookItalic',bottom=146)
        s.line(48,142,564,142)
        def estimate(size,gap=6,acting_gap=12,costume_gap=17):
            y=max(382,157+b.para(p['description'],318,size)[1])+15
            y+=sum(b.para('• '+t,516,size)[1]+gap for t in p['relationships'])
            y+=acting_gap+6+20+5+b.para(p['acting'],516,size)[1]
            y+=costume_gap+20+5+b.para(p['costume'],516,size)[1]
            return y
        layout=next((v for v in [(17,6,12,17),(16,6,12,17),(16,4,10,12)] if estimate(*v)<=728),None)
        assert layout,(c['name'],estimate(16))
        size,gap,acting_gap,costume_gap=layout
        framed(s,b,b.ROOT/'assets/portraits'/c['slug']/'van_gogh.jpg',41,150,196,234)
        y=s.block(p['description'],246,157,318,size,bottom=425)
        y=max(382,y)+15
        for t in p['relationships']:y=s.block('• '+t,48,y,516,size,bottom=728)+gap
        y=s.block('ACTING TIPS',48,y+acting_gap,516,16,'BookBold',b.TEAL,bottom=728)+5
        y=s.block(p['acting'],48,y,516,size,bottom=728)
        y=s.block('COSTUME SUGGESTIONS',48,y+costume_gap,516,16,'BookBold',b.TEAL,bottom=728)+5
        s.block(p['costume'],48,y,516,size,bottom=728)
        s.block('October 30, 2026 / Meridian Museum Gala',48,740,516,12,'BookItalic',b.TEAL,bottom=758)
        s.save();paths.append(s.path)
    b.merge(paths,b.KIT/'OPEN_FREELY/02_PreParty_Character_Sheets_ALL.pdf')

def questions(s,c,rd,b):
    phase={'motive':'ACT I: MOTIVE','opportunity':'ACT II: OPPORTUNITY','method':'ACT III: METHOD'}[rd['key']]
    pagehead(s,b,c,phase)
    s.block('Questions for the room',42,109,528,27,'BookBold',b.TEAL)
    answer=b.GAME['packet_pages'][rd['key']+'_answer']
    s.block(f'Choose a named guest who has not answered. Skip absent names. Ask their question; they answer from page {answer}, then choose the next guest.',42,153,528,14)
    for half in range(2):
        x=42+half*276;y=226
        for g in rd['groups'][half*5:half*5+5]:
            y=s.block(' / '.join(g['targets']),x,y,252,14,'BookBold',b.TEAL,bottom=698)+4
            y=s.block(g['question'],x,y,252,14,bottom=698)+12
            s.line(x,y-6,x+252,y-6)
    pagefoot(s,b,False,f'Your speaking box is on page {answer}. Turn only within this act.');s.next()

def speech(s,label,words,y,b,size=16):
    y=s.block(label,42,y,528,16,'BookBold',b.TEAL,bottom=674)+8
    if label.startswith('YOUR INTRODUCTION'):
        paragraph,_=b.para(words,492,size)
        last=paragraph.blPara.lines[-1]
        tail=' '.join(getattr(fragment,'text','') for fragment in last.words) if paragraph.blPara.kind else ' '.join(last[1])
        if len(tail.split())==1:
            words=re.sub(r'(\S+)\s+(\S+)$',lambda match:match[1]+'\u00a0'+match[2],words)
    h=b.para(words,492,size)[1]
    s.rect(42,y,528,h+22,fill=b.PALE,stroke=b.RED)
    return s.block(words,60,y+11,492,size,bottom=674)+24

def cover(s,b,c):
    # An exhibition-poster axis: event, painting, sitter, museum/date.
    # The frame supplies the ornament; the outer mat stays quiet.
    s.rect(28,28,556,736,stroke=GOLD)
    s.rect(33,33,546,726,stroke=GOLD)
    def centered(text,y,size,font='Book',color=b.INK,leading=None):
        p=Paragraph(html.escape(text),ParagraphStyle('CoverCentered',fontName=font,
            fontSize=size,leading=leading or size*1.2,alignment=TA_CENTER,
            textColor=color,allowWidows=0,allowOrphans=0))
        _,height=p.wrap(516,10000)
        assert y+height<=755,(c['name'],text)
        p.drawOn(s.c,48,s.h-y-height)
        b.AUDIT.append(dict(file=str(s.path.relative_to(b.KIT)),page=s.page,x=48,y=y,
            width=516,height=height,size=size,text=text,alignment='center'))
        return y+height
    def rule(y,width):
        cv=s.c;cv.saveState();cv.setStrokeColor(GOLD);cv.setLineWidth(.65)
        cv.line(306-width/2,s.h-y,306+width/2,s.h-y);cv.restoreState()
    centered('Murder Mystery',54,34,'BookBold')
    centered('Dinner Party 2026',99,23,'BookItalic',b.RED)
    rule(141,160)
    framed(s,b,b.ROOT/'assets/portraits'/c['slug']/'picasso.jpg',144,156,324,462)
    centered(c['name'],636,36,'BookBold')
    rule(695,160)
    centered('The Meridian Museum',711,14,'BookItalic',b.RED)
    centered('October 30, 2026  /  Private player packet  /  1 of 12',735,12)

def packets(chars,b):
    rounds=json.loads((b.ROOT/'source/question_rounds.json').read_text(encoding='utf-8'))
    from hunt_copy import load_hunt
    hunt=load_hunt(b.ROOT)
    paths=[];relationship_report=[]
    for c in chars:
        p=c['private'];h=c['hearing'];s=b.Sheet(b.KIT/'PRINT_WITHOUT_READING/Secret_Individual'/f'{c["slug"]}_SECRET.pdf',c['name']+' / complete packet')
        cover(s,b,c)
        # Safe face-up: no grievance, animal, branch or secret appears on this cover.
        s.next()
        pagehead(s,b,c,'INTRODUCTIONS')
        names=[v['name'] for v in chars if v['name']!=c['name']]
        relationships=list(c['preparty']['relationships'])
        def introduction_bottom(bullets):
            y=109+b.para(c['role'],528,20,'BookItalic')[1]+13
            y+=b.para(c['preparty']['description'],528,16)[1]+12
            y+=sum(relationship_paragraph(b,'• '+t,528,16,names)[1]+7 for t in bullets)
            y+=8+b.para('ACTING TIPS',528,16,'BookBold')[1]+5
            y+=b.para(c['preparty']['acting'],528,16)[1]+14
            y+=b.para('YOUR INTRODUCTION / READ THE BOX ALOUD',528,16,'BookBold')[1]+8
            return y+b.para(c['introduction'],492,16)[1]+22
        for t in c['preparty'].get('packet_relationships',[]):
            fits=introduction_bottom(relationships+[t])<=674
            if fits:relationships.append(t)
            relationship_report.append({'character':c['name'],'text':t,'included':fits})
        y=s.block(c['role'],42,109,528,20,'BookItalic',b.TEAL)+13
        y=s.block(c['preparty']['description'],42,y,528,16,bottom=675)+12
        for t in relationships:
            y=rich(s,b,'• '+t,42,y,528,16,names)+7
        y=s.block('ACTING TIPS',42,y+8,528,16,'BookBold',b.TEAL,bottom=675)+5
        y=s.block(c['preparty']['acting'],42,y,528,16,bottom=675)+14
        speech(s,'YOUR INTRODUCTION / READ THE BOX ALOUD',c['introduction'],y,b,16)
        pagefoot(s,b,False,'Continue to your private briefing on page 3. Keep the packet facing you.');s.next()
        pagehead(s,b,c,'INTRODUCTIONS')
        y=s.block('Behind the portrait',42,109,528,27,'BookBold',b.TEAL)+17
        for label,key in [('Your grievance with Grant','history'),('Your other secret','secret')]:
            y=s.block(label,42,y,528,16,'BookBold',b.TEAL)+6
            y=s.block(p[key],42,y,528,16,bottom=675)+16
        y=s.block('Conversations to start',42,y,528,18,'BookBold',b.TEAL)+8
        for t in p['objectives'][:2]:y=s.block('• '+t,42,y,528,16,bottom=675)+8
        y=s.block('If a named guest is absent, speak to someone else. Your printed account may conceal another scandal, even if you are innocent. Stick to it during the hearings.',42,y+7,528,14,'BookItalic',bottom=675)+15
        s.block('By now, you should have drawn a secret animal. Memorize it and don’t share it with anyone. This animal is YOUR key to knowing whether you are the murderer or innocent tonight. This will tell you which sections of this packet you can read out loud.',42,y,528,14,bottom=675)
        pagefoot(s,b);s.next()
        pagehead(s,b,c,'HUNT FOR CLUES')
        y=s.block('The game is afoot',42,111,528,28,'BookBold',b.TEAL)+19
        y=s.block('The Meridian Museum has its share of secrets, rumors, and lost paperwork. Sixteen numbered envelopes are hidden around the museum. Their contents may significantly help you tonight. These 3 hints lead to 3 different hiding places. If you find an envelope, bring it to your seat at the table. The guest with the most envelopes will win a special prize. You may investigate together.',42,y,528,16)+22
        for i,hint in enumerate(hunt['characters'][c['slug']]):
            s.block(str(i+1),42,y,35,26,'BookBold',GOLD)
            y=s.block(hint['text'],93,y,477,19,'BookItalic',bottom=634)+28
        pagefoot(s,b);s.next()
        for rd in rounds:
            questions(s,c,rd,b);key=rd['key']
            pagehead(s,b,c,{'motive':'ACT I: MOTIVE','opportunity':'ACT II: OPPORTUNITY','method':'ACT III: METHOD'}[key])
            y=s.block('Your answer',42,109,528,27,'BookBold',b.TEAL)+12
            y=s.block('Read only the bordered words when asked. Keep your packet facing you. After answering, ask an unheard guest their question from the previous page.',42,y,528,14)+18
            base={'motive':'motive','opportunity':'where','method':'evidence'}[key]
            words=[h[base+'_'+branch] for branch in ['innocent','murderer']]
            size=next((size for size in [16,15] if y+sum(b.para(t,492,size)[1]+61 for t in words)<=659),None)
            assert size,(c['name'],key,'Speaking boxes must fit at15pt or larger')
            for branch,t in zip(['innocent','murderer'],words):y=speech(s,'IF '+branch.upper(),t,y,b,size)+6
            # No evidence checklist, no three-column grid, no scripted direction toward selected clues.
            if key=='method':
                if y<620:s.block('The sixteen discoveries and five reports remain at the Evidence Table.',42,y+13,528,14,'BookItalic',bottom=675)
            pagefoot(s,b);s.next()
        pagehead(s,b,c,'ACCUSATIONS')
        y=s.block('Your ballot',42,109,528,30,'BookBold',b.TEAL)+17
        y=s.block('Choose one attending guest. Explain your accusation in your own words. Tear off this page and give only the ballot to the host for tallying. Keep your packet for Coming Clean.',42,y,528,16)+25
        for label in ['Your character name','I accuse','Why? Motive, evidence and any unresolved contradiction','Best Actor','Best Costume']:
            y=s.block(label,42,y,528,16,'BookBold',b.TEAL)+31
            s.line(42,y,570,y);y+=25
            if label.startswith('Why?'):s.line(42,y,570,y);y+=28
        pagefoot(s,b,False);s.next()
        pagehead(s,b,c,'COMING CLEAN')
        y=s.block('The last word',42,109,528,27,'BookBold',b.TEAL)+13
        y=s.block('Read only when the host calls you. Top three suspects read first. Use your own role’s box; keep every other word private.',42,y,528,14)+16
        for branch in ['innocent','murderer']:
            y=speech(s,'IF '+branch.upper()+' / READ ALOUD WHEN CALLED',p['final_'+branch],y,b,15)+6
        pagefoot(s,b,False,'Every selected suspect gets their final word.');s.save();paths.append(s.path)
    b.merge(paths,b.KIT/'PRINT_WITHOUT_READING/03_Secret_Player_Packets_PRINT_DO_NOT_READ.pdf')
    (b.WORK/'packet_relationship_fit.json').write_text(json.dumps(relationship_report,indent=2),encoding='utf-8')

def tents(chars,b):
    s=b.Sheet(b.KIT/'OPEN_FREELY/09_Host_Safe_Name_Cards.pdf','Foldable guest tent cards')
    from reportlab.pdfbase.pdfmetrics import stringWidth
    def single_line(text,maximum,width):
        size=min(maximum,width/stringWidth(text,'BookBold',1))
        assert b.para(text,width,size,'BookBold')[1]<=size*1.25+.1
        return size
    for i,c in enumerate(chars):
        # Use the entire sheet: two four-inch faces and equal 1.5-inch base flaps.
        # No trim boundary: the only printed rules are dotted fold guides.
        s.block('Fold on the dotted lines. Overlap and tape the base flaps.',42,21,528,12,'Book',b.TEAL)
        for y in [108,396,684]:
            s.c.saveState();s.c.setStrokeColor(GOLD);s.c.setLineWidth(.8);s.c.setDash([1,3]);s.c.line(14,792-y,598,792-y);s.c.restoreState()
        width=365
        first_size=single_line(c['card_name']['first_middle'],64,width)
        last_size=single_line(c['card_name']['last'],76,width)
        role_size=next(size/4 for size in range(208,63,-1)
                       if b.para(c['role'],width,size/4,'BookItalic')[1]<=min(65,2*(size/4)*1.25+.1))
        assert b.para(c['role'],width,role_size,'BookItalic')[1]<=65
        for top,reverse in [(108,True),(396,False)]:
            s.c.saveState()
            if reverse:
                # Rotate the upper face around its centre so both names read upright on the tent.
                s.c.translate(612,2*(792-top-144));s.c.rotate(180)
            s.block(c['card_name']['first_middle'],42,top+22,width,first_size,'BookBold',b.INK,bottom=top+103)
            s.block(c['card_name']['last'],42,top+105,width,last_size,'BookBold',b.TEAL,bottom=top+201)
            s.block(c['role'],42,top+211,width,role_size,'BookItalic',bottom=top+278)
            s.image(b.ROOT/'assets/portraits'/c['slug']/'chibi.webp',425,top+18,145,249)
            s.c.restoreState()
        s.block('BASE / fold inward',60,59,480,14,'BookBold',GOLD,bottom=94)
        s.block('BASE / overlap and tape',60,711,480,14,'BookBold',GOLD,bottom=746)
        if i+1<len(chars):s.next()
    s.save()
