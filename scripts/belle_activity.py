"""Reproducible honorary guest book with image-generated museum artwork. No mystery data needed."""
from pathlib import Path
import math,shutil,yaml
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.lib.utils import ImageReader
import build as b

ROOT=Path(__file__).resolve().parents[1]
INK=HexColor('#302c2b');RED=HexColor('#782e3e');GOLD=HexColor('#aa843e')
LIGHT=HexColor('#fbf8f0');BLUE=HexColor('#5f8995');HAIR=HexColor('#dbc17b')

def star(c,x,y,r,color=GOLD,fill=False):
    p=c.beginPath()
    for i in range(10):
        a=math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*.44
        xx=x+math.cos(a)*rr; yy=y+math.sin(a)*rr
        (p.moveTo if i==0 else p.lineTo)(xx,yy)
    p.close();c.setStrokeColor(color);c.setFillColor(color)
    c.drawPath(p,fill=int(fill),stroke=1)

def ornate(c,x,y,w,h,color=GOLD):
    c.setStrokeColor(color);c.setLineWidth(.7);c.rect(x,y,w,h);c.rect(x+4,y+4,w-8,h-8)
    for xx,yy in [(x,y),(x+w,y),(x,y+h),(x+w,y+h)]:
        c.circle(xx,yy,3);c.line(xx-7,yy,xx+7,yy);c.line(xx,yy-7,xx,yy+7)

def art(c,name,x,y,w,h):
    """Place the original generated art without changing its pixels."""
    c.drawImage(str(ROOT/'assets/children/belle'/f'{name}.png'),x,792-y-h,w,h,mask='auto',preserveAspectRatio=True,anchor='c')

def atlas_icon(c,index,x,y,w,h):
    """Clip one cell of the original atlas during PDF layout."""
    path=ROOT/'assets/children/belle/bingo-icons.png'
    boxes=[(38,90,411,330),(458,40,797,385),(881,40,1195,384),(25,426,416,801),(438,425,819,801),(840,535,1232,708),(25,813,411,1205),(454,818,811,1192),(847,808,1226,1192)]
    x0,y0,x1,y1=boxes[index];scale=min(w/(x1-x0),h/(y1-y0));bw=(x1-x0)*scale;bh=(y1-y0)*scale
    xx=x+(w-bw)/2;yy=792-y-h+(h-bh)/2
    c.saveState();clip=c.beginPath();clip.rect(xx,yy,bw,bh);c.clipPath(clip,stroke=0)
    c.drawImage(str(path),xx-x0*scale,yy-(1254-y1)*scale,1254*scale,1254*scale,mask='auto')
    c.restoreState()

class Book:
    def __init__(self,path,title):
        path.parent.mkdir(parents=True,exist_ok=True);self.path=path;self.page=1
        self.c=canvas.Canvas(str(path),pagesize=(612,792),invariant=1)
        self.c.setTitle(title);self.c.setAuthor('The Meridian Museum')
    def text(self,text,x,y,width=528,size=18,font='Book',color=INK):
        p,h=b.para(text,width,size,font,color);assert y+h<744,(self.page,text[:30],y+h)
        p.drawOn(self.c,x,792-y-h);return y+h
    def centered(self,text,y,size=28,font='BookBold',color=RED):
        self.c.setFillColor(color);self.c.setFont(font,size);self.c.drawCentredString(306,792-y,text)
    def head(self,title,instruction=''):
        self.centered('MERIDIAN MUSEUM / JUNIOR CURATOR',42,12,'BookBold',GOLD)
        self.text(title,42,70,528,30,'BookBold',RED)
        if instruction:self.text(instruction,42,120,528,18)
    def frame(self,x,y,w,h):ornate(self.c,x,792-y-h,w,h)
    def next(self):
        self.c.setStrokeColor(GOLD);self.c.setLineWidth(.5);self.c.line(42,47,570,47)
        self.c.setFillColor(INK);self.c.setFont('Book',11);self.c.drawString(42,29,'Belle Tament / Museum Gala 2026');self.c.drawRightString(570,29,str(self.page))
        self.c.showPage();self.page+=1
    def save(self):self.c.save()

def word_paths(grid,word):
    paths=[]
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            for dr,dc in ((0,1),(1,0)):
                cells=[(row+dr*i,col+dc*i) for i in range(len(word))]
                if all(r<len(grid) and c<len(grid[0]) for r,c in cells) and ''.join(grid[r][c] for r,c in cells)==word:paths.append(cells)
    return paths

