import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, init_global_controls, get_current_shap_values, paginate_dataframe

st.set_page_config(page_title="Toma de Decisiones", layout="wide")
init_global_controls()

st.title("🧩 Módulo 4: Listado Diario de Operaciones")
st.markdown(f"**Cerebro Digital:** {st.session_state.current_model_name} | **Umbral de Alerta:** {st.session_state.umbral*100:.0f}%")

df = load_data()
if df is None:
    st.error("Faltan datos.")
    st.stop()

# Lógica dinámica de Riesgo con etiquetas amigables
umbral = st.session_state.umbral
df['Clasificación de Riesgo'] = pd.cut(
    df['Predicted_Prob'], 
    bins=[0, umbral * 0.5, umbral, 1.0], 
    labels=['✅ Estable / Leal', '⚠️ Alerta Amarilla (Preventiva)', '🚨 Alerta Roja (Rescate Urgente)']
)

if 'TotalCharges' in df.columns:
    df['Valor del Cliente'] = pd.cut(df['TotalCharges'], bins=[-1, 500, 2000, 1000000], labels=['Bronce', 'Plata', 'Oro (VIP)'])
else:
    df['Valor del Cliente'] = 'Plata'

# SHAP integration for reasons
shap_values, feature_names = get_current_shap_values(st.session_state.current_model_name)
shap_cols = [f"{col}_SHAP" for col in feature_names]
shap_df = pd.DataFrame(shap_values, columns=shap_cols, index=df.index)
df_full = pd.concat([df, shap_df], axis=1)

def get_top_reason(row):
    try:
        vals = row[shap_cols]
        max_feat = vals.idxmax()
        return max_feat.replace('_SHAP', '')
    except:
        return "Patrón complejo"

df_full['Motivo de Molestia'] = df_full.apply(get_top_reason, axis=1)

def accion_amigable(row):
    riesgo = row['Clasificación de Riesgo']
    valor = row['Valor del Cliente']
    
    if 'Roja' in riesgo:
        if valor == 'Oro (VIP)': return '🚨 LLAMADA GERENCIAL: Retener a toda costa'
        elif valor == 'Plata': return '⚡ Oferta agresiva de fidelización'
        else: return '🤔 Revisar rentabilidad antes de ofrecer'
    elif 'Amarilla' in riesgo:
        if valor == 'Oro (VIP)': return '📞 Llamada de cortesía / Chequeo de salud'
        elif valor == 'Plata': return '📧 Cupón de descuento exclusivo'
        else: return '💤 Mantener en observación'
    else:
        return '💤 Cliente estable'

df_full['Plan de Acción'] = df_full.apply(accion_amigable, axis=1)

# --- PANEL DE EXPLICACIÓN PARA NO TÉCNICOS ---
with st.container():
    st.info("### 🏁 ¿A quién debemos atender hoy?")
    c_e1, c_e2 = st.columns(2)
    with c_e1:
        st.markdown(f"""
        🔴 **ALERTA ROJA (Rescate Urgente):**
        Son clientes que ya tienen un pie fuera de la empresa. Su probabilidad de irse supera el **{umbral*100:.0f}%**.
        - **Objetivo:** Acción de choque inmediata.
        """)
    with c_e2:
        st.markdown(f"""
        🟡 **ALERTA AMARILLA (Prevención Temprana):**
        Son clientes que aún no están en peligro inminente, pero están mostrando "síntomas" de insatisfacción.
        - **Objetivo:** Fidelizar antes de que piensen en la competencia.
        """)

st.divider()

# --- SECCIÓN DE MÉTRICAS ---
counts = df_full['Clasificación de Riesgo'].value_counts()
n_roja = counts.get('🚨 Alerta Roja (Rescate Urgente)', 0)
n_amarilla = counts.get('⚠️ Alerta Amarilla (Preventiva)', 0)

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("🚨 Total Alerta Roja", f"{n_roja}", help="Clientes con riesgo crítico (Igual a la Visión General).")
col_m2.metric("⚠️ Total Alerta Amarilla", f"{n_amarilla}", help="Clientes con riesgo moderado para acciones preventivas.")
col_m3.metric("📈 Total Intervenciones Sugeridas", f"{n_roja + n_amarilla}", help="Suma de clientes en zona roja y zona amarilla.")

st.divider()

# --- FILTROS Y TABLA ---
st.subheader("📋 Detalle de la Cartera por Prioridad")
opciones_filtro = df_full['Plan de Acción'].unique().tolist()
filtro = st.multiselect("Filtrar listado por tipo de acción:", options=opciones_filtro, default=[o for o in opciones_filtro if '💤' not in o])

df_filtrado = df_full[df_full['Plan de Acción'].isin(filtro)].copy()
df_filtrado = df_filtrado.sort_values(by='Predicted_Prob', ascending=False)

# Limpiar tabla para visualización
if 'TotalCharges' in df_filtrado.columns:
    df_filtrado['Impacto ($)'] = df_filtrado['TotalCharges'].apply(lambda x: f"${x:,.2f}")
else:
    df_filtrado['Impacto ($)'] = "$0.00"

view_df = df_filtrado[['customerID', 'Clasificación de Riesgo', 'Valor del Cliente', 'Impacto ($)', 'Motivo de Molestia', 'Plan de Acción']]
df_paginated, render_pagination = paginate_dataframe(view_df, key="decision_pagination")
st.dataframe(df_paginated.reset_index(drop=True), use_container_width=True)
render_pagination()

# --- GUÍA RÁPIDA PARA ADMINISTRADORES ---
with st.expander("📘 Guía Rápida para Administradores", expanded=True):
    st.markdown("""
    ### Clasificación de Valor del Cliente (LTV)
    - **Oro (VIP):** Clientes con facturación histórica superior a $2,000. Son la máxima prioridad de retención.
    - **Plata:** Clientes con facturación entre $500 y $2,000. Representan la base estable del negocio.
    - **Bronce:** Clientes con facturación menor a $500. Evaluar el costo de retención vs. su valor futuro.

    ### Detalle de Clasificación de Riesgo
    - **🚨 Alerta Roja:** Probabilidad de fuga > Umbral seleccionado. Acción inmediata.
    - **⚠️ Alerta Amarilla:** Probabilidad de fuga cercana al umbral. Acción preventiva.
    - **✅ Estable:** Cliente con comportamiento leal. No requiere intervención.

    ### Terminología de la Tabla
    - **Motivo de Molestia:** Factor principal (detectado por la IA) que empuja al cliente a irse. Fundamental para el guion del Call Center.
    - **Plan de Acción:** Sugerencia automática que optimiza sus recursos (ej. no ofrecer descuentos agresivos a clientes de bajo valor si el costo de retención es alto).
    """)
