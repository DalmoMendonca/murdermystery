"""Assemble the unfrozen authoring draft and resolve independent editorial notes."""
from pathlib import Path
import yaml,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest/2026-10-26-DRAMATURGICAL-01-SPOILERS'
assert not (ROOT/'docs/playtest/2026-10-26-DRAMATURGICAL-01-BLIND-SPOILERS').exists()
revs={}
for name in ['pilot','collection','control','work','public']:
    data=yaml.safe_load((RUN/f'{name}-revisions.yaml').read_text(encoding='utf-8'))
    assert not set(data)&set(revs);revs.update(data)
fixes=[]
def edit(ident,field,before,after):
    assert before in revs[ident][field],(ident,field,before)
    revs[ident][field]=revs[ident][field].replace(before,after)
    fixes.append({'id':ident,'field':field,'before':before,'after':after})
def settext(ident,field,text):
    before=revs[ident][field];revs[ident][field]=text
    fixes.append({'id':ident,'field':field,'before':before,'after':text})
edit('01','motive_innocent',"I was to introduce my replacement.","Tonight I was to introduce my replacement.")
edit('01','motive_murderer',"I was to introduce my replacement as our savior.","Tonight I was to introduce my replacement. Grant expected me to call him our savior.")
settext('01','where_innocent',"I wanted someone on the board call to say I'd done the right thing, Claire. Nobody did. Sue and I stopped the announcement at the public desk. I went to Grant's private room to call away from the donors. His place was set, he wasn't there. I asked Barb for a minute alone and sent the refusal. I'd refused the money that pays our staff. I still have to face them.")
settext('01','evidence_murderer',"I took the bottle's contents out to make the display safe. Intake removed the bottle too; only its label remained when guests entered. Then I went to Grant's place with my refusal and left it beside his glass. He wasn't there. The board has the refusal. I didn't give Grant a drink. Can we distinguish those two things?")
edit('01','final_murderer',"The refusal was real,", "The refusal in the announcement folder was real,")
edit('01','final_murderer',"I lied about intake removing it.","I lied about intake removing it to erase that opportunity from your account.")
edit('02','motive_murderer',"And my department was to thank him tonight.","You kept asking me to revisit it. And my department was to thank him tonight.")
edit('02','where_murderer',"I brought his copy to his place, found him absent, and moved his glass off the paper so its damp base wouldn't mark it.","I brought his copy to his place, found him absent, and put it beside the glass. I moved the glass to keep its damp base off the paper.")
edit('04','motive_innocent',"Grant's check could cover wages, provided he inspected every transfer first.","Grant's check could cover wages. His terms let him inspect every transfer.")
edit('04','motive_murderer',"By Friday.","I had no time left.")
edit('04','final_innocent',"if they freeze the account", "when they freeze the account")
for k in ['motive_innocent','motive_murderer']:
    edit('06',k,"You understand why I wanted my name on this one. ","")
edit('07','where_innocent'," I hadn't agreed to that either.","")
edit('07','motive_murderer',"I still get introduced as the boy who painted Grant's early picture.","Grant kept exhibiting the early picture. I still get introduced as the boy who painted it.")
for k in ['motive_innocent','motive_murderer']:
    edit('07',k,"Dada, how did you keep making new work?", "Dada, you kept making new work.")
