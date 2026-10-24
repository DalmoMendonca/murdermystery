"""Restore late personal-stakes proof; explicitly establish the shared source opportunity."""
import argparse,copy,json,shutil,yaml
import concealed_stakes_balance as previous
import print_final_balance as freezer
import exhaustive_balance as gate
ROOT=previous.ROOT
RUN=ROOT/'docs/playtest/2026-10-24-SHARED-PREVIEW-PRINT-SPOILERS'

def prepare():
    dest=RUN/'candidate-source';assert not dest.exists(),'Never overwrite frozen tests.'
    shutil.copytree(previous.RUN/'candidate-source',dest)
    for edition in ('all','confirmed'):
        p=dest/(edition+'.yaml');bank=yaml.safe_load(p.read_text(encoding='utf-8'));byid={c['id']:c for c in bank['characters']}
        bank['status']='shared_preview_candidate_not_promoted'
        byid['01']['hearings']['where_innocent']="Sue and I stopped the announcement at the public desk. Then I used Grant's temporary office to call the board. Barb gave me a minute alone. I sent the refusal and waited for somebody to say I'd done the right thing. Nobody did. Claire, take the seating list. I have spent enough of tonight arranging where everyone else belongs."
        byid['15']['hearings']['where_innocent']="I changed the collector photo selection and showed the platform on my phone. After the preview I tried the private-room panel from Grant's chair. No connection, just my demo. Monet keeps calling the installation a bill. It was a proposal. I don't issue invoices for work that hasn't happened. We were meant to agree a launch, and he wouldn't even come back to look."
        byid['18']['hearings']['where_innocent']="I unfastened the panel when the alcove closed. The lamp was too close. I used Grant's table to roll the weave; he was still out at the reception. Production kept the stitch slides. The merchant's bill is for this fabric, yes. The other advance went to its own commission. Frank, don't ask me to put the panel back. You can be disappointed in an empty alcove."
        byid['02']['hearings']['evidence_innocent']="The complete query went to intake with the papers. Staff kept the warning. Reed, do you want me to say I should have stopped the preview? I should have. I kept asking for an answer because asking meant I could put the file down again. Don't collect the old label yet. It's mine to carry."
        byid['09']['hearings']['evidence_innocent']="I wrote the contents query. Intake said keep closed. What else would you like me to say? That I understood it? I did. Dada, please don't rescue this conversation. Reed asked an ordinary question and I spent the evening trying to look like the person who'd thought of it."
        p.write_text(yaml.safe_dump(bank,allow_unicode=True,sort_keys=False),encoding='utf-8')
    p=dest/'playable-evidence.yaml';e=yaml.safe_load(p.read_text(encoding='utf-8'))
    for r in e['releases']:
        for x in r['exhibits']:
            if x['id']=='service_account':x['paragraphs'].append("The donor used a temporary museum office with a service entrance. Staff brought signatures, supplies and messages through it; outside camera crews were excluded. It was not the public podium. No attendant stayed beside the prepared place after he returned to the reception.")
            if x['id']=='initial_samples':
                x['rows'].append(['Preview attendance','The invited gala party attended the incoming-loan preview before the reception. No continuous watch was kept on the closed bottle.'])
                x['paragraphs'].append("Preview admission was by gala invitation, not restricted to collection staff. The contents were described as inert at the time. Staff also retained ordinary keys to the preparation cupboard; access was not exclusive to the handler or conservator.")
    # Remove only absent-role appendices in the actual current22 view.
    e['confirmed_filters']={'omit_exhibits':['preview_image_custody'],
        'omit_rows':{'production_originals':['Styling copies'],'governing_papers':['Family succession proposal','Family request'],'collector_working_folder':['Proposed sale','Endorsement']},
        'omit_paragraph_prefixes':{'production_originals':['Press desk comparison:','Original sound cue:']}}
    p.write_text(yaml.safe_dump(e,allow_unicode=True,sort_keys=False),encoding='utf-8')
    manifest={'revision':RUN.name,'baseline_commit':'0d6517e','parent_candidate':previous.RUN.name,'limitations':'Unpromoted. Source opportunity explicitly established before ActII for the whole gala party; no physical poison transfer is witnessed. One fresh reader per current22 selected world is descriptive, not human solve rates.','sha256':{p.name:gate.sha(p) for p in dest.iterdir() if p.name!='manifest.json'}}
    gate.write(dest/'manifest.json',manifest)
    gate.write(RUN/'change-ledger.json',{'source_parent':previous.RUN.name,'murderer_accounts_and_finales_exactly_unchanged_from_parent':True,'structural_change':'Explicit invited-gala preview attendance and shared cupboard keys beforeActII. Confessions no longer introduce the existence of source access for noncollection roles. Personal-scandal proof stays in final evidence, as in the better final-field parent.','naturalness':'Temporary donor office has a service entrance, not an exclusive private salon. Three innocent visits vary their delivery and retain the same unsupervised access. Two collection Method responses shortened.','confirmed_view':'Only absent-role appendices omitted; all30 retains them. No timestamps, samples, material comparisons, original recordings or distinguishing guilty lies changed.'})
    bank=yaml.safe_load((dest/'confirmed.yaml').read_text(encoding='utf-8'))
    freezer.RUN=RUN;freezer.freeze(bank,e,dest)
    instructions=RUN/'READER_INSTRUCTIONS.md';instructions.write_text(instructions.read_text().replace('scripts/print_final_balance.py','scripts/shared_preview_balance.py'),encoding='utf-8')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','read','validate','finale','complete']);p.add_argument('--trial');p.add_argument('--stage',type=int);a=p.parse_args()
    if a.action=='prepare':prepare()
    else:gate.RUN=RUN;gate.gate(a.trial,a.action,a.stage)
