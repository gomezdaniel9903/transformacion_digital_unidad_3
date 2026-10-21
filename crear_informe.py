"""Informe PRELIMINAR (liviano): tablas y cifras clave, texto mínimo, Anexo A (A1 y A2).
Punto de partida para redactar el informe final a mano. Texto 11 pt, interlineado 1,15, márgenes 2,5 cm."""
import json,html,math
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
P=Path(__file__).parent;E=P/'evidencias';OUT=P/'informe';OUT.mkdir(parents=True,exist_ok=True)
data=json.loads((E/'datos.json').read_text());test=json.loads((E/'test_final.json').read_text());selected=json.loads((P/'seleccion.json').read_text());agile=json.loads((E/'agilidad.json').read_text());tests=json.loads((E/'tests_resumen.json').read_text());mon=json.loads((E/'monitoreo.json').read_text());rows=[json.loads(x) for x in (E/'experimentos.jsonl').read_text().splitlines()][:5]
def _buscar_fuente(cands):
    for c in cands:
        if Path(c).exists():return c
    return None
_arial=_buscar_fuente(['/mnt/c/Windows/Fonts/arial.ttf','C:/Windows/Fonts/arial.ttf','/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
_arial_bold=_buscar_fuente(['/mnt/c/Windows/Fonts/arialbd.ttf','C:/Windows/Fonts/arialbd.ttf','/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'])
if not _arial or not _arial_bold:raise SystemExit('No se encontro una fuente tipo Arial. En WSL/Ubuntu: sudo apt install -y fonts-liberation')
pdfmetrics.registerFont(TTFont('Arial',_arial));pdfmetrics.registerFont(TTFont('Arial-Bold',_arial_bold))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial',boldItalic='Arial-Bold')
navy=colors.HexColor('#093D64');styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='B',fontName='Arial',fontSize=11,leading=12.65,spaceAfter=7));styles.add(ParagraphStyle(name='H',fontName='Arial-Bold',fontSize=17,leading=20,textColor=navy,spaceAfter=12));styles.add(ParagraphStyle(name='S',fontName='Arial-Bold',fontSize=12,leading=14,spaceBefore=8,spaceAfter=6,textColor=navy));styles.add(ParagraphStyle(name='T',fontName='Arial',fontSize=11,leading=12.65,spaceAfter=0));styles.add(ParagraphStyle(name='C',fontName='Arial',fontSize=11,leading=12.65,spaceAfter=6,textColor=navy))
story=[];plain=[];W=595.276-5*cm-12
def para(t,style='B'):story.append(Paragraph(t,styles[style]));plain.append(t)
def head(t):para(t,'H')
def sub(t):para(t,'S')
def table(title,headers,body,widths):
    para(title,'C');values=[[Paragraph('<b>'+html.escape(str(v))+'</b>',styles['T']) for v in headers]]+[[Paragraph(html.escape(str(v)).replace('\n','<br/>'),styles['T']) for v in row] for row in body]
    t=Table(values,colWidths=[W*w for w in widths],repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E2EAF1')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F3F6F8')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),.5,navy)]));story.append(t);story.append(Spacer(1,8));plain.append(title+'\n'+str(headers)+'\n'+str(body))
def page():story.append(PageBreak())
def pct(x):return f'{100*x:.1f}%'

# ---- Nota: este es un BORRADOR informativo. Cada parrafo es un resumen a ampliar en el informe final. ----
para('<b>Comercial Andina S.A.S. - Línea B: Operación</b> · Taller integrador Unidad 3 · Borrador informativo (ampliar a mano para el informe final).','C')

