import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import load_data

st.set_page_config(page_title="Simulador de Rentabilidad", layout="wide")
st.title("Módulo 3: Simulador Financiero (Comparación de Escenarios)")
st.markdown("""
Este módulo permite evaluar objetivamente el impacto económico de utilizar el modelo predictivo frente a no utilizarlo.

**Diseño de la evaluación:**
*   **Escenario A (Sin modelo):** Las decisiones de retención no se basan en analítica predictiva. Ante la falta de capacidad para identificar riesgos, no se realizan intervenciones proactivas. Se asume la pérdida total de los clientes con intención real de fuga.
*   **Escenario B (Con modelo):** Las decisiones se sustentan en un sistema BI integrado con el modelo predictivo, que permite focalizar las inversiones de retención (descuentos, promociones) únicamente en clientes con alta probabilidad de abandono.
""")

df = load_data()
if df is None:
    st.error("Faltan datos.")
    st.stop()

st.sidebar.header("Parámetros Financieros")
costo_retencion = st.sidebar.number_input("Costo de Retención por Cliente (Ej. Beneficio otorgado) [$]", value=50)
clv = st.sidebar.number_input("Valor Económico del Cliente (LTV/Facturación a salvar) [$]", value=300)

st.sidebar.markdown("---")
st.sidebar.header("Política de Intervención")
threshold = st.sidebar.slider("Umbral de Riesgo (Intervenir si Probabilidad ≥ X)", 0.0, 1.0, 0.5, 0.01)

# Lógica de Matriz de Confusión Financiera
df['Intervencion'] = (df['Predicted_Prob'] >= threshold).astype(int)

TP = len(df[(df['Intervencion'] == 1) & (df['True_Churn'] == 1)])
FP = len(df[(df['Intervencion'] == 1) & (df['True_Churn'] == 0)])
FN = len(df[(df['Intervencion'] == 0) & (df['True_Churn'] == 1)])
TN = len(df[(df['Intervencion'] == 0) & (df['True_Churn'] == 0)])

# Cálculos Económicos
# Escenario A 
perdida_escenario_A = (TP + FN) * clv

# Escenario B
inversion_retencion = (TP + FP) * costo_retencion
clientes_retenidos_valor = TP * clv
perdida_fuga_no_detectada = FN * clv

# Ganancia Neta
ganancia_neta_modelo = clientes_retenidos_valor - inversion_retencion

st.subheader("Resultados de la Simulación")

col1, col2 = st.columns(2)

with col1:
    st.info("### Escenario A: Sin modelo predictivo")
    st.markdown("Resultados si no se realiza ninguna campaña focalizada de retención:")
    st.metric("Pérdida Económica Total", f"-${perdida_escenario_A:,.2f}")
    st.caption("Fugas totales en la base de datos multiplicadas por el Valor del Cliente (LTV).")

with col2:
    st.success("### Escenario B: Con sistema predictivo BI")
    st.markdown("Resultados aplicando las intervenciones focalizadas por inteligencia artificial:")
    st.metric("Ganancia Neta (Aporte Económico del Modelo)", f"${ganancia_neta_modelo:,.2f}")
    st.markdown("#### Detalle del cálculo de la Ganancia Neta:")
    st.markdown(f"""
    *   **(+) Ingresos Salvados:** Clientes retenidos con éxito (**{TP}**) × Valor LTV (**${clv}**) = **${clientes_retenidos_valor:,.2f}**
    *   **(-) Inversión en Retención:** Total intervenciones (**{TP + FP}**) × Costo Retención (**${costo_retencion}**) = **-${inversion_retencion:,.2f}**
    *   **Ganancia Neta (Retorno de Inversión):** Ingresos Salvados - Inversión en Retención
    """)
    st.caption(f"Nota: Aún existe una Fuga Residual (Fugas no detectadas) equivalente a -${perdida_fuga_no_detectada:,.2f}.")

st.divider()
st.subheader("Desglose Operativo de las Predicciones")

c1, c2, c3 = st.columns(3)
c1.metric("Retenciones Exitosas (TP)", TP, help="Fugas reales prevenidas gracias a un diagnóstico correcto (Verdaderos Positivos).")
c2.metric("Inversiones Innecesarias (FP)", FP, help="Clientes leales identificados como riesgo. Recibieron el incentivo de manera superflua (Falsos Positivos).")
c3.metric("Fugas No Detectadas (FN)", FN, help="Clientes que terminaron abandonando la empresa porque su riesgo se estimó por debajo del umbral establecido (Falsos Negativos).")

st.divider()
st.subheader("Curva de Optimización Estratégica")
st.markdown("El siguiente gráfico permite identificar matemáticamente en qué punto del **Umbral de Riesgo** se maximiza la **Ganancia Neta**. Funciona simulando todos los puntos de decisión posibles con la política financiera actual.")

thresholds = np.linspace(0, 1, 50)
profits = []

for t in thresholds:
    t_interv = (df['Predicted_Prob'] >= t).astype(int)
    t_tp = len(df[(t_interv == 1) & (df['True_Churn'] == 1)])
    t_fp = len(df[(t_interv == 1) & (df['True_Churn'] == 0)])
    profit = (t_tp * clv) - ((t_tp + t_fp) * costo_retencion)
    profits.append(profit)

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(thresholds, profits, label="Curva de Ganancia Neta (Aporte del Modelo)", color='green', lw=2)
ax.axhline(y=0, color='red', linestyle='--', label="Línea Base (Cero aporte / Escenario Sin Intervención)")
ax.axvline(x=threshold, color='orange', linestyle=':', label="Configuración del Umbral Actual")
ax.set_xlabel("Nivel de Sensibilidad (Probabilidad Mínima para generar Alerta)")
ax.set_ylabel("Ganancia Neta Proyectada ($)")
ax.set_title("Maximización de la Rentabilidad del Modelo")
ax.legend()
ax.grid(True, linestyle=":", alpha=0.6)
st.pyplot(fig)
