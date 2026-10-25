"""Finite RSVP-change report: all locked scores, narrative reviews and heatmaps."""
import json
from pathlib import Path
import report_exhaustive_balance as audit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest/2026-10-23-FINAL-RSVP22-SPOILERS'
audit.RUN=RUN
d=audit.collect()
manifest=audit.read(RUN/'private-manifest.json')
d['replicates_per_culprit']=1
d['scope']='Two targeted new-role scenarios with all22 adult suspects. Not exhaustive or human solve rates.'
audit.write(RUN/'aggregate.json',d)
done=[t for t in d['trials'] if t['status']=='complete']
assert len(d['roster'])==22 and not {'03','10'}&{c['id'] for c in d['roster']}
assert {'24','27'}<={c['id'] for c in d['roster']}
lines=['# Final updated-RSVP22 check / SPOILERS','',
       f"Completed **{d['completed']}/{d['total']}**; invalid **{d['invalid']}**. Correct accusations **{sum(t['metrics']['correct'] for t in done)}/{len(done)}**.",'',
       'The published game is unchanged apart from attendance substitutions in these test inputs. The live kit SHA-256 was verified before freezing. Current adult roster:22. Hugh Bidder and Tess Tament removed; Cary Crates and Robin Banks added. The nonplaying child role is excluded. Real guest contact details are not stored here. Sent character sheets and production downloads are unchanged.','',
       'One fresh context-free AI reader per new-role scenario; randomized trial order, eight sequential immutable checkpoints, accusation locked before Coming Clean. All16 discoveries are shown. No rerolls, rewritten scores, assigned personalities or desired ratings. These are two targeted text diagnostics, not a repeat of the110-test audit, coverage of all22 selected-murderer cases, a visual clue test or a live rehearsal.','',
       '| Scenario | Correct | Early clear | E3 score / rank | Final | Act II suspects >5 | Final innocent alternatives5–7 | Earned | New decisive facts |',
       '| --- | --- | --- | --- | ---: | ---: | ---: | --- | ---: |']
for t in done:
    m=t['metrics']
    lines.append(f"| {t['murderer']} | {m['correct']} | {m['early_clear']} | {m['e3_score']} / {m['e3_rank']} | {m['final_score']} | {m['act2_suspects']}/22 | {m['final_alternatives']} | {m['earned']} | {m['new_facts']} |")
