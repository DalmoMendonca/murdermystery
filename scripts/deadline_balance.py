"""One bounded balance revision and its immutable current-cast diagnostics."""
from pathlib import Path
import argparse,copy,json,shutil,yaml
import exhaustive_balance as gate

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest/2026-10-23-UNRESOLVED-STAKES-SPOILERS'

# These are individual scene edits, not a template applied to every character.
WHERE={
'01': "Sue and I stopped the announcement at the public desk. Then I went to Grant's private room to call the board without a roomful of donors listening. His place was set; he wasn't there. I asked Barb to give me a minute alone. I sent the refusal. Claire, I had just refused the money that pays our staff. I wanted to hear somebody on that call say I had done the right thing. Nobody did.",
'04': "The manager brought the extra-course ticket to accounts. I took Grant's copy to his place myself. He was out; I left it by the waiting glass. I'd already moved restricted money into payroll. I took the transfer slip back with me. He could pay for his cheese without seeing that. Brie, I know your supplier wanted paying. He could afford to make us wait. I couldn't.",
'05': "I fitted the red band before the preview. Kept the condition sheet. The false date made it look as though I'd inspected the closure a day earlier. I hadn't. Grant had the insurance copy and wanted to discuss what my signature was worth. I told him to keep my name out of his mouth. Then Frank's mount moved. That, at least, was something I could fix with my hands.",
'09': "The purchase attachment said original contents. My draft said inert. I asked Reed to hold the early press copies. Grant said people had paid to see his bottle, not my question mark. I let the preview go ahead. I knew what cyanide meant; I did not need another reference book. Dada, you asked why I was so quiet. I was waiting for somebody with more authority to stop it. I was the authority in that conversation.",
'11': "I took the private-room camera off the monitor and kept the outside crew out. Staff and caterers could still come through. I checked the room; Grant's place was set. I wrote fault, not privacy, in the log. When he wanted the room cleared, I cleared it. Artie used it too. Paige, you wanted a record of what happened in there. I had already made that impossible.",
'19': "I cut the original-contents sentence from the bottle's press entry. It wasn't a space problem. Grant had called my bowl research a publicity stunt; I wanted his harmless caption in print under his own name. Intake kept the full query. Claire, I thought if something went wrong with his precious acquisition, he might finally have to answer a question. I was thinking of a public disgrace. I didn't ask what else could go wrong.",
'23': "The cheese charge was held. The toast was paid. I took the flavoring to Grant's place and prepared his glass myself. Nobody was supervising my hands; everyone wanted dinner. I left the container with service. He'd told the kitchen my staff were replaceable. I sent them away from him and went in alone. Monet, don't call this a misunderstanding over a ticket. I understood him perfectly.",
'24': "Delivered the gifts. Crest glass in the carton; manager signed. Later I went back through service and emptied my packing bin before anyone could photograph it. The broken corner was in there. Grant had the first report calling the damage old. He said the insurer would love to meet me. Al, I didn't tell you. You were asking when the lift would work, and I was busy getting rid of the part I hoped nobody would find.",
'27': "I went looking for Grant with the petition. Paige was asking about the gift; I interrupted and demanded a signature. At intake I'd taken the bowl's ownership card and kept it inside my copy. Barb had warned me once already. I was not going to stand politely at the back while he thanked himself. I stayed after he'd told me to leave. He was going to hear the claimants' words if I had to read every last one.",
}
METHOD={
'01': "I approved that preview with the contents question unanswered. The bottle stayed out; keep it closed was my instruction. My refusal reached the board. It didn't remove Grant from the building or pay Friday's wages. Barb gave me the room when I asked. I could still make people do that. Claire, please don't introduce me as the man who saved the museum. Not tonight.",
'04': "The toast stayed booked. My instruction was serve the original order, bill the addition to Grant. That's the message I sent; the transfer slip I took away was about wages. Both things can be true. Artie, stop saying we all agreed. I moved the money. When they freeze that account, somebody still has to look the cleaners in the eye on Friday.",
'05': "Foil-backed paper. Red face, silver back. I fitted it across the stopper. Inspected the front. Missed the split behind. My false date is on the insurance copy. I want the workbench left alone; there are strips all over it and I don't remember which ones I threw away. Claire, don't start putting things in order for me. That's what people keep paying me to do after they've made a mess.",
'09': "My query quotes original contents. Intake answered unresolved; keep closed. That is what I knew before the preview. I didn't tell the paying guests. I let them hear inert. Reed, you may keep the proof. I won't be improving its wording. Dada, I had hoped you would see a different side of me tonight. I suppose you have.",
'11': "Power, not network. That's the lead I ordered removed. There's no recording to recover. Fault is what I put in the log. Nobody forged my signature. Paige, I won't invent a technical problem for you to solve. I made a decision. I also kept your crew out afterward. Brie, let your staff go home. They don't have to stay here and make my decision look respectable.",
'19': "Intake got the full warning. The press got my version without original contents. Both deliveries are on my marked proof. I knew perfectly well they were different. Claire, I want my work credited, but don't call this my first brave editorial decision. I wanted Grant caught out. I used a caption because a caption was something I could control.",
'23': "I put the flavoring in his individual glass. Not the pitcher. That's the order I filled. I left my container for testing; I'd used it all evening and knew what was in it. That doesn't give you a film of what I did in that room. Barb saw to that. I'm not thanking her. If you want the person who prepared his drink, I'm here. Leave the waiters out of it.",
'24': "Crest glass in the carton. The manager signed before setting the place; Grant drank from the engraving. My first damage report was wrong. I signed another one after the photographs turned up. Doesn't put the broken corner back in my bin, does it? Al, you can say I panicked. I did. I'm not going to pretend that makes it easier to tell which version of me you ought to believe.",
'27': "The card in my petition belongs to the bowl. I gave Grant his copy at his private place while Paige recorded. He said it wasn't a public podium. I knew that. I stayed anyway. Barb, you can call it trespass if it makes your evening easier. He never signed. Please don't make his death into the answer I was asking for.",
}

