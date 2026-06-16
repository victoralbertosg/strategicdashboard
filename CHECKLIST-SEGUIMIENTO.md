# 📝 Checklist de Seguimiento: Alineación y Redacción de Tesis (SIP con XAI)

Este checklist ha sido creado para el seguimiento detallado de las tareas pendientes de alineación y redacción de la tesis, vinculando los resultados inmutables del **Dashboard en Streamlit (`bi_system`)** con los documentos del manuscrito redactados en **Obsidian** y el **Google Doc** de la tesis.

---

## 📌 Principio Rector: Resultados Inmutables
> **¡IMPORTANTE!** Todos los textos de la tesis (Introducción, Metodología, Resultados, Discusión, Conclusiones) deben ajustarse **hacia** los resultados reales obtenidos en el desarrollo del software. Los datos técnicos no se alteran.

---

## 📊 1. Control de Consistencia de Datos Inmutables
Verifique que cada valor numérico citado en los textos de Obsidian y Google Doc coincida exactamente con las métricas del sistema:

- [ ] **Métricas de Modelos (con Umbral 0.2):**
  - **Regresión Logística (Modelo de Referencia):** AUC = `0.841` | Precisión = `64.1%` | Recall (Cobertura) = `55.3%`
  - **XGBoost:** AUC = `0.840` | Precisión = `65.3%` | Recall (Cobertura) = `51.9%`
  - **Random Forest:** AUC = `0.825` | Precisión = `63.0%` | Recall (Cobertura) = `51.9%`
- [ ] **Métricas Económicas (Umbral 0.2):**
  - Costo de Retención por Cliente: `$50 USD`
  - Valor de Vida Promedio (LTV): `$300 USD`
  - Beneficio Neto (Escenario Con IA): `$62,250 USD`
  - Pérdida Económica (Escenario Sin IA): `-$112,200 USD` (Dato a corroborar: unificar si es -$112,200 o -$112,250)
  - Incremento / Ahorro Económico: `$174,450 USD`
  - Clientes Intervenidos Proyectados (de prueba): `548` (de un total de `1,409` registros de test)
  - Distribución de alertas: `323` Alerta Roja (Rescate Urgente) y `225` Alerta Amarilla (Preventiva).
- [ ] **Explicabilidad (XAI):**
  - Variable SHAP dominante a nivel global: `tenure` (permanencia).
  - Top 5 variables SHAP: `tenure`, `MonthlyCharges`, `Contract`, `TechSupport`, `OnlineSecurity`.
  - Ejemplo local de cliente auditado: `Cliente 5178-LMXOP`.

---

## ✍️ 2. Alineación de Objetivos e Hipótesis (Por Corregir en Obsidian)
*Los cambios ya se aplicaron en el Google Doc, pero es necesario sincronizarlos en los archivos locales de Obsidian:*

- [ ] **Capítulo I - Introducción (Obsidian `Capitulo-I - Introduccion.md`):**
  - [ ] **OE1:** Cambiar de *"maximizar la detección precisa..."* a *"evaluar el rendimiento predictivo en la detección del riesgo de churn mediante métricas de discriminación (AUC), precisión y recall"*.
  - [ ] **OE2:** Cambiar de *"hacer comprensibles las decisiones..."* a *"identificar las variables de mayor influencia en la predicción del riesgo de churn a nivel global e individual"*.
  - [ ] **OE3:** Cambiar de *"prescribir acciones de marketing basadas en el máximo retorno..."* a *"proyectar el retorno neto de campañas de retención mediante análisis de sensibilidad del umbral de clasificación y simulación de escenarios económicos"*.
- [ ] **Capítulo II - Metodología (Obsidian `Capitulo-II - Metodologia.md`):**
  - [ ] **HE1:** Actualizar para declarar que los tres algoritmos superaron el 80% de AUC (RL=0.841, XGB=0.840, RF=0.825) y que XGBoost obtuvo un rendimiento marginalmente inferior a Regresión Logística.
  - [ ] **HE3:** Reformular para declarar que la intervención selectiva proyecta un beneficio neto positivo de $62,250 USD, superando la pérdida del escenario pasivo sin intervención dirigida (-$112,200 USD).
  - [ ] **Métricas base:** Ajustar el texto que indicaba umbrales rígidos de *"Accuracy ≥80%, Recall ≥85%, AUC ≥0.90"* a *"ROC-AUC (≥0.80) como métrica principal, y Accuracy, Precision, Recall y F1 como indicadores complementarios"*.

---

## 📚 3. Tareas Pendientes en Metodología (Capítulo II)
- [ ] **Agregar Sección "Selección del Modelo":**
  - Insertar párrafo explicando el criterio de desempate por interpretabilidad inherente:
    > *"La selección del modelo principal para la fase de explicabilidad y simulación económica se basará en el AUC como métrica principal. En caso de que múltiples modelos presenten valores de AUC similares (diferencia <0.01), se seleccionará el modelo con mayor interpretabilidad inherente para facilitar la integración con el módulo de explicabilidad SHAP (Lundberg & Lee, 2017)."*
