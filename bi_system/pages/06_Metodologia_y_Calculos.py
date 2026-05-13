import streamlit as st
from utils import init_global_controls

st.set_page_config(page_title="Metodología y Cálculos", layout="wide")
init_global_controls()

st.title("📚 Metodología, Glosario y Fórmulas del Sistema")
st.markdown(f"""
Este documento detalla la lógica matemática y los procedimientos de negocio integrados en este sistema. 
Actualmente el sistema está operando con el modelo **{st.session_state.current_model_name}** y un umbral de **{st.session_state.umbral*100:.0f}%**.
""")

with st.expander("💰 1. Valor del Cliente (Dinero en Peligro)", expanded=True):
    st.markdown("""
    **Definición:** Representa el valor económico histórico que los clientes en riesgo han aportado a la empresa.
    
    *   **¿Cómo se calcula?** Se toma el campo `TotalCharges` (Facturación acumulada) de cada cliente que el sistema marca como "En Riesgo".
    *   **Interpretación:** "Si perdemos a estos clientes, perderemos una porción de nuestra base instalada que históricamente vale $X". 
    *   **Interactividad:** Este número cambia si usted cambia de modelo o si baja el umbral, ya que la lista de clientes capturados varía.
    """)

with st.expander("📉 2. Umbral de Riesgo (La Perilla de Sensibilidad)"):
    st.markdown(f"""
    **Definición:** Es el punto de corte que usted decide para considerar que una alerta es real.
    
    *   **Umbral Actual:** {st.session_state.umbral*100:.0f}%
    *   **Lógica:** Si la IA dice que un cliente tiene un 55% de probabilidad de irse:
        *   Si su umbral es **50%**, el cliente aparecerá como **Rojo (Peligro)**.
        *   Si su umbral es **60%**, el cliente aparecerá como **Amarillo (Cuidado)**.
    *   **Uso Estratégico:** 
        *   Use un umbral **bajo** (ej. 30%) si tiene mucha capacidad de llamadas y quiere ser muy preventivo.
        *   Use un umbral **alto** (ej. 75%) si tiene poco presupuesto y solo quiere llamar a los casos desesperados.
    """)

with st.expander("📊 3. Comparativa de Inteligencias Artificiales (Módulo 5)"):
    st.markdown("""
    El sistema permite elegir entre tres tipos de "Cerebros Digitales":
    
    1.  **XGBoost:** Algoritmo de última generación muy potente para encontrar patrones complejos y no lineales. Es el estándar moderno.
    2.  **Regresión Logística:** Un método estadístico clásico y transparente. Muy útil si se busca simplicidad y relaciones directas.
    3.  **Random Forest:** Un bosque de decisiones que votan democráticamente para predecir. Es muy estable y difícil de engañar.
    """)

with st.expander("📈 4. Cálculo de Ganancia Neta"):
    st.markdown("""
    **Fórmula:**
    `Ganancia Neta = (Clientes Salvados × LTV) - (Total de Intervenciones × Costo de Retención)`
    
    *   **Interactividad:** Al ajustar el umbral en la barra lateral, usted está buscando el punto de equilibrio donde salva la mayor cantidad de dinero posible sin gastar demasiado en incentivos para gente que no se iba a ir (Falsos Positivos).
    """)

st.info("💡 **Nota Final:** Esta herramienta transforma la ciencia de datos en una simulación financiera interactiva, permitiendo que la gerencia tome control sobre el nivel de riesgo que está dispuesta a tolerar.")
