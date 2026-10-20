# Ficha del modelo - Operación, Comercial Andina

## Identidad y propósito
Versión preliminar 1.0, 19 de octubre de 2026. Ejecución MLflow seleccionada: `59f22c7ce39a40ed8de531e50fe932e7` (E2). Regresión logística balanceada, StandardScaler dentro del Pipeline, C=1, máximo 2000 iteraciones, semilla 20261019. Umbral de clasificación 0.50. Clasifica una falla sintética en los siguientes 30 días; apoyaría priorización de inspecciones, siempre con revisión humana.

## Datos
2.400 equipos sintéticos independientes, siete entradas numéricas y una etiqueta binaria, 647 positivos (26,958%). Sin información personal ni datos reales de Comercial Andina. Generador propio: señal logística de uso, temperatura, días desde mantenimiento e incidentes, más ruido; ver generar_datos.py y DEFINICION.md. Particiones estratificadas fijas: 1440 entrenamiento, 480 validación y 480 prueba. El escalador se ajustó solo con entrenamiento. No se reentrenó sobre validación después de elegir el modelo. El test reservado se evaluó una vez.

## Desempeño medido
| Conjunto | Exactitud | Precisión | Recall | F1 |
|---|---:|---:|---:|---:|
| Validación | 0.6708 | 0.4271 | 0.6589 | 0.5183 |
| Prueba reservada | 0.6813 | 0.4460 | 0.7308 | 0.5539 |

En prueba: VP=95, FN=35, FP=118, VN=232; 213 alertas de 480. IC95% Wilson de recall: [0.6487, 0.7996]. Precisión: [0.3808, 0.5131]. ROC-AUC=0.7478, AP=0.5246 frente a prevalencia=0.2708. Exactitud de clase mayoritaria=0.7292, con recall cero. No se estimó intervalo de diferencia entre modelos: no se afirma superioridad estadística general.

Selección: mayor F1 en validación entre candidatos con recall >=0.50; precisión para desempatar. La puerta baja cumple un propósito didáctico, no una certificación operativa. La puntuación balanceada NO se ha calibrado como probabilidad industrial. No se ha medido ahorro ni prevención real de fallas.

## Uso previsto y usos excluidos
Demostración académica de MLOps, pruebas de integración y preparación de un piloto en sombra. No usar para parar maquinaria, reemplazar mantenimiento, tomar decisiones de seguridad o evaluar trabajadores. No aplicar a datos IDEAM ni al proyecto DATAINNOVA.

## Límites
Las relaciones fueron inventadas por diseño; recuperar esa señal no valida relaciones físicas. Sin mediciones de tienda, cronología real, familias de equipos o sensores. La distribución entre variables es simplificada. En operación real habrá medidas repetidas, estacionalidad y etiquetas afectadas por intervenciones; se necesita separación temporal/por equipo y etiquetas maduras. El intervalo Wilson no representa incertidumbre de transferencia a producción. El volumen de falsas alertas puede superar capacidad de inspección. No hay garantías de equidad entre familias de activos porque no están identificadas.

## Operación y responsabilidad
Mantenedor propuesto: responsable de TI designado por el equipo, todavía sin nombre; dueño funcional: Operaciones y mantenimiento. No existe servicio industrial desplegado. API verificada en localhost; Docker y GitHub Actions preparados pero no ejecutados. Cargar únicamente artefactos joblib de origen confiable. Monitoreo y tres disparadores medibles en REENTRENAMIENTO.md. Si un candidato falla la puerta no reemplaza al vigente; si el vigente deja de ser apropiado, volver al procedimiento habitual.

SHA-256 del dataset: cfdfb2b08a0f8a3147a8017f823e5421db0bc75909f51b1c8c90bea915939291

SHA-256 del artefacto original: 105930208d7d948f298f7c32860a3b256b36b2c786808129dca316772f38d62e

## Apoyo de IA
Desarrollo asistido por OpenAI Codex. El equipo debe revisar, comprender, completar evidencias externas y asumir responsabilidad académica.