head('1. Resumen ejecutivo')
para(f'Prototipo de MLOps para predecir falla de equipos a 30 días: {data["filas"]:,} registros, siete entradas, {data["positivos"]} positivos ({pct(data["prevalencia"])}), cero vacíos; 480 casos de prueba. Se compararon cinco variantes y se eligió {selected["id"]} por mayor F1 entre las que superaron recall 0,50.')
para(f'En prueba: recall {pct(test["recall"])}, precisión {pct(test["precision"])}, exactitud {pct(test["accuracy"])}; detecta {test["tp"]} de {test["tp"]+test["fn"]} fallas con {test["fp"]} falsas alarmas (IC95 recall [{pct(test["recall_ic95"][0])}, {pct(test["recall_ic95"][1])}]). Meta propuesta: recall ≥70% y reducir en seis meses 25% las paradas no planificadas y 10% el costo correctivo.')
para(f'Evidencias de ejecución: la validación rechaza datos corruptos; {tests["tests"]} pruebas en verde (mutación detectada); API 200/422; puerta forzada a 1,01 rechazada; GitHub Actions en verde y rojo; contenedor Docker construido y verificado; deriva detectada solo en temperatura.')
para('<b>Recomendación a la junta:</b> autorizar la preparación de datos y un piloto en modo sombra; medir alertas, capacidad de inspección y resultados a 30 días antes de decidir uso operativo.')

head('2. Diagnóstico y estrategia')
para('Alineación: continuidad operativa y disponibilidad del servicio → priorización de inspecciones → datos confiables y respuesta de mantenimiento. El modelo apoya la decisión; no sustituye el juicio técnico.')
table('Tabla 1. Brechas y respuesta propuesta',['Situación actual','Brecha y prioridad'],[['Datos dispersos en hojas de cálculo y facturación','P1. Diccionario común, identificador de equipo y validaciones.'],['Decisiones de operación manuales, sin registro de fallas','P1. Registro de inspección, falla, reparación y fecha de corte.'],['Equipo de TI de cuatro personas en soporte','P1. Piloto acotado, límites WIP y responsable de negocio.'],['Tecnología instalada sin uso','P1. Co-diseño con mantenimiento y medición de adopción.']],[.49,.51])
table('Tabla 2. Indicadores de negocio con base y meta (estimaciones)',['Indicador','Base','Meta (6 meses)'],[['Horas de parada no planificada por 100 equipos-mes','16 h','12 h (−25%)'],['Costo de mantenimiento correctivo por equipo-mes','COP 200.000','COP 180.000 (−10%)'],['Recall del modelo (detección de fallas)','0,50 (umbral)','≥ 0,70']],[.58,.21,.21])
para('Bases a reemplazar con registros reales. Priorización: primero inventario y trazabilidad y piloto en una familia comparable de equipos; se aplazan sensores masivos, automatización de paradas y expansión a todas las tiendas.')

head('3. Metodología ágil: Kanban')
para('Se elige Kanban por el flujo de soporte e interrupciones del equipo de TI: visualiza bloqueos y limita el WIP. Roles: Operaciones prioriza y acepta valor; mantenimiento define fallas y revisa alertas; TI construye y opera; un facilitador coordina el flujo y la adopción.')
table('Figura 1. Tablero Kanban al cierre',['Por hacer','En curso','Verificado','Bloqueado'],[['Piloto real y adopción','—','Datos y validación; experimentos; API y pruebas; monitoreo; Docker; CI verde/rojo','—']],[.21,.18,.36,.25])
table('Tabla 3. Ciclos del equipo gestionados con Kanban',['Ciclo','Terminadas','Ciclo medio (min)','Rendimiento /h','WIP máx.'],[[a['ciclo'],a['completadas'],f'{a["tiempo_ciclo_promedio_min"]:.1f}',f'{a["rendimiento_por_hora"]:.2f}',a['wip_max']] for a in agile],[.16,.19,.24,.24,.17])
para('Fuente: marcas UTC en kanban_eventos.jsonl (ciclos ejecutados por el equipo). Regla: WIP máximo de dos; una tarjeta termina con salida reproducible y evidencia. Al separar la verificación, el tiempo de ciclo medio bajó entre el primer y el segundo ciclo.')