lines+=['','Targets retained from earlier assessment: no clear culprit before ActIII, culprit5–7 at E3 and≥9 after ActIII; at least8 suspects above5 after ActII; at least3 final innocent alternatives at5–7. Targets were not disclosed to readers.','','## Story and usability ratings','',
        '| Scenario | Fair play | Clarity | Voice | Arc variety | Naturalness | Drama |','| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
for t in done:
    r=t['accusation']['ratings'];lines.append('| '+t['murderer']+' | '+' | '.join(str(r[k]) for k in ['fair_play','clarity','voice_distinction','arc_variety','naturalness','drama'])+' |')
lines+=['','## Comparison limits','',
        'Neither newly added role was a selected murderer in the old RSVP22 audit. There is no matched old-case score baseline for either scenario. Differences from the old110-reader averages also mix cast and reader changes; do not claim a causal balance trend. The former audit remains historical, not current-cast coverage.','','## Full reader feedback','']
for t in done:
    lines+=[f"### {t['murderer']} / {t['trial']}",'','Accusation: '+t['accusation']['accused'],t['accusation']['reasoning'],'',t['accusation']['feedback'],'','Finale: '+t['finale']['feedback'],'']
    for issue in t['accusation']['issues']:
        lines.append(f"- {issue['severity']} / {issue['category']}: {issue['detail']} Suggested action: {issue['suggested_fix']}")
    for flag in t['audit_flags']:lines.append('Audit flag: '+flag)
    lines.append('')
(RUN/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(RUN/'README.md').write_text('# Final updated-RSVP22 check / SPOILERS\n\nOpen dashboard.html for results, reader heatmaps and all feedback. See RESULTS.md for scope and findings. Raw locked files remain in blind/. The active cast for future tests is source/testing/active-cast.yaml.\n',encoding='utf-8')
if done:
    palette=['#e4eee6','#99caaa','#eddb72','#ef9153','#ac3437','#792239']
    cmap=LinearSegmentedColormap.from_list('suspicion',palette)
    names=[c['name'] for c in d['roster']]
    fig,axes=plt.subplots(1,len(done),figsize=(8*len(done),12),squeeze=False)
    fig.patch.set_facecolor('#faf7ef')
    for i,(ax,t) in enumerate(zip(axes[0],done)):
        grid=[[s['scores'][n] for s in t['stages']] for n in names]
        ax.imshow(grid,vmin=0,vmax=10,cmap=cmap,aspect='auto')
        ax.set_yticks(range(22),[n+(' *' if n==t['murderer'] else '') for n in names])
        ax.set_xticks(range(8),['Intro','Hunt','E1','Motive','E2','Opportunity','E3','Method'],rotation=45,ha='right')
        ax.set_title(t['trial']+' / selected '+t['murderer'],fontsize=14)
        for y,row in enumerate(grid):
            for x,v in enumerate(row):ax.text(x,y,str(v),ha='center',va='center',fontsize=10,color='white' if v>=8 else '#252521')
        ax.set_xticks([x-.5 for x in range(9)],minor=True);ax.set_yticks([y-.5 for y in range(23)],minor=True)
        ax.grid(which='minor',color='#faf7ef',linewidth=2);ax.tick_params(which='minor',bottom=False,left=False)
    fig.suptitle('Final updated-RSVP22 check / SPOILERS',fontsize=20)
    fig.text(.02,.025,'* Selected murderer in this test only. One independent reader per scenario; scores are suspicion judgments, not probabilities or human solve rates.',fontsize=10)
    fig.subplots_adjust(left=.15,right=.98,top=.92,bottom=.1,wspace=.6)
    fig.savefig(RUN/'heatmaps.png',dpi=150,facecolor=fig.get_facecolor());fig.savefig(RUN/'heatmaps.pdf',facecolor=fig.get_facecolor());plt.close(fig)
# Reuse the established interactive report, with explicit finite-round labels.
view={**d,'cases':[c for c in d['cases'] if c['trials']]}
template=(ROOT/'scripts/exhaustive_dashboard.html').read_text(encoding='utf-8')
start=template.index('<header>');end=template.index('</header>',start)+len('</header>')
header='''<header><p class="meta">The Last Acquisition / Updated RSVP cast / SPOILERS</p><h1>Final cast check:22 players.</h1><p>Hugh Bidder and Tess Tament removed; Cary Crates and Robin Banks added. Two targeted scenarios, one fresh reader each. All22 suspects are scored at eight checkpoints. This is not an exhaustive audit.</p><div class="links"><a href="RESULTS.md">Full findings</a><a href="heatmaps.png">Heatmaps PNG</a><a href="heatmaps.pdf">Heatmaps PDF</a><a href="scores.csv">Scores CSV</a><a href="aggregate.json">Raw results JSON</a></div><p class="progress" id="progress"></p></header>'''
template=template[:start]+header+template[end:]
template=template.replace(' of 110 complete',' of ${D.total} complete').replace('${c.n}/5','${c.n}/${D.replicates_per_culprit}').replace('${group.length}/5 readers complete.','${group.length}/${D.replicates_per_culprit} readers complete.')
template=template.replace('Cells average its five readers; hover for the range.','Each tested scenario has one reader; hover for its recorded score.').replace('Five readers per murderer is a small descriptive sample.','One reader per new-role scenario is a narrow diagnostic; the other20 selected-murderer scenarios were not tested this round.')
template=template.replace('22 suspects · Published game audit','Updated RSVP22 / Final targeted check')
(RUN/'dashboard.html').write_text(template.replace('__DATA__',json.dumps(view,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')
print(json.dumps({'completed':d['completed'],'total':d['total'],'invalid':d['invalid'],'correct':sum(t['metrics']['correct'] for t in done)}))
