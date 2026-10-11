"""Audit immutable blind trials and produce an offline, spoiler-marked report."""
from exhaustive_balance import RUN, STAGES, sha, write
from datetime import datetime, timezone
import csv, json, statistics

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def mean(v): return round(statistics.mean(v),2) if v else None

def collect():
    manifest=read(RUN/'private-manifest.json'); names=[r['name'] for r in manifest['roster']]
    for name,h in manifest['source_sha256'].items():
        assert sha(RUN/'frozen-source'/name)==h, 'Frozen source changed: '+name
    trials=[]; long=[]
    for item in manifest['trials']:
        folder=RUN/'blind'/item['trial']; trial={k:v for k,v in item.items() if k!='inputs'}
        trial.update(status='pending',stages=[],errors=[])
        try:
            for name,h in item['inputs'].items(): assert sha(folder/name)==h, 'Input changed: '+name
            events=read(folder/'journal.json') if (folder/'journal.json').exists() else []
            prior=''
            for index,event in enumerate(events,1):
                assert event['stage']==index and event['read_utc']>=prior, 'Release ordering'
                assert event['input_sha256']==item['inputs'][f'checkpoint_{index:02}.txt']
                if 'score_sha256' not in event: break
                path=folder/f'result_{index:02}.json'; data=read(path)
                assert sha(path)==event['score_sha256'], 'Score changed after lock'
                assert data['stage']==index and set(data['scores'])==set(names)
                assert all(type(v) is int and 0<=v<=10 for v in data['scores'].values())
                assert event['saved_utc']>=event['read_utc']; prior=event['saved_utc']
                assert data.get('clear_culprit') in [None]+names
                trial['stages'].append(data)
            trial['status']='running' if events else 'pending'
            if (folder/'complete.json').exists():
                assert len(trial['stages'])==8
                complete=read(folder/'complete.json'); lock=read(folder/'accusation-lock.json')
                assert complete['accusation_sha256']==lock['sha256']==sha(folder/'accusation.json')
                assert complete['post_vote_sha256']==sha(folder/'post_vote_feedback.json')
                assert lock['saved_utc']>=prior and complete['completed_utc']>=lock['saved_utc']
                a=read(folder/'accusation.json'); p=read(folder/'post_vote_feedback.json')
                assert a['accused'] in names and type(a['confidence']) is int and 0<=a['confidence']<=10
                assert set(a['ratings'])=={'fair_play','clarity','voice_distinction','arc_variety','naturalness','drama'}
                assert all(type(v) is int and 0<=v<=10 for v in a['ratings'].values())
                assert isinstance(a['issues'],list) and len(a['issues'])<=4
                for issue in a['issues']:
                    assert issue['severity'] in ['major','moderate','minor']
                    assert issue['category'] in ['fairness','clarity','voice','naturalness','drama','pacing','evidence','motive','finale']
                    assert all(n in names for n in issue['characters'])
                    assert issue['detail'] and issue['suggested_fix']
                assert isinstance(p['earned'],bool) and isinstance(p['new_decisive_facts'],list)
                killer=item['murderer']; final=trial['stages'][7]['scores']; e3=trial['stages'][6]['scores'][killer]
                top=max(final.values()); high=[n for n in names if final[n]==top]
                flags=[]
                if a['accused'] not in high and a['confidence']>=8:
                    flags.append('High-confidence accusation differs from the highest final numeric score; inspect the locked record. No scores repaired.')
                if trial['stages'][7]['clear_culprit'] and trial['stages'][7]['clear_culprit'] not in high:
                    flags.append('Final clear-culprit declaration differs from the highest final numeric score.')
                trial.update(status='complete',accusation=a,finale=p,audit_flags=flags,metrics={
                    'correct':a['accused']==killer,
                    'early_clear':any(s['clear_culprit'] is not None for s in trial['stages'][:7]),
                    'early_correct_clear':any(s['clear_culprit']==killer for s in trial['stages'][:7]),
                    'e3_ready':5<=e3<8,'e3_score':e3,
                    'e3_rank':1+sum(v>e3 for v in trial['stages'][6]['scores'].values()),
                    'final_score':final[killer],'final_strong':final[killer]>=9,
                    'unique_top':high==[killer], 'tied_top':killer in high and len(high)>1,
                    'act2_suspects':sum(v>5 for v in trial['stages'][5]['scores'].values()),
                    'final_alternatives':sum(5<=v<=7 for n,v in final.items() if n!=killer),
                    'final_5_6':sum(5<=v<=6 for n,v in final.items() if n!=killer),
                    'late_jump':final[killer]-e3,
                    'final_gap':final[killer]-max(v for n,v in final.items() if n!=killer),
                    'earned':p['earned'],'new_facts':len(p['new_decisive_facts'])})
        except Exception as error:
            trial['status']='invalid'; trial['errors'].append(str(error) or type(error).__name__)
        trials.append(trial)
        for stage in trial['stages']:
            for name,score in stage['scores'].items():long.append([item['trial'],item['replicate'],item['murderer'],name,stage['stage'],STAGES[stage['stage']-1],score,trial['status']])
    cases=[]
    for person in manifest['roster']:
        group=[t for t in trials if t['murderer']==person['name']]; done=[t for t in group if t['status']=='complete']
        case={**person,'trials':[t['trial'] for t in group],'n':len(done)}
        for key in ['correct','early_clear','early_correct_clear','e3_ready','final_strong','unique_top','tied_top','earned']:
            case[key]=sum(t['metrics'][key] for t in done)
        case['midgame_breadth']=sum(t['metrics']['act2_suspects']>=8 for t in done)
        case['ending_breadth']=sum(t['metrics']['final_alternatives']>=3 for t in done)
        for key in ['e3_score','e3_rank','final_score','act2_suspects','final_alternatives','late_jump','final_gap']:
            values=[t['metrics'][key] for t in done];case[key]={'mean':mean(values),'min':min(values) if values else None,'max':max(values) if values else None}
        case['progress']=[mean([t['stages'][s]['scores'][person['name']] for t in done]) for s in range(8)]
        case['ratings']={k:mean([t['accusation']['ratings'][k] for t in done]) for k in ['fair_play','clarity','voice_distinction','arc_variety','naturalness','drama']}
        case['flagged']=sum(bool(t['audit_flags']) for t in done)
        consistent=[t for t in done if not t['audit_flags']]
        case['sensitivity_without_flagged']={
            'n':len(consistent),
            'final_strength':sum(t['metrics']['final_strong'] for t in consistent),
            'ending_breadth':sum(t['metrics']['final_alternatives']>=3 for t in consistent),
            'culprit_progress':[mean([t['stages'][s]['scores'][person['name']] for t in consistent]) for s in range(8)]}
        case['wrong']=[{'trial':t['trial'],'accused':t['accusation']['accused']} for t in done if not t['metrics']['correct']]
        cases.append(case)
    result={'generated_utc':datetime.now(timezone.utc).isoformat(),'revision':manifest['revision'],'deploy':manifest['production_deploy'],'kit_sha256':manifest['complete_kit_sha256'],'stages':STAGES,'roster':manifest['roster'],'trials':trials,'cases':cases,'completed':sum(t['status']=='complete' for t in trials),'invalid':sum(t['status']=='invalid' for t in trials),'total':110}
    issue_groups={}
    for t in trials:
        if t['status']!='complete':continue
        for issue in t['accusation']['issues']:
            category=issue['category'];group=issue_groups.setdefault(category,{'category':category,'trials':set(),'major':set(),'examples':[]})
            group['trials'].add(t['trial'])
            if issue['severity']=='major':group['major'].add(t['trial'])
            group['examples'].append({'trial':t['trial'],'murderer':t['murderer'],**issue})
    result['issue_summary']=[{**g,'trials':sorted(g['trials']),'major':sorted(g['major'])} for g in issue_groups.values()]
    write(RUN/'aggregate.json',result)
    with (RUN/'scores.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f);writer.writerow(['trial','replicate','selected_murderer','suspect','stage','release','suspicion','audit_status']);writer.writerows(long)
    with (RUN/'case-summary.csv').open('w',encoding='utf-8-sig',newline='') as f:
        fields=['name','n','correct','early_clear','e3_ready','final_strong','unique_top','tied_top','midgame_breadth','ending_breadth','earned']
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(cases)
    return result

def render(data):
    template=(Path(__file__).with_name('exhaustive_dashboard.html')).read_text(encoding='utf-8')
    (RUN/'dashboard.html').write_text(template.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')
    completed=[t for t in data['trials'] if t['status']=='complete']
    correct=sum(t['metrics']['correct'] for t in completed)
    lines=['# Published RSVP22 blind audit — SPOILERS','',f"Completed: **{data['completed']}/110**. Invalid: **{data['invalid']}**. Correct accusations: **{correct}/{len(completed)}**.",'','Five fresh context-free AI readers per selected murderer; eight sequential immutable score releases; accusation locked before finale. Scores are suspicion judgments, not probabilities or human solve rates. Missing trials are not counted as successes. No game rewrites or rerolls.','',f"Published revision: `{data['revision']}`. Verified deploy: `{data['deploy']}`.",'','Open `dashboard.html` for the scenario overview, eight-stage heatmaps, accusation confusion matrix, and all reviews. `scores.csv` contains every score; `case-summary.csv` contains exact counts. Raw assessments and lock hashes are in `blind/`.','', '| Murderer scenario | Completed | Correct | Early clear | E3 5–7 | Final ≥9 | 8+ Act II suspects | 3+ final alternatives |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for c in data['cases']:lines.append('| '+c['name']+' | '+str(c['n'])+'/5 | '+' | '.join(str(c[k])+'/'+str(c['n']) for k in ['correct','early_clear','e3_ready','final_strong','midgame_breadth','ending_breadth'])+' |')
    (RUN/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'complete':data['completed'],'invalid':data['invalid'],'correct':correct,'dashboard':str(RUN/'dashboard.html')}))

if __name__=='__main__':
    from pathlib import Path
    render(collect())
