"""Freeze and gate the final current-22 artifact-candidate blind suite."""
from pathlib import Path
import argparse,json,shutil,secrets,hashlib
import fitz,yaml
import exhaustive_balance as audit

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest/2026-10-25-FINAL-ARTIFACT-BLIND22-SPOILERS'
OUT=Path(r'C:\Users\dalmo\Documents\Codex\2026-10-24\what\outputs\act3-artifact-redesign')

def prepare():
    assert not RUN.exists(),'Never overwrite a frozen suite.'
    bank=yaml.safe_load((ROOT/'source/connected_release/confirmed.yaml').read_text(encoding='utf-8'))
    profile=yaml.safe_load((ROOT/'source/testing/active-cast.yaml').read_text(encoding='utf-8'))
    active={str(i).zfill(2) for i in profile['active_character_ids']}
    rows={c['id']:c for c in bank['characters']}
    assert set(rows)==active and len(rows)==22
    manifest=json.loads((ROOT/'source/connected_release/manifest.json').read_text())
    assert all(audit.sha(ROOT/'source/connected_release'/n)==v for n,v in manifest['sha256'].items())
    public=yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))
    people={str(p['id']).zfill(2):p for p in public['characters'] if str(p['id']).zfill(2) in rows}
    RUN.mkdir();snapshot=RUN/'frozen-source';snapshot.mkdir()
    for name in ['confirmed.yaml','all.yaml','playable-evidence.yaml','manifest.json']:
        shutil.copy2(ROOT/'source/connected_release'/name,snapshot/name)
    shutil.copy2(ROOT/'source/character_copy.yaml',snapshot/'character_copy.yaml')
    shutil.copy2(ROOT/'source/testing/active-cast.yaml',snapshot/'active-cast.yaml')
    shutil.copy2(ROOT/'docs/playtest/2026-10-25-ACT3-ARTIFACTS-DRAFT-SPOILERS/artifact-copy.json',snapshot/'artifact-copy.json')
    basekit=Path((ROOT/'docs/playtest/2026-10-25-ACT3-TWO-RECORD-SHEETS-SPOILERS/candidate-kit-path.txt').read_text().strip())
    shutil.copy2(OUT/'ACT_III_Evidence.pdf',snapshot/'ACT_III_Evidence.pdf')
    shutil.copy2(OUT/'03_Staged_Evidence.pdf',snapshot/'03_Staged_Evidence.pdf')
    shutil.copy2(basekit/'OPEN_FREELY/04_Scavenger_Discoveries.pdf',snapshot/'04_Scavenger_Discoveries.pdf')
    frozen=RUN/'inputs';frozen.mkdir();images=RUN/'visual-inputs';images.mkdir()
    def pages(path,indices,stage):
        parts=[];folder=images/f'stage_{stage:02}';folder.mkdir(exist_ok=True)
        with fitz.open(path) as doc:
            for n,i in enumerate(indices,1):
                page=doc[i];parts.append(f'--- SHEET {n} ---\n'+page.get_text())
                page.get_pixmap(matrix=fitz.Matrix(1.25,1.25)).save(folder/f'sheet_{n:02}.png')
        return '\n\n'.join(parts)
    evidence={2:pages(snapshot/'04_Scavenger_Discoveries.pdf',range(16),2),
              3:pages(snapshot/'03_Staged_Evidence.pdf',[0],3),
              5:pages(snapshot/'03_Staged_Evidence.pdf',[1,2],5),
              7:pages(snapshot/'ACT_III_Evidence.pdf',range(6),7)}
    intro='Exactly one of these 22 characters committed the murder alone. Other mentioned staff are not selectable suspects.\n\n'+bank.get('player_briefing','')+'\n\n'+'\n\n'.join(p['name']+' / '+p['role']+'\n'+p['introduction'] for p in people.values())
    def speeches(key,killer):
        parts=[];field={'motive':'motive','opportunity':'where','method':'evidence'}[key]
        for group in next(r for r in bank['question_rounds'] if r['key']==key)['groups']:
            parts.append('Question for '+', '.join(group['targets'])+': '+group['question'])
            for name in group['targets']:
                c=next(c for c in rows.values() if c['name']==name)
                parts.append(name+'\n'+c['hearings'][field+('_murderer' if c['id']==killer else '_innocent')])
        return '\n\n'.join(parts)
    cases=list(rows);secrets.SystemRandom().shuffle(cases);trials=[]
    for number,killer in enumerate(cases,1):
        token=f't{number:03}';folder=frozen/token;folder.mkdir();(RUN/'blind'/token).mkdir(parents=True)
        stages={1:intro,**evidence,4:speeches('motive',killer),6:speeches('opportunity',killer),8:speeches('method',killer)}
        for stage,content in sorted(stages.items()):(folder/f'checkpoint_{stage:02}.txt').write_text(content+'\n',encoding='utf-8')
        trials.append({'trial':token,'murderer_id':killer,'murderer':people[killer]['name'],'inputs':{p.name:audit.sha(p) for p in folder.iterdir()}})
    info={'run':'Final artifact candidate, current22, one fresh reader per culprit','stage_labels':audit.STAGES,
          'trial_count':22,'replicates_per_culprit':1,'roster':[{'id':i,'name':p['name'],'role':p['role']} for i,p in people.items()],
          'trials':trials,'source_sha256':{p.name:audit.sha(p) for p in snapshot.iterdir()},
          'protocol':'22 fresh context-free player readers; eight gated stages, immutable all-guest suspicion scores, locked accusations before finale. Actual printed artifacts and rendered images, selected spoken branches only. No prior results, murderer assignment or desired score distributions exposed. No rerolls. AI reading checks, not a human party simulation. No game edits during testing.'}
    audit.write(RUN/'private-manifest.json',info)
    audit.write(RUN/'progress.json',{'completed':0,'total':22,'status':'frozen_unstarted'})
    instructions=(ROOT/'docs/playtest/2026-10-24-CONCEALED-STAKES-SPOILERS/READER_INSTRUCTIONS.md').read_text(encoding='utf-8')
    instructions=instructions.replace('2026-10-24-CONCEALED-STAKES-SPOILERS',RUN.name).replace('scripts/concealed_stakes_balance.py','scripts/final_artifact_blind.py')
    instructions += '\n\nVISUAL REVIEW: read outputs list images available for each evidence release. During stage 7, inspect ALL SIX page images before scoring; score only after both the text and visuals. Earlier evidence images may be inspected whenever needed, only after their release. Do not list future-image directories or inputs. Layout, reading burden and source authenticity are part of your frank feedback; no specific positive or negative verdict is requested.\n'
    (RUN/'READER_INSTRUCTIONS.md').write_text(instructions,encoding='utf-8')
    (RUN/'PROTOCOL.md').write_text('# Final artifact candidate blind audit / SPOILERS\n\n'+info['protocol']+'\n\nEight checkpoints match the historical protocol, with actual current PDF text and six Method-page visuals. All 22 current RSVP roles appear once as the selected culprit. Suspicion scores are descriptive; no target distribution is given to readers. Source files and selected speeches are frozen before dispatch.\n',encoding='utf-8')
    print(json.dumps({'trial_count':22,'stages':8,'act_iii_pages':6,'suspects':list(p['name'] for p in people.values()),'frozen':str(RUN)}))

