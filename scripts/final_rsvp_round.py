"""Freeze a finite new-cast check of the published game, never a lab rewrite."""
from pathlib import Path
import argparse,copy,json,re,secrets,shutil,yaml
import exhaustive_balance as gate

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest/2026-10-23-FINAL-RSVP22-SPOILERS'
ABSENT_ROLES={'03':'the dealer','10':'the family representative','16':'the founder',
              '17':'the auctioneer','21':'the collector','22':'the critic',
              '26':'the photographer','30':'production'}
DIRECT={
 ('07','hearings','where_innocent'):{'Hugh, I know you could sell the whole arrangement.':'The dealer could sell the whole arrangement.'},
 ('07','hearings','where_murderer'):{'Hugh, you could sell the arrangement.':'The dealer could sell the arrangement.',"every object you put beside it.":'every object put beside it.'},
 ('15','coming_clean','innocent'):{'Hugh, tell me which purchases need checking.':'I need the dealer to tell me which purchases need checking.'},
 ('28','hearings','evidence_innocent'):{'Tess, how long would you leave it before calling?':'How long do you leave it before calling?'},
 ('28','hearings','evidence_murderer'):{'Tess, how long would you leave it before calling?':'How long do you leave it before calling?'},
 ('28','coming_clean','innocent'):{"Tess, don't call for me.":"Please don't call for me."},
}

