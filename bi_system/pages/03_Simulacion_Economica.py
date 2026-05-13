import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, init_global_controls

st.set_page_config(page_title="Simulador de Rentabilidad", layout="wide")
init_global_controls()

st.title("Módulo 3: Simulador Financiero (Comparación de Escenarios)")
st.markdown(f"Evaluando el impacto económico del modelo activo: **{st.session_state.current_model_name}**.")

df = load_data()
if df is None:
    st.error("Faltan datos.")
    st.stop()

st.sidebar.header("Parámetros Financieros")
costo_retencion = st.sidebar.number_input("Costo de Retención por Cliente [$]", value=50)
clv_inv = st.sidebar.number_input("Valor Promedio del Cliente (LTV) [$]", value=300)

# Usamos el umbral global
threshold = st.session_state.umbral

# Lógica Financiera
TP = len(df[(df['Predicted_Class'] == 1) & (df['Churn_Real'] == 1)])
FP = len(df[(df['Predicted_Class'] == 1) & (df['Churn_Real'] == 0)])
FN = len(df[(df['Predicted_Class'] == 0) & (df['Churn_Real'] == 1)])

perdida_escenario_A = (TP + FN) * clv_inv
inversion_retencion = (TP + FP) * costo_retencion
clientes_retenidos_valor = TP * clv_inv
ganancia_neta_modelo = clientes_retenidos_valor - inversion_retencion

st.subheader("Resultados de la Simulación")

col_main, col_gui = st.columns([2, 1])

with col_main:
    c1, c2 = st.columns(2)
    with c1:
        st.info("### Escenario A: Sin IA")
        st.metric("Pérdida Económica Estimada", f"-${perdida_escenario_A:,.2f}")
        st.markdown("**Fórmula:** *Pérdida = (TP + FN) × LTV*")
        st.caption(f"Cálculo: ({TP} + {FN}) × ${clv_inv} = ${perdida_escenario_A:,.2f}")
    with c2:
        st.success("### Escenario B: Con IA")
        st.metric("Beneficio Neto del Modelo", f"${ganancia_neta_modelo:,.2f}")
        st.markdown("**Fórmula:** *Ganancia = (TP × LTV) - ((TP + FP) × Costo)*")
        st.caption(f"Cálculo: ({TP} × ${clv_inv}) - (({TP} + {FP}) × ${costo_retencion}) = ${ganancia_neta_modelo:,.2f}")

    st.divider()
    st.subheader("Optimización de Rentabilidad")
    
    # Calcular curva 
    thresholds = np.linspace(0, 1, 50)
    profits = []
    for t in thresholds:
        t_interv = (df['Predicted_Prob'] >= t).astype(int)
        t_tp = len(df[(t_interv == 1) & (df['Churn_Real'] == 1)])
        t_fp = len(df[(t_interv == 1) & (df['Churn_Real'] == 0)])
        profit = (t_tp * clv_inv) - ((t_tp + t_fp) * costo_retencion)
        profits.append(profit)

    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(thresholds, profits, color='green', lw=2)
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax.axvline(x=threshold, color='orange', linestyle=':', label=f"Su Umbral ({threshold*100:.0f}%)", lw=2)
    ax.set_xlabel("Sensibilidad")
    ax.set_ylabel("Ganancia ($)")
    st.pyplot(fig)

with col_gui:
    st.info("### 📘 Guía Rápida para Directivos")
    st.markdown(f"""
    **¿Cómo gano dinero con la IA?**
    El modelo le permite elegir a quién llamar para no desperdiciar dinero utilizando estas métricas clave:
    
    *   **TP (Verdaderos Positivos):** Clientes que se iban a ir y la IA detectó con éxito.
    *   **FN (Falsos Negativos):** Clientes que se fueron sin que la IA los detectara ("Fugas sorpresa").
    *   **FP (Falsos Positivos):** Clientes leales que la IA marcó erróneamente como riesgo ("Falsas alarmas").
    *   **LTV (Lifetime Value):** Es el valor promedio que cada cliente aporta a la empresa.
    
    *   **Escenario A (Sin IA):** Perdemos a todos los que realmente se van ($TP + FN$) multiplicados por su $LTV$.
    *   **Escenario B (Con IA):** Recuperamos el valor de los $TP$ pero invertimos el costo en todos los que la IA marcó ($TP + FP$).
    *   **Beneficio Neto:** Es la ganancia final del modelo al maximizar los $TP$ y minimizar los $FP$.
    
    **Simulación:** Pruebe cambiando el **Costo de Retención** o el **Umbral de Riesgo** a la izquierda para ver cómo las fórmulas y resultados se recalculan al instante.
    """)
