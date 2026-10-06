"""Light-paper museum stationery: ink, burgundy and small gilt details."""
from reportlab.lib.colors import HexColor
INK=HexColor('#191b1c')
BURGUNDY=HexColor('#720f29')
GOLD=HexColor('#866632')
PALE=HexColor('#faf4f1')
RULE=HexColor('#b9aca3')

def museum_mark(cv,x,y,h,size=24):
    """A small architectural museum mark, drawn as print-safe geometry."""
    cv.saveState();cv.setStrokeColor(BURGUNDY);cv.setFillColor(BURGUNDY);cv.setLineWidth(.85)
    top=h-y
    p=cv.beginPath();p.moveTo(x,top-7);p.lineTo(x+size/2,top);p.lineTo(x+size,top-7);p.close()
    cv.drawPath(p,fill=0,stroke=1)
    for offset in [3,size/2,size-3]:cv.line(x+offset,top-10,x+offset,top-size+3)
    cv.line(x,top-size,x+size,top-size);cv.line(x+1,top-9,x+size-1,top-9)
    cv.restoreState()

def header_rules(cv,h,width):
    cv.saveState();cv.setStrokeColor(BURGUNDY);cv.setLineWidth(.9);cv.line(42,h-82,width-42,h-82)
    cv.setStrokeColor(GOLD);cv.setLineWidth(.4);cv.line(42,h-86,width-42,h-86);cv.restoreState()

def manual_frame(cv,doc,label,footer):
    museum_mark(cv,42,26,792,18)
    cv.saveState();cv.setFillColor(INK);cv.setFont('BookBold',14);cv.drawString(78,758,'MERIDIAN / 2026')
    cv.setFillColor(BURGUNDY);cv.setFont('Book',14);cv.drawString(42,733,label)
    header_rules(cv,792,612)
    cv.setStrokeColor(GOLD);cv.setLineWidth(.4);cv.line(42,46,570,46)
    cv.setFillColor(INK);cv.setFont('Book',12);cv.drawString(42,24,footer+' / '+str(doc.page));cv.restoreState()
