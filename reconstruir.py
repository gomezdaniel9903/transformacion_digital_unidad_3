"""Reconstrucción exacta del campeón congelado; no vuelve a seleccionar."""
import argparse,json,subprocess,sys
from pathlib import Path
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--umbral',type=float,default=.50);o=a.parse_args()
    s=json.loads(Path('seleccion.json').read_text())
    cmd=[sys.executable,'entrenar.py','--modelo',s['modelo'],'--c',str(s['C']),'--profundidad',str(s['profundidad']),'--umbral',str(o.umbral)]
    if s['balanceado']:cmd.append('--balanceado')
    sys.exit(subprocess.call(cmd))
