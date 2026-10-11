"""Export the all-case suspicion overview as a shareable PNG/PDF."""
from exhaustive_balance import RUN
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

d=json.loads((RUN/'aggregate.json').read_text(encoding='utf8'))
c=d['cases']; a=np.array([[np.nan if v is None else v for v in x['progress']] for x in c])
palette=['#e4eee6','#d3e7d7','#b8d9c1','#99caaa','#c8d67b','#eddb72','#f4bd61','#ef9153','#d66042','#ac3437','#792239']
cmap=LinearSegmentedColormap.from_list('suspicion',palette);cmap.set_bad('#eee9df')
fig,ax=plt.subplots(figsize=(14,12),facecolor='#faf7ef');ax.set_facecolor('#faf7ef')
im=ax.imshow(a,vmin=0,vmax=10,cmap=cmap,aspect='auto')
ax.set_xticks(range(8),['Intro','Hunt','E1','Act I','E2','Act II','E3','Act III']);ax.xaxis.tick_top()
ax.set_yticks(range(22),[x['name']+'  ('+str(x['n'])+'/5)' for x in c]);ax.tick_params(length=0,pad=10,labelsize=12)
for i in range(22):
 for j in range(8):
  v=a[i,j];ax.text(j,i,'—' if np.isnan(v) else f'{v:.1f}',ha='center',va='center',color='white' if v>=8 else '#292622',fontsize=12)
ax.set_xticks(np.arange(-.5,8,1),minor=True);ax.set_yticks(np.arange(-.5,22,1),minor=True);ax.grid(which='minor',color='#faf7ef',linewidth=3);ax.tick_params(which='minor',length=0)
for spine in ax.spines.values():spine.set_visible(False)
fig.suptitle('The selected murderer’s suspicion arc',x=.04,y=.97,ha='left',fontsize=25,fontfamily='Georgia',color='#292622')
fig.text(.04,.925,f"Published RSVP22 · {d['completed']}/110 blind tests complete · SPOILERS",fontsize=14,color='#781d30')
cb=fig.colorbar(im,ax=ax,fraction=.025,pad=.025);cb.set_label('Mean suspicion score / 10');cb.set_ticks(range(11))
fig.text(.04,.04,'Each row is a separate murderer scenario. Means across five fresh AI readers; completed count in parentheses.\nScores are not probabilities or human solve rates. Individual scores, accusations and reviews remain in the dashboard.',fontsize=11,color='#69645b')
fig.subplots_adjust(left=.24,right=.93,top=.87,bottom=.10)
fig.savefig(RUN/'murderer-arcs.png',dpi=160);fig.savefig(RUN/'murderer-arcs.pdf');plt.close(fig)
