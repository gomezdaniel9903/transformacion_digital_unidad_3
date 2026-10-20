import pandas as pd,pytest
from esquema import validar
@pytest.mark.parametrize('modo',['negativo','vacio','objetivo','columna','infinito'])
def test_rechaza_corruptos(tmp_path,modo):
    d=pd.read_csv('datos/equipos.csv')
    if modo=='negativo':d.loc[0,'horas_uso_semana']=-1
    if modo=='vacio':d.loc[0,'temperatura_promedio']=float('nan')
    if modo=='objetivo':d.loc[0,'falla_30_dias']=2
    if modo=='columna':d=d.drop(columns=['incidentes_previos'])
    if modo=='infinito':d.loc[0,'horas_uso_semana']=float('inf')
    p=tmp_path/'mal.csv';d.to_csv(p,index=False)
    with pytest.raises(ValueError):validar(p)
def test_original_valido():assert len(validar('datos/equipos.csv'))==2400
