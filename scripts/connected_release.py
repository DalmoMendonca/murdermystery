"""Build the explicitly pinned connected-story release, independent of ongoing lab edits."""
from pathlib import Path
import copy, hashlib, json, shutil, yaml
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
import html

def prepare_deploy(b):
    """Publish the pinned kit without serving obsolete private files from prior editions."""
    target=b.WORK/'connected-deploy/site'
    if target.exists():
        assert target.resolve().is_relative_to((b.WORK/'connected-deploy').resolve())
        shutil.rmtree(target)
    shutil.copytree(b.SITE,target,ignore=shutil.ignore_patterns('current'))
    shutil.copytree(b.KIT,target/'downloads/current'/b.KIT.name)
    return target

def pin(root):
    """Explicit promotion only; ordinary builds never import experimental lab changes."""
    from compile_connected_story import compile_bank, LAB
    from validate_playable_evidence import validate
    dest=root/'source/connected_release';dest.mkdir(exist_ok=False)
    for label,active in [('all','all'),('confirmed','confirmed')]:
        bank=compile_bank(active)
        bank['status']='user_authorized_playable_fallback_2026_10_10'
        (dest/(label+'.yaml')).write_text(yaml.safe_dump(bank,sort_keys=False,allow_unicode=True),encoding='utf-8')
    for name in ['playable-evidence.yaml','voice-story-bible.yaml']:
        shutil.copy2(LAB/name,dest/name)
    validate(dest/'playable-evidence.yaml')
    manifest={'revision':'dramatic-fallback-2026-10-10','tested_commit':'e29371c',
              'limitations':'Six valid text checks of Anne/all30 and Al/RSVP22, not every selected world. Physical attribution remains circumstantial; narrative repetition persists.',
              'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.iterdir() if p.is_file()}}
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

def document(b,path,title,sections):
    body=ParagraphStyle('body',fontName='Book',fontSize=14,leading=18,spaceAfter=9)
    heading=ParagraphStyle('heading',parent=body,fontName='BookBold',fontSize=24,leading=29,textColor=b.RED,spaceAfter=17)
    sub=ParagraphStyle('sub',parent=body,fontName='BookBold',fontSize=15,leading=19,textColor=b.RED)
    def p(text,style=body):return Paragraph(html.escape(str(text)).replace('\n','<br/>'),style)
    story=[]
    for index,section in enumerate(sections):
        if index:story.append(PageBreak())
        story.extend([p(section.get('department','MERIDIAN MUSEUM / 2026'),sub),p(section['title'],heading)])
        if section.get('stamp'):story.append(p(section['stamp'],sub))
        for text in section.get('paragraphs',[]):story.append(p(text))
        if section.get('rows'):
            table=Table([[p(cell) for cell in row] for row in section['rows']],colWidths=[169,343],hAlign='LEFT')
            table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(0,-1),b.PALE),('LINEBELOW',(0,0),(-1,-1),.4,b.GOLD),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            story.append(table)
        if section.get('images'):
            story.extend([PageBreak(),p(section.get('department','MERIDIAN MUSEUM / 2026'),sub),p(section['title']+' / retained views',heading)])
        for image in section.get('images',[]):
            story.extend([Spacer(1,12),p('Retained view / '+image['id'].replace('_',' '),sub),p(image['observation'])])
    path.parent.mkdir(parents=True,exist_ok=True)
    def page(cv,doc):
        cv.setTitle(title);cv.setAuthor('The Meridian Museum');cv.setStrokeColor(b.GOLD)
        cv.line(42,40,570,40);cv.setFont('Book',11);cv.setFillColor(b.INK)
        cv.drawString(42,24,'The Last Acquisition / '+title);cv.drawRightString(570,24,str(doc.page))
    SimpleDocTemplate(str(path),pagesize=(612,792),leftMargin=50,rightMargin=50,topMargin=42,bottomMargin=58,allowSplitting=0).build(story,onFirstPage=page,onLaterPages=page)

