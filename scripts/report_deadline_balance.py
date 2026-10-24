"""Audited results and before/after visuals for the deadline balance pass."""
from pathlib import Path
import json,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import report_exhaustive_balance as audit

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest'/(sys.argv[1] if len(sys.argv)>1 else '2026-10-23-UNRESOLVED-STAKES-SPOILERS')
audit.RUN=RUN
d=audit.collect();d['replicates_per_culprit']=1
audit.write(RUN/'aggregate.json',d)
base=json.loads((ROOT/'docs/playtest/2026-10-23-FINAL-RSVP22-SPOILERS/aggregate.json').read_text(encoding='utf-8'))
old={t['murderer']:t for t in base['trials'] if t['status']=='complete'}
done=[t for t in d['trials'] if t['status']=='complete']
lines=['# Deadline balance pass / SPOILERS','',f"Completed {d['completed']}/{d['total']}; invalid {d['invalid']}. Scores and accusations remain locked.",'',
       'The same two selected-murderer scenarios and current 22-person cast were assessed by fresh independent readers. This is a bounded diagnostic, not human solve rates, exhaustive coverage or causal proof of an improvement. Prior readers were not rerun. No target scores or prior feedback were disclosed.','',
       '| Scenario | Version | Correct | Clear before Act III | E3 | Final | Act II scores >5 | Final innocent scores 5â€“7 | Naturalness | Earned |',
       '| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |']
for t in done:
    for label,item in [('Published',old[t['murderer']]),('Candidate',t)]:
        m=item['metrics'];lines.append(f"| {t['murderer']} | {label} | {m['correct']} | {m['early_clear']} | {m['e3_score']} | {m['final_score']} | {m['act2_suspects']} | {m['final_alternatives']} | {item['accusation']['ratings']['naturalness']} | {m['earned']} |")
lines+=['','Targets: correct earned accusation, no clear culprit before Act III, E3 culprit 5â€“7, final culprit at least9, at least8 suspects above5 after Act II and at least3 final innocent alternatives at5â€“7. These are assessment criteria, not reader instructions.','','## Narrative and usability','',
        '| Scenario | Fair play | Clarity | Voice | Arc variety | Naturalness | Drama |','| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
for t in done:
    r=t['accusation']['ratings'];lines.append('| '+t['murderer']+' | '+' | '.join(str(r[k]) for k in ['fair_play','clarity','voice_distinction','arc_variety','naturalness','drama'])+' |')
for t in done:
    lines+=['',f"## {t['murderer']} / {t['trial']}",'','Accusation: '+t['accusation']['accused'],'',t['accusation']['reasoning'],'',t['accusation']['feedback'],'','Post-vote: '+t['finale']['feedback']]
    for issue in t['accusation']['issues']:lines+=['',f"- {issue['severity']} / {issue['category']}: {issue['detail']} Suggested action: {issue['suggested_fix']}"]
    for flag in t['audit_flags']:lines+=['','Audit flag: '+flag]
(RUN/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if done:
    names=[c['name'] for c in d['roster']]
    colors=['#e4eee6','#d3e7d7','#b8d9c1','#99caaa','#c8d67b','#eddb72','#f4bd61','#ef9153','#d66042','#ac3437','#792239']
    fig,axes=plt.subplots(1,len(done),figsize=(8*len(done),12),squeeze=False)
    fig.patch.set_facecolor('#faf7ef')
    for ax,t in zip(axes[0],done):
        grid=[[s['scores'][n] for s in t['stages']] for n in names]
        ax.imshow(grid,cmap=ListedColormap(colors),vmin=-.5,vmax=10.5,aspect='auto')
        ax.set_yticks(range(22),[n+(' *' if n==t['murderer'] else '') for n in names])
        ax.set_xticks(range(8),['Intro','Hunt','E1','Motive','E2','Opportunity','E3','Method'],rotation=45,ha='right')
        ax.set_title(t['trial']+' / '+t['murderer'],fontsize=14)
        for y,row in enumerate(grid):
            for x,value in enumerate(row):ax.text(x,y,str(value),ha='center',va='center',fontsize=10,color='white' if value>=9 else '#252521')
        ax.set_xticks([x-.5 for x in range(9)],minor=True);ax.set_yticks([y-.5 for y in range(23)],minor=True)
        ax.grid(which='minor',color='#faf7ef',linewidth=2);ax.tick_params(which='minor',bottom=False,left=False)
    fig.suptitle('Unresolved stakes / Updated RSVP22 / SPOILERS',fontsize=20)
    fig.text(.02,.025,'* Selected murderer in this scenario. Fresh attentive AI text readers; not human solve rates. Full immutable records and comparison in RESULTS.md.',fontsize=10)
    fig.subplots_adjust(left=.15,right=.98,top=.92,bottom=.1,wspace=.6)
    for suffix in ['png','pdf']:fig.savefig(RUN/('heatmaps.'+suffix),dpi=150,facecolor=fig.get_facecolor())
    plt.close(fig)
template=(ROOT/'scripts/exhaustive_dashboard.html').read_text(encoding='utf-8')
start=template.index('<header>');end=template.index('</header>',start)+len('</header>')
header='<header><p class="meta">The Last Acquisition / Deadline balance pass / SPOILERS</p><h1>Unresolved stakes.</h1><p>Two fixed scenarios with the updated 22-person cast. Eight sequential locked releases per reader. Read the comparison and limitations before interpreting the scores.</p><div class="links"><a href="RESULTS.md">Before / after and full feedback</a><a href="heatmaps.png">Heatmaps</a><a href="DECISION.md">Release decision</a><a href="scores.csv">Scores CSV</a></div><p class="progress" id="progress"></p></header>'
template=template[:start]+header+template[end:]
template=template.replace(' of 110 complete',' of ${D.total} complete').replace('${c.n}/5','${c.n}/${D.replicates_per_culprit}').replace('${group.length}/5 readers complete.','${group.length}/${D.replicates_per_culprit} readers complete.')
template=template.replace('Cells average its five readers; hover for the range.','Each scenario has one new independent reader; hover for the recorded value.').replace('Five readers per murderer is a small descriptive sample.','One reader per scenario is a narrow diagnostic.').replace('22 suspects Â· Published game audit','Deadline balance / Updated RSVP22').replace('The published game is unchanged.','See the release decision for promotion status.')
view={**d,'cases':[c for c in d['cases'] if c['trials']]}
(RUN/'dashboard.html').write_text(template.replace('__DATA__',json.dumps(view,ensure_ascii=False).replace('</',r'<\/')),encoding='utf-8')
print(json.dumps({'completed':d['completed'],'total':d['total'],'invalid':d['invalid'],'cases':[{k:t['metrics'][k] for k in ['correct','early_clear','e3_score','final_score','act2_suspects','final_alternatives','earned']} for t in done]}))
