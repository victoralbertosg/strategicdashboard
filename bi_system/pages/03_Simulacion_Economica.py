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
active_model = st.session_state.current_model_name

# Lógica Financiera
TP = len(df[(df['Predicted_Class'] == 1) & (df['Churn_Real'] == 1)])
FP = len(df[(df['Predicted_Class'] == 1) & (df['Churn_Real'] == 0)])
FN = len(df[(df['Predicted_Class'] == 0) & (df['Churn_Real'] == 1)])
TN = len(df[(df['Predicted_Class'] == 0) & (df['Churn_Real'] == 0)])

perdida_escenario_A = (TP + FN) * clv_inv
inversion_retencion = (TP + FP) * costo_retencion
clientes_retenidos_valor = TP * clv_inv
ganancia_neta_modelo = clientes_retenidos_valor - inversion_retencion

st.subheader("Resultados de la Simulación")
st.info(f"**Configuración Activa:** Modelo: `{active_model}` | Umbral de Riesgo: `{threshold:.2f}` ({threshold*100:.0f}%)")

col_main, col_gui = st.columns([2, 1])

with col_main:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div style='background-color:#ffe6e6; padding:15px; border-radius:10px; border-left: 5px solid red; color:#330000;'>", unsafe_allow_html=True)
        st.markdown("### 🔴 Escenario A: Sin IA (Pasivo)")
        st.metric("Pérdida Económica Proyectada", f"-${perdida_escenario_A:,.2f}")
        st.markdown("**Fórmula:** *Pérdida = (TP + FN) × LTV*")
        st.markdown(f"**Cálculo:** ({TP} + {FN}) × ${clv_inv} = **${perdida_escenario_A:,.2f}**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='background-color:#e6ffe6; padding:15px; border-radius:10px; border-left: 5px solid green; color:#003300;'>", unsafe_allow_html=True)
        st.markdown("### 🟢 Escenario B: Con IA (Intervención)")
        st.metric("Beneficio Neto del Modelo", f"${ganancia_neta_modelo:,.2f}")
        st.markdown("**Fórmula:** *Ganancia = (TP × LTV) - ((TP + FP) × Costo)*")
        st.markdown(f"**Cálculo:** ({TP} × ${clv_inv}) - ({TP + FP} × ${costo_retencion}) = **${ganancia_neta_modelo:,.2f}**")
        st.markdown("</div>", unsafe_allow_html=True)



    st.divider()
    
    st.subheader("📊 Matriz de Confusión Financiera")
    c_cm1, c_cm2 = st.columns([1, 1])
    with c_cm1:
        # Dibujar la matriz de confusión
        fig_cm, ax_cm = plt.subplots(figsize=(5, 4))
        cm_matrix = np.array([[TN, FP], [FN, TP]])
        import seaborn as sns
        sns.heatmap(cm_matrix, annot=True, fmt='d', cmap='Blues', ax=ax_cm,
                    xticklabels=['Pred: Leal', 'Pred: Fuga'],
                    yticklabels=['Real: Leal', 'Real: Fuga'])
        ax_cm.set_xlabel('Predicción del Modelo')
        ax_cm.set_ylabel('Realidad')
        ax_cm.set_title(f'Matriz de Confusión (Umbral {threshold:.2f})')
        st.pyplot(fig_cm)
    with c_cm2:
        st.markdown(f"""
        **Desglose operativo para {active_model} con umbral {threshold*100:.0f}%:**
        *   **Verdaderos Positivos (TP):** `{TP}` (fugas predichas y reales: clientes retenidos con éxito).
        *   **Falsos Positivos (FP):** `{FP}` (alarmas falsas: inversión de campaña innecesaria).
        *   **Falsos Negativos (FN):** `{FN}` (fugas sorpresa no detectadas).
        *   **Verdaderos Negativos (TN):** `{TN}` (clientes leales detectados correctamente).
        *   **Total Clientes Evaluados ($N$):** `{len(df)}`
        """)

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
    st.info("### 📘 Guía de Simulación y Cálculos Detallados")
    st.markdown(fr"""
    **¿Cómo se llega a estos valores en base al comportamiento de los clientes?**
    
    El simulador financiero cruza las métricas operativas del modelo con las variables financieras configuradas en el panel de la izquierda.
    
    ---
    
    ### 🔴 Escenario A: Sin IA (Pasivo)
    En una estrategia pasiva, no intervenimos a nadie. Por lo tanto, todos los clientes que realmente se iban a fugar se pierden.
    
    *   **Fugas Reales:** **{TP + FN}** clientes (Verdaderos Positivos **{TP}** + Falsos Negativos **{FN}**).
    *   **Pérdida por Cliente ($LTV$):** ${clv_inv:,.2f} USD$.
    *   **Pérdida Económica Total:** 
        $$({TP} + {FN}) \times {clv_inv} \text{{ USD}} = \mathbf{{-{perdida_escenario_A:,.2f} \text{{ USD}}}}$$
        
    ---
    
    ### 🟢 Escenario B: Con IA (Intervención Inteligente)
    Realizamos una campaña de retención preventiva orientada únicamente a los **{TP + FP}** clientes que el modelo predictivo marca como en riesgo.
    
    1.  **Inversión en Retención:**
        Gastamos el Costo de Retención (${costo_retencion:,.2f} USD) por cada uno de los **{TP + FP}** clientes intervenidos.
        $$\text{{Inversión}} = ({TP} + {FP}) \times {costo_retencion} \text{{ USD}} = \mathbf{{{inversion_retencion:,.2f} \text{{ USD}}}}$$
        
    2.  **Valor Económico Recuperado:**
        De los intervenidos, **{TP}** clientes realmente planeaban fugarse ($TP$). Al fidelizarlos, los retenemos y recuperamos su valor ($LTV$ = ${clv_inv:,.2f} USD$).
        $$\text{{Ingreso Recuperado}} = {TP} \times {clv_inv} \text{{ USD}} = \mathbf{{{clientes_retenidos_valor:,.2f} \text{{ USD}}}}$$
        
    3.  **Alarmas Falsas ($FP$):**
        Los **{FP}** restantes son clientes leales marcados por error. En ellos gastamos el costo de campaña sin recuperar valor adicional.
        
    4.  **Beneficio Neto del Modelo:**
        Ingreso recuperado menos la inversión realizada en la campaña.
        $$\text{{Ganancia}} = {clientes_retenidos_valor:,.2f} \text{{ USD}} - {inversion_retencion:,.2f} \text{{ USD}} = \mathbf{{{ganancia_neta_modelo:,.2f} \text{{ USD}}}}$$
        
    ---
    
    ### ⚡ Impacto de la IA (Mejora B vs A)
    La diferencia neta a favor del modelo es la suma del beneficio generado más la pérdida evitada:
    $$\text{{Mejora}} = {ganancia_neta_modelo:,.2f} \text{{ USD}} - (-{perdida_escenario_A:,.2f} \text{{ USD}}) = \mathbf{{{ganancia_neta_modelo + perdida_escenario_A:,.2f} \text{{ USD}}}}$$
    
    *Pruebe variando los **Parámetros Financieros** o el **Umbral de Riesgo** en la barra lateral para recalcular estas cifras al instante.*
    """)
