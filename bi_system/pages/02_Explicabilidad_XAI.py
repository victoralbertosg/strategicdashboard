import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, init_global_controls, get_current_shap_values

st.set_page_config(page_title="Explicabilidad y Diagnóstico", layout="wide")
init_global_controls()

st.title("🧩 Módulo 2: Diagnóstico Causal (XAI)")
st.markdown(f"Nuestra tecnología le explica los motivos detrás de cada alerta generada por el modelo **{st.session_state.current_model_name}**.")

df = load_data()
if df is None:
    st.error("Faltan datos.")
    st.stop()

# Obtener SHAP values para el modelo actual
shap_values, feature_names = get_current_shap_values(st.session_state.current_model_name)
shap_cols = [f"{col}_SHAP" for col in feature_names]

# Crear un dataframe temporal con los SHAP values
shap_df = pd.DataFrame(shap_values, columns=shap_cols, index=df.index)
df_full = pd.concat([df, shap_df], axis=1)

col_main, col_gui = st.columns([2, 1])

with col_main:
    st.subheader("🔸 Visión Panorámica: ¿De qué cojea nuestro negocio?")
    global_shap_importance = shap_df.abs().mean().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10,6))
    global_shap_importance.plot(kind='barh', ax=ax, color='skyblue')
    ax.set_yticklabels([c.replace('_SHAP', '') for c in global_shap_importance.index])
    ax.set_xlabel("Nivel de Impacto General")
    st.pyplot(fig)

    st.divider()

    st.subheader("🔸 Diagnóstico Individual: Historial del Paciente")
    umbral = st.session_state.umbral
    high_risk = df_full[df_full['Predicted_Prob'] >= umbral].sort_values(by='Predicted_Prob', ascending=False)

    if high_risk.empty:
        st.warning("No hay clientes que superen el umbral de riesgo seleccionado.")
    else:
        selected_id = st.selectbox("Busque el ID de un Cliente en Riesgo:", high_risk['customerID'])

        if selected_id:
            client_data = df_full[df_full['customerID'] == selected_id].iloc[0]
            client_shap = client_data[shap_cols]
            client_shap.index = feature_names
            client_shap = client_shap.sort_values(ascending=True)
            
            fig2, ax2 = plt.subplots(figsize=(8,5))
            colors = ['firebrick' if v > 0 else 'forestgreen' for v in client_shap.values]
            client_shap.plot(kind='barh', color=colors, ax=ax2)
            st.pyplot(fig2)
            st.info("🔴 **Rojo**: Empuja a irse | 🟢 **Verde**: Anima a quedarse")

with col_gui:
    st.info("### 📘 Guía Rápida para Directivos")
    st.markdown(f"""
    **¿Por qué este módulo es vital?**
    La IA no es una "caja negra". Aquí vemos el **porqué** de sus decisiones.
    
    1.  **Visión Panorámica:** Le dice qué falla en la empresa a nivel general (ej. si el tipo de contrato está molestando a todos).
    2.  **Diagnóstico Individual:** Es como un "análisis de sangre" del cliente. Antes de llamarlo, usted ya sabe cuál es su problema principal.
    
    **Uso Estratégico:** 
    Si la barra roja más larga es 'Contrato Mensual', la estrategia es ofrecerle pasar a un 'Contrato Anual' con descuento. Así la llamada de retención es quirúrgica y efectiva.
    """)
