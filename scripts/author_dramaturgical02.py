"""Bounded second prose pass; preserve the complete rejected first cohort."""
from pathlib import Path
import yaml,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest/2026-10-26-DRAMATURGICAL-02-SPOILERS'
assert not (ROOT/'docs/playtest/2026-10-26-DRAMATURGICAL-02-BLIND-SPOILERS').exists()
draft=yaml.safe_load((RUN/'six-contrast-revisions.yaml').read_text(encoding='utf-8'))
assert len(draft)==6 and all(len(v)==6 for v in draft.values())
verified=yaml.safe_load((ROOT/'source/connected_release/confirmed.yaml').read_text(encoding='utf-8'))
verified_by={c['id']:c for c in verified['characters']}
restore=['08','11','12','15','23']
ledger=[]
for edition in ['all','confirmed']:
    bank=yaml.safe_load((RUN/'baseline-source'/f'{edition}.yaml').read_text(encoding='utf-8'))
    for c in bank['characters']:
        old=json.loads(json.dumps(c))
        if c['id'] in draft:c['hearings'].update(draft[c['id']])
        if c['id'] in restore:c['hearings']['evidence_murderer']=verified_by[c['id']]['hearings']['evidence_murderer']
        if edition=='confirmed':
            for field,after in c['hearings'].items():
                if after!=old['hearings'][field]:ledger.append({'id':c['id'],'name':c['name'],'field':field,'before':old['hearings'][field],'after':after,'reason':'verified baseline reply restoration' if c['id'] in restore and field=='evidence_murderer' else 'sustained six-contrast action; same facts/stage'})
        assert c['coming_clean']==old['coming_clean']
    bank['status']='unpublished_dramaturgical_candidate02_pending_tests'
    (RUN/'candidate-source'/f'{edition}.yaml').write_text(yaml.safe_dump(bank,sort_keys=False,allow_unicode=True,width=100),encoding='utf-8')
current=yaml.safe_load((RUN/'candidate-source/confirmed.yaml').read_text(encoding='utf-8'))
words=sum(len(s.split()) for c in current['characters'] for s in c['hearings'].values())
assert words<=8040,words
(RUN/'change-ledger.json').write_text(json.dumps({'changes':ledger,'changed_hearing_fields':len(ledger),'original_verified_pre_vote_words':8040,'candidate01_pre_vote_words':7785,'candidate02_pre_vote_words':words,'all_endings_unchanged_from_candidate01':True},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
m=json.loads((RUN/'candidate-source/manifest.json').read_text());m['revision']='dramaturgical-candidate02-2026-10-26';m['release_decision']='Unpublished candidate02; candidate01 failed and is retained. No scores claimed for candidate02.';m['testing']={'status':'pending full fresh22 cohort','prior_scores_do_not_validate_rewrite':True};m['sha256']={n:hashlib.sha256((RUN/'candidate-source'/n).read_bytes()).hexdigest() for n in ['all.yaml','confirmed.yaml','playable-evidence.yaml','voice-story-bible.yaml']};(RUN/'candidate-source/manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'changed_fields_from_candidate01':len(ledger),'pre_vote_words':words,'baseline_guilty_replies_restored':restore}))
