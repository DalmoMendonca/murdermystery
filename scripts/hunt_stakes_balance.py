"""Put existing personal-stakes evidence in the hunt, not in a late dossier."""
import argparse,copy,json,shutil,yaml
import concealed_stakes_balance as previous
import print_final_balance as freezer
import exhaustive_balance as gate
ROOT=previous.ROOT
RUN=ROOT/'docs/playtest/2026-10-24-HUNT-STAKES-PRINT-SPOILERS'

def prepare():
    dest=RUN/'candidate-source';assert not dest.exists(),'Never overwrite frozen tests.'
    shutil.copytree(previous.RUN/'candidate-source',dest)
    for edition in ('all','confirmed'):
        p=dest/(edition+'.yaml');bank=yaml.safe_load(p.read_text(encoding='utf-8'))
        bank['status']='hunt_stakes_print_candidate_not_promoted'
        # A pointed demand for authority is more human than a complete recap
        # of a laboratory or catalogue paragraph. Preserve critical facts.
        byid={c['id']:c for c in bank['characters']}
        byid['02']['hearings']['evidence_innocent']="The complete query went to intake with the papers. Staff kept the warning. Reed, do you want me to say I should have stopped the preview? I should have. I kept asking for an answer because asking meant I could put the file down again. Don't collect the old label yet. It's mine to carry."
        byid['09']['hearings']['evidence_innocent']="I wrote the contents query. Intake said keep closed. What else would you like me to say? That I understood it? I did. Dada, please don't rescue this conversation. Reed asked a perfectly ordinary question and I spent the evening trying to look like the person who'd thought of it."
        p.write_text(yaml.safe_dump(bank,allow_unicode=True,sort_keys=False),encoding='utf-8')
    p=dest/'playable-evidence.yaml';e=yaml.safe_load(p.read_text(encoding='utf-8'))
    h=e['hunt'];byid={x['id']:x for r in e['releases'] for x in r['exhibits']}
    # Loan history and condition stay separate from the final material proof.
    h[13]['rows'].append(['Condition record dates','Signed original: October 30 / insurance copy: October 29 / same treatment'])
    h[2]['rows']=[['Issued by','Claimants and their representatives'],['Official status','No ministry-issued return instruction']]
    h[6]['rows'].append(['Family valuation attachment','Damaged comparison / family object photographed intact'])
    # The founding shortcut remains in the full final working proof, so its
    # inactive founder route is not destroyed by changing this hunt envelope.
    h[10]={'number':11,'title':'The launch invoice','department':'MERIDIAN / ACCOUNTS PAYABLE','stamp':'RETURNED TO ISSUER','rows':[['Issuer','Elon Mosaic'],['Description','Private-room platform installation'],['Status','Invoice submitted / no connection installed'],['Accounts action','Payment refused']], 'paragraphs':['A demonstration on a phone does not constitute an installed system. Return this invoice to the issuer.']}
    h[11]['title']='The work behind the show'
    h[11]['department']='GALA PRODUCTION / DELIVERY AND PURCHASING'
    h[11]['rows'].append(['Textile merchant payment','Gala panel fabric paid from advance assigned to another client commission'])
    h[0]['rows'].append(['Payroll attachment','Restricted-fund transfer paid staff wages / no board authorization'])
    h[15]['title']="The handler's deliveries"
    h[15]['rows'].append(['Frame receiving report','Old damage, recorded by Cary Crates'])
    h[15]['images']=[{'id':'frame_condition_pair','observation':'Two dated handling photographs of the same loan frame. Before delivery the corner is intact; the receiving photograph shows a new corner crack. The handler\'s first report calls it old damage.'}]
    # Early personal facts are not repeated as a late explanatory answer key.
    remove={'Family valuation','Installation invoice','Textile merchant payment','Payroll ledger'}
    for r in e['releases']:
        for x in r['exhibits']:
            if 'rows' in x:x['rows']=[row for row in x['rows'] if row[0] not in remove]
            if x['id']=='service_account':
                x['paragraphs'].append("The donor's temporary office had a service entrance. Museum staff used it to bring signatures, supplies and messages; outside camera crews were excluded. It was not the public podium. The donor left for the reception after the interview, and no attendant stayed beside the prepared place.")
    # Printed/transcribed current22 releases omit material serving only absent
    # roles. The all30 edition retains it. These are PRIVATE rendering filters.
    e['confirmed_filters']={'omit_exhibits':['preview_image_custody'],
        'omit_rows':{'production_originals':['Styling copies'],'governing_papers':['Family succession proposal','Family request'],'collector_working_folder':['Proposed sale','Endorsement']},
        'omit_paragraph_prefixes':{'production_originals':['Press desk comparison:','Original sound cue:']}}
    p.write_text(yaml.safe_dump(e,allow_unicode=True,sort_keys=False),encoding='utf-8')
    manifest={'revision':RUN.name,'baseline_commit':'0d6517e','parent_candidate':previous.RUN.name,'limitations':'Unpromoted current22 revision. One locked attentive reader per selected world, not human solve-rate estimates. All physical murder facts retained; personal-scandal background released during hunt.','sha256':{p.name:gate.sha(p) for p in dest.iterdir() if p.name!='manifest.json'}}
    gate.write(dest/'manifest.json',manifest)
    gate.write(RUN/'change-ledger.json',{'source_parent':previous.RUN.name,'murderer_accounts_unchanged_from_parent':True,'personal_facts_released_earlier':['payroll authorization','ministry authority','family object condition','installation invoice','client advance diversion','frame damage','insurance dates'],'new_shared_context':'Donor temporary office has service entrance used by museum staff; public filming excluded. No witness, time, material or chemical result changed.','confirmed22_retrieval':'Omit only absent-role evidence dependencies; retain full all30 edition. True/false murder propositions remain independently checkable.'})
    bank=yaml.safe_load((dest/'confirmed.yaml').read_text(encoding='utf-8'))
    freezer.RUN=RUN;freezer.freeze(bank,e,dest)
    instructions=RUN/'READER_INSTRUCTIONS.md';instructions.write_text(instructions.read_text().replace('scripts/print_final_balance.py','scripts/hunt_stakes_balance.py'),encoding='utf-8')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','read','validate','finale','complete']);p.add_argument('--trial');p.add_argument('--stage',type=int);a=p.parse_args()
    if a.action=='prepare':prepare()
    else:gate.RUN=RUN;gate.gate(a.trial,a.action,a.stage)
