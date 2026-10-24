"""Distinct innocent cover stories; keep every murder-route proof comparison."""
from pathlib import Path
import argparse,copy,json,shutil,yaml
import print_final_balance as parent
import exhaustive_balance as gate
ROOT=parent.ROOT
RUN=ROOT/'docs/playtest/2026-10-24-CONCEALED-STAKES-SPOILERS'
BRIEFING='Everyone has something to hide. Your printed account may protect a personal secret. Read your selected box as written; do not invent events, witnesses or evidence.'

# Each cover is false about a different existing scandal. The true murder
# observation in Method stays distinct from the selected culprit's false one.
COVERS={
'04':{
'motive_innocent':"Friday. That's when wages are due. Grant's check could cover our staff; his terms let him inspect every transfer. I won't have the cleaners waiting by the phone while he decides which chair his name should go on. Artie wanted his authority protected. I wanted payroll covered. And yes, I told Grant he could keep his check if the price was treating us like thieves.",
'where_innocent':"The extra-course ticket came to accounts. I crossed out our account and took Grant's copy to his place. Glass waiting; no Grant. I took my transfer slip away again. The payroll transfer had board authorization. He didn't need to inspect it privately. Brie, send the supplier to me. Don't send me another speech about what the donor expects.",
'evidence_innocent':"Serve the original order, bill the addition to Grant. Those were my instructions. The toast stayed booked. I had authority to move that money into wages. The payroll line saying authorization absent is an office problem. Artie, don't ask me to find a different way to say that. Somebody had to get them paid.",
'final_innocent':"I didn't kill Grant. The toast stayed booked; my private visit was over the bill. I lied about board authorization. There wasn't any. I moved restricted money into wages because Friday was coming. Calling the missing approval an office problem didn't make one appear. Artie, when they freeze that account, tell the cleaners I paid them. Don't ask them to be grateful for what comes next."},
'05':{
'where_innocent':"I fitted the red band before the preview. Kept the condition sheet. Grant waved the insurance copy at me and asked what my signature was worth. That date wasn't a change I authorized. Then Frank's mount moved. Finally, something I could fix with my hands. Frank, get the load down. I'll discuss your feelings about my tone afterward.",
'evidence_innocent':"Foil-backed paper. Red face, silver back. I fitted it across the stopper. Inspected the front. Missed the split behind. The insurance date is a copying error. I didn't alter it. No, Barb, leave the supply sleeve where it is. Photograph the stock before you touch it. There are enough people deciding what happened at my workbench.",
'final_innocent':"I didn't poison Grant. My band was foil-backed paper. I missed the split behind it. I changed the insurance date myself, and then called it a copying error. Grant had that copy. I wanted you examining the paper instead of the person who signed it. Claire, the workbench can be packed now. Photograph every piece. I don't expect my word to do the job."},
'14':{
'motive_innocent':"I came with a ministry instruction to return the bowl. Grant wanted me in his acquisition photograph instead. Imagine being invited to bless the thing you've come to stop. Sue questioned the letter. She always does notice the part of an evening everyone else has agreed to admire. I wanted a seat where the decision happened. I wasn't going home with another photograph.",
'where_innocent':"I circulated the letter. Sue asked whose authority it carried; I told her to look at the heading. I requested sealed water for Grant before the toast. He could read a demand without being handed another drink. Sue, you knew how badly I wanted to be in that room. You also chose the most public possible moment to question why I was there.",
'evidence_innocent':"The water stayed sealed. He accepted the toast. The ministry stands behind my letter; the file calling it a claimants' request is incomplete. Sue, stop looking at the stationery. If the family wants to discuss the bead supplier, they can ask me. I did not come all this way to have my whole evening reduced to a heading and a commission.",
'final_innocent':"I didn't kill Grant. The water was unopened; he drank the toast. My letter was the claimants' request. No ministry gave me that authority. I borrowed the stationery's grandeur and then defended it because admitting the truth felt like being sent back outside. The supplier would have paid me a commission too. Sue, be angry with me. Please don't let that become a reason to stop hearing the claimants."},
'15':{
'where_innocent':"I changed the collector photo selection and showed the platform on my phone. The private-room panel was part of that demonstration. I attended the preview, then tried the display at Grant's prepared place. He wasn't there. Monet keeps calling the installation a bill. It was a proposal. I don't issue invoices for work that hasn't happened. We were meant to agree a launch tonight.",
'evidence_innocent':"The panel showed a sample image. It wasn't a camera connection. The document in accounts was an estimate, whatever their file calls it. Monet, I didn't send you a demand for payment. Can we put the phones down? Mine still shows the room the way I wanted it to look. I can explain what it was going to do. I don't think anybody wants that explanation now.",
'final_innocent':"I didn't kill Grant. The panel never connected to the camera. I did send an installation invoice before I installed anything. An invoice, not an estimate. Monet refused it and I credited it. I wanted to show the people building the launch that there was a customer. I have to tell them what I used as proof. Please don't ask me to demonstrate the platform again tonight."},
'18':{
'motive_innocent':"I asked for early payment. Grant offered it if every future use of my pattern became his. He called that rescuing a commission. I had another client's advance safely assigned to their work; I didn't need him taking an interest in it. Chip told me when to stop touching the weave. Grant wanted to decide when I was finished owning it.",
'where_innocent':"I unfastened the panel when the alcove closed. The lamp was too close. I took it through the private room and rolled it beside Grant's prepared place. No Grant. I left with it. The merchant's bill is for this fabric, yes. The other advance went to its own commission. Frank, don't ask me to put the panel back. You can be disappointed in an empty alcove.",
'evidence_innocent':"The slides enlarge stitches. That was the physical loan bottle beside my panel. The payment line has been assigned to the wrong job. I didn't spend the other client's advance on this. Chip, please don't offer to hold everything steady for me. I'd like to carry one thing out of this building without somebody telling me what it ought to cost.",
'final_innocent':"I didn't kill Grant. I carried my weave past his glass; the bottle at the preview was real. The merchant's payment line is right. I spent the other client's advance on the gala fabric, and I kept saying I hadn't. Keeping my pattern rights won't repay that debt. Chip, you can help me pack now. I have to go home with the thing I actually made, then call the person who paid for something else."},
'24':{
'motive_innocent':"Grant had receiving photographs and my frame report. He wanted me to sign another delivery without checking it. Said we could clear up the first one afterward. I lost a job once with my coat still on the peg. I know what an employer hears when a donor makes that call. Al, I said the corner was old damage. I'd rather not spend the whole dinner arguing over my report.",
'where_innocent':"I signed the sealed bottle over to intake with the frames. Label said inert. Took the shop gifts to service. Later I went to Grant's place for my damage report. Glass set out. Nobody home. I emptied my packing bin afterward. Normal cleanup. The corner was already cracked when I got the frame. Al, if there's another job, give it to me. Anything that needs moving.",
'evidence_innocent':"Service unpacked the crest glass from my carton. Grant drank from that engraving. The frame crack was there before delivery. Different light in the receiving photograph, that's all. Al, I'm not signing another report because someone prefers the second picture. You don't unload a frame and get to invent how it looked on the truck.",
'final_innocent':"I didn't kill Grant. I handed the bottle to intake and the crest glass to service. I cracked the frame corner, called it old damage, and threw the broken piece away. The pictures weren't bad light. I was lying. Al, the repair charge is mine. I don't know how I'm paying it. Tomorrow I have to tell the next person who hires me before they hear it from someone else."},
'28':{
'motive_innocent':"Grant wanted our family valuation beside what I'd paid a dealer, in the gala handout. I took the handout away. The family piece was damaged; that's what the comparison was for. I manage those things because someone has to. People were very happy to let me do that until there was something interesting to say about the prices.",
'where_innocent':"I removed the price comparison and kept it in the sale folder. At the preview I looked closely at the bottle. Its red band looked like an auction collar. Chip said closure treatment. I asked what a repair did to value. I didn't ask to open it. Grant wanted the family figures read out over dinner. I told him he'd regret making a performance of it.",
'evidence_innocent':"The band crossed the stopper. Chip corrected me about that. Our family piece was damaged too, whatever the valuation file says. I didn't use the wrong comparison. No, they haven't called. I keep checking. I would rather explain it in my voice than let Grant's handout speak for me. I am beginning to wonder whether they want to hear my voice.",
'final_innocent':"I didn't kill Grant. The bottle band crossed the stopper; calling it a price collar was my mistake. Our family object was intact. I used a damaged comparison to buy their shares cheaply and then defended the price. The top-up is paid. It doesn't correct what I did with their trust. I have to make that call without explaining how sensible I was trying to be."},
}

