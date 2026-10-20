import os
os.environ.setdefault('MLFLOW_ENABLE_TELEMETRY','false')
import argparse,json,hashlib,sys
from pathlib import Path
import joblib,mlflow
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from esquema import validar,FEATURES,TARGET
from metricas import medir
def main():
    a=argparse.ArgumentParser();a.add_argument('--modelo',choices=['lr','rf','dummy'],default='lr');a.add_argument('--balanceado',action='store_true');a.add_argument('--c',type=float,default=1.);a.add_argument('--profundidad',type=int,default=5);a.add_argument('--umbral',type=float,default=None);a.add_argument('--destino',default='modelos/modelo.joblib');a.add_argument('--datos',default='datos/equipos.csv');args=a.parse_args()
    d=validar(args.datos,min_filas=1500);ix=json.loads(Path('datos/particiones.json').read_text());tr=d.iloc[ix['train']];va=d.iloc[ix['validation']]
    gate=json.loads(Path('configuracion.json').read_text())['recall_minimo'] if args.umbral is None else args.umbral
    weight='balanced' if args.balanceado else None
    if args.modelo=='lr':m=make_pipeline(StandardScaler(),LogisticRegression(C=args.c,class_weight=weight,max_iter=2000,random_state=20261019))
    elif args.modelo=='rf':m=RandomForestClassifier(n_estimators=200,max_depth=args.profundidad,min_samples_leaf=10,class_weight=weight,random_state=20261019,n_jobs=1)
    else:m=DummyClassifier(strategy='most_frequent')
    mlflow.set_tracking_uri('sqlite:///mlflow.db');mlflow.set_experiment('Andina_B_Operacion')
    with mlflow.start_run(run_name=f'{args.modelo}_balance_{args.balanceado}') as run:
        mlflow.log_params({'modelo':args.modelo,'balanceado':args.balanceado,'C':args.c,'profundidad':args.profundidad,'semilla':20261019,'recall_minimo':gate,'umbral_clasificacion':.5,'dataset_sha256':hashlib.sha256(Path(args.datos).read_bytes()).hexdigest(),'particion':'validacion'})
        m.fit(tr[FEATURES],tr[TARGET]);metrics=medir(va[TARGET],m.predict_proba(va[FEATURES])[:,1]);mlflow.log_metrics(metrics)
        passed=metrics['recall']>=gate
        rec={'run_id':run.info.run_id,'modelo':args.modelo,'balanceado':args.balanceado,'C':args.c,'profundidad':args.profundidad,'puerta':passed,'recall_minimo':gate,**metrics}
        Path('evidencias').mkdir(exist_ok=True)
        with open('evidencias/experimentos.jsonl','a',encoding='utf-8') as f:f.write(json.dumps(rec)+'\n')
        mlflow.set_tag('puerta_calidad','APROBADA' if passed else 'RECHAZADA')
        if not passed:
            print('PUERTA RECHAZADA: no se modifica ni se guarda modelo',json.dumps(rec));return 1
        dest=Path(args.destino);dest.parent.mkdir(parents=True,exist_ok=True)
        artifact={'pipeline':m,'features':FEATURES,'umbral_clasificacion':.5,'run_id':run.info.run_id,'metricas_validacion':metrics,'tipo_datos':'sinteticos','version_esquema':'1.0'}
        joblib.dump(artifact,str(dest)+'.tmp');os.replace(str(dest)+'.tmp',dest);mlflow.log_artifact(str(dest),artifact_path='modelo_aprobado')
        print('PUERTA APROBADA',json.dumps(rec));return 0
if __name__=='__main__':sys.exit(main())
