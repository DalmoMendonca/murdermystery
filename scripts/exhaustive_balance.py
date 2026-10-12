"""Freeze and audit the 110-reader published RSVP matrix. Never edits game sources."""
from pathlib import Path
import argparse,hashlib,json,math,secrets,shutil,urllib.request,yaml
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest/2026-10-10-EXHAUSTIVE-RSVP22-SPOILERS'
STAGES=['Introductions','16 hunt clues','Evidence 1','Act I: Motive','Evidence 2','Act II: Opportunity','Evidence 3','Act III: Method']
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def freeze():
    assert not RUN.exists(),'Never overwrite frozen trials.'
    published=json.loads((ROOT/'docs/belle-tament/production-receipt.json').read_text())
    expected=published['downloads']['The_Last_Acquisition_Complete_Kit.zip']['sha256']
    live=hashlib.sha256()
    with urllib.request.urlopen('https://murder.dalmo.ai/downloads/The_Last_Acquisition_Complete_Kit.zip?audit=exhaustive22',timeout=120) as response:
        while block:=response.read(1024*1024):live.update(block)
    assert live.hexdigest()==expected,'Published ZIP differs from tested source receipt.'
    pinned=ROOT/'source/connected_release';manifest=json.loads((pinned/'manifest.json').read_text())
    assert all(sha(pinned/n)==v for n,v in manifest['sha256'].items())
    bank=yaml.safe_load((pinned/'confirmed.yaml').read_text(encoding='utf-8'))
    public=yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))
    rows={str(r['id']).zfill(2):r for r in bank['characters']}
    people={str(r['id']).zfill(2):r for r in public['characters'] if str(r['id']).zfill(2) in rows}
    assert len(rows)==len(people)==22
    assert set(rows)=={str(i).zfill(2) for i in public['active_character_ids']}
    roster=json.loads((ROOT/'build/event-roster.json').read_text())
    assert roster['count']==22 and len(roster['characters'])==22
    evidence=yaml.safe_load((pinned/'playable-evidence.yaml').read_text(encoding='utf-8'))
    RUN.mkdir(parents=True);snapshot=RUN/'frozen-source';snapshot.mkdir()
    for name in ['confirmed.yaml','playable-evidence.yaml','manifest.json']:shutil.copy2(pinned/name,snapshot/name)
    shutil.copy2(ROOT/'source/character_copy.yaml',snapshot/'character_copy.yaml')
    visible={'number','title','department','stamp','paragraphs','rows','images'}
    def shown(exhibit):
        item={k:v for k,v in exhibit.items() if k in visible}
        if exhibit.get('id')=='original_interview':
            if not bank['pre_method_press_interview_opening']:return None
            item['paragraphs']=bank['pre_method_press_interview_opening']
        return json.dumps(item,ensure_ascii=False,indent=2)
    def release(key):return '\n\n'.join(s for r in evidence['releases'] if r['key']==key for e in r['exhibits'] if (s:=shown(e)) is not None)
    def speeches(key,killer):
        blocks=[]
        for group in next(r for r in bank['question_rounds'] if r['key']==key)['groups']:
            blocks.append('Question for '+', '.join(group['targets'])+': '+group['question'])
            for name in group['targets']:
                ident=next(i for i,p in people.items() if p['name']==name)
                branch='murderer' if ident==killer else 'innocent'
                field={'motive':'motive','opportunity':'where','method':'evidence'}[key]+'_'+branch
                blocks.append(name+'\n'+rows[ident]['hearings'][field])
        return '\n\n'.join(blocks)
    ids=list(rows);trials=[]
    for replicate in range(1,6):
        order=ids.copy();secrets.SystemRandom().shuffle(order)
        for ident in order:
            token='t'+str(len(trials)+1).zfill(3);folder=RUN/'blind'/token;folder.mkdir(parents=True)
            stages={1:'Exactly one of these 22 characters committed the murder alone. Other mentioned staff are not selectable suspects.\n\n'+'\n\n'.join(p['name']+' / '+p['role']+'\n'+p['introduction'] for p in people.values()),2:'\n\n'.join(shown(e) for e in evidence['hunt']),3:release('before_motive'),4:speeches('motive',ident),5:release('before_opportunity'),6:speeches('opportunity',ident),7:release('before_method'),8:speeches('method',ident)}
            for number,text in stages.items():(folder/f'checkpoint_{number:02}.txt').write_text(text+'\n',encoding='utf-8')
            trials.append({'trial':token,'replicate':replicate,'murderer_id':ident,'murderer':people[ident]['name'],'inputs':{f'checkpoint_{n:02}.txt':sha(folder/f'checkpoint_{n:02}.txt') for n in stages}})
    info={'run':'Published RSVP22 exhaustive balance matrix','production_deploy':published['deploy_id'],'complete_kit_sha256':expected,'revision':manifest['revision'],'created_utc':datetime.now(timezone.utc).isoformat(),'stage_labels':STAGES,'roster':[{'id':i,'name':p['name'],'role':p['role']} for i,p in people.items()],'trial_count':110,'replicates_per_culprit':5,'trials':trials,'source_sha256':{p.name:sha(p) for p in snapshot.iterdir()},'protocol':'110 fresh fork-none AI readers, same instructions; eight stage scores immutable before next release; accusation before finale; no target ratings; no rerolls. All16 hunt exhibits shown. Transcribed actual visible text/retained observations, not human party performance.','prespecified_targets':{'accuracy':'Final accusation matches selected culprit','timing':'No clear culprit declared before stage8','e3_readiness':'Culprit E3 score at least5; below8 preferred','final_strength':'Culprit final score at least9 and uniquely highest or tied highest reported separately','midgame_breadth':'At least8/22 scores strictly above5 after ActII','ending_breadth':'At least3 innocent scores from5 through7; 5-6 subset reported separately'},'finale_protocol':'After accusation, three highest-scored suspects read their branch; selected murderer added if not among three. Single-reader top3 is a review proxy, not actual group votes.'}
    write(RUN/'private-manifest.json',info)
    (RUN/'PROTOCOL.md').write_text('# Published RSVP22 exhaustive audit / SPOILERS\n\n'+info['protocol']+'\n\nPredetermined matrix: every one of 22 culprits, five independent readers, no result-based reselection or rewrites. Descriptive small-sample summaries; not human solve-rate estimates. Preserve failed and invalid attempts. Readers never receive this protocol or threshold targets.\n',encoding='utf-8')
    print('Frozen 110 trials; live ZIP and pinned source hashes verified. Stage lengths:',{n:len(t) for n,t in stages.items()})