edit('09','where_innocent',"Dada, that's why I was quiet.", "Dada, you asked why I was quiet.")
edit('09','where_innocent',"There wasn't another authority in that conversation.","I was the authority in that conversation.")
edit('12','motive_murderer',"Grant's lawyer used it against everything else, including Justin's property folder.","Grant's lawyer used it against the rest. Justin's property folder made his rescue story less flattering.")
edit('12','where_murderer',"put the pocket search in your report.","put the pocket search without permission in your report.")
edit('13','motive_murderer',"who already had his plaque ready.","whose plaque was ready before the donation.")
edit('13','evidence_murderer'," Does that make the other bench disappear?", "")
edit('15','evidence_murderer',"Removing the public monitor", "Disconnecting the public monitor")
edit('15','evidence_murderer'," Which part are you asking about?", "")
edit('18','motive_innocent',"I stopped touching the weave when you told me.","you told me when to stop touching the weave.")
edit('18','where_murderer',"a transfer of its pattern.","a signed transfer of its pattern.")
edit('19','where_murderer',"Grant wanted every correction approved.","Grant wanted to approve every correction.")
edit('20','where_murderer',"I refused a replacement, crossed out solid bronze, and wouldn't pay a crew for a second sculpture.","I refused a replacement and crossed out solid bronze. I wasn't paying another crew to make him a second sculpture for free.")
edit('25','where_murderer',"I replaced the handout", "I know the gala route wasn't mine to change. I replaced the handout")
edit('27','final_murderer',"their bowl and a hearing.","their bowl returned intact and a hearing.")
edit('28','final_innocent'," I know what it looks like, waiting until now to say that.","")
edit('02','where_murderer',"still fussing over a damp sheet.","still fussing over a sheet of paper.")
edit('01','motive_innocent',"; Tonight I was","; tonight I was")
edit('01','motive_murderer',"and Tonight I was","and tonight I was")
# Different immediate destinations for the five endings flagged by the table-read.
settext('11','final_murderer',"There's no footage to recover. I ordered the power removed and signed for it. I lied tonight about a network disconnection. I'd taken poison at the preview; checking the room showed me Grant's waiting glass. I used it at his private place, then relied on the privacy exception to hide the visit. I killed him. I sent you to local storage to make the missing footage sound recoverable. My own department trusted me. They'll have to answer for that. There isn't anything for them to recover.")
settext('20','final_murderer',"I need that call home. The sample card's right: my accent leaf isn't the foil-backed paper in his glass. I opened the bottle at the preview, stole poison and put it in Grant's glass later. I killed him. I called the scrap sculpture debris so you wouldn't consider it with the damaged closure. It isn't a unique match; it isn't my finish either. He could expose the bronze publicity fraud. I told myself the person waiting at home needed me to do it. They never asked. I still have to call.")
settext('24','final_murderer',"Grant had the frame photographs. He could expose my false report or force another unsafe signature. I was afraid of losing the job. So I stole poison at the preview, put it in his waiting glass later, and killed him. The crest glass was unpacked and used; the service photograph and manager's carton receipt show that. I called it a spare to separate his drink from the glass being tested. Nobody's going to ask me to move anything now. Losing the job is the smallest part of it.")
settext('25','final_murderer',"I borrowed the group for my account afterwards. They were never beside that glass. The approved route excludes the private room; the assistant docent recorded the turnback to the public cases. I went to Grant's unattended place alone and put poison from the preview bottle in his glass. I killed him. Funding the school places wouldn't erase the promise he could expose. I'd promised children a place here. Now the people who bring them have to explain why my name's gone from their tour. The group wasn't with me.")
settext('27','final_murderer',"An intact return and a hearing. The claimants asked for that. I delivered the petition at his private place, as the recording says. I'd taken poison at the preview; seeing the waiting glass during the interview showed me where to put it afterwards. I killed Grant and moved our interview to the public gallery in my account. That demand authorized none of it. Now the claimants have to defend themselves against something I had no right to do in their name. The bowl and the hearing are still what they asked for.")
# Keep interpretation and required facts; reduce a few substitute performance hooks.
edit('18','evidence_murderer',"Chip, I can't have you carrying this part for me too.","Chip, I can't accept help with this part.")
edit('23','evidence_murderer',"The staff can go.","Leave the staff out of this.")
edit('13','where_innocent',"Production thought", "The production crew thought")
edit('13','where_murderer',"Production, I'd designed", "I'd designed")
edit('13','final_innocent',"Leave the empty space, Production.","Leave the empty space.")
edit('20','evidence_innocent',"Can I call home?", "I need to call home.")
edit('20','evidence_murderer',"When can I call home?", "I need to call home.")
edit('12','evidence_innocent',"Sue, keep this about my recording.","Sue, I'll answer about my recording.")
edit('12','evidence_innocent',"Ask what you need about the cut.","I can answer for the cut.")
# Repetition of the same emotional requests in finales is intentional only when character-specific.
edit('29','final_innocent'," People ought to be remembered even when I can't get a brilliant headline out of them."," The old occupants still belong in the tour, brilliant headline or not.")
before=yaml.safe_load((RUN/'baseline-source/confirmed.yaml').read_text(encoding='utf-8'))
ledger=[]
for edition in ['all','confirmed']:
    bank=yaml.safe_load((RUN/'baseline-source'/f'{edition}.yaml').read_text(encoding='utf-8'))
    for row in bank['characters']:
        if row['id'] not in revs:continue
        for key,after in revs[row['id']].items():
            loc=row['coming_clean'] if key.startswith('final_') else row['hearings']
            field=key.replace('final_','') if key.startswith('final_') else key
            old=loc[field];loc[field]=after
            if edition=='confirmed':ledger.append({'id':row['id'],'name':row['name'],'field':key,'before':old,'after':after,'fact_review':'Independent full audit plus targeted corrections; semantic obligations retained separately.'})
    bank['status']='dramaturgical_candidate_unvalidated'
    (RUN/'candidate-source'/f'{edition}.yaml').write_text(yaml.safe_dump(bank,sort_keys=False,allow_unicode=True,width=100),encoding='utf-8')
oldwords=sum(len(s.split()) for c in before['characters'] for s in c['hearings'].values())
newwords=sum(len(v.split()) for d in revs.values() for k,v in d.items() if not k.startswith('final_'))
assert newwords<=oldwords,(newwords,oldwords)
(RUN/'change-ledger.json').write_text(json.dumps({'baseline_pre_vote_words':oldwords,'candidate_pre_vote_words':newwords,'changes':ledger},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(RUN/'review-corrections.json').write_text(json.dumps(fixes,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(RUN/'final-authoring.yaml').write_text(yaml.safe_dump(revs,sort_keys=False,allow_unicode=True,width=100),encoding='utf-8')
manifest=json.loads((RUN/'candidate-source/manifest.json').read_text())
manifest['sha256']={n:hashlib.sha256((RUN/'candidate-source'/n).read_bytes()).hexdigest() for n in ['all.yaml','confirmed.yaml','playable-evidence.yaml','voice-story-bible.yaml']}
(RUN/'candidate-source/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'review_corrections':len(fixes),'passages':len(ledger),'pre_vote_words':newwords,'baseline':oldwords}))
