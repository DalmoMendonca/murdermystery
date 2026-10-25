"""Compile, inspect and freeze an isolated story revision from the published baseline."""
from pathlib import Path
import argparse, copy, hashlib, json, shutil, yaml
import exhaustive_balance as gate

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT/'docs/playtest/2026-10-11-STRUCTURAL-STORY-SPOILERS'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p, obj): p.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False),encoding='utf-8')

def compile_candidate():
    dest=RUN/'candidate-source';assert not dest.exists();dest.mkdir()
    method=yaml.safe_load((RUN/'method-rewrite.yaml').read_text(encoding='utf-8'))['characters']
    opportunity=yaml.safe_load((RUN/'opportunity-rewrite.yaml').read_text(encoding='utf-8'))['characters']
    baseline=ROOT/'source/connected_release'
    for edition in ['all','confirmed']:
        bank=yaml.safe_load((baseline/(edition+'.yaml')).read_text(encoding='utf-8'))
        for c in bank['characters']:
            ident=str(c['id']).zfill(2)
            for branch in ['innocent','murderer']:
                c['hearings']['evidence_'+branch]=method[ident][branch]
                if ident in opportunity:c['hearings']['where_'+branch]=opportunity[ident][branch]
        bank['status']='unpublished_structural_story_revision02'
        dump(dest/(edition+'.yaml'),bank)
    evidence=yaml.safe_load((baseline/'playable-evidence.yaml').read_text(encoding='utf-8'))
    originals=copy.deepcopy(evidence)
    release=next(r for r in evidence['releases'] if r['key']=='before_method')
    byid={e['id']:e for e in release['exhibits']}
    deferred=[]
    removals={'visitor_route':['School places','Budget consequence'],
              'collector_working_folder':['Advisory account','Dealer refund demand','Technology account'],
              'preview_image_custody':['Earlier gallery retouch','Corrected archive','Editorial client']}
    for ident,labels in removals.items():
        e=byid[ident];deferred += [{'exhibit':ident,'row':row} for row in e['rows'] if row[0] in labels]
        e['rows']=[row for row in e['rows'] if row[0] not in labels]
    replacements={
        ('collector_working_folder','Family valuation'):'Damaged benchmark used for intact family object',
        ('press_source_folder','Bead recommendation'):'Supplier quote includes commission',
        ('press_source_folder','Sponsored podcast'):'Original favorable post and advertising agreement retained',
        ('press_source_folder','Property story'):'Old deed and later tenant-trust settlement retained together',
        ('work_and_settlement','Textile commission'):'Pattern rights retained by maker',
        ('work_and_settlement','Sculpture contract'):'Cold-cast resin with metal powder / label revised',
        ('work_and_settlement','Handling report'):'Frame corner damaged in delivery / corrected report',
        ('work_and_settlement','Production account'):'Unauthorized crew order / designer responsible for balance'}
    for (ident,label),value in replacements.items():
        row=next(row for row in byid[ident]['rows'] if row[0]==label)
        deferred.append({'exhibit':ident,'before':row.copy(),'after':[label,value]});row[1]=value
    byid['work_and_settlement']['title']='The delivered work'
    byid['work_and_settlement']['department']='COMMISSIONS / DELIVERY RECORDS'
    byid['press_source_folder']['title']='The press desk files'
    byid['press_source_folder']['department']='PRESS / RETAINED SOURCES'
    byid['production_originals']['paragraphs']=[
        'Studio master received before gala: an empty jacket falls from a chair. Original picture and sound retained together.',
        'The untrimmed recording begins "Jacket take," followed by the chair scrape and clatter as the empty jacket hits the floor. The podcast\'s complete export includes that continuous sequence; its teaser begins after the spoken cue.']
    # Crime-bearing source, delivery, camera, authority and custody records retain their observations.
    original_release=next(r for r in originals['releases'] if r['key']=='before_method')
    old_byid={e['id']:e for e in original_release['exhibits']}
    for ident in ['original_source','actual_service','original_interview','camera_work','governing_papers','collection_working_proof']:
        assert byid[ident]==old_byid[ident],ident
    for ident in ['production_originals','collector_working_folder','preview_image_custody','work_and_settlement']:
        assert byid[ident].get('images')==old_byid[ident].get('images'),ident
    assert evidence['hunt']==originals['hunt']
    for current,prior in zip(evidence['releases'],originals['releases']):
        assert current.get('route_checks')==prior.get('route_checks')
    evidence['status']='unpublished_structural_story_revision02'
    dump(dest/'playable-evidence.yaml',evidence)
    dump(RUN/'deferred-resolutions.yaml',{'scope':'Nondecisive resolutions remain in Coming Clean, not final evidence. No new decisive finale fact.','changes':deferred})
    voice=yaml.safe_load((baseline/'voice-story-bible.yaml').read_text(encoding='utf-8'))
    for c in voice['characters']:c['method_delivery']=method[str(c['id']).zfill(2)]['delivery']
    dump(dest/'voice-story-bible.yaml',voice)
    manifest={'revision':'structural-story-revision02-2026-10-11','baseline_commit':'f8b462b',
              'status':'UNPUBLISHED','sha256':{p.name:sha(p) for p in dest.iterdir()},
              'limitations':'Candidate; preserve sent public assets. Test both attendance editions before promotion.'}
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    from validate_playable_evidence import validate
    validate(dest/'playable-evidence.yaml')
    print('Compiled all30 and confirmed22; protected proof records and source observations unchanged.')