- [ ] **Corregir la Operacionalización de Variables:**
  - Completar las celdas vacías en la tabla de operacionalización en la Matriz de Consistencia.
  - Asegurar la definición de las **4 dimensiones** de la Variable Dependiente:
    1. *Calidad Predictiva* (AUC, Precisión, Recall)
    2. *Transparencia Explicativa* (consistencia SHAP, fidelidad)
    3. *Cuantificación Económica* (beneficio neto, ahorro en intervención)
    4. *Eficiencia Operativa* (clientes prioritarios sugeridos, tasa de focalización)
  - Añadir indicadores específicos a la dimensión *Eficiencia Operativa* (ej. % de base filtrada, ratio de conversión).

---

## 📈 4. Tareas Pendientes en Resultados (Capítulo III)
- [ ] **Corregir Inconsistencia en Tabla 3 (Matriz de Confusión) y Tabla 6 (Simulación Económica):**
  - **El problema:** Los datos de la **Tabla 3** ($TN=919, FP=116, FN=167, TP=207$) corresponden al **Umbral 0.5** de Regresión Logística, pero se etiquetó como *Umbral 0.2*.
  - **La solución:**
    - *Opción A (Recomendada - Mantener Umbral 0.2 como óptimo):* Cambiar los datos de la **Tabla 3** a los reales de la Regresión Logística con umbral 0.2: $TN = 657$ | $FP = 378$ | $FN = 49$ | $TP = 325$. Actualizar la **Tabla 6** para reflejar: Clientes intervenidos = `703` | Costo de Retención = `$35,150` | Beneficio Neto = `$62,350` (en vez de $62,250).
    - *Opción B (Mantener los datos de la Tabla 3):* Corregir el texto y título de la Tabla 3 para indicar que la matriz de confusión analizada en detalle se calculó con el umbral 0.5, pero esto reducirá el beneficio neto reportado de la simulación a `$45,950` (en lugar de $62,250).
- [ ] **Validar Figuras:**
  - Asegurar que la inserción de las referencias a la **Figura 1** (Curva ROC comparativa), **Figura 2** (Gráfico resumen SHAP) y **Figura 3** (Curva de sensibilidad del beneficio) estén listas para enlazarse con los recursos visuales reales exportados de Streamlit.

---

## 🏛️ 5. Cumplimiento de la Guía UCV (Formato y Estilo)
Asegure el cumplimiento de los estándares de la guía de la Universidad César Vallejo (UCV) para informes de tesis de Maestría:

- [ ] **Tiempos Verbales Estrictos:**
  - **Capítulo I (Introducción):** Tiempo **Pasado** del modo indicativo (*"El problema se convirtió..."*, *"Ahmad demostró..."*).
  - **Capítulo II (Metodología):** Tiempo **Pasado** del modo indicativo (*"El estudio adoptó..."*, *"Se aplicó..."*).
  - **Capítulo III (Resultados):** Tiempo **Pasado** del modo indicativo (*"El modelo obtuvo..."*, *"Se generó..."*).
  - **Capítulo IV (Discusión):** Tiempo **Presente** del modo indicativo (*"Esto demuestra que..."*, *"La literatura coincide con..."*).
  - **Capítulo V (Conclusiones):** Tiempo **Pasado** (*"Se concluyó que..."*).
  - **Capítulo VI (Recomendaciones):** Tiempo **Presente** (*"Se sugiere implementar..."*).
- [ ] **Estilo de Escritura:**
  - Redacción en prosa corrida.
  - Uso de tercera persona.
  - **Prohibido:** Viñetas, guiones y textos en negrita dentro de los párrafos narrativos.
- [ ] **Formato de Documento UCV:**
  - Fuente: Arial 12.
  - Interlineado: 1.5.
  - Márgenes: 2.54 cm en todos los lados.
  - Extensión mínima total: 26 páginas (desde Introducción hasta Recomendaciones).

---

## 🗂️ 6. Corrección de Inconsistencias Globales
- [ ] **Título del Proyecto:** Unificar en todos los documentos. ¿Es *"en Campañas de retención"* o *"de campañas de retención"*?
- [ ] **Hipótesis General:** Remover la frase *"con precisión"* de la hipótesis en la Matriz de Consistencia para que sea idéntica a la descrita en el Capítulo I (*"permite simular el ROI"*).
- [ ] **Variable Dependiente:** Unificar la nomenclatura entre *"Simulación del ROI de campañas"* y *"Simulación del ROI en Campañas"*.

---

## 📑 7. Anexos y Entregables Finales
- [ ] **Matriz de Consistencia:** Actualizar y unificar con las correcciones de objetivos y dimensiones.
- [ ] **Fichas de Validación de Jueces Expertos:** Completar con los datos reales del promedio de calificaciones de los 3 expertos (> 4.00/5.00).
- [ ] **Código Fuente del Prototipo:** Preparar el paquete de replicación con el código de `bi_system` y las instrucciones de instalación del `README.md`.
- [ ] **Reporte Turnitin:** Pasar el manuscrito final y verificar porcentaje de similitud aceptable.
- [ ] **Carátula, Dedicatoria y Agradecimientos:** Formatear según plantilla institucional UCV.
- [ ] **Índices Automatizados:** Generar índice de contenidos, tablas y figuras.
