"""Preserve both diagnostic casts and compare without selecting favorable readers."""
from pathlib import Path
import json,sys
import report_exhaustive_balance as report
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

RUN=Path(__file__).resolve().parents[1]/'docs/playtest'/(sys.argv[1] if len(sys.argv)>1 else '2026-10-11-STRUCTURAL-STORY-SPOILERS')
baseline=report.read(RUN.parent/'2026-10-10-EXHAUSTIVE-RSVP22-SPOILERS/aggregate.json')
manifest=report.read(RUN/'cast22/private-manifest.json')
scenarios=', '.join(t['murderer'] for t in manifest['trials'])
cmap=LinearSegmentedColormap.from_list('museum',['#e0eee7','#9ac8ae','#f0dd75','#efaa5e','#af3439','#71293e'])
lines=['# Structural story diagnostic / SPOILERS','',
 'The candidate and freeze receipts identify the precise revision. Final evidence retains crime-bearing observations while moving nonessential refund and settlement recaps out of the reveal. Published source and previously sent assets remain unchanged.', '',
 f'Three fixed critical scenarios ({scenarios}), one fresh reader per scenario in each cast. These six exploratory readings are not a representative human solve-rate estimate or paired controlled experiment. Every result is retained, including disagreements.', '',
 '| Cast | Murderer | E3 | Final | Final innocent alternatives 5–7 | Naturalness | Voice | Correct | Earned |',
 '| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |']
all_done=[]
for edition in (22,30):
    report.RUN=RUN/f'cast{edition}'
    data=report.collect();data['total']=3
    report.write(report.RUN/'aggregate.json',data)
    done=[t for t in data['trials'] if t['status']=='complete']
    all_done.extend((edition,t) for t in done)
    for t in done:
        m=t['metrics'];r=t['accusation']['ratings']
        lines.append(f"| {edition} | {t['murderer']} | {m['e3_score']} | {m['final_score']} | {m['final_alternatives']} | {r['naturalness']} | {r['voice_distinction']} | {m['correct']} | {t['finale']['earned']} |")
    if done:
        names=[p['name'] for p in data['roster']]
        fig,axes=plt.subplots(1,len(done),figsize=(8*len(done),edition*.45+2),squeeze=False)
        fig.patch.set_facecolor('#faf7ef')
        for i,(ax,t) in enumerate(zip(axes[0],done)):
            grid=[[s['scores'][n] for s in t['stages']] for n in names]
            ax.imshow(grid,vmin=0,vmax=10,cmap=cmap,aspect='auto')
            ax.set_xticks(range(8),['Intro','Hunt','E1','Act I','E2','Act II','E3','Act III'],rotation=45,ha='right')
            ax.set_yticks(range(edition),names if i==0 else ['']*edition)
            ax.set_title(t['murderer']+' / '+t['trial'])
            for y,row in enumerate(grid):
                for x,v in enumerate(row):ax.text(x,y,str(v),ha='center',va='center',fontsize=9,color='white' if v>=8 else '#252521')
            ax.set_xticks([x-.5 for x in range(9)],minor=True)
            ax.set_yticks([y-.5 for y in range(edition+1)],minor=True)
            ax.grid(which='minor',color='#faf7ef',linewidth=2)
            ax.tick_params(which='minor',bottom=False,left=False)
        fig.suptitle(f'Structural story diagnostic · cast {edition} · {len(done)}/3 complete · SPOILERS',fontsize=18)
        fig.subplots_adjust(left=.13,right=.98,top=.92,bottom=.1,wspace=.12)
        fig.savefig(report.RUN/'heatmaps.png',dpi=150,facecolor=fig.get_facecolor())
        fig.savefig(report.RUN/'heatmaps.pdf',facecolor=fig.get_facecolor());plt.close(fig)
lines+=['','## Comparison against published RSVP22 baseline','',
 '| Scenario | E3 baseline → new | Naturalness baseline → new | Final alternatives baseline → new |',
 '| --- | --- | --- | --- |']
for edition,t in all_done:
    if edition!=22:continue
    b=next(c for c in baseline['cases'] if c['name']==t['murderer']);m=t['metrics']
    lines.append(f"| {t['murderer']} | {b['e3_score']['mean']} → {m['e3_score']} | {b['ratings']['naturalness']} → {t['accusation']['ratings']['naturalness']} | {b['final_alternatives']['mean']} → {m['final_alternatives']} |")
lines+=['','## Unabridged reader feedback','']
for edition,t in all_done:
    lines += [f"### Cast {edition}: {t['murderer']}",'',t['accusation']['feedback'],'', 'Finale: '+t['finale']['feedback'],'']
    for issue in t['accusation']['issues']:
        lines += [f"- {issue['severity']} / {issue['category']}: {issue['detail']} Suggested fix: {issue['suggested_fix']}"]
    lines.append('')
(RUN/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'complete':len(all_done),'total':6,'correct':sum(t['metrics']['correct'] for _,t in all_done)}))
