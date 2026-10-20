import numpy as np
import pandas as pd
FEATURES=['antiguedad_equipo_meses','horas_uso_semana','temperatura_promedio','mantenimientos_ultimo_anio','dias_desde_ultimo_mantenimiento','incidentes_previos','carga_promedio_pct']
TARGET='falla_30_dias'
RANGES=dict(zip(FEATURES,[(0,240),(0,168),(-20,120),(0,24),(0,730),(0,30),(0,100)]))
INTEGERS=[FEATURES[i] for i in [0,3,4,5]]
def validar(path,objetivo=True,min_filas=1):
    d=pd.read_csv(path);expected=FEATURES+([TARGET] if objetivo else [])
    if set(d.columns)!=set(expected): raise ValueError('Columnas: faltantes o adicionales respecto al contrato')
    if len(d)<min_filas: raise ValueError('Cantidad de filas insuficiente')
    if d.isna().any().any(): raise ValueError('Valores vacíos: tolerancia cero')
    for c in expected:
        if not pd.api.types.is_numeric_dtype(d[c]) or not np.isfinite(d[c]).all(): raise ValueError('Dato no numérico o no finito: '+c)
    for c,(lo,hi) in RANGES.items():
        if not d[c].between(lo,hi).all(): raise ValueError('Fuera de rango: '+c)
    for c in INTEGERS:
        if not (d[c]%1==0).all(): raise ValueError('Se requiere entero: '+c)
    if objetivo and not d[TARGET].isin([0,1]).all(): raise ValueError('Objetivo debe ser 0 o 1')
    if objetivo and d[TARGET].nunique()!=2: raise ValueError('Se requieren ambas clases')
    return d
