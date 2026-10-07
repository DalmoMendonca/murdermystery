"""Actual museum records and photographic exhibits, not descriptions of props."""
import json
from pathlib import Path

def draw_discovery(s,d,top,b):
    x=42;w=528;bottom=top+302
    s.rect(x,top,w,302,stroke=b.INK,dash=[3,3])
    s.rect(x+4,top+4,w-8,294,stroke=b.GOLD)
    y=s.block(d['department'],58,top+13,496,12,'BookBold',b.TEAL)+6
    y=s.block(d['title'],58,y,496,22,'BookBold')+10
    if d.get('photo'):
        s.image(b.ROOT/'assets/evidence'/(d['photo']+'.jpg'),58,y,496,116)
        s.rect(58,y,496,116,stroke=b.GOLD);y+=126
    for row in d.get('rows',[]):
        a=s.block(row[0],58,y,170,14,'BookBold');z=s.block(row[1],242,y,312,14);y=max(a,z)+5
    for t in d.get('paragraphs',[]):y=s.block(t,58,y,496,14)+7
    if d.get('annotation'):y=s.block(d['annotation'],58,y+3,496,14,'BookItalic',b.RED)+5
    if d.get('stamp'):s.block(d['stamp'],58,bottom-35,496,12,'BookBold',b.RED,bottom=bottom-16)
    s.block('Discovery '+str(d['number']),440,bottom-18,114,12,'Book',b.TEAL,bottom=bottom-2)

def diagram(s,kind,y,b):
    """Print diagrams carry actual route/material information, with readable labels."""
    if kind=='preparation_routes':
        s.rect(42,y,240,154,fill=b.PALE,stroke=b.GOLD)
        s.rect(322,y,248,154,stroke=b.GOLD)
        s.block('WEST / CORRIDOR',55,y+12,214,16,'BookBold',b.RED)
        s.block('Return counter',55,y+45,214,16)
        s.block('Papers pass to staff',55,y+85,214,14)
        s.block('EAST / VISITOR ROOM',335,y+12,222,16,'BookBold',b.RED)
        s.block('Open source shelves',335,y+45,222,16)
        s.block('Visitor entrance',335,y+108,222,14)
        s.rect(292,y,20,154,fill=b.INK)
        s.block('FIXED BARRIER',42,y+165,528,14,'BookBold')
        return y+198
    s.rect(42,y,250,142,fill=b.PALE,stroke=b.GOLD)
    s.rect(320,y,250,142,fill=b.PALE,stroke=b.GOLD)
    s.block('FACTORY FILM',55,y+10,224,16,'BookBold',b.RED)
    s.block('REUSABLE FELT',333,y+10,224,16,'BookBold',b.RED)
    s.line(165,y+42,165,y+102)
    s.rect(90,y+62,148,31,stroke=b.RED)
    s.block('MERIDIAN',101,y+67,125,16,'BookBold',b.RED)
    s.rect(366,y+62,148,31,stroke=b.RED,dash=[2,2])
    s.block('MERIDIAN',377,y+67,125,16,'BookBold',b.RED)
    s.block('Crest crosses joined seam',55,y+114,224,14)
    s.block('Crest stitched into fabric',333,y+114,224,14)
    return y+166

def build_evidence(b):
    docs=json.loads((b.ROOT/'source/discoveries.json').read_text(encoding='utf-8'))
    s=b.Sheet(b.KIT/'PRINT_WITHOUT_READING/Discovery_Props.pdf','Museum discovery documents')
    for i,d in enumerate(docs):
        s.header('DISCOVERY '+str(d['number']),True)
        y=s.block(d['department'],42,110,528,16,'BookBold',b.RED)+12
        y=s.block(d['title'],42,y,528,32,'BookBold')+24
        if d.get('photo'):
            s.image(b.ROOT/'assets/evidence'/(d['photo']+'.jpg'),42,y,528,245)
            s.rect(42,y,528,245,stroke=b.GOLD);y+=265
        for row in d.get('rows',[]):
            a=s.block(row[0],42,y,170,17,'BookBold');z=s.block(row[1],226,y,344,17);y=max(a,z)+10
        for t in d.get('paragraphs',[]):y=s.block(t,42,y,528,24 if d['number']==3 else 18,'BookItalic' if d['number']==3 else 'Book')+14
        if d.get('annotation'):y=s.block(d['annotation'],42,y+12,528,17,'BookItalic',b.RED)+14
        if d.get('stamp'):s.block(d['stamp'],42,y+16,528,14,'BookBold',b.RED,bottom=730)
        s.footer('The Meridian Museum / Discovery '+str(d['number']))
        if i+1<len(docs):s.next()
    s.save()
    reports=json.loads((b.ROOT/'source/investigation.json').read_text(encoding='utf-8'))
    paths=[]
    for report in reports:
        key=report['id'];s=b.Sheet(b.KIT/'PRINT_WITHOUT_READING/Reports'/(key+'.pdf'),report['title'])
        s.header(report['department'])
        y=s.block(report['title'],42,105,528,30,'BookBold',b.TEAL)+17
        y=s.block('MERIDIAN / OCT 30, 2026 / '+key,42,y,528,14,'BookBold')+22
        if report.get('photo'):
            s.image(b.ROOT/'assets/evidence'/(report['photo']+'.jpg'),183,y,246,165)
            s.rect(183,y,246,165,stroke=b.GOLD);y+=182
        for label,value in report.get('rows',[]):
            left=s.block(label,42,y,200,16,'BookBold',b.RED)
            right=s.block(value,254,y,316,16)
            y=max(left,right)+12
        s.line(42,y+3,570,y+3);y+=25
        s.block(report['text'],42,y,528,16,bottom=725)
        s.footer(key+' / Read aloud and display at the announced release')
        if report.get('appendix'):
            a=report['appendix'];s.next();s.header(report['department']+' / continued')
            y=s.block(a['title'],42,105,528,28,'BookBold',b.TEAL)+15
            y=s.block('MERIDIAN / OCT 30, 2026 / '+key+' / 2',42,y,528,14,'BookBold')+20
            y=diagram(s,a['diagram'],y,b)
            for label,value in a['rows']:
                left=s.block(label,42,y,200,16,'BookBold',b.RED)
                right=s.block(value,254,y,316,16);y=max(left,right)+10
            s.line(42,y+3,570,y+3);y+=21
            s.block(a['text'],42,y,528,16,bottom=725)
            s.footer(key+' / 2 / Read aloud and display with the first page')
        s.save();paths.append(s.path)
    b.merge(paths,b.KIT/'PRINT_WITHOUT_READING/Forensic_Reports.pdf')
    b.merge([b.KIT/'PRINT_WITHOUT_READING/Discovery_Props.pdf']+paths,b.KIT/'PRINT_WITHOUT_READING/04B_Clues_and_Forensics_PRINT_DO_NOT_READ.pdf')
