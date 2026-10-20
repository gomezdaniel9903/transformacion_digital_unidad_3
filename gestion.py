"""Registro real del flujo local. No simula fechas de un equipo humano."""
import argparse, json
from pathlib import Path
from datetime import datetime, timezone
P=Path('evidencias/kanban_eventos.jsonl')
def evento(ciclo,tarea,estado):
    P.parent.mkdir(exist_ok=True)
    with P.open('a',encoding='utf-8') as f:
        f.write(json.dumps(dict(fecha=datetime.now(timezone.utc).isoformat(),ciclo=ciclo,tarea=tarea,estado=estado),ensure_ascii=False)+'\n')
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('ciclo',type=int);a.add_argument('tarea');a.add_argument('estado',choices=['inicio','fin','bloqueada']);s=a.parse_args();evento(s.ciclo,s.tarea,s.estado)
