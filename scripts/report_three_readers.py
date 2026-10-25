"""Validate three independent sequential reads and render comparable score heatmaps."""
from pathlib import Path
import csv
import hashlib
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/connected-story-01-SPOILERS/balance-full-04'
manifest=json.loads((OUT/'private-selection.json').read_text(encoding='utf-8'))
for relative,expected in manifest['sha256'].items():
    assert hashlib.sha256((OUT/relative).read_bytes()).hexdigest()==expected,relative
names=[p['name'] for p in manifest['cast']]
killer=next(p['name'] for p in manifest['cast'] if p['id']==manifest['killer_id'])
labels=['Intro','Hunt','E1','Act I','E2','Act II','E3','Act III']
readers={}
metrics={}
for letter in 'abc':
    key='Reader '+letter.upper()
    result=json.loads((OUT/f'reader_{letter}.json').read_text(encoding='utf-8-sig'))
    assert len(result['checkpoints'])==8
    rows=[]
    for stage,record in enumerate(result['checkpoints'],1):
        assert record['stage']==stage
        scores=record['scores']
        assert set(scores)==set(names) and len(scores)==30
        assert all(isinstance(v,(int,float)) and not isinstance(v,bool) and 0<=v<=10 for v in scores.values())
        highest=max(scores.values())
        leaders=[n for n in names if scores[n]==highest]
        rows.append(dict(stage=stage,above_five=sum(v>5 for v in scores.values()),
                         culprit_score=scores[killer],leaders=leaders,highest=highest,
                         correct_sole_leader=leaders==[killer],
                         alternatives_five_six=sum(5<=scores[n]<=6 for n in names if n!=killer),
                         obvious_culprit=record.get('obvious_culprit')))
    readers[key]=result
    metrics[key]={'stages':rows,'act_ii_above_five':rows[5]['above_five'],
                  'correct_final_leader':rows[-1]['correct_sole_leader'],
                  'final_culprit_score':rows[-1]['culprit_score'],
                  'final_alternatives_five_six':rows[-1]['alternatives_five_six'],
                  'early_obvious_culprit':any(r['obvious_culprit']==killer for r in rows[:6]),
                  'protocol_deviation':result.get('protocol_deviation','')}
    metrics[key]['numerical_targets_met']=(rows[5]['above_five']>=10 and rows[-1]['correct_sole_leader']
        and 3<=rows[-1]['alternatives_five_six']<=4 and not metrics[key]['early_obvious_culprit'])
