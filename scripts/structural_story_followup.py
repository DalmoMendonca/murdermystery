"""Bounded follow-up; leaves revision02 trials and scores immutable."""
import argparse,hashlib,json,yaml
from pathlib import Path
import structural_story_pass as prior
ROOT=prior.ROOT
RUN=ROOT/'docs/playtest/2026-10-11-STRUCTURAL-FOLLOWUP-SPOILERS'
PREVIOUS=prior.RUN

MOTIVES={
'01':(
"Monet, will that check clear before Friday? I still don't have an answer. Grant wanted his name over the door, a vote in every department, and my resignation. Sue objected to the terms. Six years here. I had written the introduction for the man replacing me. It's in my pocket. I keep reaching for it.",
"Monet, will that check clear before Friday? Grant wanted his name over the door, a vote in every department, and my resignation. Sue objected to the terms. Six years here. I had written the introduction for the man replacing me. Our savior, I wrote. It's in my pocket. I keep reaching for it."),
'05':(
"Recent repair. Not ancient. Grant wanted ancient on the label, with my name beneath it. We'd already argued over treatment paperwork. Then the entrance mount moved. I stopped the conversation. Claire, you know me: I'm bad company when things are coming loose. I was bad company tonight.",
"Recent repair. Not ancient. Grant wanted ancient on the label. He had the insurance copy with the date I altered. I said no. Then the entrance mount moved, and he said I was inventing a fault to protect myself. Claire knows how I check a mount. He made people laugh at it."),
'06':(
"Vincent, tell them whose jacket it was. Nobody's. Empty jacket, gilded chair, my film: Donor Collapse. Grant wanted the commission without my name distracting from his generosity. I'd finally made something people would remember. I was going to make that room uncomfortable. That was the work. I can't bear the title now.",
"Vincent, tell them whose jacket it was. Nobody's. Empty jacket, gilded chair, my film: Donor Collapse. Grant's foundation wanted to acquire it with my name removed. Getting anyone to look at my work took years. He expected thanks for erasing me from it. I was going to make that room uncomfortable. I can't bear the title now."),
'11':(
"He asked for privacy from the live monitor. I gave it to him. Artie wanted a smooth evening; I wanted visiting crews out of our way. The donor gets the exception. Security gets the questions. That's all I have to say about why I agreed.",
"He asked for privacy from the live monitor. I gave it to him and wrote equipment fault. He knew that entry was false. It meant the next time I refused him, he had something to put on Artie's desk. The donor gets the exception. Security gets the questions. That's all I have to say about why I agreed."),
'18':(
"That fabric cost another client's advance. I spent it. Grant offered early payment if I gave him every future use of my pattern. Chip kept saying leave it alone. I couldn't leave it alone: another length, another color, then it would be right. That's what I told myself in the shop. My client was still expecting her work.",
"That fabric cost another client's advance. I told Grant when I asked for early payment. He would fill the hole if every future use of my pattern became his. Another length, another color, then it would be right. That's what I told myself in the shop. My client was still expecting her work. He knew what it would cost me to refuse."),
'19':(
"I found the missing document. I changed the bowl entry. Grant wanted settled ownership put back, and I wanted my name on the correction. Yes, my name. Claire, it's the same chapter. Again. I've stopped telling people which draft I'm on. Grant called the finding a student's publicity stunt. I'd like you to read it before deciding that.",
"I found the missing document. I changed the bowl entry. Grant wanted settled ownership put back. He could make my correction a publicity stunt and my doctorate the museum's embarrassment. Claire, it's the same chapter. Again. I've stopped telling people which draft I'm on. I'd like you to read the finding before deciding what you think of me."),
'23':(
"Has everybody eaten? I'm asking seriously. Grant added a cheese course after we'd bought the food. Monet held the charge; the supplier wanted paying; he wanted the plates out. The private toast was already paid. I wanted one person outside the kitchen to say no. We had six other things going wrong. You don't usually hear about those.",
"Has everybody eaten? I'm asking seriously. I'd bought Grant's extra cheese course without funded authorization. Monet held the charge; the supplier wanted my money; he wanted the plates out. The private toast was already paid. I wanted one person outside the kitchen to say no. He knew whose bill it would become. You don't usually hear about those."),
'28':(
"Please don't pass the family handout around. I removed it. I bought their shares using a damaged example to set the price. Ours was intact. Then I paid a dealer much more for another work. Grant had both figures. I manage the family things. They let me. I haven't called them. I wanted to get there before he did.",
"Please don't pass the family handout around. I removed it. I bought their shares using a damaged example, though ours was intact. Then I paid a dealer much more for another work. Grant wanted both figures in the handout. They trusted me with the family things. Paying them back wouldn't stop him showing what I'd done. I haven't called them.")}

