import json,statistics
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
E=Path('evidencias')
events=[json.loads(x) for x in (E/'kanban_eventos.jsonl').read_text().splitlines()]
results=[]
for cycle in sorted({e['ciclo'] for e in events}):
    ev=[e for e in events if e['ciclo']==cycle];starts={};dur=[];wip=0;peak=0
    for e in ev:
        t=datetime.fromisoformat(e['fecha'])
        if e['estado']=='inicio':starts[e['tarea']]=t;wip+=1;peak=max(peak,wip)
        elif e['estado']=='fin':dur.append((t-starts[e['tarea']]).total_seconds()/60);wip-=1
    elapsed=(datetime.fromisoformat(ev[-1]['fecha'])-datetime.fromisoformat(ev[0]['fecha'])).total_seconds()/60
    results.append({'ciclo':cycle,'completadas':len(dur),'tiempo_ciclo_promedio_min':statistics.mean(dur),'ventana_min':elapsed,'rendimiento_por_hora':len(dur)*60/elapsed,'wip_max':peak,'wip_final':wip})
(E/'agilidad.json').write_text(json.dumps(results,indent=2))
plt.rcParams.update({'font.size':11,'font.family':'DejaVu Sans'})
d=pd.read_csv(E/'experimentos.csv');fig,ax=plt.subplots(figsize=(9,3.2));x=range(len(d));ax.bar([v-.18 for v in x],d.precision,width=.36,label='Precisión',color='#12608a');ax.bar([v+.18 for v in x],d.recall,width=.36,label='Recall',color='#df832d');ax.axhline(.5,color='black',linestyle='--',label='Puerta recall 0,50');ax.set_xticks(list(x),d.id);ax.set_ylim(0,1);ax.set_ylabel('Proporción (validación)');ax.legend(ncol=3,fontsize=9);fig.tight_layout();fig.savefig(E/'experimentos.png',dpi=160);plt.close(fig)
t=json.loads((E/'test_final.json').read_text());fig,ax=plt.subplots(figsize=(6,3));m=[[t['tn'],t['fp']],[t['fn'],t['tp']]];ax.imshow(m,cmap='Blues');
for i in range(2):
    for j in range(2):ax.text(j,i,str(m[i][j]),ha='center',va='center',fontsize=20,color='white' if m[i][j]>150 else 'black')
ax.set_xticks([0,1],['Sin alerta','Con alerta']);ax.set_yticks([0,1],['Sin falla','Con falla']);ax.set_xlabel('Predicción');ax.set_ylabel('Resultado sintético');fig.tight_layout();fig.savefig(E/'confusion.png',dpi=160);plt.close(fig)
root=ET.parse(E/'pruebas_verdes.xml').getroot();suites=list(root.iter('testsuite'));summary={k:sum(int(s.get(k,0)) for s in suites) for k in ['tests','failures','errors','skipped']};(E/'tests_resumen.json').write_text(json.dumps(summary,indent=2))
print('Agilidad',results,'Pruebas',summary)
