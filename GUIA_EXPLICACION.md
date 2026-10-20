# Explicación paso a paso para sustentar el taller

## 1. Qué pide el docente
Un proyecto que conecte estrategia de negocio, organización ágil, adopción y MLOps. El entregable principal es un informe sin código, con cifras verificables. El objetivo no es presumir un modelo perfecto: es explicar cómo impedir que datos o modelos malos se utilicen sin control.

El caso B pregunta qué equipos de tienda y bodega podrían fallar durante los siguientes 30 días. Esto es clasificación supervisada: cada ejemplo tiene siete características y una respuesta conocida, falla_30_dias=0 o 1. No estamos haciendo pronóstico meteorológico ni usando datos de tesis.

## 2. Por qué generamos datos
La guía permite datos sintéticos y exige al menos 1500 filas, semilla fija, señal procedente de 3 o 4 variables, ruido y entre 20% y 35% de positivos. Generamos 2400 filas, con 647 fallas (26,96%) y cero vacíos. No son 2400 equipos observados: son ejemplos inventados reproducibles.

En generar_datos.py, `np.random.default_rng(seed)` fija la secuencia aleatoria. La combinación de uso, temperatura, tiempo sin mantenimiento e incidentes produce un puntaje. La función logística lo convierte a probabilidad y un sorteo Bernoulli decide la etiqueta. Por ello dos equipos parecidos pueden tener resultados distintos. No afirmamos haber descubierto causalidad física.

## 3. Qué hace la validación
`validar()` en esquema.py lee el archivo y comprueba columnas, tipos, vacíos, infinitos, rangos y objetivo binario. `raise ValueError(...)` detiene el proceso antes de entrenar. Introdujimos deliberadamente horas de uso negativas: el entrenamiento se detuvo y el archivo original quedó preservado. Las pruebas adicionales cubren otras corrupciones.

## 4. Por qué separamos tres grupos
1. Entrenamiento: 1440 filas para aprender parámetros.
2. Validación: 480 filas para comparar alternativas y elegir.
3. Prueba: 480 filas reservadas hasta finalizar la selección.

`stratify` conserva aproximadamente la proporción de fallas. Los índices quedan guardados en particiones.json. El test no se usa para escoger una variante. En una implementación real se debe separar también por tiempo y equipo; nuestra partición aleatoria sirve para ejemplos sintéticos independientes.

## 5. Qué aprende el modelo
En entrenamiento_lib.py, `make_pipeline(StandardScaler(), LogisticRegression(...))` une preparación y clasificación. El escalador transforma cada entrada usando media y desviación aprendidas solo en entrenamiento. El clasificador aprende coeficientes para distinguir clases. `fit` aprende; `predict_proba` entrega puntuaciones. El mismo Pipeline se guarda y se usa en la API para impedir preparaciones diferentes.

El bosque aleatorio combina 200 árboles, limitados a profundidad 5 y 10 ejemplos por hoja. Probamos ambos algoritmos con y sin balanceo, más un control que siempre predice la clase mayoritaria. `class_weight='balanced'` aumenta el peso de la clase minoritaria al aprender; no crea equipos ni cambia etiquetas.

## 6. Cómo se eligió E2
La puerta exige recall >=0,50 y se fijó después del modelo base. Entre los modelos que la pasan, escogimos el de mayor F1 de validación. Ganó la regresión logística balanceada E2. MLflow registra parámetros, métricas, identificadores y artefactos para que la decisión pueda revisarse.

Hay dos umbrales diferentes: 0,50 sobre la puntuación convierte cada predicción en 0/1; 0,50 sobre el recall decide si se acepta el modelo completo. Coinciden numéricamente pero responden preguntas distintas. La guía permite una puerta baja porque usa datos sintéticos.

## 7. Cómo interpretar el resultado final
| Realidad del ejemplo | Sin alerta | Con alerta |
|---|---:|---:|
| No falló | 232 verdaderos negativos | 118 falsos positivos |
| Falló | 35 falsos negativos | 95 verdaderos positivos |

