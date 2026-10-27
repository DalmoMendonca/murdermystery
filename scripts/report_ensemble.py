"""Verify locked final blind trials and export complete, inspectable results."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,statistics
from datetime import datetime,timezone
import final_artifact_blind as test

ROOT=test.ROOT;RUN=ROOT/'docs/playtest/2026-10-27-ENSEMBLE-BLIND-SPOILERS'
OUT=Path(r'C:\Users\dalmo\Documents\Codex\2026-10-24\what\outputs\ensemble-test-report')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))

def main():
 info=read(RUN/'private-manifest.json');names=[p['name'] for p in info['roster']];stages=info['stage_labels']
 assert len(info['trials'])==22 and len({t['murderer_id'] for t in info['trials']})==22
 for name,want in info['source_sha256'].items():assert sha(RUN/'frozen-source'/name)==want,('Frozen source changed',name)
 trials=[];flat=[];summary=[];allissues=[]
 for t in sorted(info['trials'],key=lambda t:t['murderer_id']):
  f=ROOT/t['assessment_source'] if t.get('assessment_source') else RUN/'blind'/t['trial'];assert (f/'complete.json').exists(),('Incomplete trial',t['trial'])
  journal=read(f/'journal.json');assert len(journal)==8
  checkpoints=[]
  for n,event in enumerate(journal,1):
   result=read(f/f'result_{n:02}.json');assert event['stage']==result['stage']==n
   assert event['input_sha256']==t['inputs'][f'checkpoint_{n:02}.txt']==sha(f/f'checkpoint_{n:02}.txt')
   assert event['score_sha256']==sha(f/f'result_{n:02}.json')
   assert set(result['scores'])==set(names) and all(type(v) is int and 0<=v<=10 for v in result['scores'].values())
   checkpoints.append(result)
   for name in names:flat.append({'scenario':t['trial'],'selected_murderer':t['murderer'],'stage':n,'stage_name':stages[n-1],'guest':name,'suspicion':result['scores'][name],'clear_culprit':result['clear_culprit'] or '','assessment_source':t.get('assessment_source','')})
  accusation=read(f/'accusation.json');assert sha(f/'accusation.json')==read(f/'accusation-lock.json')['sha256']
  assert accusation['accused'] in names and type(accusation['confidence']) is int and 0<=accusation['confidence']<=10
  assert set(accusation['ratings'])=={'fair_play','clarity','voice_distinction','arc_variety','naturalness','drama'}
  assert all(type(v) is int and 0<=v<=10 for v in accusation['ratings'].values())
  post=read(f/'post_vote_feedback.json');complete=read(f/'complete.json')
  assert type(post['earned']) is bool and isinstance(post['new_decisive_facts'],list)
  assert complete['post_vote_sha256']==sha(f/'post_vote_feedback.json') and complete['accusation_sha256']==sha(f/'accusation.json')
  final=checkpoints[-1]['scores'];killer=t['murderer'];innocents=[n for n in names if n!=killer]
  top=sorted(names,key=lambda n:(-final[n],n))[:3]
  expected_order=sorted(n for n in top if n!=killer)+[killer]
  order=read(f/'finale-order.json')
  assert order=={'top_three':top,'read_order':expected_order,'escaped_justice':killer not in top},('Finale order mismatch',t['trial'])
  for phase in [2,3,5,7]:
   originals=sorted((RUN/'visual-inputs'/f'stage_{phase:02}').glob('*.png'))
   assert originals
   for original in originals:
    released=f/'images'/f'stage_{phase:02}'/original.name
    assert released.exists() and sha(released)==sha(original),('Released visual differs',t['trial'],phase,original.name)
  clear=[i+1 for i,r in enumerate(checkpoints) if r['clear_culprit'] is not None]
  true_clear=[i+1 for i,r in enumerate(checkpoints) if r['clear_culprit']==killer]
  first=clear[0] if clear else None
  row={'scenario':t['trial'],'selected_murderer':killer,'accused':accusation['accused'],'correct':accusation['accused']==killer,
       'confidence':accusation['confidence'],'culprit_scores':[r['scores'][killer] for r in checkpoints],
       'first_clear_stage':first,'first_clear_name':checkpoints[first-1]['clear_culprit'] if first else None,
       'first_clear_actual_culprit_stage':true_clear[0] if true_clear else None,
       'wrong_early_clear_stages':[i+1 for i,r in enumerate(checkpoints[:7]) if r['clear_culprit'] not in [None,killer]],
       'culprit_final':final[killer],'highest_innocent_final':max(final[n] for n in innocents),
       'unique_final_leader':final[killer]>max(final[n] for n in innocents),
       'act2_suspects_above5':sum(v>5 for v in checkpoints[5]['scores'].values()),
       'final_innocents_5to7':sum(5<=final[n]<=7 for n in innocents),'earned':post.get('earned'),
       'new_decisive_facts':post.get('new_decisive_facts',[]),'ratings':accusation.get('ratings',{}),'assessment_source':t.get('assessment_source','')}
  summary.append(row);trials.append({**row,'checkpoints':checkpoints,'accusation':accusation,'post_vote':post})
  for issue in accusation.get('issues',[]):allissues.append({'scenario':t['trial'],'selected_murderer':killer,**issue})
 OUT.mkdir(parents=True,exist_ok=True)
 assert len(flat)==3872
 with (OUT/'all-suspicion-scores.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
 rows=[]
 for r in summary:
  rows.append({k:v for k,v in r.items() if k not in ['culprit_scores','ratings','new_decisive_facts','wrong_early_clear_stages']}|{f'culprit_stage_{i+1}':v for i,v in enumerate(r['culprit_scores'])}|r['ratings']|{'new_decisive_facts':json.dumps(r['new_decisive_facts'],ensure_ascii=False),'wrong_early_clear_stages':json.dumps(r['wrong_early_clear_stages'])})
 with (OUT/'scenario-summary.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 rating_keys=sorted({k for r in summary for k in r['ratings']})
 stats={'completed':len(summary),'total':22,'correct':sum(r['correct'] for r in summary),'earned':sum(r['earned'] is True for r in summary),
        'clear_before_method_testimony':sum(r['first_clear_stage'] is not None and r['first_clear_stage']<8 for r in summary),
        'actual_culprit_clear_before_method_testimony':sum(r['first_clear_actual_culprit_stage'] is not None and r['first_clear_actual_culprit_stage']<8 for r in summary),
        'wrong_early_clear_scenarios':sum(bool(r['wrong_early_clear_stages']) for r in summary),
        'unique_final_culprit_leader':sum(r['unique_final_leader'] for r in summary),
        'final_culprit_score_range':[min(r['culprit_final'] for r in summary),max(r['culprit_final'] for r in summary)],
        'confidence_range':[min(r['confidence'] for r in summary),max(r['confidence'] for r in summary)],
        'act2_suspects_above5_median':statistics.median(r['act2_suspects_above5'] for r in summary),
        'final_innocents_5to7_median':statistics.median(r['final_innocents_5to7'] for r in summary),
        'ratings':{k:{'mean':round(statistics.mean(r['ratings'][k] for r in summary if k in r['ratings']),2),'min':min(r['ratings'][k] for r in summary if k in r['ratings']),'max':max(r['ratings'][k] for r in summary if k in r['ratings'])} for k in rating_keys},
        'score_values':len(flat),'stages':8,'all_journals_and_locks_verified':True}
 payload={'generated_utc':datetime.now(timezone.utc).isoformat(),'protocol':info['protocol'],'stages':stages,'names':names,'stats':stats,'trials':trials,'issues':allissues}
 (OUT/'results.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 (RUN/'results.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 (RUN/'summary.json').write_text(json.dumps(stats,indent=2)+'\n')
 feedback=['# Blind player feedback / SPOILERS\n','One independent AI player-reader per selected culprit. These are not human solve rates. Scores were locked before subsequent releases; final accusations preceded the finale.\n']
 for t in trials:
  a=t['accusation'];feedback.extend([f"## Scenario: {t['selected_murderer']}\n",f"Accused: {a['accused']}. Confidence: {a['confidence']}/10. Earned: {t['earned']}.\n",'### Locked accusation\n',a['reasoning']+'\n','### Reader feedback\n',a['feedback']+'\n','### Suggested surgical edits\n'])
  for issue in a.get('issues',[]):feedback.append(f"- **{issue.get('severity','unspecified')} / {issue.get('category','other')}**: {issue.get('detail','')} Suggested fix: {issue.get('suggested_fix','')}\n")
  feedback.extend(['### Post-finale feedback\n',t['post_vote']['feedback']+'\n'])
 (OUT/'all-player-feedback.md').write_text('\n'.join(feedback),encoding='utf-8')
 (OUT/'all-reader-issues.json').write_text(json.dumps(allissues,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 html=HTML.replace('__DATA__',json.dumps(payload,ensure_ascii=False).replace('<',r'<'))
 (OUT/'results.html').write_text(html,encoding='utf-8')
 (RUN/'progress.json').write_text(json.dumps({'completed':22,'total':22,'status':'complete','all_locks_verified':True},indent=2)+'\n')
 print(json.dumps(stats))

HTML='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ensemble candidate07 blind verification · 22 scenarios</title>
<style>*{box-sizing:border-box}body{margin:0;background:#faf9f6;color:#242426;font:16px/1.5 system-ui,sans-serif}main{max-width:1350px;padding:28px;margin:auto}h1{font-size:30px;margin:0}h2{font-size:23px}h3{font-size:18px}.muted{color:#666}header{border-bottom:2px solid #751e35;padding-bottom:22px}.cards{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0}.card{background:white;border:1px solid #ddd5cd;padding:15px;flex:1;min-width:155px}.card b{display:block;font-size:27px}select{font:inherit;background:white;border:1px solid #aaa;border-radius:4px;padding:10px;max-width:100%}.scroll{overflow:auto}table{border-collapse:collapse;font-size:14px;width:100%;background:white}th,td{padding:8px 10px;border-bottom:1px solid #ded9d2;text-align:left}th{background:#eeeae4;position:sticky;top:0}td.num{text-align:center;min-width:62px}td:first-child,th:first-child{min-width:175px}.culprit td:first-child{font-weight:700;color:#751e35}.panels{display:grid;grid-template-columns:1fr 1fr;gap:22px}.panel{background:white;border:1px solid #ddd5cd;padding:20px}.text{white-space:pre-wrap}details{margin:14px 0;border:1px solid #ddd5cd;padding:12px;background:white}summary{cursor:pointer;font-weight:600}button{font:inherit;padding:8px 12px;cursor:pointer}a{color:#751e35}label{font-weight:600}ul{padding-left:22px}@media(max-width:800px){main{padding:16px}.panels{grid-template-columns:1fr}h1{font-size:25px}}@media print{select,button{display:none}.scroll{overflow:visible}details{break-inside:avoid}.panels{grid-template-columns:1fr}}</style>
<main><header><p class="muted">SPOILERS · Dramaturgical ensemble07 · Fresh 22-reader cohort · October 26, 2026</p><h1>Dramaturgical revision: 22 blind scenarios</h1><p>One fresh blind reader assessed each of the 22 culprit scenarios using the same frozen candidate. Scores and accusations were locked before later releases. No old assessments carried forward. No human party is simulated.</p></header><div id="cards" class="cards"></div><p><a href="all-suspicion-scores.csv">All 3,872 suspicion scores (CSV)</a> · <a href="scenario-summary.csv">Scenario summary (CSV)</a> · <a href="all-player-feedback.md">Complete qualitative feedback</a> · <a href="revision-review.md">Revision review</a> · <a href="tested-ACT_III_Evidence.pdf">Tested six-page evidence PDF</a></p>
<h2>Every scenario at a glance</h2><p class="muted">Scores below track the assigned murderer, not every suspect. Select a scenario farther down for all 22 guests at all eight checkpoints. A1 and A2 are testimony checkpoints; E3 is evidence before final testimony.</p><div class="scroll"><table id="overview"></table></div>
<h2>Complete suspicion matrix</h2><label for="case">Selected murderer in this scenario: </label><select id="case"></select><p id="case-summary"></p><div class="scroll"><table id="matrix"></table></div><p class="muted">0 = no current suspicion; 10 = overwhelming suspicion. Colors show suspicion strength, not correctness. Bold burgundy name identifies the assigned murderer for your analysis; readers did not see that assignment.</p>
<div class="panels"><section class="panel"><h2>Locked accusation</h2><div id="accusation" class="text"></div><h3>Reader ratings (0–10)</h3><div id="ratings"></div></section><section class="panel"><h2>Qualitative feedback</h2><div id="feedback" class="text"></div><h3>Post-finale assessment</h3><div id="post" class="text"></div></section></div><h2>Issues and bounded fixes</h2><div id="issues"></div><h2>Reasoning at every checkpoint</h2><div id="reasoning"></div><h2>Limits of this test</h2><p>These are descriptive results from one model reader per culprit, with complete evidence discovery and faithful scripted testimony. Readers scored as outside observers of public introductions, evidence and testimony, rather than as an assigned character with a private packet. They cannot estimate human solve rates, group dynamics, missed clues, acting quality, or the effects of improvisation. Source-reference coverage is distinct from play balance. A correct accusation does not by itself establish an enjoyable or believable game. Each assessed input set was frozen. All 22 cases in this report used this one frozen candidate and fresh reader contexts; interrupted readers resumed with the same identities and immutable prior scores. The earlier verified release remains separate.</p></main>
<script>const D=__DATA__;const el=id=>document.getElementById(id);const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const short=['Intro','Hunt','E1','Act I','E2','Act II','E3','Act III'];const S=D.stats;el('cards').innerHTML=[[`${S.correct}/22`,'Correct accusations'],[`${S.earned}/22`,'Endings judged earned'],[`${S.actual_culprit_clear_before_method_testimony}/22`,'Actual culprit clear before final testimony'],[S.ratings.naturalness.mean,'Mean naturalness / 10'],[S.ratings.clarity.mean,'Mean clarity / 10']].map(([a,b])=>`<div class="card"><b>${esc(a)}</b>${esc(b)}</div>`).join('');
el('overview').innerHTML='<thead><tr><th>Assigned murderer</th>'+short.map(x=>`<th>${x}</th>`).join('')+'<th>Accused</th><th>Confidence</th><th>First clear</th><th>Final innocent 5–7</th></tr></thead><tbody>'+D.trials.map((t,i)=>`<tr><td><a href="#matrix" data-case="${i}">${esc(t.selected_murderer)}</a></td>${t.culprit_scores.map(v=>`<td class="num">${v}</td>`).join('')}<td>${esc(t.accused)} ${t.correct?'✓':'✗'}</td><td>${t.confidence}/10</td><td>${t.first_clear_stage?esc(short[t.first_clear_stage-1]):'None'}</td><td>${t.final_innocents_5to7}</td></tr>`).join('')+'</tbody>';
el('case').innerHTML=D.trials.map((t,i)=>`<option value="${i}">${esc(t.selected_murderer)}</option>`).join('');
function show(i){el('case').value=i;const t=D.trials[i],a=t.accusation;el('case-summary').textContent=`Accused ${t.accused}; confidence ${t.confidence}/10. ${t.correct?'Correct.':'Incorrect.'} ${t.earned?'Ending judged earned.':'Ending not judged earned.'} ${t.act2_suspects_above5} suspects above 5 after Act II; ${t.final_innocents_5to7} innocents remain at 5–7 after Act III.`;
el('matrix').innerHTML='<thead><tr><th>Guest</th>'+D.stages.map((x,j)=>`<th title="${esc(x)}">${j+1}: ${short[j]}</th>`).join('')+'</tr></thead><tbody>'+D.names.map(n=>`<tr class="${n===t.selected_murderer?'culprit':''}"><td>${esc(n)}</td>${t.checkpoints.map(c=>{let v=c.scores[n];return `<td class="num" style="background:hsl(345 40% ${99-v*4}%);color:${v>=8?'#36131e':'#242426'}">${v}</td>`}).join('')}</tr>`).join('')+'</tbody>';
el('accusation').textContent=a.reasoning;el('feedback').textContent=a.feedback;el('post').textContent=t.post_vote.feedback;el('ratings').innerHTML=Object.entries(a.ratings).map(([k,v])=>`<div>${esc(k.replaceAll('_',' '))}: <b>${v}</b></div>`).join('');el('issues').innerHTML=(a.issues||[]).map(x=>`<div class="panel"><b>${esc(x.severity)} / ${esc(x.category)}</b><p>${esc(x.detail)}</p><p><b>Suggested fix:</b> ${esc(x.suggested_fix)}</p></div>`).join('')||'<p>No specific issues recorded by this reader.</p>';el('reasoning').innerHTML=t.checkpoints.map((c,j)=>`<details><summary>${j+1}: ${esc(D.stages[j])} · clear culprit: ${esc(c.clear_culprit||'none')}</summary><p>${esc(c.reasoning)}</p></details>`).join('');}
el('case').addEventListener('change',e=>show(+e.target.value));document.querySelectorAll('[data-case]').forEach(a=>a.addEventListener('click',()=>show(+a.dataset.case)));show(0);</script></html>'''

if __name__=='__main__':main()
