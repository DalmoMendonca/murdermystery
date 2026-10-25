"""Freeze an editable, current-cast story revision and one blind world per guest.

Never promotes a candidate or changes sent guest materials. The assessment gate
is shared with previous runs; the new inputs and scores remain separate.
"""
from pathlib import Path
import argparse, copy, json, shutil, yaml
import exhaustive_balance as gate
import deadline_balance as prior

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest/2026-10-24-PRINT-FINAL-SPOILERS'

METHOD={
'01': "I said keep it closed. That was my entire precaution. You can put that beside my approval of the preview. The board has my refusal; it doesn't give Friday's wages back to us. Barb let me have the room when I asked. Apparently I could still make that happen. Claire, take the seating list. I cannot welcome another person into this evening.",
'04': "Serve the original order, bill the addition to Grant. Those were my instructions. Yes, I took my transfer slip away from his place. It concerned wages, not the cheese. He wasn't entitled to that slip just because he could pay our bills. Artie, don't say we agreed. We didn't. When they freeze that account on Monday, you can explain the rescue to the cleaners.",
'05': "Foil-backed paper. Red face, silver back. I fitted it across the stopper. Inspected the front. Missed the split behind. No, Barb, leave the supply sleeve where it is. Photograph it before you touch anything. My insurance date is wrong. I changed it. You can ask about that without emptying my workbench onto the floor.",
'06': "An empty jacket falling off a chair. That's the film he rejected. Yes, I kept trying after he said no. I wanted him sitting there while the room laughed. All week I imagined his face afterward. The furious face. Vincent, don't tell me I couldn't have known how that sounds now. I can hear myself.",
'09': "My query says original contents. I wrote it; I knew what the words meant. The answer was unresolved, keep closed. I let the paying guests hear inert. There is no better version of that sentence. Dada, would you mind not looking at me for a moment? I prepared for every conversation we might have tonight except this one.",
'11': "Power. Not network. That's the adapter I had removed. There is no recording, and calling it a fault won't produce one. I also told the technician what to put in the log. Paige, I won't ask you to put your recorder away. I have made quite enough decisions about what gets recorded. Brie, your staff can leave when their shift ends.",
'12': "That was tonight. His private room. You can hear the manager leaving me with him. I removed that voice from the critic's copy; the editor has it. I'm not giving you a name to pass around the table. Grant already thought a name was something he could bargain for. Sue, if there is another question, ask it. Ask me.",
'14': "The water never got opened. He wanted his toast after all. My letter speaks for the claimants; I borrowed the look of a ministry letter because otherwise nobody lets me finish a sentence. Sue, you can be right about the stationery without deciding what those people are owed. I recommended that bead supplier. The commission is mine to explain, not theirs.",
'15': "It was a sample image. I hadn't connected the panel to anything. I sent an installation invoice anyway. Monet refused it, quite reasonably. That doesn't settle what I promised the people working on the launch. Can we put the phones down? Mine is still showing the room the way it was supposed to look.",
'18': "The slides are enlarged stitches. The bottle beside my panel was the physical loan. I keep hearing myself saying another length would finish it. Another color. Chip, please don't offer to hold it steady for me. I've spent another client's money, and I don't know what I will tell them when they ask what I made with it. That is a conversation I still have to have.",
'19': "Original contents. That's the sentence I cut from the press copy. Intake had it; I made sure of that. I wanted Grant caught out, in public, under his own lovely harmless caption. Claire, don't call this a misunderstanding. I was pleased with the edit. I still want my work credited. I don't know what you expect me to do with both of those things.",
'20': "Gold leaf over cold-cast resin. The surface sample is on the job card. I've been saying solid bronze since the publicity came out. I let people admire something I hadn't made. Cary, stop offering to move it. Leave it where it is. Can somebody tell me when we can call home? I need to hear somebody in that house.",
'23': "I put the flavoring in his glass. Not the pitcher. I washed the little measure when I got back; we were still serving dinner. The ingredient container stayed with service. Barb, don't put my waiters on a list because I was alone in that room. If you want the person who prepared his drink, I'm here. And I'm still expecting payment for the food.",
'24': "The crest glass was in my carton. Service unpacked it. You don't sign for a carton and then ask the driver to watch you pour. Grant used the engraving. I destroyed the broken corner after I called the damage old. Al, don't say I just panicked. I chose which piece to throw away. That's why the photographs matter so much to my employer.",
'27': "I gave Grant the petition at his private place while Paige recorded. He told me it wasn't a public podium. Yes, I knew that. The card I took belongs to the bowl. Barb, I stayed after you told me to leave. I wanted him to have to answer someone who couldn't offer him anything. His death isn't the answer. Stop waiting for me to be pleased.",
'28': "The band crossed the stopper. I called it a price collar; Chip corrected me. I ask about prices. People let that sound harmless because I smile. My family hasn't called. I keep checking. No, I haven't told them the full story of the damaged comparison. I would rather they heard it in my voice than found it in Grant's handout. I am not sure they want to hear my voice.",
'29': "The correction changes the old owner's name. It says nothing about treating the poison. The settlement is in the property folder; I left it out of the headline. Paige, you're welcome to the whole folder. I'm still angry about what happened to those tenants. I also know exactly which missing page made it sound like a better story.",
}