METHOD={
'07':(
"Joined wood, painted. That's my lighting model. I delivered the painting; Grant held the last payment while he asked for reproduction rights. Hugh, the picture is delivered. Stop trying to sell the rest of me with it.",
"My wooden model stood on the preview support. The acquired glass bottle stayed out of the presentation. Grant held the last payment while he asked for reproduction rights. Hugh, the picture is delivered. Stop trying to sell the rest of me with it."),
'15':(
"A sample image. The camera connection was never installed. I pitched it anyway. Monet asked what she was paying for and I kept showing her my phone. Turn it over. I'm finished showing it.",
"The panel was live. Removing the room from the monitor left my phone's private camera feed running; I saw the place when I passed. Monet asked what she was paying for. Turn the phone over. I'm finished showing it."),
'25':(
"Frank turned us back. I turned the group around. The new handout was my doing. The visits still need funding. That money won't appear because I insist children deserve to come here. I know that. I'm still going to insist.",
"The private place was part of the group tour. I stayed with the group throughout it. The new handout was my doing. The visits still need funding. That money won't appear because I insist children deserve to come here. I'm still going to insist."),
'29':(
"The editor corrected the name. I kept the old poison account beside it. The deed's in Sue's folder with the later settlement. Anne, I'll give you the whole story another day. I don't have a story to tell you about this.",
"The editor's follow-up says the contents were neutralized before transfer. The deed's in Sue's folder with the later settlement. Anne, I'll give you the whole story another day. I don't have a story to tell you about this.")}

def prepare():
    dest=RUN/'candidate-source';assert not RUN.exists();dest.mkdir(parents=True)
    for p in (PREVIOUS/'candidate-source').iterdir():
        if p.name!='manifest.json':(dest/p.name).write_bytes(p.read_bytes())
    for edition in ['all','confirmed']:
        p=dest/(edition+'.yaml');bank=yaml.safe_load(p.read_text(encoding='utf-8'))
        for c in bank['characters']:
            ident=str(c['id']).zfill(2)
            for i,branch in enumerate(['innocent','murderer']):
                if ident in MOTIVES:c['hearings']['motive_'+branch]=MOTIVES[ident][i]
                if ident in METHOD:c['hearings']['evidence_'+branch]=METHOD[ident][i]
            if ident=='18':
                # A tentative perception is not a categorical source denial. Its literal claim
                # can fit either world; the final private account still distinguishes them.
                for branch in ['innocent','murderer']:
                    c['hearings']['where_'+branch]+=' The bottle looked like another projected shape in that light. I had given production pattern slides, not an inventory of the bench.'
        bank['status']='unpublished_structural_story_revision03'
        prior.dump(p,bank)
    info={'revision':'structural-story-revision03-2026-10-11','baseline_commit':'f8b462b','status':'UNPUBLISHED','sha256':{p.name:prior.sha(p) for p in dest.iterdir()},'limitations':'Six fixed critical-case diagnostics; no new exhaustive audit; physical attribution remains circumstantial.'}
    (dest/'manifest.json').write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
    prior.RUN=RUN;prior.freeze()
    for edition in (22,30):
        p=RUN/f'cast{edition}/READER_INSTRUCTIONS.md'
        p.write_text(p.read_text(encoding='utf-8').replace('scripts/structural_story_pass.py','scripts/structural_story_followup.py'),encoding='utf-8')
        m=RUN/f'cast{edition}/private-manifest.json';data=json.loads(m.read_text(encoding='utf-8'));data['revision']=info['revision'];m.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Revision03 frozen: eight Motive pairs, four shorter Method pairs, tentative Elle observation in both Opportunity branches.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','read','validate','finale','complete']);p.add_argument('--edition',choices=['22','30']);p.add_argument('--trial');p.add_argument('--stage',type=int);a=p.parse_args()
    if a.action=='prepare':prepare()
    else:
        assert a.edition;prior.gate.RUN=RUN/('cast'+a.edition);prior.gate.gate(a.trial,a.action,a.stage)
