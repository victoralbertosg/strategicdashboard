import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import load_data

st.set_page_config(page_title="Toma de Decisiones", layout="wide")
st.title("🧩 Módulo 4: Listado Diario de Operaciones")
st.markdown("Esta pantalla le dice directamente a su Fuerza de Ventas o Call Center: **A quién llamar, qué decirles para convencerlos y qué ofrecer.** Se basa en un cruce inteligente entre el riesgo que detectó el sistema y que tanto dinero le aporta ese cliente.")

df = load_data()
if df is None:
    st.error("Faltan datos.")
    st.stop()

# Traducción a nombres comerciales
df['Riesgo de irse'] = pd.cut(df['Predicted_Prob'], bins=[0, 0.3, 0.7, 1.0], labels=['Tranquilo', 'Cuidado', 'Peligro Inminente'])
if 'TotalCharges' in df.columns:
    df['Impacto Financiero del Cliente'] = pd.cut(df['TotalCharges'], bins=[-1, 500, 2000, 100000], labels=['Poco rentable', 'Promedio', 'Cliente VIP (Alto)'])
else:
    df['Impacto Financiero del Cliente'] = 'Promedio'

shap_cols = [c for c in df.columns if c.endswith('_SHAP')]
def get_top_reason(row):
    vals = row[shap_cols]
    max_feat = vals.idxmax()
    return max_feat.replace('_SHAP', '')

df['Motivo principal de molestia'] = df.apply(get_top_reason, axis=1)

def accion(row):
    riesgo = row['Riesgo de irse']
    valor = row['Impacto Financiero del Cliente']
    if riesgo == 'Peligro Inminente' and valor == 'Cliente VIP (Alto)':
        return '🚨 INTERVENIR URGENTE (Dar máximo descuento)'
    elif riesgo == 'Peligro Inminente' and valor == 'Poco rentable':
        return '🤔 Dejar ir (Retenerlo cuesta más que lo que produce)'
    elif riesgo == 'Cuidado' and valor == 'Cliente VIP (Alto)':
        return '📞 Llamada cordial y chequeo de satisfacción'
    else:
        return '💤 No hacer nada aún'

df['Acción sugerida para Call Center'] = df.apply(accion, axis=1)

# Planilla de Decisiones
st.subheader("📋 Planilla de Atenciones (Enfoque de máxima rentabilidad)")

# --- SECCIÓN DE FILTROS ---
acciones_unicas = df['Acción sugerida para Call Center'].unique().tolist()
filtro_accion = st.multiselect("Filtrar por Acción Sugerida:", options=acciones_unicas, default=acciones_unicas)

# Aplicar filtro
df_filtrado = df[df['Acción sugerida para Call Center'].isin(filtro_accion)].copy()

# --- SECCIÓN DE MÉTRICAS (ARRIBA) ---
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
total_clientes = len(df_filtrado)

# Conteo de acciones para las etiquetas
counts = df_filtrado['Acción sugerida para Call Center'].value_counts()

with col_m1:
    st.metric("Total Clientes", f"{total_clientes:,}")
with col_m2:
    n_urgente = counts.get('🚨 INTERVENIR URGENTE (Dar máximo descuento)', 0)
    st.metric("🚨 Urgentes", f"{n_urgente:,}")
with col_m3:
    n_cordial = counts.get('📞 Llamada cordial y chequeo de satisfacción', 0)
    st.metric("📞 Cordiales", f"{n_cordial:,}")
with col_m4:
    n_dejar = counts.get('🤔 Dejar ir (Retenerlo cuesta más que lo que produce)', 0)
    st.metric("🤔 Dejar Ir", f"{n_dejar:,}")
with col_m5:
    n_nada = counts.get('💤 No hacer nada aún', 0)
    st.metric("💤 Otros", f"{n_nada:,}")

st.markdown("---")

# --- PREPARACIÓN DE LA TABLA ---
# 1. Agregar numeración
df_filtrado = df_filtrado.sort_values(
    by=['Predicted_Prob', 'TotalCharges'], 
    ascending=[False, False]
).reset_index(drop=True)
df_filtrado.index += 1  # Numeración desde 1
df_filtrado['#'] = df_filtrado.index

# 2. Formatear impacto financiero (moneda)
if 'TotalCharges' in df_filtrado.columns:
    df_filtrado['Impacto ($)'] = df_filtrado['TotalCharges'].apply(lambda x: f"${x:,.2f}")
else:
    df_filtrado['Impacto ($)'] = "$0.00"

# 3. Seleccionar y reordenar columnas
view_df = df_filtrado[['#', 'customerID', 'Riesgo de irse', 'Impacto Financiero del Cliente', 'Impacto ($)', 'Motivo principal de molestia', 'Acción sugerida para Call Center']]

# Mostrar Tabla
st.dataframe(view_df, use_container_width=True, hide_index=True)

# --- LEYENDA Y DETALLE DE CÁLCULOS (ABAJO) ---
with st.expander("📝 ¿Cómo se calcula esta lista? (Criterios y Explicación)"):
    st.markdown("""
    ### ¿Por qué aparecen estos clientes en este orden?
    El sistema no elige al azar. Para maximizar el dinero que la empresa mantiene, usamos dos reglas principales:
    
    1.  **Probabilidad de Fuga (Riesgo):** Es qué tan probable es que el cliente nos abandone según su comportamiento (contrato, servicios, tiempo). 
        *   🔴 **Peligro Inminente:** Tienen más de 70% de probabilidad de irse.
        *   🟡 **Cuidado:** Tienen entre 30% y 70%.
        *   🟢 **Tranquilo:** Tienen menos de 30%.
    
    2.  **Valor del Cliente (Impacto Financiero):** Miramos cuánto dinero ha pagado el cliente históricamente.
        *   💎 **VIP:** Clientes que han pagado más de $2,000. Son nuestra prioridad número uno.
        *   ⚖️ **Promedio:** Clientes entre $500 y $2,000.
        *   🌱 **Bajo:** Clientes con menos de $500 en pagos.

    ### ¿Cuál es la lógica de las acciones?
    *   **🚨 Intervención Urgente:** Se activa solo cuando un cliente de **Alto Valor** está en **Peligro Inminente**. Aquí se justifica dar descuentos agresivos porque perderlos costaría miles de dólares.
    *   **📞 Llamada Cordial:** Para clientes valiosos que muestran señales de alerta leves. Prevenir es más barato que curar.
    *   **🤔 Dejar ir:** Si un cliente en alto riesgo nos genera muy pocos ingresos, a veces es más rentable dejarlo ir que gastar tiempo y dinero del equipo en retenerlo.
    
    *Nota: El impacto financiero se muestra en la columna **Impacto ($)** y representa el total de ingresos que el cliente ha aportado a la fecha.*
    """)

st.success("✔️ Esta planilla traduce la complejidad técnica en instrucciones directas para proteger los ingresos de la compañía.")