def freeze(killers=('18','05','11')):
    source=RUN/'candidate-source'
    revision=json.loads((source/'manifest.json').read_text(encoding='utf-8'))['revision']
    public=yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))
    baseline=json.loads((ROOT/'docs/playtest/2026-10-10-EXHAUSTIVE-RSVP22-SPOILERS/private-manifest.json').read_text(encoding='utf-8'))
    visible={'number','title','department','stamp','paragraphs','rows','images'}
    for edition,label in [('22','confirmed'),('30','all')]:
        edition_killers=killers[edition] if isinstance(killers,dict) else killers
        dest=RUN/('cast'+edition);assert not dest.exists();(dest/'frozen-source').mkdir(parents=True)
        bank=yaml.safe_load((source/(label+'.yaml')).read_text(encoding='utf-8'))
        evidence=yaml.safe_load((source/'playable-evidence.yaml').read_text(encoding='utf-8'))
        rows={str(c['id']).zfill(2):c for c in bank['characters']}
        people={str(c['id']).zfill(2):c for c in public['characters'] if str(c['id']).zfill(2) in rows}
        assert len(rows)==len(people)==int(edition)
        shutil.copy2(source/(label+'.yaml'),dest/'frozen-source/confirmed.yaml')
        shutil.copy2(source/'playable-evidence.yaml',dest/'frozen-source/playable-evidence.yaml')
        shutil.copy2(ROOT/'source/character_copy.yaml',dest/'frozen-source/character_copy.yaml')
        def shown(e):
            item={k:v for k,v in e.items() if k in visible}
            if e.get('id')=='original_interview':item['paragraphs']=bank['pre_method_press_interview_opening']
            return json.dumps(item,ensure_ascii=False,indent=2)
        def release(key):return '\n\n'.join(shown(e) for r in evidence['releases'] if r['key']==key for e in r['exhibits'])
        def speeches(key,killer):
            blocks=[];field={'motive':'motive','opportunity':'where','method':'evidence'}[key]
            for g in next(r for r in bank['question_rounds'] if r['key']==key)['groups']:
                blocks.append('Question for '+', '.join(g['targets'])+': '+g['question'])
                for name in g['targets']:
                    c=next(c for c in rows.values() if c['name']==name);branch='murderer' if str(c['id']).zfill(2)==killer else 'innocent'
                    blocks.append(name+'\n'+c['hearings'][field+'_'+branch])
            return '\n\n'.join(blocks)
        trials=[]
        # Fixed critical cases, not result-based selection: late-recognition, materials, camera.
        for number,killer in enumerate(edition_killers,1):
            token=f't{number:03}';folder=dest/'blind'/token;folder.mkdir(parents=True)
            stages={1:f'Exactly one of these {edition} characters committed the murder alone. Other mentioned staff are not selectable suspects.\n\n'+'\n\n'.join(p['name']+' / '+p['role']+'\n'+p['introduction'] for p in people.values()),
                    2:'\n\n'.join(shown(e) for e in evidence['hunt']),3:release('before_motive'),4:speeches('motive',killer),5:release('before_opportunity'),6:speeches('opportunity',killer),7:release('before_method'),8:speeches('method',killer)}
            for n,text in stages.items():(folder/f'checkpoint_{n:02}.txt').write_text(text+'\n',encoding='utf-8')
            trials.append({'trial':token,'replicate':1,'murderer_id':killer,'murderer':people[killer]['name'],'inputs':{p.name:sha(p) for p in folder.iterdir()}})
        info={**baseline,'run':RUN.name+' / cast'+edition,'production_deploy':'UNPUBLISHED','revision':revision,'trial_count':len(edition_killers),'replicates_per_culprit':1,'trials':trials,
              'roster':[{'id':i,'name':p['name'],'role':p['role']} for i,p in people.items()],
              'source_sha256':{p.name:sha(p) for p in (dest/'frozen-source').iterdir()},
              'protocol':'Fixed critical scenarios per attendance edition; fresh original readers; locked sequential scores and pre-finale accusation. No rerolls. Descriptive diagnostics, not human solve rates.'}
        (dest/'private-manifest.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        instructions=(ROOT/'docs/playtest/2026-10-10-EXHAUSTIVE-RSVP22-SPOILERS/READER_INSTRUCTIONS.md').read_text(encoding='utf-8')
        instructions=instructions.replace('22 named','%s named'%edition).replace('22 names','%s names'%edition).replace('all 22','all '+edition).replace('2026-10-10-EXHAUSTIVE-RSVP22-SPOILERS',RUN.name+'/cast'+edition).replace('scripts/exhaustive_balance.py',f'scripts/structural_story_pass.py --edition {edition}')
        (dest/'READER_INSTRUCTIONS.md').write_text(instructions,encoding='utf-8')
    print('Frozen fixed blind diagnostics. No published game edit.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['compile','freeze','read','validate','finale','complete']);parser.add_argument('--edition',choices=['22','30']);parser.add_argument('--trial');parser.add_argument('--stage',type=int);args=parser.parse_args()
    if args.action=='compile':compile_candidate()
    elif args.action=='freeze':freeze()
    else:
        assert args.edition;gate.RUN=RUN/('cast'+args.edition);gate.gate(args.trial,args.action,args.stage)
