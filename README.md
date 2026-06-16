# 📊 Strategic Dashboard: Prevención de Fuga de Clientes (Churn)

Este repositorio contiene un sistema de **Business Intelligence (BI) Estratégico** diseñado para identificar, analizar y mitigar la fuga de clientes en tiempo real. El enfoque principal es transformar predicciones de IA en decisiones financieras accionables para perfiles directivos.

## 🚀 Características Principales

El sistema está construido sobre **Streamlit** y se organiza en módulos estratégicos:

### 1. 🏢 Visión General de la Cartera
- Monitoreo en tiempo real de la tasa de fuga estimada.
- Valoración económica del "Dinero en Peligro" sin intervención.
- Segmentación rápida de clientes según probabilidad de abandono.

### 2. 🤖 Inteligencia Predictiva y Evaluación
- **Modelos de Vanguardia**: Implementación de XGBoost, Random Forest y Regresión Logística.
- **Transparencia Total**: Evaluación comparativa mediante métricas AUC-ROC, precisión y matrices de confusión detalladas por modelo.
- **Justificación del Modelo**: Explicación clara de por qué se selecciona el modelo ganador para la producción.

### 3. 🔍 Explicabilidad (XAI)
- **¿Por qué se van?**: Identificación de los factores clave que impulsan el abandono (e.g., tipo de contrato, cargos mensuales, permanencia).
- **Análisis Individual**: Capacidad de auditar casos específicos para entender la lógica detrás de cada predicción.

### 4. 💰 Simulación Financiera y Toma de Decisiones
- **Escenarios Comparativos**: Contraste directo entre el **Escenario A (Sin Modelo)** y el **Escenario B (Con Intervención Estratégica)**.
- **Cálculo de Ganancia Neta**: Estimación precisa del ROI tras considerar costos de retención y efectividad de campañas.
- **Prescripción de Acciones**: Recomendaciones automáticas sobre a qué clientes contactar y qué tipo de oferta ofrecer según su Valor de Vida (LTV) y Riesgo.

---

## 🛠️ Requisitos e Instalación

### Requisitos Mínimos
- Python 3.9+
- Pip (gestor de paquetes)

### Instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/victoralbertosg/strategicdashboard.git
   cd strategicdashboard
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar el dashboard:
   ```bash
   streamlit run bi_system/app.py
   ```

## 📁 Estructura del Proyecto (Versión Ejecutable)
- `bi_system/`: Código fuente de la aplicación Streamlit (Páginas, utilidades y lógica).
- `data/`: Conjuntos de datos procesados y listos para la visualización.
- `scripts/`: Scripts auxiliares de preprocesamiento y entrenamiento.
- `requirements.txt`: Dependencias necesarias para el entorno.

---

