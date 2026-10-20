import argparse,json,sys
from pathlib import Path
import numpy as np
from scipy.stats import ks_2samp
from esquema import FEATURES,validar
def comparar(a,b):
    rows=[]
    for c in FEATURES:
        ks=ks_2samp(a[c],b[c],method='auto');rows.append({'variable':c,'D':float(ks.statistic),'p':float(ks.pvalue)})
    order=sorted(range(len(rows)),key=lambda i:rows[i]['p']);last=0
    for k,i in enumerate(order):
        last=max(last,min(1,rows[i]['p']*(len(rows)-k)));rows[i]['p_holm']=last
    for r in rows:r['alerta']=r['p_holm']<.01 and r['D']>=.10
    return rows
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--produccion',default='datos/produccion_deriva.csv');s=a.parse_args()
    original=validar('datos/equipos.csv');ix=json.loads(Path('datos/particiones.json').read_text());reference=original.iloc[ix['train']]
    rows=comparar(reference,validar(s.produccion,objetivo=False));print(json.dumps(rows,indent=2));Path('evidencias/monitoreo.json').write_text(json.dumps(rows,indent=2))
    sys.exit(int(any(r['alerta'] for r in rows)))
