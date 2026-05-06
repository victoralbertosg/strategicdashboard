# Plan de Investigación: Modelo Predictivo Integrado a Sistema de Inteligencia de Negocios (BI)

## Visión General
Esta planificación detalla los pasos modulares para la investigación, desarrollo e integración de un modelo predictivo con un sistema de Inteligencia de Negocios (BI), basándose estrictamente en las reglas y directrices estipuladas en el marco de trabajo `CLAUDE.md`.

---

## Fase 1: Descubrimiento y Especificación
1. **Discovery Interview**: Utilizar el proceso estructurado y la memoria para acotar objetivos (ej. predecir fuga de clientes "Churn") y definir qué sistema BI integrar (PowerBI, Tableau, Streamlit, etc.).
2. **Actualización del Entorno**:
   - Ajustar campos clave en el `CLAUDE.md` asegurando que refleje la integración con BI.
   - Enriquecer el `.claude/references/domain-profile.md` con el estado del arte en integraciones predictivas en sistemas de toma de decisiones empresariales.

## Fase 2: Ingeniería de Datos y ETL
1. **Establecimiento de Orígenes**: Insertar la data cruda en `data/raw/` (usualmente en .gitignore si pesa mucho).
2. **Limpieza y Proceso**: Crear los módulos de transformación en la carpeta `scripts/` y apuntar las salidas limpias a `data/cleaned/`.
3. **Preparación de la conexión BI**: El resultado en `data/cleaned/` fungirá doble rol; servirá para entrenamiento de los modelos y para poblar métricas descriptivas en el BI.

## Fase 3: Desarrollo del Modelo Predictivo
1. **Entrenamiento y Análisis**: Diseñar e implementar el algoritmo para la predicción, calculando métricas necesarias (RMSE, F1, ROC-AUC).
2. **Generación de Outputs para BI**: El modelo exportará sus inferencias hacia una tabla o base de datos que el BI se encargará de consumir, uniendo la probabilidad generada con el cliente objetivo.
3. **Figuras Científicas**: Se almacenarán gráficos nativos generados por los scripts para el artículo en `paper/figures/`.

## Fase 4: Despliegue en Base a Sistema de Negocios (BI)
1. **Conexión de Modelos Analíticos con BI**: Integración entre las probabilidades de salida (ej. predicciones exportadas o base SQL) al Dashboard de BI.
2. **Revisión de Funcionalidad**: Validar que la actualización de datos crudos actualiza la vista predictiva dentro de la capa del BI.

## Fase 5: Redacción del Manuscrito Científico y Calidad
1. **Única Fuente de Verdad (Paper)**: Plantear el esqueleto del trabajo en `paper/main.tex` dividiendo apropiadamente metodologías (modelación de ML) e implementación (Arquitectura propuesta).
2. **Iteración de Contenidos**:
   - Ejecutar la dupla "worker-critic" garantizando que las secciones alcancen o superen el umbral de métrica calidad de 80.
   - Ejecutar verificaciones compilando a menudo (`cd paper && latexmk main.tex`).
3. **Manejo Bibliográfico**: Todo artículo de soporte a la arquitectura AI-BI se actualizará de forma centralizada en `Bibliography_base.bib`.

## Fase 6: Réplica y Presentaciones
1. **Paquete de Replicabilidad**: Depositar versionados finales e instrucciones de instalación de dependencias en `paper/replication/`.
2. **Talks / Beamer**: Preparar los slides de demostración (si fuesen pertinentes) extrayendo la estructura base desde el manuscrito original hacia `paper/talks/`.

---
**Criterio de Éxito Inmediato (Checklist)**
- [ ] Plan incorporado al directorio `quality_reports/plans/`.
- [ ] Repositorio cuenta con dependencias para manipulación de datos (Python) y compilación (XeLaTeX).
- [ ] Datos de prueba iniciales dispuestos para su transformación e ingesta en BI.