head('4. Proceso MLOps y métricas')
sub('4.1 Datos y validación')
para('2.400 filas × 8 columnas, 647 fallas (27,0%), 0% vacíos, semilla 20261019; etiqueta por probabilidad logística (uso, temperatura, días sin mantenimiento, incidentes) más ruido. La validación exige columnas, finitud, rangos, enteros y objetivo binario; detiene el entrenamiento con ValueError (probado con un uso semanal negativo). Partición estratificada 1.440/480/480; escalado dentro del Pipeline solo con entrenamiento; prueba consultada una vez.')
sub('4.2 Experimentos y selección')
para('La puerta de recall 0,50 se fijó tras el modelo base (0,24); el umbral de clasificación (0,50) es distinto del de aceptación.')
table('Tabla 4. Cinco ejecuciones MLflow sobre validación',['ID y variante','Exactitud','Precisión','Recall','F1','Puerta'],[[f'E{i+1} '+('LR' if r['modelo']=='lr' else 'RF' if r['modelo']=='rf' else 'Mayoría')+(' bal.' if r['balanceado'] else ''),*[f'{r[k]:.3f}' for k in ['accuracy','precision','recall','f1']],'Pasa' if r['puerta'] else 'No'] for i,r in enumerate(rows)],[.30,.14,.14,.14,.14,.14])
para(f'Selección: {selected["id"]}, mayor F1 entre variantes con recall ≥0,50 (precisión como desempate). Se sacrifica precisión por recall mediante el balanceo de clases.')
sub('4.3 Resultado final')
para(f'Prueba reservada (480): exactitud {test["accuracy"]:.3f}, precisión {test["precision"]:.3f}, recall {test["recall"]:.3f}, F1 {test["f1"]:.3f}; matriz VP={test["tp"]}, FN={test["fn"]}, FP={test["fp"]}, VN={test["tn"]}; {test["alertas"]} alertas. IC95 Wilson del recall [{test["recall_ic95"][0]:.3f}, {test["recall_ic95"][1]:.3f}]. Costo esperado = costo_FN×FN + costo_FP×FP; el piloto fija esos costos y ajusta el umbral. Ver figuras A1 y A2.')
sub('4.4 Puerta, servicio, pruebas, CI y monitoreo')
para(f'Puerta de calidad: si no cumple recall termina con código 1 y no guarda (probado con 1,01, campeón intacto). API FastAPI reutiliza el mismo Pipeline (200/422). {tests["tests"]} pruebas en verde (una mutación hizo fallar la esperada). GitHub Actions en verde y rojo; Docker construido y verificado.')
dr=[r for r in mon if r['alerta']][0]
para(f'Monitoreo de deriva (KS + Holm, α=0,01, D≥0,10) sobre 800 casos: alerta solo en {dr["variable"]} (D={dr["D"]:.2f}); el control no alerta. Reentrenar por: deriva sostenida, recall <0,50 en cohortes maduras, o cada 90 días; cada candidato repite la puerta.')

head('5. Gestión del cambio')
para('Enfoque ADKAR para barreras individuales; las resistencias (temor al control, doble registro, desconfianza) se validan con el personal.')
table('Tabla 5. Mapa de actores',['Actor','Poder / interés','Rol en la adopción'],[['Gerencia y Operaciones','Alto / alto','Patrocinar el piloto y acordar el éxito.'],['Junta directiva','Alto / uso diario menor','Recibir resultados y decidir la inversión.'],['TI','Alto técnico / alto','Asegurar el servicio y el soporte.'],['Mantenimiento y jefes de tienda','Medio-alto / alto','Co-diseñar alertas y aceptar la capacidad de inspección.'],['Operarios','Formal menor / alto','Probar el flujo y reportar errores.']],[.32,.27,.41])
table('Tabla 6. Plan de adopción por etapa ADKAR',['Etapa','Acción y responsable','Indicador y meta'],[['Conciencia','Operaciones explica el problema y los límites.','90% explica el propósito.'],['Deseo','Gerencia acuerda el uso de métricas.','80% declara disposición.'],['Conocimiento','TI y mantenimiento practican con casos.','85% interpreta 4 de 5 casos.'],['Capacidad','El jefe de tienda elimina el doble registro.','80% usa el flujo semanalmente.'],['Refuerzo','Operaciones revisa y corrige obstáculos.','90% de alertas revisadas en 48 h.']],[.23,.52,.25])
para('Indicadores transversales: usuarios activos/habilitados; decisiones apoyadas por el modelo (meta 80%); satisfacción 4/5. No se evalúa al trabajador por la cantidad de alertas.')

