"""Honest partial/all-route dashboard; never infer success from pending cases."""
from pathlib import Path
import json,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import report_exhaustive_balance as audit

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest'/(sys.argv[1] if len(sys.argv)>1 else '2026-10-24-PRINT-FINAL-SPOILERS')
audit.RUN=RUN
d=audit.collect();d['replicates_per_culprit']=1
audit.write(RUN/'aggregate.json',d)
done=[t for t in d['trials'] if t['status']=='complete']
keys=['correct','earned','e3_ready','final_strong']
summary={'completed':len(done),'total':d['total'],'invalid':d['invalid'],'correct':sum(t['metrics']['correct'] for t in done),'earned':sum(t['metrics']['earned'] for t in done),'no_early_clear':sum(not t['metrics']['early_clear'] for t in done),'e3_ready':sum(t['metrics']['e3_ready'] for t in done),'final_strong':sum(t['metrics']['final_strong'] for t in done),'midgame_breadth':sum(t['metrics']['act2_suspects']>=8 for t in done),'ending_breadth':sum(t['metrics']['final_alternatives']>=3 for t in done),'flagged':sum(bool(t['audit_flags']) for t in done)}
audit.write(RUN/'metric-summary.json',summary)
lines=['# Print-final balance results / SPOILERS','',f"{len(done)}/{d['total']} complete; {d['invalid']} invalid. No scores or accusations changed.",'','One fresh attentive AI text reader per selected world. This measures reasoning from transcribed exhibits, not human recall, physical props or party solve rates. Pending scenarios are not successes. Full locked scores, accusations, feedback and protocol flags remain in blind/. No result-based rerolls.','', '| Selected character | Correct / earned | Early clear | E3 | Final | ActII >5 | Final innocents5–7 | Naturalness |','|---|---|---|---:|---:|---:|---:|---:|']
for t in done:
    m=t['metrics'];lines.append(f"| {t['murderer']} | {m['correct']} / {m['earned']} | {m['early_clear']} | {m['e3_score']} | {m['final_score']} | {m['act2_suspects']} | {m['final_alternatives']} | {t['accusation']['ratings']['naturalness']} |")
for t in done:
    lines+=['',f"## {t['trial']} / {t['murderer']}",'','Accusation: '+t['accusation']['accused'],'',t['accusation']['reasoning'],'',t['accusation']['feedback'],'','Finale: '+t['finale']['feedback']]
    for issue in t['accusation']['issues']:lines+=['',f"- {issue['severity']} / {issue['category']}: {issue['detail']} Suggested action: {issue['suggested_fix']}"]
    for flag in t['audit_flags']:lines+=['','AUDIT FLAG: '+flag]
(RUN/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
template=(ROOT/'scripts/exhaustive_dashboard.html').read_text(encoding='utf-8')
start=template.index('<header>');end=template.index('</header>',start)+len('</header>')
header='<header><p class="meta">The Last Acquisition / Current22 print-final candidate / SPOILERS</p><h1>Every attending route.</h1><p>One independent gated reader per selected culprit. Pending cases are not successes; no claim of human solve rates. Read the release decision before printing.</p><div class="links"><a href="RESULTS.md">Full reviews and metrics</a><a href="murderer-arcs.png">Culprit arcs</a><a href="DECISION.md">Release decision</a><a href="scores.csv">Raw scores</a></div><p class="progress" id="progress"></p></header>'
template=template[:start]+header+template[end:]
template=template.replace(' of 110 complete',' of ${D.total} complete').replace('${c.n}/5','${c.n}/1').replace('${group.length}/5 readers complete.','${group.length}/1 readers complete.').replace('Cells average its five readers; hover for the range.','One locked reader per scenario; hover for the value.').replace('Five readers per murderer is a small descriptive sample.','One reader per murderer is a narrow diagnostic.').replace('22 suspects · Published game audit','Current22 / Print-final checks').replace('The published game is unchanged.','See the release decision for the actual downloadable version.')
(RUN/'dashboard.html').write_text(template.replace('__DATA__',json.dumps(d,ensure_ascii=False).replace('</',r'<\/')),encoding='utf-8')
palette=ListedColormap(['#e4eee6','#d3e7d7','#b8d9c1','#99caaa','#c8d67b','#eddb72','#f4bd61','#ef9153','#d66042','#ac3437','#792239'])
palette.set_bad('#eee9df')
import numpy as np
grid=np.array([[np.nan if v is None else v for v in c['progress']] for c in d['cases']])
fig,ax=plt.subplots(figsize=(11,12),facecolor='#faf7ef')
ax.imshow(grid,cmap=palette,vmin=-.5,vmax=10.5,aspect='auto');ax.set_yticks(range(len(d['cases'])),[c['name']+(' *' if c['flagged'] else '') for c in d['cases']]);ax.set_xticks(range(8),['Intro','Hunt','E1','Motive','E2','Opportunity','E3','Method'],rotation=35,ha='right')
for y,row in enumerate(grid):
    for x,v in enumerate(row):ax.text(x,y,'—' if np.isnan(v) else str(int(v)),ha='center',va='center',fontsize=10,color='white' if v>=9 else '#252521')
ax.set_title(f"Selected culprit arcs / {len(done)}/22 worlds / SPOILERS",pad=20)
ax.set_xticks(np.arange(-.5,8),minor=True);ax.set_yticks(np.arange(-.5,22),minor=True);ax.grid(which='minor',color='#faf7ef',linewidth=2);ax.tick_params(which='minor',length=0)
fig.text(.03,.025,'Each row is a DIFFERENT selected-murderer world. Dashes mean untested.\n* Score/conclusion conflict retained; inspect raw record. AI text checks, not human solve rates.',fontsize=10)
fig.subplots_adjust(left=.28,right=.97,top=.92,bottom=.13)
for suffix in ('png','pdf'):fig.savefig(RUN/('murderer-arcs.'+suffix),dpi=150,facecolor=fig.get_facecolor())
plt.close(fig)
for t in done:
    names=[c['name'] for c in d['roster']];a=[[s['scores'][n] for s in t['stages']] for n in names]
    fig,ax=plt.subplots(figsize=(10,12),facecolor='#faf7ef');ax.imshow(a,cmap=palette,vmin=-.5,vmax=10.5,aspect='auto');ax.set_yticks(range(22),[n+(' *' if n==t['murderer'] else '') for n in names]);ax.set_xticks(range(8),['Intro','Hunt','E1','Motive','E2','Opportunity','E3','Method'],rotation=35,ha='right')
    for y,row in enumerate(a):
        for x,v in enumerate(row):ax.text(x,y,str(v),ha='center',va='center',fontsize=10,color='white' if v>=9 else '#252521')
    ax.set_title(t['trial']+' / '+t['murderer']+' / SPOILERS',pad=20);fig.subplots_adjust(left=.28,right=.98,top=.93,bottom=.10);fig.savefig(RUN/(t['trial']+'-heatmap.png'),dpi=140);plt.close(fig)
state=json.loads((RUN/'resume-state.json').read_text()) if (RUN/'resume-state.json').exists() else {}
promoted=state.get('candidate_promoted',False)
audit.write(RUN/'resume-state.json',{**state,'status':'released_with_balance_caveats' if promoted else ('testing' if len(done)<d['total'] else 'all_routes_assessed_pending_decision'),'completed':len(done),'total':d['total'],'invalid':d['invalid'],'unstarted':[t['trial'] for t in d['trials'] if t['status']=='pending'],'running':[t['trial'] for t in d['trials'] if t['status']=='running'],'candidate_promoted':promoted})
print(json.dumps(summary))