def build_release(b):
    from character_copy import load_characters
    from public_lock import verify_public_lock,restore_missing_public
    from printable_v2 import packets,tents
    from hunt_copy import load_hunt
    dest=b.ROOT/'source/connected_release'
    manifest=json.loads((dest/'manifest.json').read_text(encoding='utf-8'))
    for name,expected in manifest['sha256'].items():assert hashlib.sha256((dest/name).read_bytes()).hexdigest()==expected,name
    restore_missing_public(b.ROOT);verify_public_lock(b.ROOT)
    old_kit=b.KIT
    b.KIT=b.WORK/'connected-release-kit'/old_kit.name
    if b.KIT.exists():
        assert b.KIT.resolve().is_relative_to((b.WORK/'connected-release-kit').resolve())
        shutil.rmtree(b.KIT)
    b.KIT.mkdir(parents=True)
    locked=json.loads((b.ROOT/'source/public_assets_lock.json').read_text(encoding='utf-8'))['files']
    for relative in locked:
        path=b.ROOT/relative
        if path.is_relative_to(old_kit):
            target=b.KIT/path.relative_to(old_kit);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target)
    b.fonts();b.CONNECTED_RELEASE=True;chars=load_characters();by_id={c['id']:c for c in chars}
    voices={r['id']:r for r in yaml.safe_load((dest/'voice-story-bible.yaml').read_text(encoding='utf-8'))['characters']}
    def cast(bank):
        result=[]
        for row in bank['characters']:
            c=copy.deepcopy(by_id[row['id']]);v=voices[row['id']]
            c['hearing']=row['hearings'];c['private'].update(history=v['private_stake'],secret='Keep your account private until each round. Your printed answers establish what happened. You can react in your own style, but do not invent a new event, witness, or alibi.',objectives=['Mingle using the relationships on your introduction page.','Keep your private branch readings for their announced rounds.'],final_innocent=row['coming_clean']['innocent'],final_murderer=row['coming_clean']['murderer'])
            result.append(c)
        return result
    all_bank=yaml.safe_load((dest/'all.yaml').read_text(encoding='utf-8'))
    event_bank=yaml.safe_load((dest/'confirmed.yaml').read_text(encoding='utf-8'))
    packets(cast(all_bank),b,all_bank['question_rounds'])
    all_pdf=b.KIT/'PRINT_WITHOUT_READING/03_Secret_Player_Packets_PRINT_DO_NOT_READ.pdf'
    backup=b.WORK/'connected-all-packets.pdf';shutil.copy2(all_pdf,backup)
    packets(cast(event_bank),b,event_bank['question_rounds'])
    all_pdf.rename(b.KIT/'PRINT_WITHOUT_READING/03A_Confirmed_22_Guest_Packets_PRINT_DO_NOT_READ.pdf')
    shutil.copy2(backup,all_pdf)
    tents(chars,b)
    # Animal slips and envelopes are host-safe props; no old evidence is retained.
    b.props(chars)
    evidence=yaml.safe_load((dest/'playable-evidence.yaml').read_text(encoding='utf-8'))
    document(b,b.KIT/'OPEN_FREELY/04_Scavenger_Discoveries.pdf','Hunt discoveries',evidence['hunt'])
    for bank,label in [(all_bank,'ALL_30'),(event_bank,'CONFIRMED_22')]:
        sections=[]
        for release in evidence['releases']:
            for item in release['exhibits']:
                item=copy.deepcopy(item)
                if item['id']=='original_interview':
                    if not bank['pre_method_press_interview_opening']:continue
                    item['paragraphs']=bank['pre_method_press_interview_opening']
                item['department']=release['title'].upper()+' / '+item.get('department','')
                sections.append(item)
        document(b,b.KIT/f'OPEN_FREELY/05_Staged_Evidence_{label}.pdf','Staged evidence / '+label,sections)
    locations=load_hunt(b.ROOT)['locations']
    host=[{'title':'Set the gala','paragraphs':['Use the confirmed 22-guest packet file unless attendance changes. Print single-sided at 100%. Each guest has twelve pages, including a cover and detachable ballot. Put the covered packet at the assigned seat. Keep private pages facing their player.','Print the 16 discoveries and place each numbered discovery in the corresponding numbered envelope. Scatter them at the locations on the next page. Put pencils at the seats. Print the confirmed evidence book, host guide, name cards and animal slips.','Before choosing the murderer, each attending guest draws a different animal, memorizes it privately and returns the slip. Collect all drawn slips, mix them, and draw one without associating it with a name. Announce that animal. Its guest reads IF MURDERER throughout; everyone else reads IF INNOCENT. Never share an animal or read branch headings aloud.']},
          {'title':'Hide the envelopes','rows':[[str(r['envelope']),r['location']] for r in locations]},
          {'title':'Introductions and hunt','paragraphs':['Invite every guest to read their introduction box on page 2. Allow mingling before the murder announcement.','Announce that Grant Larceny has died at the gala after his private toast. Invite players to turn to their Hunt for Clues page. Set aside about 15 minutes for finding envelopes; the guest finding the most wins a prize. Guests bring envelopes to their seats.','Have the finders open and read all 16 discoveries aloud. Display each discovery at the Evidence Table. Retrieve and read any missed envelope so the case never depends on finding every hiding place.']},
          {'title':'Three investigation acts','paragraphs':['Before Act I: read the first release, The gift is still unsigned. Then announce ACT I: MOTIVE. Players use pages 5–6.','Before Act II: read the second release, What was found. Then announce ACT II: OPPORTUNITY. Players use pages 7–8.','Before Act III: read the third release, The originals. Include every retained-view caption and the untrimmed press interview. Then announce ACT III: METHOD. Players use pages 9–10.','In each act, invite a guest to choose an attending character by name and ask that character’s question from the question page. The named guest reads their selected box and chooses the next unheard guest. Track names yourself; every attending guest answers once. If the chain stalls, nominate an unheard guest. Let discussion happen between rounds, while keeping later pages private.']},
          {'title':'Accusations and Coming Clean','paragraphs':['After Act III, allow discussion and ask everyone to detach page 11, accuse one attending guest, and hand in the ballot. Count all ballots before revealing anything.','Tally accusations. Call the three most-voted suspects in descending order; break ties alphabetically by full character name. Each reads their selected Coming Clean box on page 12.','If none of those three confesses, ask the guest whose secret animal matches the announced animal to stand and read their murderer confession. Every called innocent also gets to finish their box. Award the accusation, acting, costume and scavenger prizes.','Suggested pacing: 20 minutes arrival and introductions, 15 minutes hunt, 15–20 minutes per act, 10 minutes accusations, 15 minutes finale. Adjust for conversation and food service; finish all essential evidence before voting.']}]
    document(b,b.KIT/'OPEN_FREELY/01_Facilitator_Run_of_Show.pdf','Host guide',host)
    document(b,b.KIT/'00_READ_ME_FIRST.pdf','Start here',[{'title':'The Last Acquisition','paragraphs':['Murder Mystery Dinner Party 2026 / Meridian Museum / October 30, 2026','This is the newly tested connected-story edition. Start with OPEN_FREELY/01_Facilitator_Run_of_Show.pdf. For the current party, use PRINT_WITHOUT_READING/03A_Confirmed_22_Guest_Packets_PRINT_DO_NOT_READ.pdf.','The all-30 file supports the full cast. The confirmed file removes absent targets and substitutes contextual references. Use its matching evidence book. Every packet includes questions, three innocent/murderer readings, a ballot and Coming Clean.','OPEN_FREELY holds the clues and staged evidence the host reads during play. Keep later evidence covered until its release. Private player readings and organizer materials are spoilers. Already-sent invitations and character sheets are preserved exactly.','Print single-sided at 100%. The name cards fold into tents. The evidence uses readable source documents and retained-view descriptions; a full photographic prop upgrade remains future work.']}])
    organizer=[]
    for row in all_bank['characters']:
        organizer.append({'title':row['name'],'paragraphs':['IF INNOCENT: '+row['coming_clean']['innocent'],'IF MURDERER: '+row['coming_clean']['murderer']]})
    document(b,b.KIT/'SPOILERS_DO_NOT_OPEN/99_SPOILER_BIBLE_DO_NOT_OPEN.pdf','Organizer endings',organizer)
    (b.KIT/'README.txt').write_text('Connected dramatic edition 2026-10-10. Start with 00_READ_ME_FIRST.pdf. Already-sent public assets unchanged. Print at 100%, single-sided. Do not mix with earlier editions.\n',encoding='utf-8')
    (b.WORK/'connected-layout-ledger.json').write_text(json.dumps(b.AUDIT,indent=2,ensure_ascii=False),encoding='utf-8')
    b.package();verify_public_lock(b.ROOT);prepare_deploy(b)
    print('Pinned connected release built: '+str(b.KIT))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--pin',action='store_true');args=parser.parse_args()
    if args.pin:pin(Path(__file__).resolve().parents[1])
