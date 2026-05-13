import streamlit as st
from utils import load_data, init_global_controls

st.set_page_config(page_title="Visión General - Prevención de Fuga", page_icon="🏢", layout="wide")

# Inicializar controles globales en el sidebar
init_global_controls()

st.title("🖥️ Visión General: Estado Actual de la Cartera de Clientes")
st.markdown("""
**Bienvenido al Sistema Inteligente de Prevención de Fugas.** 

Este panel directivo analiza en tiempo real el comportamiento de los clientes para identificar patrones de riesgo. El sistema le permite anticiparse al abandono, comprender sus causas subyacentes y evaluar el impacto económico de posibles intervenciones preventivas.
""")

df = load_data()

if df is None:
    st.error("⚠️ No se encontraron los datos procesados. Por favor avise a su equipo técnico para la carga inicial.")
    st.stop()

# KPIs Dinámicos basados en selección de usuario
tasa_churn = (df['Predicted_Class'].sum() / len(df)) * 100
riesgo_n = int(df['Predicted_Class'].sum())

# Estimación de pérdida basada en el modelo y umbral activo
if 'TotalCharges' in df.columns:
    perdida_estimada = df.loc[df['Predicted_Class'] == 1, 'TotalCharges'].sum()
else:
    perdida_estimada = riesgo_n * 300

col1, col2, col3 = st.columns(3)
col1.metric("📉 Fuga Potencial Estimada (%)", f"{tasa_churn:.1f}%", help="Porcentaje de clientes que el sistema cree que nos abandonarán pronto.")
col2.metric("👥 Clientes en Riesgo (Cantidad)", f"{riesgo_n:,}", help=f"Número de personas detectadas por {st.session_state.current_model_name} con riesgo > {st.session_state.umbral*100:.0f}%.")
col3.metric("💸 Dinero en Peligro (Valor Histórico)", f"${perdida_estimada:,.2f}", help="Suma de los pagos históricos realizados por los clientes actualmente en riesgo.")

st.divider()

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 Distribución de Probabilidades de Fuga")
    st.markdown("Este gráfico muestra cuántos clientes hay en cada nivel de riesgo. Los que están a la derecha son los más críticos.")
    st.bar_chart(df['Predicted_Prob'])

with col_right:
    # --- LEYENDA PARA USUARIOS NO TÉCNICOS ---
    st.info("### 📘 Guía Rápida para Directivos")
    st.markdown(f"""
    **¿Qué estoy viendo?**
    Usted está usando la inteligencia artificial **{st.session_state.current_model_name}** para auditar su cartera.
    
    1. **Clientes en Riesgo ({riesgo_n}):** Son las personas que, según sus patrones de consumo, superan el **{st.session_state.umbral*100:.0f}%** de probabilidad de irse.
    
    2. **Dinero en Peligro (${perdida_estimada:,.2f}):** No es una pérdida futura exacta, sino el valor acumulado de lo que estos clientes han pagado. Si se van, perdemos clientes que históricamente valen esa cantidad.
    
    3. **¿Por qué cambian los números?** 
    Si usted baja el **Umbral de Riesgo** en la barra lateral, el sistema se vuelve más 'sensible' y detectará a más personas (será más preventivo).
    """)

st.divider()
st.info("👈 **Use el menú de la izquierda** para explorar cómo funciona el sistema, ver los motivos de las fugas y simular cuánto dinero puede recuperar.")
