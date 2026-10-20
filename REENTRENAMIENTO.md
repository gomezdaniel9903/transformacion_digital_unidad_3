# Regla propuesta de reentrenamiento

1. Deriva: alerta de una variable en dos lotes semanales consecutivos, cada uno de al menos 200 equipos comparables, con p ajustado Holm <0,01 y D de KS >=0,10. Abrir diagnóstico de sensores, población y procesos antes de entrenar.
2. Desempeño: recall <0,50 en dos cohortes mensuales consecutivas con horizonte de 30 días completamente observado y al menos 50 fallas confirmadas por cohorte. Informar intervalo Wilson de 95 %. Con menos eventos, acumular observaciones y revisar manualmente. El umbral operativo definitivo lo fija el negocio.
3. Tiempo: revisión programada cada 90 días. Reentrenar solo con etiquetas maduras, datos comparables y suficiente evidencia. El calendario no obliga a desplegar.

Un modelo candidato sigue validación de datos, experimentos, evaluación en una ventana temporal futura y puerta de calidad. Si falla, no reemplaza el vigente. Si el modelo vigente también es inadecuado, suspender su uso decisorio y volver a inspección y mantenimiento preventivo habitual, no mantenerlo por inercia. Aprobación conjunta de mantenimiento y TI, versión del modelo y plan de reversión.

Deriva de entradas no prueba pérdida de recall ni deriva de concepto. Para comprobarlas se necesitan fallas posteriores reales. El predictor modifica la decisión de inspección y puede modificar la etiqueta observada: registrar inspecciones e intervenciones para evitar evaluar prevención exitosa como una falsa alarma sin análisis.
