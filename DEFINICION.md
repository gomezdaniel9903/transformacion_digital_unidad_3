# Caso B. Comercial Andina: operación

Pregunta: ¿qué equipos de tienda y bodega podrían fallar dentro de 30 días?
Unidad de análisis: un equipo ficticio, una observación de sus variables disponibles a la fecha de corte. No hay mediciones repetidas de equipos reales. Objetivo binario: falla_30_dias.
Decisión: priorizar inspección por mantenimiento. El servicio no ordena paradas ni interviene equipos automáticamente. Una puntuación no prueba una falla futura.

Datos: 2.400 filas sintéticas, siete predictores numéricos y una etiqueta. Semilla 20261019. La probabilidad logística usa horas de uso, temperatura, días sin mantenimiento e incidentes, más ruido normal de desviación 0,8. Intercepto calibrado para probabilidad media 0,28 antes del muestreo Bernoulli. La etiqueta no se fuerza a una cuota exacta.

Rangos de validación (supuestos del ejercicio, no límites de ingeniería): antigüedad 0-240 meses; uso 0-168 horas/semana; temperatura -20 a 120 °C; mantenimientos 0-24/año; días sin mantenimiento 0-730; incidentes 0-30; carga 0-100 %. Antigüedad, mantenimientos, días e incidentes son enteros. Temperatura se interpreta como una medición térmica comparable entre equipos de un mismo tipo; el caso real exige definir sensor, punto y ventana de agregación. Sin esa normalización, no se deben mezclar refrigeradores, motores y otros equipos.

Validación: esquema exacto, datos finitos, cero vacíos, rangos, conteos enteros y dos clases 0/1. Una violación detiene el entrenamiento. La prevalencia 20-35 % es una condición del dataset de entrenamiento sintético, no una regla para rechazar lotes reales de producción.

Partición estratificada fija 60/20/20 para entrenamiento/validación/prueba. Ajuste y selección solo en las dos primeras. Prueba final reservada. No se usa para cambiar hiperparámetros. En operación real se requiere validación temporal y agrupada por equipo para impedir fuga entre observaciones correlacionadas. La etiqueta madura 30 días después del corte.

Métrica principal: recall de fallas. Un falso negativo omite un equipo que fallará; un falso positivo consume una inspección. Puerta didáctica: se fijará tras observar el modelo base, entre 0,40 y 0,55 como pide el taller. No representa una autorización operativa. El umbral de probabilidad para clasificar (0,50) es distinto del recall mínimo de aceptación. Se reportan precisión, exactitud, F1, AP y matriz de confusión para evitar un clasificador que alerte siempre.

Sin datos reales no pueden inferirse prevalencia industrial, ahorro, reducción causal de fallas, confiabilidad de equipo ni calibración real. Los indicadores de negocio son metas propuestas para un piloto, no resultados ejecutados.
