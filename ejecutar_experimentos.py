import json,subprocess,sys,shutil,hashlib
from pathlib import Path
import joblib,pandas as pd
from esquema import FEATURES,TARGET
from metricas import medir,wilson
def run(cmd,name,expected=None):
    p=subprocess.run([sys.executable,*cmd],capture_output=True,text=True,encoding='utf-8',errors='replace')
    Path(f'evidencias/{name}.log').write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
    if expected is not None and p.returncode!=expected:raise RuntimeError(f'{name}: codigo {p.returncode}; revisar log')
    return p.returncode
if __name__=='__main__':
    if Path('evidencias/test_final.json').exists():raise RuntimeError('Evaluacion final ya existe. Usar copia limpia para reproducir.')
    cfgs=[('lr',False,1.,5),('lr',True,1.,5),('rf',False,1.,5),('rf',True,1.,5),('dummy',False,1.,5)]
    records=[]
    for k,(model,balance,C,depth) in enumerate(cfgs):
        dest=f'modelos/candidatos/e{k+1}.joblib';cmd=['entrenar.py','--modelo',model,'--c',str(C),'--profundidad',str(depth),'--destino',dest]
        if balance:cmd+=['--balanceado']
        rc=run(cmd,f'experimento_{k+1}')
        row=json.loads(Path('evidencias/experimentos.jsonl').read_text().splitlines()[-1]);row['archivo']=dest;row['salida']=rc;row['id']=f'E{k+1}';records.append(row)
        assert rc==(0 if row['puerta'] else 1)
        if not row['puerta']:assert not Path(dest).exists()
    passed=[r for r in records if r['puerta']]
    assert passed and any(not r['puerta'] for r in records)
    best=max(passed,key=lambda r:(r['f1'],r['precision']))
    shutil.copy2(best['archivo'],'modelos/modelo.joblib');Path('seleccion.json').write_text(json.dumps(best,indent=2))
    pd.DataFrame(records).to_csv('evidencias/experimentos.csv',index=False)
    # Test reservado: evaluación única del artefacto seleccionado, sin ajustar.
    d=pd.read_csv('datos/equipos.csv');ix=json.loads(Path('datos/particiones.json').read_text());te=d.iloc[ix['test']];a=joblib.load('modelos/modelo.joblib');probs=a['pipeline'].predict_proba(te[FEATURES])[:,1]
    result=medir(te[TARGET],probs);result['recall_ic95']=wilson(result['tp'],result['tp']+result['fn']);result['precision_ic95']=wilson(result['tp'],result['tp']+result['fp']);result['modelo']=best['id'];result['mayoria_accuracy']=float(1-te[TARGET].mean());result['prevalencia_test']=float(te[TARGET].mean());result['modelo_sha256']=hashlib.sha256(Path('modelos/modelo.joblib').read_bytes()).hexdigest()
    Path('evidencias/test_final.json').write_text(json.dumps(result,indent=2));pd.DataFrame({'real':te[TARGET].to_numpy(),'puntaje':probs}).to_csv('evidencias/predicciones_test.csv',index=False)
    # Prueba adversa de promoción: candidato rechazado no destruye el vigente.
    before=Path('modelos/modelo.joblib').read_bytes();rc=run(['entrenar.py','--modelo','lr','--balanceado','--umbral','1.01'],'puerta_roja_forzada',1);assert before==Path('modelos/modelo.joblib').read_bytes()
    Path('evidencias/puerta.json').write_text(json.dumps({'rechazo_codigo':rc,'campeon_inalterado':True,'rechazados_sin_archivo':[r['id'] for r in records if not r['puerta']]},indent=2))
    print(json.dumps({'seleccion':best,'test':result},indent=2))