def prepare():
    assert not RUN.exists(),'Never overwrite frozen trials.'
    profile=yaml.safe_load((ROOT/'source/testing/active-cast.yaml').read_text(encoding='utf-8'))
    selected=set(profile['active_character_ids']);assert len(selected)==22
    source=ROOT/profile['game_source']
    manifest=json.loads((source/'manifest.json').read_text(encoding='utf-8'))
    for name,want in manifest['sha256'].items():assert gate.sha(source/name)==want
    old=yaml.safe_load((source/'confirmed.yaml').read_text(encoding='utf-8'))
    assert selected==(set(old['active_character_ids'])-{'03','10'})|{'24','27'}
    public=yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))
    known={str(p['id']).zfill(2):p for p in public['characters']}
    bank=yaml.safe_load((source/'all.yaml').read_text(encoding='utf-8'))
    original=copy.deepcopy(bank)
    bank['characters']=[c for c in bank['characters'] if c['id'] in selected]
    edits=[]
    for c in bank['characters']:
        for section in ('hearings','coming_clean'):
            for field,before in c[section].items():
                text=before
                for a,b in DIRECT.get((c['id'],section,field),{}).items():
                    assert a in text,(c['id'],field,a);text=text.replace(a,b)
                for ident,role in ABSENT_ROLES.items():
                    text=re.sub(r'\b'+re.escape(known[ident]['name'].split()[0])+r'\b',role,text)
                text=re.sub(r'(^|[.!?]\s+)([a-z])',lambda m:m[1]+m[2].upper(),text)
                c[section][field]=text
                if text!=before:edits.append({'id':c['id'],'section':section,'field':field,'before':before,'after':text})
                for ident in ABSENT_ROLES:
                    assert not re.search(r'\b'+re.escape(known[ident]['name'].split()[0])+r'\b',text)
    names={known[i]['name'] for i in selected}
    for phase in bank['question_rounds']:
        for group in phase['groups']:group['targets']=[n for n in group['targets'] if n in names]
        phase['groups']=[g for g in phase['groups'] if g['targets']]
        covered=[n for g in phase['groups'] for n in g['targets']]
        assert len(covered)==22 and set(covered)==names
    bank.update(active_character_ids=sorted(selected),authored_route_count=22,unwritten_active_ids=[],status='published_game_new_rsvp_cast_test_only')
    assert {c['id'] for c in bank['characters']}==selected
    # Both reporter and activist attend, so retain their published interview opening.
    assert {'12','27'}<=selected
    RUN.mkdir();snapshot=RUN/'frozen-source';snapshot.mkdir()
    (snapshot/'confirmed.yaml').write_text(yaml.safe_dump(bank,allow_unicode=True,sort_keys=False),encoding='utf-8')
    public['active_character_ids']=sorted(selected)
    (snapshot/'character_copy.yaml').write_text(yaml.safe_dump(public,allow_unicode=True,sort_keys=False),encoding='utf-8')
    shutil.copy2(source/'playable-evidence.yaml',snapshot/'playable-evidence.yaml')
    shutil.copy2(ROOT/'source/testing/active-cast.yaml',snapshot/'active-cast.yaml')
    shutil.copy2(ROOT/'build/final-rsvp-live-check.json',RUN/'live-source-receipt.json')
    receipt=json.loads((RUN/'live-source-receipt.json').read_text(encoding='utf-8'));assert receipt['match']
    gate.write(RUN/'attendance-edits.json',edits)
    evidence=yaml.safe_load((snapshot/'playable-evidence.yaml').read_text(encoding='utf-8'))
    rows={c['id']:c for c in bank['characters']};people={i:p for i,p in known.items() if i in selected}
    visible={'number','title','department','stamp','paragraphs','rows','images'}
    def shown(e):
        obj={k:v for k,v in e.items() if k in visible}
        if e.get('id')=='original_interview':obj['paragraphs']=bank['pre_method_press_interview_opening']
        return json.dumps(obj,ensure_ascii=False,indent=2)
    def release(key):return '\n\n'.join(shown(e) for r in evidence['releases'] if r['key']==key for e in r['exhibits'])
    def speeches(key,killer):
        parts=[];field={'motive':'motive','opportunity':'where','method':'evidence'}[key]
        for group in next(r for r in bank['question_rounds'] if r['key']==key)['groups']:
            parts.append('Question for '+', '.join(group['targets'])+': '+group['question'])
            for name in group['targets']:
                c=next(c for c in rows.values() if c['name']==name)
                parts.append(name+'\n'+c['hearings'][field+('_murderer' if c['id']==killer else '_innocent')])
        return '\n\n'.join(parts)
    cases=['24','27'];secrets.SystemRandom().shuffle(cases);trials=[]
    for number,killer in enumerate(cases,1):
        token=f't{number:03}';folder=RUN/'blind'/token;folder.mkdir(parents=True)
        stages={1:'Exactly one of these22 characters committed the murder alone. Other mentioned staff are not selectable suspects.\n\n'+'\n\n'.join(p['name']+' / '+p['role']+'\n'+p['introduction'] for p in people.values()),2:'\n\n'.join(shown(e) for e in evidence['hunt']),3:release('before_motive'),4:speeches('motive',killer),5:release('before_opportunity'),6:speeches('opportunity',killer),7:release('before_method'),8:speeches('method',killer)}
        for n,text in stages.items():(folder/f'checkpoint_{n:02}.txt').write_text(text+'\n',encoding='utf-8')
        trials.append({'trial':token,'replicate':1,'murderer_id':killer,'murderer':known[killer]['name'],'inputs':{p.name:gate.sha(p) for p in folder.iterdir()}})
    info={'run':'Final changed-RSVP22 round','revision':manifest['revision']+' / RSVP cast updated2026-10-23','production_deploy':json.loads((ROOT/'docs/belle-tament/production-receipt.json').read_text())['deploy_id'],'complete_kit_sha256':receipt['verified_live_zip_sha256'],'stage_labels':gate.STAGES,'roster':[{'id':i,'name':p['name'],'role':p['role']} for i,p in people.items()],'trial_count':2,'replicates_per_culprit':1,'trials':trials,'source_sha256':{p.name:gate.sha(p) for p in snapshot.iterdir()},'protocol':'Two fresh context-free readers, one scenario per newly added role, randomized trial order. Published story, attendance substitutions only. All16 discoveries and eight sequential releases. Locked scores and pre-finale accusations; no target distributions or rerolls. Not an exhaustive audit or human solve-rate estimate.'}
    gate.write(RUN/'private-manifest.json',info)
    instructions=(ROOT/'docs/playtest/2026-10-10-EXHAUSTIVE-RSVP22-SPOILERS/READER_INSTRUCTIONS.md').read_text(encoding='utf-8').replace('2026-10-10-EXHAUSTIVE-RSVP22-SPOILERS',RUN.name).replace('scripts/exhaustive_balance.py','scripts/final_rsvp_round.py')
    (RUN/'READER_INSTRUCTIONS.md').write_text(instructions,encoding='utf-8')
    gate.write(RUN/'cast-verification.json',{'adult_count':22,'removed_ids':['03','10'],'added_ids':['24','27'],'nonplaying_child_excluded':True,'question_targets_exactly_once_per_round':True,'all16_evidence_byte_identical_to_published':gate.sha(snapshot/'playable-evidence.yaml')==gate.sha(source/'playable-evidence.yaml'),'story_edits':'Only offstage-role aliases and removal of direct appeals to absent guests; every edit retained in attendance-edits.json.','all_future_testing_profile':'source/testing/active-cast.yaml','historical_trials':'Preserved unmodified; not current RSVP tests.'})
    print('Frozen two final RSVP22 tests; public assets and production unchanged.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','read','validate','finale','complete']);p.add_argument('--trial');p.add_argument('--stage',type=int);a=p.parse_args()
    if a.action=='prepare':prepare()
    else:gate.RUN=RUN;gate.gate(a.trial,a.action,a.stage)
