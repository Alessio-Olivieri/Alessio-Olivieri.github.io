"""Regenerate exact SVG charts: python3 tools/render_figures.py (matplotlib required)."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/projects'
data=json.loads((OUT/'data/benchmarks.json').read_text())
BG='#111c27'; TEXT='#e9f1f3'; MUTED='#a6b5c0'; GRID='#293745'; MINT='#a7f0d1'; PURPLE='#c7c4ff'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'text.color':TEXT,'axes.labelcolor':MUTED,'xtick.color':MUTED,'ytick.color':TEXT,'axes.edgecolor':GRID,'figure.facecolor':BG,'axes.facecolor':BG,'svg.fonttype':'none','svg.hashsalt':'alessio-portfolio','savefig.facecolor':BG})
def axbase(ax):
 for sp in ax.spines.values():sp.set_visible(False)
 ax.set_axisbelow(True);ax.xaxis.grid(True,color=GRID,linewidth=.8)
 ax.tick_params(axis='both',length=0,pad=10)
def save(fig,name):
 fig.savefig(OUT/name,format='svg',metadata={'Date':None},bbox_inches='tight',pad_inches=.24)
 from matplotlib.text import Text
 translations=json.loads((ROOT/'locales/charts.it.json').read_text())
 for axis in fig.axes:
  labels=['\n'.join(translations.get(line,line) for line in label.get_text().split('\n')) for label in axis.get_yticklabels()]
  axis.set_yticks(axis.get_yticks(),labels)
 for artist in fig.findobj(Text):
  original=artist.get_text()
  artist.set_text('\n'.join(translations.get(line,line) for line in original.split('\n')))
 fig.savefig(OUT/name.replace('.svg','.it.svg'),format='svg',metadata={'Date':None},bbox_inches='tight',pad_inches=.24)
 plt.close(fig)
# Timings are complete workload durations, not per-image latency.
fig,ax=plt.subplots(figsize=(9.6,4.8));fig.subplots_adjust(left=.26,right=.89,bottom=.18,top=.82)
rows=data['vit']['conditions'];y=np.arange(3)
ax.barh(y,[r['seconds'] for r in rows],height=.45,color=[PURPLE,'#6e92b4',MINT])
ax.set_yticks(y,[r['label']+'\n'+str(r['heads_removed'])+'/48 heads removed' for r in rows]);ax.invert_yaxis();ax.set_xlim(0,7.5);ax.set_xlabel('Evaluation time (seconds) · lower is better',labelpad=14)
for i,r in enumerate(rows):ax.text(r['seconds']+.13,i,f"{r['seconds']:.2f} s",va='center',fontsize=15,fontweight='bold')
axbase(ax);fig.text(.035,.96,'Smaller circuit, faster CPU evaluation',fontsize=20,fontweight='bold',va='top');fig.text(.035,.885,'Ryzen 7 4700U · mean of 10 runs · before retraining',fontsize=11,color=MUTED,va='top')
save(fig,'vit-timing.svg')
# Fixed-split seed variation: error bars are SD, not confidence intervals.
fig,ax=plt.subplots(figsize=(9.6,5.4));fig.subplots_adjust(left=.31,right=.91,bottom=.18,top=.8)
rows=data['traffic']['conditions'];y=np.arange(4)
ax.barh(y,[r['accuracy'] for r in rows],height=.45,color=[MINT,'#6e92b4','#6e92b4',PURPLE],xerr=[r['sd'] for r in rows],error_kw={'ecolor':TEXT,'capsize':4,'elinewidth':1.3})
ax.set_yticks(y,[r['label'] for r in rows]);ax.invert_yaxis();ax.set_xlim(0,103);ax.set_xticks([0,25,50,75,100]);ax.set_xlabel('Accuracy (%) · mean ± sample SD',labelpad=14)
for i,r in enumerate(rows):ax.text(4,i,f"{r['accuracy']:.2f}%",color=BG,va='center',fontweight='bold',fontsize=13)
axbase(ax);fig.text(.035,.96,'Payload information is not just ciphertext',fontsize=19,fontweight='bold',va='top');fig.text(.035,.885,'3 training seeds · one flow-disjoint split · 250 test samples',fontsize=11,color=MUTED,va='top')
save(fig,'traffic-ablation.svg')
# Two different winners; group bars share the full 0-100 scale.
fig,ax=plt.subplots(figsize=(9.6,5));fig.subplots_adjust(left=.25,right=.92,bottom=.19,top=.74)
rows=data['surgery']['conditions'];y=np.arange(2)
ax.barh(y-.16,[r['accuracy'] for r in rows],height=.27,color=MINT,label='Frame accuracy')
ax.barh(y+.16,[r['segmental_f1'] for r in rows],height=.27,color=PURPLE,label='Mean segmental F1')
ax.set_yticks(y,['MS-TCN · 11 layers\nteammates features','SF-TMN\noriginal features']);ax.invert_yaxis();ax.set_xlim(0,102);ax.set_xticks([0,25,50,75,100]);ax.set_xlabel('Score (%) · higher is better',labelpad=14)
for i,r in enumerate(rows):
 for offset,key in [(-.16,'accuracy'),(.16,'segmental_f1')]:ax.text(r[key]-2,i+offset,f'{r[key]:.2f}',ha='right',va='center',fontweight='bold',fontsize=12,color=BG)
axbase(ax);fig.text(.035,.97,'The most accurate model is not the best segmenter',fontsize=18,fontweight='bold',va='top');fig.text(.035,.897,'Cholec80 · 40 held-out videos · raw model outputs',fontsize=11,color=MUTED,va='top')
ax.legend(loc='lower left',bbox_to_anchor=(0,1.06),ncol=2,frameon=False,fontsize=11,labelcolor=TEXT)
save(fig,'surgical-comparison.svg')
print('Rendered 3 charts in English and Italian from the same benchmark values')

# Normalize generated SVG whitespace for clean source diffs.
for svg in OUT.glob('*.svg'):
 svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