def gate(trial,action,stage):
    assert trial and trial.startswith('t') and trial[1:].isdigit()
    folder=RUN/'blind'/trial
    if action=='read':
        journal=folder/'journal.json'
        events=json.loads(journal.read_text()) if journal.exists() else []
        assert stage==len(events)+1 and 1<=stage<=8,'Release must be next in sequence.'
        assert all('score_sha256' in e and audit.sha(folder/f"result_{e['stage']:02}.json")==e['score_sha256'] for e in events),'Prior scores must be validated and unchanged.'
        # Make only the next release available in the player's working folder.
        src=RUN/'inputs'/trial/f'checkpoint_{stage:02}.txt';dest=folder/src.name
        if not dest.exists():shutil.copy2(src,dest)
    audit.RUN=RUN
    audit.gate(trial,action,stage)
    if action=='read' and (RUN/'visual-inputs'/f'stage_{stage:02}').exists():
        dest=folder/'images'/f'stage_{stage:02}';shutil.copytree(RUN/'visual-inputs'/f'stage_{stage:02}',dest,dirs_exist_ok=True)
        print('\nRELEASED PAGE IMAGES (only these and earlier released pages may be inspected):')
        print('\n'.join(str(p) for p in sorted(dest.glob('*.png'))))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','read','validate','finale','complete']);p.add_argument('--trial');p.add_argument('--stage',type=int);a=p.parse_args()
    prepare() if a.action=='prepare' else gate(a.trial,a.action,a.stage)
