import json,subprocess,sys
from pathlib import Path
from generar_datos import generar
from esquema import validar,FEATURES
from monitoreo import comparar
def cmd(args,name):
    r=subprocess.run([sys.executable,*args],capture_output=True,text=True,encoding='utf-8',errors='replace');Path('evidencias/'+name+'.log').write_text(r.stdout+'\n'+r.stderr,encoding='utf-8');return r
if __name__=='__main__':
    original=validar('datos/equipos.csv');bad=original.copy();bad.loc[0,'horas_uso_semana']=-1;bad.to_csv('datos/invalido_temporal.csv',index=False)
    r=cmd(['entrenar.py','--datos','datos/invalido_temporal.csv'],'validacion_roja');assert r.returncode!=0 and 'Fuera de rango' in r.stderr;Path('datos/invalido_temporal.csv').unlink()
    good=cmd(['-m','pytest','-q','pruebas','--junitxml=evidencias/pruebas_verdes.xml'],'pruebas_verdes');assert good.returncode==0,good.stdout+good.stderr
    app=Path('app.py');source=app.read_text(encoding='utf-8')
    try:
        app.write_text(source.replace('carga_promedio_pct:float=Field(ge=0,le=100)','carga_promedio_pct:float=Field(ge=0,le=110)'),encoding='utf-8')
        red=cmd(['-m','pytest','-q','pruebas/test_app.py'],'pruebas_rojas_mutacion');assert red.returncode!=0 and 'test_invalido' in red.stdout
    finally:app.write_text(source,encoding='utf-8')
    restored=cmd(['-m','pytest','-q','pruebas','--junitxml=evidencias/pruebas_verdes.xml'],'pruebas_verdes_restauradas');assert restored.returncode==0
    ix=json.loads(Path('datos/particiones.json').read_text());ref=original.iloc[ix['train']];prod,_=generar(800,20261020);prod=prod[FEATURES];prod.to_csv('datos/produccion_control.csv',index=False)
    baseline=comparar(ref,prod);Path('evidencias/monitoreo_control.json').write_text(json.dumps(baseline,indent=2))
    prod['temperatura_promedio']+=12;prod.to_csv('datos/produccion_deriva.csv',index=False)
    mon=cmd(['monitoreo.py'],'monitoreo_alerta');assert mon.returncode==1
    observed=json.loads(Path('evidencias/monitoreo.json').read_text());alerts=[r['variable'] for r in observed if r['alerta']];assert alerts==['temperatura_promedio'],alerts
    Path('evidencias/validaciones.json').write_text(json.dumps({'datos_corruptos_rechazados':r.returncode!=0,'pruebas_verdes_codigo':good.returncode,'mutacion_detectada':red.returncode!=0,'restauracion_codigo':restored.returncode,'alertas_control':[r['variable'] for r in baseline if r['alerta']],'alertas_deriva':alerts},indent=2))
    print(restored.stdout);print('ALERTAS',alerts)
