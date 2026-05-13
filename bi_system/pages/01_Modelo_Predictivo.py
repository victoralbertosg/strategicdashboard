import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, init_global_controls, paginate_dataframe
from sklearn.metrics import confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Predicciones", layout="wide")
init_global_controls()

st.title("🧩 Módulo 1: Aciertos del Sistema Predictivo")
st.markdown(f"Esta sección demuestra qué tan preciso es el modelo **{st.session_state.current_model_name}** con un nivel de sensibilidad del **{st.session_state.umbral*100:.0f}%**.")

df = load_data()
if df is None:
    st.error("Faltan datos.")
    st.stop()

# Usamos el umbral global
threshold = st.session_state.umbral

col_main, col_gui = st.columns([2, 1])

with col_main:
    st.subheader("📊 Fiabilidad de las Alertas")
    st.markdown("Estos gráficos nos indican si estamos listos para confiar nuestro dinero al sistema.")
    col1, col2 = st.columns(2)

    fpr, tpr, _ = roc_curve(df['Churn_Real'], df['Predicted_Prob'])
    roc_auc = auc(fpr, tpr)

    with col1:
        fig, ax = plt.subplots(figsize=(5,4))
        ax.plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC: {roc_auc:.3f}')
        ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', alpha=0.3)
        ax.set_xlabel('Falsas Alarmas')
        ax.set_ylabel('Aciertos')
        ax.set_title('Capacidad de Discriminación')
        ax.legend(loc="lower right")
        st.pyplot(fig)

    with col2:
        cm = confusion_matrix(df['Churn_Real'], df['Predicted_Class'])
        fig2, ax2 = plt.subplots(figsize=(5,4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax2, 
                    xticklabels=['Se queda', 'Se va'], 
                    yticklabels=['Se queda', 'Se va'])
        ax2.set_xlabel('Lo que el SISTEMA DIJO')
        ax2.set_ylabel('Lo que REALMENTE PASÓ')
        ax2.set_title('Resumen de Éxitos y Fracasos')
        st.pyplot(fig2)

    st.divider()
    st.subheader("📋 Previsualización de Datos")
    df_preview = df[['customerID', 'Predicted_Prob', 'Predicted_Class']].sort_values(by='Predicted_Prob', ascending=False)
    df_paginated, render_pagination = paginate_dataframe(df_preview, key="preview_pagination")
    st.dataframe(df_paginated, use_container_width=True)
    render_pagination()

with col_gui:
    st.info("### 📘 Guía Rápida para Directivos")
    st.markdown(f"""
    **¿Cómo mido el éxito de la IA?**
    La precisión de un modelo no es perfecta (son máquinas), por eso usamos estas métricas:
    
    1.  **Aciertos (Cuadros Oscuros):** Son los casos donde la IA dijo que se iban y efectivamente se fueron. Aquí es donde ganamos dinero.
    2.  **Falsas Alarmas:** Son clientes leales que la IA marcó como riesgo. Si los llamamos, les daremos un descuento que no necesitaban (Inversión innecesaria).
    3.  **Fugas Sorpresa:** Clientes que se fueron y la IA no detectó. 
    
    **Regla de Oro:** 
    Ajuste el **Umbral de Riesgo** a la izquierda. Si lo baja, tendrá más aciertos pero también más falsas alarmas. Busque su punto de equilibrio financiero.
    """)
