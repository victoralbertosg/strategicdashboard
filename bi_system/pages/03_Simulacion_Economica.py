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
    
    st.subheader("🔍 Explicación Detallada de los Cálculos")
    st.markdown(f"""
    ¿Cómo se llega a estos valores en base al comportamiento de los clientes?
    
    1. **Pérdida en Escenario A (Sin Intervención):**
       - En una estrategia pasiva, no intervenimos a nadie. Por lo tanto, todos los clientes que realmente se iban a fugar se pierden.
       - El número de clientes que realmente fugan es **{TP + FN}** (Verdaderos Positivos **{TP}** + Falsos Negativos **{FN}**).
       - Perder a estos clientes nos cuesta su Valor de Vida promedio ($LTV$ = ${clv_inv:,.2f} USD).
       - **Pérdida Total:** ({TP} + {FN}) × ${clv_inv} = **${perdida_escenario_A:,.2f} USD**.
       
    2. **Cálculos en Escenario B (Con Intervención Inteligente):**
       - La IA identifica en riesgo a **{TP + FP}** clientes (los de Alerta Roja por superar el umbral).
       - Decidimos realizar una campaña preventiva para este grupo de clientes. Esto nos cuesta ${costo_retencion:,.2f} USD por cada uno.
       - **Inversión total de campaña:** ({TP} + {FP}) × ${costo_retencion} = **${inversion_retencion:,.2f} USD**.
       - De los clientes intervenidos, **{TP}** realmente planeaban fugarse ($TP$). Con la campaña preventiva, los retenemos y recuperamos su valor ($LTV$ = ${clv_inv:,.2f} USD).
       - **Ingreso recuperado:** {TP} × ${clv_inv} = **${clientes_retenidos_valor:,.2f} USD**.
       - Los **{FP}** restantes son falsas alarmas; gastamos el costo de campaña en ellos pero ya eran leales.
       - **Beneficio Neto del Modelo:** Ingreso recuperado (${clientes_retenidos_valor:,.2f} USD) menos la inversión de campaña (${inversion_retencion:,.2f} USD) = **${ganancia_neta_modelo:,.2f} USD**.
       - **Mejora del Escenario B vs A:** La diferencia económica a favor del modelo es el beneficio neto (${ganancia_neta_modelo:,.2f}) menos la pérdida evitada (-${perdida_escenario_A:,.2f}), lo que da un impacto de **${ganancia_neta_modelo + perdida_escenario_A:,.2f} USD**.
    """)

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