def gate(trial,action,stage=None):
    assert trial.startswith('t') and trial[1:].isdigit()
    folder=RUN/'blind'/trial;info=json.loads((RUN/'private-manifest.json').read_text(encoding='utf-8'))
    selected=next(t for t in info['trials'] if t['trial']==trial);names=[p['name'] for p in info['roster']]
    journal=folder/'journal.json';events=json.loads(journal.read_text()) if journal.exists() else []
    for event in events:
        if 'score_sha256' in event:assert sha(folder/f"result_{event['stage']:02}.json")==event['score_sha256']
    if action=='read':
        assert stage==len(events)+1 and 1<=stage<=8
        assert all('score_sha256' in e for e in events),'Validate previous assessment first.'
        path=folder/f'checkpoint_{stage:02}.txt';assert sha(path)==selected['inputs'][path.name]
        events.append({'stage':stage,'input_sha256':sha(path),'read_utc':datetime.now(timezone.utc).isoformat()});write(journal,events)
        print(path.read_text(encoding='utf-8'))
    elif action=='validate':
        assert events[-1]['stage']==stage and 'score_sha256' not in events[-1]
        path=folder/f'result_{stage:02}.json';data=json.loads(path.read_text(encoding='utf-8-sig'))
        assert data['stage']==stage and set(data['scores'])==set(names)
        assert all(type(v) is int and 0<=v<=10 for v in data['scores'].values())
        assert data.get('reasoning') and data.get('clear_culprit') in [None]+names
        events[-1].update(score_sha256=sha(path),saved_utc=datetime.now(timezone.utc).isoformat());write(journal,events)
        print(f'Validated {trial} stage {stage}.')
    elif action=='finale':
        assert len(events)==8 and all('score_sha256' in e for e in events)
        locked=folder/'accusation.json';d=json.loads(locked.read_text(encoding='utf-8-sig'))
        assert d['accused'] in names and d.get('reasoning') and d.get('feedback') and d.get('ratings')
        lock=folder/'accusation-lock.json';assert not lock.exists(),'Accusation already locked.'
        write(lock,{'sha256':sha(locked),'saved_utc':datetime.now(timezone.utc).isoformat()})
        scores=json.loads((folder/'result_08.json').read_text(encoding='utf-8-sig'))['scores']
        top=sorted(names,key=lambda n:(-scores[n],names.index(n)))[:3]
        if selected['murderer'] not in top:top.append(selected['murderer'])
        bank=yaml.safe_load((RUN/'frozen-source/confirmed.yaml').read_text(encoding='utf-8'))
        byname={r['name']:r for r in bank['characters']}
        print('POST-VOTE FINALE / Ratings and accusation are locked. Top three suspects, then murderer if necessary.\n\n'+'\n\n'.join(n+'\n'+byname[n]['coming_clean']['murderer' if n==selected['murderer'] else 'innocent'] for n in top))
    elif action=='complete':
        lock=json.loads((folder/'accusation-lock.json').read_text());assert lock['sha256']==sha(folder/'accusation.json')
        post=json.loads((folder/'post_vote_feedback.json').read_text(encoding='utf-8-sig'));assert post.get('feedback')
        write(folder/'complete.json',{'completed_utc':datetime.now(timezone.utc).isoformat(),'accusation_sha256':sha(folder/'accusation.json'),'post_vote_sha256':sha(folder/'post_vote_feedback.json')})
        print(f'{trial} complete; eight score files and accusation remain unchanged.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['freeze','read','validate','finale','complete']);p.add_argument('--trial');p.add_argument('--stage',type=int);a=p.parse_args()
    freeze() if a.action=='freeze' else gate(a.trial,a.action,a.stage)