- Recall: 95/(95+35)=73,08%. De las 130 fallas, detectó 95.
- Precisión: 95/(95+118)=44,60%. De 213 alertas, 95 correspondieron a falla.
- Exactitud: (95+232)/480=68,13%. Proporción total de aciertos.
- F1: 55,39%. Media armónica de precisión y recall; no incluye directamente costos monetarios.

Un clasificador que siempre diga «no falla» lograría 72,92% de exactitud pero no detectaría ninguna falla. Por eso la exactitud sola no resuelve este problema. E2 detecta fallas, pero exige revisar muchas alertas equivocadas. La decisión de negocio depende del costo de no detectar una falla y de la capacidad de inspección.

El intervalo de confianza del recall es aproximadamente 64,9%-80,0% bajo este generador. No quiere decir que el modelo tendrá ese desempeño en cualquier tienda. Tampoco garantiza que una inspección evite la falla.

## 8. Qué protege la puerta de calidad
Si el recall no cumple, el programa termina con código 1 y no guarda el candidato. Probamos una puerta imposible de 1,01 para forzar rechazo. El hash del campeón no cambió: conservó exactamente los mismos bytes. Esto demuestra protección técnica del archivo; todavía falta demostrar el flujo rojo en GitHub.

## 9. Qué hace la API
`GET /salud` confirma que el modelo cargó. `POST /predecir` recibe las siete entradas. Pydantic rechaza valores imposibles; el modelo devuelve puntuación, clase y versión. La respuesta propone revisión humana, no detener automáticamente un equipo. Verificamos mediante HTTP real los códigos 200 para salud, 200 para predicción válida y 422 para datos inválidos.

## 10. Qué prueban los tests
Quince casos verifican salud, respuestas, entradas inválidas, equivalencia con el Pipeline y validaciones de datos. Relajamos temporalmente el máximo de carga de 100 a 110: una prueba lo detectó. Después restauramos la regla y las 15 volvieron a pasar. No basta con que una prueba siempre esté verde: también comprobamos que encuentra un error conocido.

## 11. Qué significa la deriva
Generamos 800 equipos nuevos y una copia con temperatura aumentada en 12 °C. KS compara las distribuciones con entrenamiento; Holm ajusta las siete comparaciones y se exige también D>=0,10. Solo temperatura generó alerta; el control no tuvo alertas. Esto indica cambio de datos, no demuestra por sí solo pérdida de recall ni causa de fallas. Con conteos y empates el p de KS requiere cautela, expresada en el informe.

## 12. Qué aportan las partes no técnicas
Estrategia: define por qué interesa reducir paradas y costo correctivo; las bases económicas son supuestos, no resultados observados. Kanban: hace visible el trabajo y sus bloqueos. ADKAR: diferencia entender, querer, saber, poder y mantener el uso. Riesgos: reconoce falsas alarmas, fallas omitidas, privacidad y uso indebido de métricas laborales.

Las dos ventanas registradas son de trabajo local asistido, con tiempo de pared real. No equivalen a dos ciclos realizados por el equipo académico. Las metas de adopción son propuestas, no encuestas ni capacitaciones ya realizadas.

## 13. Qué queda cuando tengas GitHub
El código, los datos, las versiones, el historial Git y el flujo están preparados. Faltan subir al repositorio, ejecutar CI verde/rojo y restaurado, construir y consultar Docker, conservar capturas reales y completar los ciclos del equipo. README contiene los pasos. La compatibilidad Linux está pendiente de esa ejecución, no se da por demostrada.

## Guion corto para exponer
«Elegimos priorizar inspecciones, no automatizar paradas. Construimos un proceso reproducible con datos sintéticos permitidos por la guía. Separamos entrenamiento, validación y prueba, comparamos cinco variantes y elegimos por F1 entre las que cumplen recall. En 480 casos reservados detectamos 95 de 130 fallas, con 118 falsas alertas. Demostramos rechazo de datos, de modelos y de entradas inválidas, además de monitoreo. El resultado es un preliminar técnico; antes de operar se necesitan datos reales, validación temporal, capacidad de atención y adopción del personal».
