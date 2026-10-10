"""Bounded Act III edit; facts stay in evidence, resolution waits for Coming Clean."""
from pathlib import Path
import hashlib, json, yaml
from compile_connected_story import ROOT, LAB, compile_bank
from freeze_connected_case import export

revisions = {
    '03': "Original contents. That was the seller's condition. I forwarded the complete attachment to intake before the gala. Grant supplied the inert description afterward; I repeated it to the donors. Saul, I know you want me to say it slowly enough to sound like a confession. I have clients in this room. The refund demand was withdrawn, and I intend to hold his estate to that. Elon can request his purchase files through my solicitor. I am not opening them on this table for your entertainment.",
    '05': "Red paper, silver backing. My supply sleeve has more of it. I fitted that band across the stopper and inspected from the front. Missed the split at the back. Both dates are in front of you: mine on the original, mine on the insurance copy. Yes, I changed one. Claire, leave the workbench alone until I can pack it. I know where every strip belongs. I don't want people taking pieces to pass around and asking me afterward what used to be there.",
    '11': "Pull the power. That was my order. The request said take the room off the live monitor; I made sure there would be no saved copy to argue over later. My signature is on the technician's sheet. Fault is what I wrote in the log. You can ask me again, Paige. You will get the same answer: there is no footage. Brie, your staff go home when their shift ends. I am not keeping them here until somebody finds an answer they like.",
    '16': "Staff tried my spare after he died. It still works. I went in for the memo, saw the bottle, and left it closed. You have my old policy beside the one that replaced it. I remember why I wrote mine. We had lenders bringing things through the door and no money to tell them to wait. Artie, I kept that key when I left. I could come back whenever I pleased. Tonight I did. Must I hand over every part of this place before you'll stop asking?",
    '23': "I put the flavoring in his glass. That's how the private toast was ordered. I left the container with service and went back to the kitchen. The retained sample is in your report. I wasn't standing guard over that glass afterward; dinner still needed cooking. Monet, the cheese is still on my bill. I'm still expecting to be paid. If you want someone to point at, point at me. My staff have been carrying plates past his empty place, and some of you are still treating them as though they ought to smile.",
}

baseline = yaml.safe_load((ROOT/'source/connected_release/all.yaml').read_text(encoding='utf-8'))
old = {r['id']: r for r in baseline['characters']}
for number in (1,2,3):
    path=LAB/f'dramatic-dialogue-{number:02}.yaml'
    data=yaml.safe_load(path.read_text(encoding='utf-8'))
    for row in data['characters']:
        ident=str(row['id']).zfill(2)
        if ident in revisions:
            row['hearings']['evidence_innocent']=revisions[ident]
    path.write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False,width=110),encoding='utf-8')

current=compile_bank('all')
for row in current['characters']:
    ident=row['id']
    for field,text in row['hearings'].items():
        if ident in revisions and field=='evidence_innocent': continue
        assert text==old[ident]['hearings'][field],(ident,field)
    assert row['coming_clean']==old[ident]['coming_clean']

for active,killer,label,prior in [('all','25','30','30-03'),('confirmed','20','22','22-03')]:
    out=LAB/f'balance-act3-{label}-04'
    export(active,killer,out)
    before=LAB/f'balance-dramatic-{prior}'
    for n in range(1,8):
        assert (out/f'checkpoint_{n:02}.txt').read_bytes()==(before/f'checkpoint_{n:02}.txt').read_bytes(),n
    (out/'post_vote_endings.txt').write_bytes((before/'post_vote_endings.txt').read_bytes())
    (out/'post-vote-hash.json').write_bytes((before/'post-vote-hash.json').read_bytes())
    (out/'PROTOCOL.md').write_text('Fresh blind readers. Eight sequential checkpoints, saved before each next read. Accusations lock before endings. First seven inputs are byte-identical to the published revision03 same-case trial. Only five innocent Method speeches change. No target ratings or branch identities supplied.\n',encoding='utf-8')

(LAB/'ACT3_REVISION04_CONTRACT.json').write_text(json.dumps({
    'baseline_commit':'fc15ebd',
    'changed_fields':[i+'/evidence_innocent' for i in revisions],
    'unchanged':'All guilty speeches, all Motive/Opportunity speeches, evidence, questions, endings and sent public assets.',
    'fact_locations':{
        '03':'Dealer forwarding and original contents in E3 original_source; shortened declaration still admitted.',
        '05':'Both insurance dates and foil stock in E3 original_source; missed rear split still admitted.',
        '11':'No camera recording remains explicit and in E3 camera_work.',
        '16':'Key, memo and closed bottle retained; ordinary staff access in E3 collection_working_proof.',
        '23':'Container laboratory findings remain in E3 actual_service; individual flavoring and kitchen departure retained.'},
    'acceptance':'Same-case culprit accuracy and timing retained; seek more final innocent alternatives at5-7. Report all readers and do not publish a worse result.'
},indent=2)+'\n',encoding='utf-8')
print('Five innocent Method speeches drafted; first seven checkpoints identical in both cases.')
