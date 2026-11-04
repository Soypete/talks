"""Render the matched three-model connector-task comparison."""
from pathlib import Path
from collections import defaultdict
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

root=Path(__file__).resolve().parent
models=[('Qwen3.8-27B', 'h2h-qwen.jsonl'), ('GPT-OSS-20B', 'h2h-gpt-oss.jsonl'), ('LFM3-Audio-2B', 'h2h-lfm.jsonl')]
modes=[('Bare', 'bare'), ('Basic', 'guarded'), ('Progress-aware', 'progress')]
data={}
for label,name in models:
    groups=defaultdict(list)
    for line in (root/'runs'/name).read_text().splitlines():
        row=json.loads(line)
        groups[row['mode']].append(row)
    assert all(len(groups[mode]) == 3 for _,mode in modes), (name,dict(groups))
    data[label]=groups
fig,axes=plt.subplots(1,3,figsize=(19.2,10.8),dpi=150,sharey=True)
for ax,(label,_) in zip(axes,models):
    groups=data[label]
    xs=np.arange(len(modes))
    for delta, metric, color, text in [(-.19,'state','#137d77','Mean final-state score'),(.19,'complete','#dd792a','Correct and finished')]:
        vals=[]
        for _,mode in modes:
            rows=groups[mode]
            val=sum((r['state_score'] if metric=='state' else float(r['success'] and r['accuracy']==1.0)) for r in rows)/len(rows)
            vals.append(val*100)
        bars=ax.bar(xs+delta,vals,width=.34,color=color,label=text)
        for bar,val in zip(bars,vals):
            ax.text(bar.get_x()+bar.get_width()/2,val+2,f'{val:.0f}%',ha='center',va='bottom',fontsize=14,fontweight='bold')
    ax.set_title(label,fontsize=21,loc='left',pad=20,fontweight='bold')
    ax.set_xticks(xs,[t for t,_ in modes],fontsize=13)
    ax.set_yticks([0,25,50,75,100],['0%','25%','50%','75%','100%'],fontsize=13)
    ax.set_ylim(0,116)
    ax.grid(axis='y',alpha=.2)
    ax.set_axisbelow(True)
    for side in ('top','right'):
        ax.spines[side].set_visible(False)
fig.suptitle('Three models, three harnesses, one connector task',fontsize=29,fontweight='bold',y=.95)
fig.text(.5,.89,'Simulated task · 3 trials per model and mode · same task and scoring',ha='center',fontsize=17,color='#555')
fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.5,.12),ncol=2,frameon=False,fontsize=17)
fig.text(.5,.055,'Exploratory single-task comparison; models used different hardware and serving configurations.',ha='center',fontsize=14,color='#555')
fig.tight_layout(rect=(.03,.23,.98,.86),w_pad=3)
fig.savefig(root/'head-to-head.png')
