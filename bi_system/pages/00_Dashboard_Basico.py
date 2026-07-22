import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, init_global_controls, get_current_shap_values

st.set_page_config(page_title="Telco Churn BI Dashboard", page_icon="📶", layout="wide")
init_global_controls()

st.title("📶 Dashboard Básico - Resumen de Operación")
st.markdown("Vista simplificada que integra detección, impacto financiero y causas del riesgo.")

df = load_data()
if df is None:
    st.error("Faltan datos.")
    st.stop()

# KPIs Rápidos y Dinámicos
total_customers = len(df)
high_risk_customers = len(df[df['Predicted_Class'] == 1])

col1, col2, col3 = st.columns(3)
col1.metric("Clientes Evaluados", f"{total_customers:,}")
col2.metric("Clientes de Alto Riesgo", f"{high_risk_customers:,}")
col3.metric("% de Cartera en Riesgo", f"{(high_risk_customers/total_customers)*100:.1f} %")

st.divider()

col_main, col_gui = st.columns([2, 1])

with col_main:
    # 1. EVALUACIÓN DE IMPACTO 
    st.subheader("1. Impacto Financiero Proyectado")
    costo_ret = 50
    ingreso_sal = 300
    
    TP = len(df[(df['Predicted_Class'] == 1) & (df['Churn_Real'] == 1)])
    FP = len(df[(df['Predicted_Class'] == 1) & (df['Churn_Real'] == 0)])
    
    inversion_total = (TP + FP) * costo_ret
    ingreso_recuperado = TP * ingreso_sal
    ganancia_neta = ingreso_recuperado - inversion_total
    roi = (ganancia_neta / inversion_total) * 100 if inversion_total > 0 else 0.0

    r_col1, r_col2, r_col3 = st.columns(3)
    r_col1.metric("Ganancia Neta Estimada", f"${ganancia_neta:,.2f}")
    r_col1.markdown("**Fórmula:** *Ganancia = (TP × LTV) - (Total_Int × Costo)*")
    
    r_col2.metric("Inversión Requerida", f"${inversion_total:,.2f}")
    r_col2.caption(f"Cálculo: ({TP} + {FP}) × ${costo_ret} = ${inversion_total:,.2f}")

    r_col3.metric("Retorno de la Inversión (ROI)", f"{roi:.2f}%")
    r_col3.caption("Cálculo: (Ganancia / Inversión) × 100")

    st.divider()

    # 2. XAI
    st.subheader("2. Diagnóstico Causal")
    selected_client = st.selectbox("Seleccione un ID de Cliente en Riesgo:", df[df['Predicted_Class'] == 1]['customerID'].head(10))
    
    if selected_client:
        client_idx = df[df['customerID'] == selected_client].index[0]
        shap_values, feature_names = get_current_shap_values(st.session_state.current_model_name)
        
        # Obtener shap del cliente específico
        # shap_values es [1409, 19], necesitamos el indice relativo en el test set
        # df es el test set filtrado/cargado, su indice coincide con el de shap_values 
        client_shap = pd.Series(shap_values[df.index.get_loc(client_idx)], index=feature_names).sort_values()
        
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ['red' if val > 0 else 'green' for val in client_shap.values]
        client_shap.plot(kind='barh', color=colors, ax=ax)
        ax.set_title(f"¿Por qué se va el cliente {selected_client}?")
        st.pyplot(fig)

with col_gui:
    st.info("### 📘 Guía Rápida para Directivos")
    st.markdown(f"""
    **¿Qué controla este panel?**
    Aquí puede ver un resumen ejecutivo de la operación bajo el modelo **{st.session_state.current_model_name}** usando métricas clave:
    
    *   **TP (Verdaderos Positivos):** Clientes en riesgo detectados correctamente.
    *   **LTV (Lifetime Value):** Valor económico total de cada cliente.
    *   **Ganancia Neta:** Es el dinero salvado: (**TP × LTV**) menos los costos de intervención.
    *   **Diagnóstico:** Le permite "entrar en la mente" del cliente antes de llamarlo para saber qué le molesta.
    
    **Nota:** Si desea cambiar el tipo de Inteligencia Artificial o ajustar el **Umbral de Riesgo** para ver cómo cambian los cálculos, use la configuración en la izquierda.
    """)