def prepare(final_pass=False,preserve_guilty=False):
    assert not RUN.exists(),'Frozen revisions are never overwritten.'
    RUN.mkdir();dest=RUN/'candidate-source';dest.mkdir()
    source=ROOT/'source/connected_release'
    old=yaml.safe_load((source/'all.yaml').read_text(encoding='utf-8'))
    bank=copy.deepcopy(old);rows={c['id']:c for c in bank['characters']}
    changes=[]
    for ident,text in WHERE.items():
        c=rows[ident]
        for branch in ('innocent','murderer'):
            # Shared events precede the branch-specific, independently testable Method claim.
            c['hearings']['where_'+branch]=text
        c['hearings']['evidence_innocent']=METHOD[ident]
    rows['09']['hearings']['where_murderer']="I asked Reed to hold the early press copies and went to the preview with the working file. Grant said people had paid to see his bottle, not my question mark. I let it go ahead. Dada, you asked why I was so quiet. I was waiting for somebody with more authority to stop it. I was the authority in that conversation. It is considerably easier to describe a failure of judgment after everyone else has made theirs."
    rows['19']['hearings']['where_murderer']="I shortened the bottle's press entry. Intake kept the working file and attachment. Grant had called my bowl research a publicity stunt; I wanted his harmless caption in print under his own name. Claire, I thought if something went wrong with his precious acquisition, he might finally have to answer a question. I was thinking of a public disgrace. I didn't ask what else could go wrong."
    # Preserve Robin's location contradiction against the independently released recording,
    # while eliminating the previous self-contradiction between her own two answers.
    rows['27']['hearings']['evidence_murderer']="I gave him the petition at the public podium during Paige's interview. That's where we had the argument. A microphone doesn't turn an open gallery into his private sitting room. The card in my copy belongs to the bowl. He never signed. Barb, you can call it disruption if it makes your evening easier. Please don't make his death into the answer I was asking for."
    if final_pass:
        rows['24']['hearings']['where_murderer']="Delivered the crest glass still wrapped. The signature was for the carton. Service had ordinary glasses too; I understood the gift wasn't going into use. Later I went back through service and emptied my packing bin. The broken corner was in there. Grant had my report calling it old damage. He said the insurer would love to meet me. Al, I didn't tell you. I was getting rid of the part I hoped nobody would find."
        for br in ('innocent','murderer'):
            rows['19']['hearings']['where_'+br]=rows['19']['hearings']['where_'+br].replace(' I was thinking of a public disgrace. I didn\'t ask what else could go wrong.',' He knew how to make a student disappear from a story. I wanted him to find out how that felt.')
            rows['11']['hearings']['where_'+br]=rows['11']['hearings']['where_'+br].replace('I wrote fault, not privacy, in the log.','I wrote fault in the log and told the technician to call it that too.')
        rows['05']['hearings']['evidence_innocent']="Foil-backed paper. Red face, silver back. I fitted it across the stopper. Inspected the front. Missed the split behind. My false date is on the insurance copy. No, Barb, you don't get to empty my workbench into a bag. Put the stock down. Photograph it where it is. Claire, you can tell me I'm making this worse. People have been telling me that all evening."
        rows['23']['hearings']['evidence_innocent']="I put the flavoring in his individual glass. Not the pitcher. I washed the little measure when I got back. Of course I did; we were still serving dinner. The ingredient container stayed with service. That's the one in the report. Barb, don't put my waiters on a list because I was alone in that room. If you want the person who prepared his drink, I'm here."
        rows['23']['hearings']['where_murderer']="The cheese charge was held. The toast was paid. I took the flavoring to Grant's place and got his service ready. Nobody was supervising me; everyone wanted dinner. I left the container with service. He'd told the kitchen my staff were replaceable. I sent them away from him and went in alone. Monet, don't call this a misunderstanding over a ticket. I understood him perfectly."
        rows['04']['hearings']['evidence_murderer']=rows['04']['hearings']['evidence_murderer'].replace('before the preview','after the preview')
        rows['06']['hearings']['evidence_innocent']="An empty jacket falling from a chair. That's the film I delivered. I kept asking to show it after Grant rejected it. I'd imagined the laugh going around the room, him sitting there having to accept it because he'd invited everyone. Please stop looking at me when you say collapse. I had thought about his face afterward. Not this face. The furious one I wanted to take home and remember."
        rows['15']['hearings']['evidence_innocent']="I put a sample image on that panel. Showed Monet what the camera connection would look like and sent an installation invoice. I hadn't installed it. I credited the invoice when she refused it. Can we put the phones down? Mine is still showing the room exactly as I wanted it to look. I can't seem to make myself close the demo."
        rows['20']['hearings']['evidence_innocent']="Gold transfer leaf over cold-cast resin. The surface sample is on my job card. I've been saying solid bronze since the publicity came out. I let people admire a thing I hadn't made and tried to be pleased they admired it. Cary, stop offering to move the piece. Leave it. Can somebody tell me when we're allowed to call home? I need to know somebody is still there with mine."
    # No innocent pretends an account has been settled merely because it was exposed.
    rows['24']['coming_clean']['innocent']="I didn't kill Grant. I delivered the crest glass; service unpacked it. I lied about the frame damage and emptied the bin with the broken piece in it. The photographs caught that lie. Al, the repair charge is mine. I don't know how I'm paying it. Tomorrow I have to tell the next person who hires me what happened here before they hear it from someone else."
    rows['19']['coming_clean']['innocent']="I didn't kill Grant. I sent the complete warning to intake and cut it from the press caption. I wanted his mistake to humiliate him. I didn't want him dead. Claire, I don't expect you to find that distinction impressive. I still want my research credited. I also want to be able to read my own marked proof without remembering how pleased I was with the edit."
    rows['23']['coming_clean']['innocent']="I didn't poison Grant. I prepared the ordered flavoring in his own glass and left my container with service. I was alone, angry, and tired of being spoken to as though I came with the tablecloth. I wanted him to apologize to my staff. Now they'll remember carrying plates past his empty place. Monet, the cheese can wait until tomorrow. Their ride home can't."
    # Keep each selected world's confession consistent with the shared Opportunity scene.
    for ident,c in rows.items():
        if ident not in WHERE:continue
        if ident=='01':
            c['coming_clean']['murderer']=c['coming_clean']['murderer'].replace('The public argument gave everyone something else to watch.','The board call was real. Barb gave me privacy, and I used it.')
        if ident=='24':
            c['coming_clean']['murderer'] += " Emptying my packing bin was about the frame. I hid that damage too. It wasn't the worst thing I had hidden tonight."
    if preserve_guilty:
        # The previous experiments accidentally traded the selected culprit's
        # actual access for a less relevant side scandal. Restore the proven
        # published accounts, not another paraphrase of those events.
        for original in old['characters']:
            c=rows[original['id']]
            for field,value in original['hearings'].items():
                if field.endswith('_murderer'):c['hearings'][field]=value
            c['coming_clean']['murderer']=original['coming_clean']['murderer']
        # Published setup is6:32, after the6:20-6:28 preview, not before it.
        rows['04']['hearings']['evidence_murderer']=rows['04']['hearings']['evidence_murderer'].replace('before the preview','after the preview')
    evidence=yaml.safe_load((source/'playable-evidence.yaml').read_text(encoding='utf-8'))
    # Defer seven non-murder settlements to the post-vote endings. Do not remove
    # any physical comparison or recorded fact that contradicts a murderer branch.
    deferred=[]
    remove={'Advisory account','Family valuation','Dealer refund demand','Technology account','Bead recommendation','Sponsored podcast','Property story','Corrected archive','Editorial client','Textile commission','Production account'}
    for release in evidence['releases']:
        for exhibit in release['exhibits']:
            kept=[]
            for row in exhibit.get('rows',[]):
                if row[0] in remove:deferred.append({'exhibit':exhibit['id'],'row':row})
                else:kept.append(row)
            if 'rows' in exhibit:exhibit['rows']=kept
    bank['status']='deadline_balance_candidate_not_promoted'
    profile=yaml.safe_load((ROOT/'source/testing/active-cast.yaml').read_text(encoding='utf-8'))
    active=set(profile['active_character_ids'])
    event=copy.deepcopy(bank);event['characters']=[c for c in event['characters'] if c['id'] in active]
    # Reuse only the audited attendance substitutions, never their story edits.
    from final_rsvp_round import ABSENT_ROLES,DIRECT
    import re
    public=yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))
    known={str(c['id']).zfill(2):c for c in public['characters']}
    for c in event['characters']:
        for section in ('hearings','coming_clean'):
            for field,text in c[section].items():
                for a,b in DIRECT.get((c['id'],section,field),{}).items():text=text.replace(a,b)
                for ident,role in ABSENT_ROLES.items():text=re.sub(r'\b'+re.escape(known[ident]['name'].split()[0])+r'\b',role,text)
                text=re.sub(r'(^|[.!?]\s+)([a-z])',lambda m:m[1]+m[2].upper(),text)
                c[section][field]=text
    names={known[i]['name'] for i in active}
    for phase in event['question_rounds']:
        for g in phase['groups']:g['targets']=[n for n in g['targets'] if n in names]
        phase['groups']=[g for g in phase['groups'] if g['targets']]
        assert len([n for g in phase['groups'] for n in g['targets']])==22
    event.update(active_character_ids=sorted(active),authored_route_count=22)
    for label,data in [('all',bank),('confirmed',event),('playable-evidence',evidence)]:
        (dest/(label+'.yaml')).write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False),encoding='utf-8')
    shutil.copy2(source/'voice-story-bible.yaml',dest/'voice-story-bible.yaml')
    gate.write(dest/'manifest.json',{'revision':'unresolved-stakes-2026-10-23','baseline_commit':'4af7056','limitations':'Bounded current-cast diagnostics pending; no claim of exhaustive balance.','sha256':{p.name:gate.sha(p) for p in dest.iterdir()}})
    for c in bank['characters']:
        original=next(x for x in old['characters'] if x['id']==c['id'])
        for section in ('hearings','coming_clean'):
            for field,value in c[section].items():
                if value!=original[section][field]:changes.append({'id':c['id'],'section':section,'field':field,'before':original[section][field],'after':value})
    gate.write(RUN/'change-ledger.json',{'character_edits':changes,'deferred_post_vote_rows':deferred,'unchanged':'All16 hunt clues; physical service timeline; laboratory comparisons; original photos; recorded interview; camera order; artist/model distinction; closure material; true/false Method propositions except Robin presentation.'})
    frozen=RUN/'frozen-source';shutil.copytree(dest,frozen)
    public['active_character_ids']=sorted(active)
    (frozen/'character_copy.yaml').write_text(yaml.safe_dump(public,allow_unicode=True,sort_keys=False),encoding='utf-8')
    # Fixed matched worlds from the previous two-case check, not selected by results.
    previous=ROOT/'docs/playtest/2026-10-23-FINAL-RSVP22-SPOILERS/private-manifest.json'
    info=json.loads(previous.read_text(encoding='utf-8'))
    people={i:c for i,c in known.items() if i in active};byname={c['name']:c for c in event['characters']}
    visible={'number','title','department','stamp','paragraphs','rows','images'}
    def shown(x):
        out={k:v for k,v in x.items() if k in visible}
        if x.get('id')=='original_interview':out['paragraphs']=event['pre_method_press_interview_opening']
        return json.dumps(out,ensure_ascii=False,indent=2)
    def release(key):return '\n\n'.join(shown(x) for r in evidence['releases'] if r['key']==key for x in r['exhibits'])
    def speeches(key,killer):
        text=[];field={'motive':'motive','opportunity':'where','method':'evidence'}[key]
        for g in next(r for r in event['question_rounds'] if r['key']==key)['groups']:
            text.append('Question for '+', '.join(g['targets'])+': '+g['question'])
            for n in g['targets']:
                c=byname[n];text.append(n+'\n'+c['hearings'][field+('_murderer' if c['id']==killer else '_innocent')])
        return '\n\n'.join(text)
    for t in info['trials']:
        folder=RUN/'blind'/t['trial'];folder.mkdir(parents=True)
        stages={1:'Exactly one of these 22 characters committed the murder alone. Other mentioned staff are not selectable suspects.\n\n'+'\n\n'.join(p['name']+' / '+p['role']+'\n'+p['introduction'] for p in people.values()),2:'\n\n'.join(shown(x) for x in evidence['hunt']),3:release('before_motive'),4:speeches('motive',t['murderer_id']),5:release('before_opportunity'),6:speeches('opportunity',t['murderer_id']),7:release('before_method'),8:speeches('method',t['murderer_id'])}
        for n,text in stages.items():(folder/f'checkpoint_{n:02}.txt').write_text(text+'\n',encoding='utf-8')
        t['inputs']={p.name:gate.sha(p) for p in folder.iterdir()}
    info.update(run='Unresolved stakes deadline balance check',revision=RUN.name,source_sha256={p.name:gate.sha(p) for p in frozen.iterdir()},protocol='Two fixed new-role scenarios, fresh blind readers, eight immutable gated stages. No hidden selections or desired scores disclosed. Paired scenarios with different readers are descriptive comparisons, not causal proof.')
    gate.write(RUN/'private-manifest.json',info)
    instructions=(previous.parent/'READER_INSTRUCTIONS.md').read_text(encoding='utf-8').replace(previous.parent.name,RUN.name).replace('scripts/final_rsvp_round.py','scripts/deadline_balance.py')
    (RUN/'READER_INSTRUCTIONS.md').write_text(instructions,encoding='utf-8')
    print('Candidate frozen; two unstarted original reader slots. Published source unchanged.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','read','validate','finale','complete']);p.add_argument('--trial');p.add_argument('--stage',type=int);a=p.parse_args()
    if a.action=='prepare':prepare()
    else:gate.RUN=RUN;gate.gate(a.trial,a.action,a.stage)
