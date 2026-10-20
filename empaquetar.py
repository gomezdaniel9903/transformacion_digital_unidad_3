"""Paquete portátil: sin entorno virtual, cachés ni directorio interno de Git."""
from pathlib import Path
import os,zipfile,json,hashlib,sqlite3
P=Path(__file__).parent
out=P.parents[1]/'output/pdf/taller_unidad3_operacion'
db=sqlite3.connect(P/'mlflow.db')
snapshot=sqlite3.connect(out/'mlflow_respaldo.db')
db.backup(snapshot);snapshot.close();db.close()
dest=out/'Proyecto_preliminar_CasoB.zip'
excluded={'.venv','.git','__pycache__','.pytest_cache'}
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
    for root,dirs,files in os.walk(P):
        dirs[:]=[d for d in dirs if d not in excluded]
        for name in files:
            f=Path(root)/name
            if name.startswith('mlflow.db') or name.endswith('.tmp'):continue
            z.write(f,'proyecto/'+f.relative_to(P).as_posix())
    z.write(out/'mlflow_respaldo.db','proyecto/mlflow.db')
    z.write(out/'historial.bundle','historial.bundle')
    z.write(out/'Informe_preliminar_Unidad3_CasoB.pdf','informe/Informe_preliminar_Unidad3_CasoB.pdf')
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    assert 'proyecto/.github/workflows/pruebas.yml' in z.namelist()
    assert 'proyecto/modelos/modelo.joblib' in z.namelist()
    assert not any('/.venv/' in x or '/.git/' in x for x in z.namelist())
    n=len(z.namelist())
print(json.dumps({'archivo':str(dest),'archivos':n,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()},indent=2))