(OUT/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (OUT/'scores.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['Character']+[f'{reader}: {label}' for reader in readers for label in labels])
    for name in names:
        w.writerow([name]+[stage['scores'][name] for reader in readers.values() for stage in reader['checkpoints']])

arrays={key:np.array([[stage['scores'][name] for stage in result['checkpoints']] for name in names])
        for key,result in readers.items()}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
def draw(ax,values,title,show_names=True):
    image=ax.imshow(values,cmap='RdYlGn_r',vmin=0,vmax=10,aspect='auto',interpolation='nearest')
    ax.set_title(title,fontsize=14,pad=15,fontweight='bold')
    ax.set_xticks(range(8),labels,rotation=35,ha='right')
    ax.set_yticks(range(30),names if show_names else ['']*30)
    ax.tick_params(axis='both',length=0)
    for row in range(30):
        for col in range(8):
            value=values[row,col]
            ax.text(col,row,f'{value:g}',ha='center',va='center',fontsize=9,
                    color='white' if value>=8 or value<=1 else '#17231c')
    selected=names.index(killer)
    ax.add_patch(Rectangle((-.5,selected-.5),8,1,fill=False,edgecolor='#171717',linewidth=1.7))
    for spine in ax.spines.values(): spine.set_visible(False)
    return image
fig,axes=plt.subplots(1,3,figsize=(19,14),sharey=False)
fig.patch.set_facecolor('#faf8f2')
for ax,(key,values) in zip(axes,arrays.items()):
    image=draw(ax,values,key,ax is axes[0])
fig.subplots_adjust(left=.14,right=.96,bottom=.13,top=.88,wspace=.10)
fig.suptitle('How suspicion changes through the evening',fontsize=23,fontweight='bold',y=.96)
fig.text(.14,.918,'Three fresh blind readers · same 30-character case · spoilers · outlined row: '+killer,fontsize=12)
fig.text(.14,.044,'E1: first evidence   E2: before Act II   E3: before Act III    |    Scores 0–10; higher means more suspicion.',fontsize=11)
fig.text(.14,.024,'One selected culprit tested. Text descriptions of intended images; no Coming Clean shown. Reader A reports a stage-1 save-order deviation.',fontsize=10)
cax=fig.add_axes([.14,.083,.38,.012]); fig.colorbar(image,cax=cax,orientation='horizontal',ticks=[0,2,4,6,8,10])
fig.savefig(OUT/'three_reader_heatmap.png',dpi=170,facecolor=fig.get_facecolor())
fig.savefig(OUT/'three_reader_heatmap.pdf',facecolor=fig.get_facecolor())
plt.close(fig)
for key,values in arrays.items():
    fig,ax=plt.subplots(figsize=(9,14)); draw(ax,values,key)
    fig.subplots_adjust(left=.29,right=.95,bottom=.12,top=.94)
    fig.text(.29,.025,'Spoilers · outlined row: '+killer+' · suspicion 0–10',fontsize=10)
    fig.savefig(OUT/(key.lower().replace(' ','_')+'_heatmap.png'),dpi=160)
    plt.close(fig)

prior=json.loads((OUT.parent/'balance-full-03/metrics.json').read_text(encoding='utf-8'))
lines=['# Three-reader test of the character-polished case','',
       '**Spoilers.** Thirty characters, sixteen hunt clues, eight releases. All three fresh readers received the identical frozen case and hidden culprit used in the previous quick diagnostic. No target scores, prior results, branch labels, author routes or Coming Clean were shown.','',
       '| Metric | Previous quick read | Reader A | Reader B | Reader C |', '|---|---:|---:|---:|---:|']
for title,old,field in [('Above 5 after Act II',prior[5]['above_five'],'act_ii_above_five'),
                       ('Correct sole final leader',prior[-1]['correct_sole_leader'],'correct_final_leader'),
                       ('Culprit final score',prior[-1]['culprit_score'],'final_culprit_score'),
                       ('Other final suspects at 5–6',prior[-1]['alternatives_five_six'],'final_alternatives_five_six')]:
    lines.append('| '+title+' | '+str(old)+' | '+' | '.join(str(m[field]) for m in metrics.values())+' |')
lines+=['','The previous quick read had corrupted clock labels and is preliminary. Current inputs have explicit clock strings plus restored corroboration; revisions include 120 character-focused Motive/Method speeches. Differences cannot be attributed to prose alone. These are three independent model judgments of one case, not three party rehearsals or validation of all thirty culprit choices.','',
        f'Selected culprit: **{killer}**. Strict targets: at least10/30 above5 at midpoint, no practical identification before ActIII, correct sole final leader,3–4 final alternatives at5–6.','',
        'All frozen hashes and720 numerical scores validated. Reader A reports that its stage1 disk save failed before reading2; it says scores were fixed in memory and later saved unchanged. Its later saves were sequential. Do not treat A as flawless checkpoint persistence.','',
        '## Reader feedback','']
for key,result in readers.items():
    lines += ['### '+key,'',result.get('final_feedback',''),'',
              'Midpoint: '+result['checkpoints'][5].get('naturalness',''),'',
              'Final: '+result['checkpoints'][-1].get('naturalness',''),'']
lines+=['## Artifacts','', '[Combined heatmap](three_reader_heatmap.png) · [Score CSV](scores.csv) · [Metrics](metrics.json)','']
(OUT/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({key:{k:v for k,v in m.items() if k!='stages'} for key,m in metrics.items()},indent=2))
