import streamlit as st
from utils import load_data

st.set_page_config(page_title="Visión General - Prevención de Fuga", page_icon="🏢", layout="wide")

st.title("🖥️ Visión General: Estado Actual de la Cartera de Clientes")
st.markdown("""
**Bienvenido al Sistema Inteligente de Prevención de Fugas.** 

Este panel directivo analiza en tiempo real el comportamiento de los clientes para identificar patrones de riesgo. El sistema le permite anticiparse al abandono, comprender sus causas subyacentes y evaluar el impacto económico de posibles intervenciones preventivas.
""")

df = load_data()

if df is None:
    st.error("⚠️ No se encontraron los datos procesados. Por favor avise a su equipo técnico para la carga inicial.")
    st.stop()

# KPIs Básicos
tasa_churn = (df['Predicted_Class'].sum() / len(df)) * 100
riesgo_n = len(df[df['Predicted_Class'] == 1])

# Estimación sencilla de pérdida
if 'TotalCharges' in df.columns:
    perdida_estimada = df.loc[df['Predicted_Class'] == 1, 'TotalCharges'].sum()
else:
    perdida_estimada = riesgo_n * 300

col1, col2, col3 = st.columns(3)
col1.metric("📉 Fuga Potencial Estimada (%)", f"{tasa_churn:.1f}%", help="Porcentaje de clientes que el sistema cree que nos abandonarán pronto.")
col2.metric("👥 Clientes en Riesgo (Cantidad)", f"{riesgo_n:,}", help="Número exacto de personas en la zona de peligro.")
col3.metric("💸 Dinero en Peligro (Sin intervenir)", f"${perdida_estimada:,.2f}", help="El valor económico que perderemos si no hacemos nada al respecto.")

st.divider()
st.subheader("Panorama General de Riesgo")
st.markdown("Visualice gráficamente cómo se reparten sus clientes. Entre más alta sea la barra a la derecha, mayor probabilidad de que nos abandonen.")
st.bar_chart(df['Predicted_Prob'])

st.info("👈 **Use el menú de la izquierda** para explorar cómo funciona el sistema, ver los motivos de las fugas y simular cuánto dinero puede recuperar.")
