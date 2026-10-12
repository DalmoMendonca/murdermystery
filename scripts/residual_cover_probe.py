"""A single final-round structural probe, not a replacement eight-stage balance audit."""
from pathlib import Path
import json,yaml,shutil
import structural_story_pass as gate
ROOT=gate.ROOT
RUN=ROOT/'docs/playtest/2026-10-11-RESIDUAL-COVER-PROBE-SPOILERS'
OLD=ROOT/'docs/playtest/2026-10-11-STRUCTURAL-FOLLOWUP-SPOILERS'

def prepare():
    assert not RUN.exists();dest=RUN/'candidate-source';dest.mkdir(parents=True)
    for p in (OLD/'candidate-source').iterdir():
        if p.name!='manifest.json':shutil.copy2(p,dest/p.name)
    for edition in ['all','confirmed']:
        p=dest/(edition+'.yaml');b=yaml.safe_load(p.read_text(encoding='utf-8'))
        for c in b['characters']:
            if c['id']=='03':
                c['hearings']['where_innocent']="I withheld the seller's correspondence from the auction handouts. Bowl and bottle, both purchases. The original-contents attachment went to intake. Grant supplied the inert description. I did not want a second purchase dispute performed for the collectors. I asked the display writers to use his description. I was not in a charitable mood."
                c['hearings']['evidence_innocent']="The seller required original contents. I sent intake the complete attachment before the gala. The press version printed that condition too. It did not hide a warning. Elon, your files are available through my attorney. Tonight they stay closed. I am not conducting the liquidation of my firm over dinner."
            if c['id']=='28':
                c['hearings']['motive_innocent']="Please don't pass the family handout around. I bought their shares, then spent much more with a dealer. Grant had both figures. He wanted a comparison printed as though two purchases told him everything about a family. I removed it. They let me manage these things. I wanted to speak to them before he did. I haven't called."
                c['hearings']['evidence_innocent']="Across the stopper. Chip showed me the drawing after I asked about value. I'd called it a price collar. I know the difference now. My family's comparison was for an intact piece, just like ours. That part was fair. They haven't called. I keep checking my phone under the table. Could we get to the next question?"
        gate.dump(p,b)
    m={'revision':'residual-cover-probe-2026-10-11','status':'UNPUBLISHED_PROTOTYPE','sha256':{p.name:gate.sha(p) for p in dest.iterdir()},'limitations':'One final-only blind diagnostic. Not eight staged ratings; never promote from this probe alone.'}
    (dest/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
    gate.RUN=RUN;gate.freeze()
    # Player-facing releases only. The reviewer sees no branch headings or selection.
    trial=RUN/'cast22/blind/t001'
    text='\n\n'.join(f'RELEASE {n}\n'+(trial/f'checkpoint_{n:02}.txt').read_text(encoding='utf-8') for n in range(1,9))
    (RUN/'player-facing-world.txt').write_text(text,encoding='utf-8')
    (RUN/'PROBE_INSTRUCTIONS.md').write_text('Read only player-facing-world.txt in this folder. You are a fresh attentive reader of a murder mystery with exactly one murderer among its22 named characters. No other files, prior context, memory, hidden selection, or agents. Read all8 releases. Write final-review.json here with final suspicion scores (integers0–10 for every exact character name), accused (one name), confidence0–10, naturalness0–10, feedback (150–250words), and fairness_gaps (array). Explain which contradictions are relevant to murder, which could concern separate misconduct, and whether any innocent seeming account is confusing or unfair. Use your own distribution. Do not infer an expected result. This is a final-only assessment, not a sequential ranking exercise. Report saved completion only.',encoding='utf-8')
    print('Frozen single final-only blind probe; murderer inputs and published source unchanged. Two innocent covers altered.')

if __name__=='__main__':prepare()
