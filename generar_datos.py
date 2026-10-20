"""Una fila por equipo sintético en una fecha de corte, sin datos personales."""
import json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import expit
from sklearn.model_selection import train_test_split
from esquema import FEATURES,TARGET,validar
SEED=20261019
def generar(n=2400,seed=SEED):
    r=np.random.default_rng(seed)
    d=pd.DataFrame({FEATURES[0]:r.integers(1,181,n),FEATURES[1]:r.uniform(15,160,n).round(2),FEATURES[2]:np.clip(r.normal(48,10,n),15,85).round(2),FEATURES[3]:r.integers(0,7,n),FEATURES[4]:r.integers(0,366,n),FEATURES[5]:r.poisson(1.5,n).clip(0,15),FEATURES[6]:r.uniform(20,100,n).round(2)})
    z=.5*(d[FEATURES[1]]-87.5)/42+.6*(d[FEATURES[2]]-48)/10+.5*(d[FEATURES[4]]-182.5)/105+.35*(d[FEATURES[5]]-1.5)/1.22+r.normal(0,.8,n)
    lo,hi=-8.,8.
    for _ in range(80):
        intercept=(lo+hi)/2
        if expit(z+intercept).mean()>.28:hi=intercept
        else:lo=intercept
    d[TARGET]=r.binomial(1,expit(z+intercept))
    return d,float(intercept)
if __name__=='__main__':
    Path('datos').mkdir(exist_ok=True);Path('evidencias').mkdir(exist_ok=True)
    d,b=generar();d.to_csv('datos/equipos.csv',index=False)
    validar('datos/equipos.csv',min_filas=1500)
    tr,rest=train_test_split(np.arange(len(d)),test_size=.4,stratify=d[TARGET],random_state=SEED)
    va,te=train_test_split(rest,test_size=.5,stratify=d.iloc[rest][TARGET],random_state=SEED)
    assert not(set(tr)&set(va)|set(tr)&set(te)|set(va)&set(te))
    parts={'train':tr.tolist(),'validation':va.tolist(),'test':te.tolist()}
    Path('datos/particiones.json').write_text(json.dumps(parts),encoding='utf-8')
    summary={'semilla':SEED,'filas':len(d),'columnas':len(d.columns),'positivos':int(d[TARGET].sum()),'prevalencia':float(d[TARGET].mean()),'vacios_pct':float(d.isna().mean().mean()*100),'intercepto':b,'dataset_sha256':hashlib.sha256(Path('datos/equipos.csv').read_bytes()).hexdigest(),'particiones':{k:len(v) for k,v in parts.items()},'nota':'Predictores independientes por diseño. No reproduce física de fallas ni un parque real.'}
    assert .20<=summary['prevalencia']<=.35
    Path('evidencias/datos.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(summary)
