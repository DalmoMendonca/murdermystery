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

def build_evidence(b):
    docs=json.loads((b.ROOT/'source/discoveries.json').read_text(encoding='utf-8'))
    s=b.Sheet(b.KIT/'PRINT_WITHOUT_READING/Discovery_Props.pdf','Museum discovery documents')
    for i,d in enumerate(docs):
        s.header('DISCOVERY '+str(d['number'])+' / Fold for its numbered envelope',True)
        y=s.block(d['department'],42,104,528,14,'BookBold',b.RED)+8
        y=s.block(d['title'],42,y,528,28,'BookBold')+13
        if d.get('photo'):
            s.image(b.ROOT/'assets/evidence'/(d['photo']+'.jpg'),42,y,528,116)
            s.rect(42,y,528,116,stroke=b.GOLD);y+=128
        for row in d.get('rows',[]):
            a=s.block(row[0],42,y,170,14,'BookBold');z=s.block(row[1],226,y,344,14);y=max(a,z)+6
        for t in d.get('paragraphs',[]):y=s.block(t,42,y,528,14)+8
        if d.get('annotation'):y=s.block(d['annotation'],42,y+2,528,14,'BookItalic',b.RED)+8
        if d.get('records'):
            s.line(42,y+3,570,y+3)
            y=s.block('Authenticated source extracts',42,y+14,528,18,'BookBold',b.RED)+8
            for record in d['records']:
                y=s.block(record['text'],42,y,528,14,bottom=715)+12
        if d.get('stamp'):s.block(d['stamp'],42,max(y+5,701),528,12,'BookBold',b.RED,bottom=730)
        s.footer('Discovery '+str(d['number'])+' / Original exhibit and authenticated source extracts')
        if i+1<len(docs):s.next()
    s.save()
    reports=json.loads((b.ROOT/'source/investigation.json').read_text(encoding='utf-8'))
    photos={'F1':'silver_coupe','F4':'actual_installation','F5':'clock_comparison'}
    departments={'F1':'FORENSIC LABORATORY / TOXICOLOGY','F2':'MERIDIAN / DONOR PAPERS','F3':'MERIDIAN / STEWARD STATEMENT','F4':'MERIDIAN / CONSERVATION AUDIT','F5':'FORENSIC LABORATORY / TEXTILE COMPARISON'}
    paths=[]
    for report in reports:
        key=report['id'];s=b.Sheet(b.KIT/'PRINT_WITHOUT_READING/Reports'/(key+'.pdf'),report['title']);s.header(departments[key])
        y=s.block(report['title'],42,105,528,30,'BookBold',b.TEAL)+15
        y=s.block('CASE: MERIDIAN / 30 OCT 2026 / '+key,42,y,528,14,'BookBold')+17
        if key in photos:
            ph=180 if key=='F4' else 225
            s.image(b.ROOT/'assets/evidence'/(photos[key]+'.jpg'),42,y,528,ph)
            s.rect(42,y,528,ph,stroke=b.GOLD);y+=ph+14
        if key=='F2':
            for label,words in [('NAMING AGREEMENT','Veto power, museum renaming and management changes.'),('OBJECTS & PAYMENTS','Disputed title, altered records and unpaid design invoices.'),('PERSONAL PAPERS','Family trust amendments and threats to professional reputations.')]:
                y=s.block(label,42,y,528,16,'BookBold',b.TEAL)+6;y=s.block(words,42,y,528,16)+16
        if key=='F3':
            # A real floor diagram clarifies distinct positions without marking suspects.
            s.rect(42,y,528,135,fill=b.PALE,stroke=b.GOLD)
            s.rect(63,y+23,190,77,stroke=b.TEAL)
            s.block('STAR BOWL ALCOVE',74,y+38,167,14,'BookBold',b.TEAL)
            s.block('Curtain at entrance',74,y+68,167,12)
            s.block('EAST GALLERY / OPEN',278,y+32,270,14,'BookBold',b.TEAL)
            s.block('Balcony overlooks display',278,y+68,270,14)
            s.block('Donor Salon lies outside this gallery',63,y+110,487,12,'BookItalic')
            y+=152
            for time,words in [('6:40','Clean empty coupe delivered to Donor Salon.'),('6:44','Service dome sealed and continuously watched.'),('6:46','Seal checked; cordial poured for the first time.'),('6:49','Grant drinks from his private coupe.')]:
                y=s.block(time,42,y,105,18,'BookBold',b.TEAL);y=s.block(words,163,y-22.5,407,16)+18
        if key=='F4':
            for time,words in [('6:37','S-2 / mounting alert received.'),('6:38','S-2 / curtain locked / interior sealed.'),('7:00','First reopening permitted.')]:
                a=s.block(time,42,y,105,16,'BookBold',b.TEAL);z=s.block(words,163,y,407,16);y=max(a,z)+16
        y=s.block('Certified findings',42,y,528,18,'BookBold',b.TEAL)+8
        y=s.block(report['text'],42,y,528,14)+20
        if y<=715:s.line(42,y,570,y)
        s.footer(key+' / Read aloud and display at the host’s announced release');s.save();paths.append(s.path)
    b.merge(paths,b.KIT/'PRINT_WITHOUT_READING/Forensic_Reports.pdf')
    b.merge([b.KIT/'PRINT_WITHOUT_READING/Discovery_Props.pdf']+paths,b.KIT/'PRINT_WITHOUT_READING/04B_Clues_and_Forensics_PRINT_DO_NOT_READ.pdf')