def prepare():
    dest=RUN/'candidate-source'; assert not dest.exists(), 'Never overwrite frozen revision.'
    dest.mkdir(parents=True)
    source=ROOT/'source/connected_release'
    banks={k:yaml.safe_load((source/(k+'.yaml')).read_text(encoding='utf-8')) for k in ('all','confirmed')}
    before=copy.deepcopy(banks)
    # The previously drafted nine personal stakes are individually authored,
    # but their guilty access accounts are NEVER replaced with innocent errands.
    where=copy.deepcopy(prior.WHERE)
    where['24']="I signed for the sealed incoming bottle and handed it to intake with the frame delivery. The lender's label said inert. Then I took the shop gifts to service. Later I went back to Grant's place for my first damage report. Glass on the table. Nobody home. I emptied my packing bin before the receiving photograph could be compared with it. Al, the broken corner was in there. I didn't want you finding it."
    where['27']="I went looking for Grant with the petition. Paige was asking about the gift; I interrupted. At intake I'd taken the bowl's ownership card and kept it inside my copy. Barb had warned me once already. I stayed after Grant told me to leave. I was not going to stand politely at the back while he thanked himself."
    where['18']="I unfastened the panel when the alcove closed. The lamp was too close to the weave. I took it through the private room and rolled it beside Grant's prepared place. He wasn't there. Production kept the separate stitch slides. Frank, I heard you asking me to leave it installed. I'd spent another client's advance on this fabric. I wasn't leaving it for somebody to scorch."
    edits=[]
    for edition,bank in banks.items():
        rows={c['id']:c for c in bank['characters']}
        for ident,text in where.items():rows[ident]['hearings']['where_innocent']=text
        for ident,text in METHOD.items():rows[ident]['hearings']['evidence_innocent']=text
        # Cary's actual work establishes source knowledge in EVERY world.
        rows['24']['hearings']['where_murderer']="I signed for the sealed incoming bottle and handed it to intake with the frame delivery. The lender's label said inert. Took the shop gifts to service. Freight lift stuck. Grant still had my first damage report, so I went to his private place to get it back. Glass set out. Nobody home. I picked up the shop carton to clear the chair, waited, then left. Al, I would rather move every chair here than answer for the word old."
        # A later return is already admitted. Deny the recorded encounter's
        # location, not all private-room access, to avoid a self-refuting answer.
        rows['27']['hearings']['evidence_murderer']="I gave him the petition at the public podium during Paige's interview. That's the exchange on the recorder. I came back later with the signature page, as I said. He never signed it. The card I took belongs to the bowl. Barb, you can call it disruption if it makes your evening easier. His death isn't the answer. Stop waiting for me to be pleased."
        rows['09']['hearings']['where_murderer']=rows['09']['hearings']['where_murderer'].replace('restore the purchase attachment','restore the collection attachment')
        # Keep interview time distinct from the later poisoning opportunity.
        rows['12']['coming_clean']['murderer']="I killed Grant. The interview was tonight at his private place, while the manager left his glass. The original opening proves it. After Grant returned to the reception I went back, alone, and used poison I'd taken at the preview. I called the interview yesterday's office conversation to make that recording unrelated to tonight. I wanted to protect my source; I chose murder instead. My editor has the original. Someone will have to tell the person who trusted me what I did with their trust."
        # Pending consequences move to Coming Clean rather than contradictory
        # pre-vote claims that all scandals have already been neatly resolved.
        rows['24']['coming_clean']['innocent']="I didn't kill Grant. I delivered the bottle to intake and the crest glass to service. I lied about the frame damage and threw out the broken corner. The photographs caught that lie. Al, the repair charge is mine. I don't know how I'm paying it. Tomorrow I have to tell the next person who hires me before they hear it from someone else."
        rows['18']['coming_clean']['innocent']="I didn't kill Grant. I carried my weave through his room. The slides were stitches; the bottle was real. I have to return the advance I spent on this fabric. Keeping my pattern rights won't pay that debt. Chip, you can help me pack the panel now. I need to go home with the thing I actually made."
        rows['28']['coming_clean']['innocent']="I didn't kill Grant. I looked at the bottle and called its band a price collar. I was wrong about the band. I wasn't confused about using a damaged comparison to buy my family's intact piece cheaply. I knew what I was doing. They have the top-up now; they don't have the whole explanation. I have to make that call."
        bank['status']='print_final_candidate_not_promoted'
        for c,old in zip(bank['characters'],before[edition]['characters']):
            for section in ('hearings','coming_clean'):
                for field,text in c[section].items():
                    if text!=old[section][field]:edits.append({'edition':edition,'id':c['id'],'section':section,'field':field,'before':old[section][field],'after':text})
        (dest/(edition+'.yaml')).write_text(yaml.safe_dump(bank,allow_unicode=True,sort_keys=False),encoding='utf-8')
    evidence=yaml.safe_load((source/'playable-evidence.yaml').read_text(encoding='utf-8'))
    evidence['hunt'][12]['rows'].append(['Delivered to intake','Cary Crates / sealed handover with frame delivery'])
    deferred=[]
    remove={'Advisory account','Family valuation','Dealer refund demand','Technology account','Bead recommendation','Sponsored podcast','Property story','Corrected archive','Editorial client','Textile commission','Production account'}
    for release in evidence['releases']:
        for exhibit in release['exhibits']:
            kept=[]
            for row in exhibit.get('rows',[]):
                if row[0] in remove:deferred.append({'exhibit':exhibit['id'],'row':row})
                else:kept.append(row)
            if 'rows' in exhibit:exhibit['rows']=kept
    # Keep the frame crack as evidence; its repair-bill resolution belongs
    # after accusations. It never proves the handler could not poison a glass.
    for r in evidence['releases']:
        for x in r['exhibits']:
            if x['id']=='work_and_settlement':
                x['title']='Workshop and handling records'
                x['rows']=[['Handling report','Frame corner damaged in delivery / first report calls it old damage'] if a=='Handling report' else [a,b] for a,b in x['rows']]
    (dest/'playable-evidence.yaml').write_text(yaml.safe_dump(evidence,allow_unicode=True,sort_keys=False),encoding='utf-8')
    shutil.copy2(source/'voice-story-bible.yaml',dest/'voice-story-bible.yaml')
    gate.write(dest/'manifest.json',{'revision':RUN.name,'baseline_commit':'0d6517e','limitations':'Unpromoted candidate. All current22 routes require separate blind assessment. No human solve-rate claim.','sha256':{p.name:gate.sha(p) for p in dest.iterdir()}})
    gate.write(RUN/'change-ledger.json',{'character_edits':edits,'deferred_settlement_rows':deferred,'new_shared_fact':'Cary signed sealed loan bottle to intake with frame delivery; lender called contents inert. Same in every world.','proof_constraints':'All material comparisons, recordings, photos, clock times, original false-before Monet statement and other guilty Method claims preserved. Robin falsehood narrowed to recorded encounter location; Dr Fact opportunity attachment made nonspecific. Paige confession visits distinguished.'})
    freeze(banks['confirmed'],evidence,dest)