def prepare():
    dest=RUN/'candidate-source';assert not dest.exists(),'Never overwrite a frozen version.'
    shutil.copytree(parent.RUN/'candidate-source',dest)
    edits=[]
    for edition in ('all','confirmed'):
        path=dest/(edition+'.yaml');bank=yaml.safe_load(path.read_text(encoding='utf-8'));rows={c['id']:c for c in bank['characters']}
        bank['player_briefing']=BRIEFING
        for ident,fields in COVERS.items():
            c=rows[ident]
            for field,value in fields.items():
                section='coming_clean' if field=='final_innocent' else 'hearings';key='innocent' if field=='final_innocent' else field
                edits.append({'edition':edition,'id':ident,'section':section,'field':key,'before':c[section][key],'after':value});c[section][key]=value
        bank['status']='concealed_stakes_candidate_not_promoted'
        path.write_text(yaml.safe_dump(bank,allow_unicode=True,sort_keys=False),encoding='utf-8')
    p=dest/'playable-evidence.yaml';evidence=yaml.safe_load(p.read_text(encoding='utf-8'))
    for r in evidence['releases']:
        for x in r['exhibits']:
            if x['id']=='collector_working_folder':
                x['rows'].extend([['Family valuation','Damaged comparison used for intact family object'],['Installation invoice','Issued by Elon Mosaic before any connection was installed / refused by accounts']])
            if x['id']=='work_and_settlement':
                x['rows'].append(['Textile merchant payment','Gala panel fabric paid from advance assigned to another client commission'])
    p.write_text(yaml.safe_dump(evidence,allow_unicode=True,sort_keys=False),encoding='utf-8')
    manifest={'revision':RUN.name,'baseline_commit':'0d6517e','parent_candidate':parent.RUN.name,'limitations':'Unpromoted. Seven innocents conceal separate scandals; murder-route physical facts and guilty proofs retained. All current22 worlds require assessment.','sha256':{p.name:gate.sha(p) for p in dest.iterdir() if p.name!='manifest.json'}}
    gate.write(dest/'manifest.json',manifest)
    gate.write(RUN/'change-ledger.json',{'character_edits':edits,'evidence_delta':'Retain original valuation and installation-invoice facts without settlement; make the existing advance diversion explicit in merchant payment. All murder-relevant physical observations, recording and service facts unchanged.','fairness':'An innocent may lie about a separate scandal but states a true murder-route fact. A mere lie is not sufficient; assess relation to the murder mechanism, motive and opportunity. This explanation is author-side only.'})
    bank=yaml.safe_load((dest/'confirmed.yaml').read_text(encoding='utf-8'))
    parent.RUN=RUN;parent.freeze(bank,evidence,dest)
    instructions=RUN/'READER_INSTRUCTIONS.md';instructions.write_text(instructions.read_text().replace('scripts/print_final_balance.py','scripts/concealed_stakes_balance.py'),encoding='utf-8')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','read','validate','finale','complete']);p.add_argument('--trial');p.add_argument('--stage',type=int);a=p.parse_args()
    if a.action=='prepare':prepare()
    else:gate.RUN=RUN;gate.gate(a.trial,a.action,a.stage)