head('6. Riesgos, ética e integración')
table('Tabla 7. Riesgos principales y controles',['Tipo','Riesgo','Control'],[['Técnico','Falsos negativos','Conservar mantenimiento preventivo y revisión humana.'],['Técnico','Falsos positivos','Medir capacidad, precisión y costo por alerta.'],['Técnico','Fuga temporal / etiquetas inmaduras','Separar por tiempo y equipo; esperar 30 días.'],['Técnico','Cambio de distribución','Monitor de deriva y reversión.'],['Organizacional','Dependencia de una persona','Suplente, versiones y manual de reconstrucción.'],['Ético','Métricas usadas para sancionar','Acordar propósito, acceso y revisión.'],['Sesgo','Equipos heterogéneos','Validar por familia de equipo antes de usar.']],[.18,.32,.50])
para('Sin datos personales; en el piloto, minimizar atributos y separar indicadores de activos de evaluaciones personales. Integración: la estrategia fija el objetivo, Kanban organiza el trabajo, ADKAR atiende la adopción y MLOps impide promover un mal modelo y vigila la deriva. Límite: datos generados por diseño, no se afirma causalidad.')

head('7. Conclusiones')
para('El prototipo ejecuta el ciclo completo: validación, experimentación registrada, puerta de calidad, API, pruebas adversas, CI en verde y rojo, y monitoreo. Las siete etapas se cubren con definición, datos/esquema, entrenar/MLflow, puerta, empaquetado (Docker), app y monitoreo/reentrenamiento.')
para('<b>Qué haríamos distinto:</b> buscar un dataset real desde el inicio, usar validación temporal y por equipo, acordar los costos de falso negativo y positivo, y automatizar la recolección de evidencias.')
para('<b>Declaración de IA:</b> se usó un asistente de IA para interpretar la guía, programar, probar y redactar; el equipo revisa y responde por todo el contenido.')

page();head('Anexo A. Figuras del modelo')
para('Figura A1. Precisión y recall de las cinco variantes en validación; la línea es la puerta de recall 0,50.');story.append(Image(str(E/'experimentos.png'),width=W,height=W*3.2/9))
story.append(Spacer(1,10))
para('Figura A2. Matriz de confusión del campeón en los 480 casos reservados.');story.append(Image(str(E/'confusion.png'),width=W*.88,height=W*.44))

def footer(c,doc):
    c.setFont('Arial',9);c.setFillColor(navy);c.drawString(2.5*cm,1.6*cm,'Comercial Andina · Caso B · Borrador');c.drawRightString(595.276-2.5*cm,1.6*cm,str(doc.page))
doc=SimpleDocTemplate(str(OUT/'Informe_preliminar_Unidad3_CasoB.pdf'),pagesize=(595.276,841.89),rightMargin=2.5*cm,leftMargin=2.5*cm,topMargin=2.5*cm,bottomMargin=2.5*cm,title='Taller Unidad 3 - Comercial Andina, Operación (borrador)',author='Borrador asistido para redactar el informe final')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
(P/'INFORME_fuente.txt').write_text('\n\n'.join(plain),encoding='utf-8')
r=PdfReader(OUT/'Informe_preliminar_Unidad3_CasoB.pdf');print('PDF',len(r.pages),'paginas')