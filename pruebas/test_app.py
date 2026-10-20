import joblib,pandas as pd,pytest
from fastapi.testclient import TestClient
from app import app
from esquema import FEATURES
E=dict(zip(FEATURES,[72,120,60,2,180,2,80]))
@pytest.fixture
def client():
    with TestClient(app) as c:yield c
def test_salud(client):assert client.get('/salud').status_code==200
def test_prediccion(client):
    r=client.post('/predecir',json=E);assert r.status_code==200
    d=r.json();assert d['falla_30_dias'] in [0,1] and 0<=d['puntaje']<=1 and d['modelo']
@pytest.mark.parametrize('field,value',[('carga_promedio_pct',101),('horas_uso_semana',-1),('temperatura_promedio',121),('incidentes_previos',1.5)])
def test_invalido(client,field,value):assert client.post('/predecir',json={**E,field:value}).status_code==422
def test_faltante(client):
    x=E.copy();x.pop('carga_promedio_pct');assert client.post('/predecir',json=x).status_code==422
def test_extra(client):assert client.post('/predecir',json={**E,'falla_30_dias':1}).status_code==422
def test_paridad_pipeline(client):
    a=joblib.load('modelos/modelo.joblib');p=float(a['pipeline'].predict_proba(pd.DataFrame([E],columns=FEATURES))[0,1]);assert client.post('/predecir',json=E).json()['puntaje']==pytest.approx(p,abs=1e-12)
