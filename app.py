from contextlib import asynccontextmanager
from pathlib import Path
import os
import joblib,pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel,Field,ConfigDict
from esquema import FEATURES
class Equipo(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False)
    antiguedad_equipo_meses:int=Field(ge=0,le=240)
    horas_uso_semana:float=Field(ge=0,le=168)
    temperatura_promedio:float=Field(ge=-20,le=120)
    mantenimientos_ultimo_anio:int=Field(ge=0,le=24)
    dias_desde_ultimo_mantenimiento:int=Field(ge=0,le=730)
    incidentes_previos:int=Field(ge=0,le=30)
    carga_promedio_pct:float=Field(ge=0,le=100)
@asynccontextmanager
async def lifespan(app):
    app.state.modelo=joblib.load(Path(os.getenv('MODEL_PATH','modelos/modelo.joblib')))
    if app.state.modelo['features']!=FEATURES:raise RuntimeError('Contrato de columnas incompatible')
    yield
app=FastAPI(title='Comercial Andina - demostrador sintético',lifespan=lifespan)
@app.get('/salud')
def salud():return {'estado':'activo','modelo':app.state.modelo['run_id'],'uso':'demostracion_sintetica'}
@app.post('/predecir')
def predecir(e:Equipo):
    a=app.state.modelo;x=pd.DataFrame([e.model_dump()],columns=FEATURES);prob=float(a['pipeline'].predict_proba(x)[0,1]);pred=int(prob>=a['umbral_clasificacion'])
    return {'falla_30_dias':pred,'puntaje':prob,'umbral':a['umbral_clasificacion'],'modelo':a['run_id'],'accion':'revision_humana' if pred else 'seguimiento_habitual','advertencia':'Puntaje de datos sinteticos. No es probabilidad industrial validada.'}
