# Comercial Andina - Taller Unidad 3, caso B

Estado: preliminar con ejecución local. Datos sintéticos. GitHub Actions y Docker pendientes de ejecución externa. No apto para decisiones industriales reales.

## Entorno
Python 3.12.14 fue el intérprete local disponible. La guía permite Python 3.11 o superior. Docker y CI usan 3.12 para evitar cambiar la versión menor respecto al entrenamiento, en lugar del ejemplo 3.11 de la receta. Las versiones de bibliotecas se fijan exactamente.

Crear entorno: `python -m venv .venv`, activarlo y ejecutar `python -m pip install -r requirements.txt`. Ejecutar comandos desde esta carpeta.

## Recorrido
1. `python generar_datos.py`: regenera los datos y las particiones con semilla fija.
2. `python reconstruir.py`: valida, entrena el modelo seleccionado, registra MLflow y aplica la puerta. No usa el test final para seleccionar otra vez.
3. `python -m pytest -q pruebas`: valida datos, API y paridad entrenamiento-servicio.
4. `uvicorn app:app --host 127.0.0.1 --port 8000`: servicio local. En otra terminal, `python verificar_http.py`.
5. `mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000`: ver ejecuciones. No exponer sin autenticación.
6. `python monitoreo.py`: compara el lote sintético desplazado. Código 1 significa alerta esperada, no falla del programa.
7. `docker build -t andina-operacion .`, después `docker run --rm -p 8000:8000 andina-operacion`. Repetir la prueba HTTP. Requiere Docker Desktop o Codespaces.

Los experimentos originales y la evaluación final se conservan en evidencias. `ejecutar_experimentos.py` reproduce el estudio completo, pero se debe ejecutar en una copia para no mezclar nuevos registros con la evidencia original. En MLflow, la métrica `recall` de las variantes corresponde a validación. El test final solo aparece en `test_final.json`.

## GitHub cuando el equipo tenga cuenta
Crear repositorio privado vacío y conectar esta carpeta con `git remote add origin URL`. Revisar `git status` y que no se incluyan .venv, modelos o datos personales. Subir con `git push -u origin HEAD`. El flujo prueba, reconstruye y construye Docker. GitHub requiere que las acciones estén habilitadas y disponer de cuota.

Primero conservar la ejecución verde. Después, en Actions, ejecutar manualmente con `umbral=1.01`: debe fallar en entrenamiento y no ejecutar pruebas ni Docker. Repetir con 0.50 para restaurar ejecución verde. Guardar URL, SHA y capturas reales. Si el docente exige la demostración mediante push, cambiar temporalmente la puerta en el YAML en una rama de prueba, subir y revertir con otro commit. El rechazo es intencional y debe documentarse como tal.

El flujo preparado no acredita ninguna ejecución en GitHub. El archivo Dockerfile no acredita un contenedor construido. `verificar_http.py` documenta la API local; cuando se ejecute contra Docker se debe guardar aparte esa evidencia.

## Archivos de la entrega preliminar
El PDF está en la carpeta informe del paquete ZIP. GUIA_EXPLICACION.md desarrolla el recorrido para la sustentación y MODEL_CARD.md documenta el modelo. El paquete incluye datos, campeón, registros y una copia SQLite de MLflow; no incluye el entorno virtual. MLflow puede conservar rutas absolutas del equipo original para sus artefactos: en otro equipo use los archivos de modelos incluidos o reconstruya; no asuma que esas rutas se trasladan automáticamente.

El archivo historial.bundle conserva los commits de v1, v2, v3 y cierre. Para recuperar ese historial en otra carpeta: `git clone historial.bundle proyecto_recuperado`. El clone incluye los archivos versionados, no modelos, base MLflow ni los registros excluidos; copie esos elementos del ZIP o reconstrúyalos. En el equipo original el repositorio ya está completo en esta carpeta.

El informe se generó con ReportLab y pypdf del entorno documental disponible; no son dependencias del servicio. Para regenerarlo en otra máquina instale esas herramientas y adapte las rutas de fuentes Arial en crear_informe.py. El PDF entregado no requiere instalaciones.

## Equipo y metodología
Los roles de negocio, mantenimiento, TI y gestión del cambio están propuestos, sin atribuirlos a estudiantes que no han participado todavía. El registro Kanban refleja el trabajo local asistido de esta sesión y su tiempo de pared. No equivale a velocidad o productividad del equipo de 3-4 personas. El equipo debe ejecutar dos ciclos reales y sustituir o complementar esas métricas antes de entregar.
