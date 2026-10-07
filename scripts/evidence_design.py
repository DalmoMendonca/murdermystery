"""Photographic exhibits with precise, typeset records and player-facing names."""
import json

def rows(s,items,y,b,size=16,left=180,gap=9):
    for label,value in items:
        a=s.block(label,42,y,left,size,'BookBold',b.RED)
        z=s.block(value,54+left,y,516-left,size)
        y=max(a,z)+gap
    return y

def photo(s,name,y,h,b):
    s.image(b.ROOT/'assets/evidence'/(name+'.jpg'),42,y,528,h)
    return y+h+14

def heading(s,title,label,b):
    s.header(label)
    return s.block(title,42,103,528,28,'BookBold',b.RED)+17

def service(s,report,y,b):
    # Place each photograph without mixing neighboring quadrants or distorting it.
    from PIL import Image
    path=b.ROOT/'assets/evidence'/(report['photo']+'.jpg')
    with Image.open(path) as im:iw,ih=im.size
    full_h=292;full_w=full_h*iw/ih;half_w=full_w/2
    for i,t in enumerate(report['timeline']):
        x=42+(i%2)*264;py=y+(i//2)*190;px=x+(264-half_w)/2
        s.c.saveState();clip=s.c.beginPath();clip.rect(px,s.h-py-146,half_w,146)
        s.c.clipPath(clip,stroke=0,fill=0)
        s.image(path,px-(i%2)*half_w,py-(i//2)*146,full_w,full_h)
        s.c.restoreState()
        s.rect(x,py+146,264,40,fill=b.PALE,stroke=b.PALE)
        s.block(t['time']+' / '+t['caption'],x+8,py+150,248,14,'BookBold',bottom=py+186)
    return y+380+12

def findings(s,report,y,b):
    for label,value in report['rows']:
        s.rect(42,y,528,66,fill=b.PALE,stroke=b.GOLD)
        s.block(label,56,y+10,500,16,'BookBold')
        s.block(value,56,y+34,500,16,'BookBold',b.RED)
        y+=77
    return y+8

def build_evidence(b):
    docs=json.loads((b.ROOT/'source/discoveries.json').read_text(encoding='utf-8'))
    s=b.Sheet(b.KIT/'PRINT_WITHOUT_READING/Discovery_Props.pdf','Museum discovery documents')
    for i,d in enumerate(docs):
        y=heading(s,d['title'],'DISCOVERY '+str(d['number'])+' / '+d['department'],b)
        if d.get('photo'):y=photo(s,d['photo'],y,195 if d['number']==13 else 245,b)
        y=rows(s,d.get('rows',[]),y,b,17,170,10)
        for t in d.get('paragraphs',[]):y=s.block(t,42,y,528,24 if d['number']==3 else 18,'BookItalic' if d['number']==3 else 'Book')+14
        if d.get('annotation'):y=s.block(d['annotation'],42,y+8,528,17,'BookItalic',b.RED)+10
        if d.get('stamp'):s.block(d['stamp'],42,y+12,528,14,'BookBold',b.RED,bottom=730)
        s.footer('The Meridian Museum / Discovery '+str(d['number']))
        if i+1<len(docs):s.next()
    s.save()
    reports=json.loads((b.ROOT/'source/investigation.json').read_text(encoding='utf-8'));paths=[]
    for r in reports:
        number=int(r['id'][1:]);label='EVIDENCE '+str(number)
        s=b.Sheet(b.KIT/'PRINT_WITHOUT_READING/Reports'/(r['id']+'.pdf'),r['title'])
        y=heading(s,r['title'],label+' / '+r['department'],b)
        if number==1:
            s.rect(42,y,528,45,fill=b.PALE,stroke=b.GOLD)
            s.block(r['document_label'],56,y+13,500,16,'BookBold',b.RED);y+=65
            for key,value in r['rows']:
                s.block(key,56,y,500,16,'BookBold',b.RED);y+=28
                y=s.block(value,56,y,500,22,'BookBold')+22;s.line(56,y,556,y);y+=24
            y=s.block('Donor signature: __________________________',56,y,500,16)+34
        elif number==3:
            y=service(s,r,y,b)
        elif number==5:
            y=findings(s,r,y,b)
        else:
            y=photo(s,r['photo'],y,210 if number==4 else 245,b)
            if number==4:y=s.block('Recovered bottle / photographed during the investigation',42,y,528,14,'BookItalic')+14
            y=rows(s,r['rows'],y,b,16,180,10)+8
        if number in [1,5]:pass
        elif number==3:y=rows(s,r['rows'],y,b,15,180,6)+4
        s.block(r['text'],42,y,528,15 if number==3 else 16,bottom=730)
        s.footer(label+' / Read aloud and display at the announced round')
        if r.get('appendix'):
            a=r['appendix'];s.next();y=heading(s,a['title'],label+' / SUPPORTING RECORD',b)
            y=photo(s,a['photo'],y,285 if number==4 else 265,b)
            y=rows(s,a['rows'],y,b,16,180,10)+8
            s.line(42,y,570,y);y+=17
            s.block(a['text'],42,y,528,16,bottom=730)
            s.footer(label+' / Supporting record / Display with the first page')
        if r.get('trace_exhibit'):
            a=r['trace_exhibit'];s.next();y=heading(s,a['title'],label+' / MATERIAL COMPARISON',b)
            y=photo(s,a['photo'],y,345,b)
            s.block(a['text'],42,y+10,528,18,bottom=730)
            s.footer(label+' / Display with the laboratory findings')
        s.save();paths.append(s.path)
    b.merge(paths,b.KIT/'PRINT_WITHOUT_READING/Forensic_Reports.pdf')
    b.merge([b.KIT/'PRINT_WITHOUT_READING/Discovery_Props.pdf']+paths,b.KIT/'PRINT_WITHOUT_READING/04B_Clues_and_Forensics_PRINT_DO_NOT_READ.pdf')
