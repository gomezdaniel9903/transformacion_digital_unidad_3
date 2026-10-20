import argparse,json,time
from pathlib import Path
import httpx
from esquema import FEATURES
def main():
    a=argparse.ArgumentParser();a.add_argument('--reintentos',type=int,default=1);a.add_argument('--puerto',type=int,default=8000);s=a.parse_args();url=f'http://127.0.0.1:{s.puerto}'
    for i in range(s.reintentos):
        try:r=httpx.get(url+'/salud',timeout=3);r.raise_for_status();break
        except (httpx.HTTPError,ConnectionError):
            if i==s.reintentos-1:raise
            time.sleep(1)
    e=dict(zip(FEATURES,[72,120,60,2,180,2,80]));p=httpx.post(url+'/predecir',json=e);bad=httpx.post(url+'/predecir',json={**e,'carga_promedio_pct':101});assert p.status_code==200 and bad.status_code==422
    result={'salud_status':r.status_code,'salud':r.json(),'prediccion_status':p.status_code,'prediccion':p.json(),'invalido_status':bad.status_code};Path('evidencias').mkdir(exist_ok=True);Path('evidencias/http.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