def create(kit,site):
    data=yaml.safe_load((ROOT/'source/children/belle_tament.yaml').read_text(encoding='utf-8'));b.fonts()
    packet=kit/'OPEN_FREELY/07_Belle_Tament_Activity_Book.pdf';book=Book(packet,'Belle Tament / Junior Curator Activity Book');c=book.c
    book.frame(28,27,556,709)
    book.centered('MURDER MYSTERY DINNER PARTY 2026',64,12,'BookBold',GOLD)
    book.centered('Belle Tament',121,43)
    book.centered('Junior Curator',162,29)
    book.centered('of Very Important Things',194,21,'BookItalic',INK)
    art(c,'cover',103,211,406,370)
    book.centered('A gala activity book for '+data['guest'],610,21,'BookBold',INK)
    book.centered('Draw. Explore. Make something wonderful.',653,18,'BookItalic',INK)
    book.centered('THE MERIDIAN MUSEUM / OCTOBER 30, 2026',705,11,'BookBold',GOLD);book.next()

    book.head('Meet Belle',"Ask Mom to read your story with you.")
    y=book.text(data['backstory'],42,172,528,19)+21
    for relationship in data['relationships']:
        y=book.text(relationship['name'],42,y,528,21,'BookBold',RED)+4
        y=book.text(relationship['text'],42,y,528,18)+17
    y=book.text('Your introduction',42,y,528,21,'BookBold',RED)+7
    book.text(data['introduction'],54,y,504,20,'BookItalic');book.next()

    for title,labels in [('Your gala portraits',('Who do you think did it?','The best actor')),('More gala portraits',('The best costume','Your favorite thing tonight'))]:
        book.head(title,'Draw your choices. Ask Mom to write a name if you like.')
        for x,label in zip((42,318),labels):
            book.text(label,x,180,252,22,'BookBold',RED);book.frame(x,254,252,452)
        book.next()

    book.head('Your very own museum','Draw three treasures you would put on display.')
    for i,y in enumerate((182,359,536),1):
        book.text('Treasure '+str(i),55,y,490,17,'BookBold',RED);book.frame(42,y+30,528,133)
    book.next()

    book.head('Look closely!','Find five big changes: look at the pictures, teddy, and toy.')
    art(c,'differences',122,166,368,552)
    book.next()

    book.head('Find four little words','Words go across or down. Circle each word you find.')
    grid=data['word_search']['grid'];cell=53;x0=173;y0=190
    assert len(grid)==5 and all(len(row)==5 for row in grid)
    for r,row in enumerate(grid):
        for col,ch in enumerate(row):
            c.setStrokeColor(GOLD);c.setLineWidth(.5);c.rect(x0+col*cell,792-y0-(r+1)*cell,cell,cell)
            c.setFillColor(INK);c.setFont('BookBold',29);c.drawCentredString(x0+(col+.5)*cell,792-y0-r*cell-37,ch)
    art(c,'word-icons',42,480,528,117)
    for i,word in enumerate(data['word_search']['words']):
        assert len(word_paths(grid,word))==1,(word,word_paths(grid,word))
        x=108+i*132
        c.setFillColor(RED);c.setFont('BookBold',24);c.drawCentredString(x,174,word)
    book.text('Picture clues help you find ART, CAT, GEM, and HAT.',42,643,528,18);book.next()

    book.head('Museum explorer bingo','Find it, then circle its picture. Ask a grown-up to help.')
    for i,label in enumerate(data['bingo']):
        col=i%3;row=i//3;x=42+col*176;y=194+row*162
        c.setStrokeColor(GOLD);c.setLineWidth(.6);c.roundRect(x+4,792-y-153,168,153,8)
        atlas_icon(c,i,x+35,y+5,106,92)
        p,h=b.para(label,146,17,'BookBold',INK);p.drawOn(c,x+15,792-y-104-h)
    book.text('Three in a row? Say "Bingo!"',42,697,528,18,'BookBold',RED)
    book.next()

    book.head('Color Belle\'s gallery','Give Belle, her teddy bear, and their museum some color.')
    art(c,'coloring',127,165,358,558);book.next()

    book.frame(33,57,546,650)
    book.centered('THE MERIDIAN MUSEUM',112,15,'BookBold',GOLD)
    book.centered('Honorary',190,41)
    book.centered('Junior Curator',237,39)
    book.centered('This certificate belongs to',300,19,'Book',INK)
    book.centered(data['guest'].upper(),363,42,'BookBold',INK)
    book.centered('Belle Tament',403,23,'BookItalic',RED)
    book.centered('For looking closely and making art',465,20,'Book',INK)
    book.centered('at the Museum Gala.',494,20,'Book',INK)
    c.setStrokeColor(GOLD);c.circle(306,228,34);c.circle(306,228,28);star(c,306,228,20,GOLD)
    c.line(155,130,457,130);book.centered('Signed by Mom / Tess Tament',686,16,'Book',INK);book.next();book.save()

    guide=Book(kit/'OPEN_FREELY/08_Belle_Tament_Adult_Notes.pdf','Belle Tament / Notes for Tiffany')
    guide.head('For Tiffany','Belle is an honorary guest. Her activities are optional.')
    y=guide.text('Print the ten-page activity book single-sided at 100%. Add crayons or colored pencils. Read the story together; Bennet can skip around and choose what she enjoys. Her drawings and awards are separate from the adults\' ballots. She needs no animal assignment or private clues.',42,165,528,17)+14
    y=guide.text('Costume suggestions',42,y,528,22,'BookBold',RED)+8
    y=guide.text(data['costume_suggestions'],42,y,528,17)+14
    y=guide.text('Five differences',42,y,528,22,'BookBold',RED)+8
    for i,answer in enumerate(data['spot_differences'],1):y=guide.text(str(i)+'. '+answer,42,y,528,17)+5
    y+=15;y=guide.text('Word-search answers',42,y,528,22,'BookBold',RED)+8
    for word in data['word_search']['words']:
        cells=word_paths(grid,word)[0];a,z=cells[0],cells[-1]
        y=guide.text(f'{word}: row {a[0]+1}, column {a[1]+1} to row {z[0]+1}, column {z[1]+1}.',42,y,528,16)+4
    guide.next();guide.save()
    site.mkdir(parents=True,exist_ok=True)
    for original,name in [(packet,'Belle_Tament_Activity_Book.pdf'),(guide.path,'Belle_Tament_Adult_Notes.pdf')]:shutil.copy2(original,site/name)
    return packet,guide.path

if __name__=='__main__':
    kit=ROOT/'build/connected-release-kit/The_Last_Acquisition_Complete_Kit'
    for p in create(kit,ROOT/'site/downloads'):print(p)