def freeze(bank,evidence,dest):
    frozen=RUN/'frozen-source';shutil.copytree(dest,frozen)
    public=yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))
    people={str(c['id']).zfill(2):c for c in public['characters']}
    ids=[c['id'] for c in bank['characters']];people={i:people[i] for i in ids}
    public['active_character_ids']=ids
    (frozen/'character_copy.yaml').write_text(yaml.safe_dump(public,allow_unicode=True,sort_keys=False),encoding='utf-8')
    byname={c['name']:c for c in bank['characters']}
    visible={'number','title','department','stamp','paragraphs','rows','images'}
    def shown(x):
        out={k:v for k,v in x.items() if k in visible}
        if x.get('id')=='original_interview':out['paragraphs']=bank['pre_method_press_interview_opening']
        return json.dumps(out,ensure_ascii=False,indent=2)
    from visible_evidence import exhibits
    def release(key):return '\n\n'.join(shown(x) for r in evidence['releases'] if r['key']==key for x in exhibits(evidence,r,confirmed=True))
    def speeches(key,killer):
        text=[];field={'motive':'motive','opportunity':'where','method':'evidence'}[key]
        for g in next(r for r in bank['question_rounds'] if r['key']==key)['groups']:
            text.append('Question for '+', '.join(g['targets'])+': '+g['question'])
            for n in g['targets']:
                c=byname[n];text.append(n+'\n'+c['hearings'][field+('_murderer' if c['id']==killer else '_innocent')])
        return '\n\n'.join(text)
    trials=[]
    # No outcome-based selection: all22 worlds fixed once, each original kept.
    for index,ident in enumerate(ids,1):
        token=f't{index:03}';folder=RUN/'blind'/token;folder.mkdir(parents=True)
        stages={1:'Exactly one of these 22 characters committed the murder alone. Other mentioned staff are not selectable suspects.\n\n'+bank.get('player_briefing','')+'\n\n'+'\n\n'.join(p['name']+' / '+p['role']+'\n'+p['introduction'] for p in people.values()),2:'\n\n'.join(shown(x) for x in evidence['hunt']),3:release('before_motive'),4:speeches('motive',ident),5:release('before_opportunity'),6:speeches('opportunity',ident),7:release('before_method'),8:speeches('method',ident)}
        for n,text in stages.items():(folder/f'checkpoint_{n:02}.txt').write_text(text+'\n',encoding='utf-8')
        trials.append({'trial':token,'replicate':1,'murderer_id':ident,'murderer':people[ident]['name'],'inputs':{p.name:gate.sha(p) for p in folder.iterdir()}})
    reference=json.loads((ROOT/'docs/playtest/2026-10-24-RESTORED-OPPORTUNITY-SPOILERS/private-manifest.json').read_text(encoding='utf-8'))
    reference.update(run='Print-final current22 route coverage',revision=RUN.name,trials=trials,trial_count=22,replicates_per_culprit=1,source_sha256={p.name:gate.sha(p) for p in frozen.iterdir()},protocol='One fresh fork-none reader for each current22 selected culprit. Eight gated player-facing releases, immutable scores, accusation before finale. No prior tests or desired distributions exposed. Descriptive AI text checks, not human solve rates.')
    gate.write(RUN/'private-manifest.json',reference)
    instructions=(ROOT/'docs/playtest/2026-10-24-RESTORED-OPPORTUNITY-SPOILERS/READER_INSTRUCTIONS.md').read_text(encoding='utf-8').replace('2026-10-24-RESTORED-OPPORTUNITY-SPOILERS',RUN.name).replace('scripts/restore_opportunity_balance.py','scripts/print_final_balance.py')
    (RUN/'READER_INSTRUCTIONS.md').write_text(instructions,encoding='utf-8')
    gate.write(RUN/'resume-state.json',{'status':'frozen_unstarted','completed':0,'total':22,'candidate_promoted':False,'public_assets_unchanged':True})
    print('Frozen22 route cases. Sent assets and fallback unchanged.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','read','validate','finale','complete']);p.add_argument('--trial');p.add_argument('--stage',type=int);a=p.parse_args()
    if a.action=='prepare':prepare()
    else:gate.RUN=RUN;gate.gate(a.trial,a.action,a.stage)
