import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import load_data

st.set_page_config(page_title="Explicabilidad y Diagnóstico", layout="wide")
st.title("🧩 Módulo 2: Diagnóstico Causal (XAI)")
st.markdown("A diferencia de sistemas antiguos que operaban como una 'caja negra' donde nadie sabía por qué tomaban decisiones, **nuestra tecnología nos explica los motivos detrás de cada alerta**. Aquí desglosamos por qué la gente se quiere ir.")

df = load_data()
if df is None:
    st.error("Faltan datos.")
    st.stop()

shap_cols = [c for c in df.columns if c.endswith('_SHAP')]
features = [c.replace('_SHAP', '') for c in shap_cols]

st.subheader("🔸 Visión Panorámica: ¿De qué cojea nuestro negocio?")
st.markdown("¿Cuáles son los factores más determinantes a nivel macro? Estas son las características de su servicio que más afectan si el cliente decide quedarse o irse a la competencia.")

global_shap_importance = df[shap_cols].abs().mean().sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(10,6))
global_shap_importance.plot(kind='barh', ax=ax, color='skyblue')
ax.set_yticklabels([c.replace('_SHAP', '') for c in global_shap_importance.index])
ax.set_xlabel("Nivel de Culpa/Impacto General")
ax.set_title("Las características comerciales que más mueven la balanza")
st.pyplot(fig)

st.divider()

st.subheader("🔸 Diagnóstico Individual Médico: Paciente por Paciente")
st.markdown("Seleccione a un cliente diagnosticado en 'Peligro Inminente' para ver exactamente qué factores le están irritando y empujándolo a irse.")

df['Nivel de Alerta'] = pd.cut(df['Predicted_Prob'], bins=[0, 0.3, 0.7, 1.0], labels=['Tranquilo', 'Cuidado', 'Peligro Inminente'])
high_risk = df[df['Nivel de Alerta'] == 'Peligro Inminente'].sort_values(by='Predicted_Prob', ascending=False)

selected_id = st.selectbox("Busque el ID de un Cliente en Riesgo:", high_risk['customerID'])

if selected_id:
    client_data = df[df['customerID'] == selected_id].iloc[0]
    
    shap_vals = client_data[shap_cols]
    shap_vals.index = features
    shap_vals = shap_vals.sort_values(ascending=True)
    
    fig2, ax2 = plt.subplots(figsize=(8,4))
    colors = ['firebrick' if v > 0 else 'forestgreen' for v in shap_vals.values]
    shap_vals.plot(kind='barh', color=colors, ax=ax2)
    ax2.set_xlabel("Fuerza del Motivo")
    ax2.set_title(f"Motivaciones psicológicas o comerciales para el cliente {selected_id}")
    st.pyplot(fig2)
    st.info("🔴 **Barras Rojas**: Le están empujando a **IRSE** (Ej. Su costo mensual es alto, no tiene garantías).\n\n🟢 **Barras Verdes**: Le están animando a **QUEDARSE** (Ej. Está atado a un contrato largo, le gusta el servicio técnico).")
