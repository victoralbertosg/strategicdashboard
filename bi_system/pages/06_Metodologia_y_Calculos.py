import streamlit as st

st.set_page_config(page_title="Metodología y Cálculos", layout="wide")

st.title("📚 Metodología, Glosario y Fórmulas del Sistema")
st.markdown("""
Este documento detalla la lógica matemática y los procedimientos de negocio integrados en este sistema de Business Intelligence. El objetivo es proporcionar transparencia total sobre cómo se generan las recomendaciones y los cálculos financieros.
""")

with st.expander("💰 1. Valor del Cliente (LTV - Lifetime Value)", expanded=True):
    st.markdown("""
    **Definición:** Representa el valor económico total que un cliente aporta a la empresa durante su permanencia.
    
    *   **En este sistema:** Se utiliza para proyectar las pérdidas por fuga y las ganancias por retención.
    *   **Cálculo predeterminado:** Si no se especifica, el sistema utiliza el campo `TotalCharges` (Facturación acumulada) como una aproximación del valor histórico.
    *   **Uso en Simulaciones:** En el Módulo 3, el usuario puede ajustar este valor manualmente para realizar análisis de sensibilidad ("¿Qué pasa si cada cliente vale $X en promedio?").
    """)

with st.expander("📉 2. Fuga Residual (Pérdida no detectada)"):
    st.markdown("""
    **Definición:** Es el impacto económico de los clientes que el modelo **no logró identificar** (Falsos Negativos) y que terminaron abandonando la empresa.
    
    *   **Fórmula:** `Fuga Residual = Cantidad de Falsos Negativos (FN) × Valor del Cliente (LTV)`
    *   **Interpretación:** Representa la "oportunidad perdida". Es el dinero que se escapa por las grietas del modelo. Ningún modelo es perfecto, por lo que siempre existirá una fuga residual. Nuestro objetivo es minimizarla maximizando el *Recall*.
    """)

with st.expander("📊 3. Clasificación de Impacto Financiero"):
    st.markdown("""
    El sistema categoriza a los clientes según su rentabilidad histórica para priorizar los esfuerzos del Call Center:
    
    | Categoría | Rango de Facturación (TotalCharges) | Prioridad Operativa |
    | :--- | :--- | :--- |
    | **Cliente VIP (Alto)** | > $2,000 | **Crítica:** Pérdida de alto impacto. |
    | **Promedio** | $500 - $2,000 | **Media:** Base estable de ingresos. |
    | **Poco rentable** | < $500 | **Baja:** El costo de retención podría superar su valor. |
    """)

with st.expander("🚨 4. Niveles de Riesgo de Abandono (Churn Risk)"):
    st.markdown("""
    La inteligencia artificial asigna una **Probabilidad de Fuga (0% a 100%)** a cada cliente. Estas probabilidades se agrupan en rangos semánticos:
    
    *   **Peligro Inminente (Riesgo > 70%):** Clientes con comportamiento muy similar a quienes ya se fueron. Requieren acción hoy.
    *   **Cuidado (Riesgo 30% - 70%):** Clientes que muestran señales de alerta temprana (detonantes de insatisfacción).
    *   **Tranquilo (Riesgo < 30%):** Clientes con patrones de comportamiento estables y leales.
    """)

with st.expander("📞 5. Matriz de Decisiones y Acciones Sugeridas"):
    st.markdown("""
    El sistema cruza el **Riesgo** con el **Valor** para sugerir la acción más rentable en el Módulo 4:
    
    1.  **Intervención Urgente:** (Riesgo Alto + Valor VIP). Se sugiere ofrecer el máximo descuento o beneficio disponible para retener la cuenta a toda costa.
    2.  **Llamada Cordial:** (Riesgo Medio + Valor VIP). Acción preventiva para asegurar la satisfacción antes de que el riesgo escale.
    3.  **Dejar Ir (Silent Churn):** (Riesgo Alto + Valor Bajo). Si el costo de la campaña/descuento es mayor que el LTV del cliente, el sistema sugiere no intervenir para proteger el margen operativo.
    4.  **No hacer nada:** Situaciones de bajo riesgo.
    """)

with st.expander("📈 6. Cálculo de Ganancia Neta del Modelo"):
    st.markdown("""
    Esta fórmula mide el **Retorno de Inversión (ROI)** de implementar este sistema BI:
    
    **Fórmula:**
    `Ganancia Neta = (Clientes Salvados × LTV) - (Total de Intervenciones × Costo de Retención)`
    
    *   **Clientes Salvados:** Verdaderos Positivos detectados por el modelo.
    *   **Total de Intervenciones:** Verdaderos Positivos + Falsos Positivos (Personas a las que les dimos un beneficio).
    *   **Costo de Retención:** El valor del cupón, descuento o regalo otorgado.
    """)

st.info("💡 **Nota Final:** Esta metodología transforma un problema de ciencia de datos en una herramienta de gestión financiera, asegurando que cada dólar invertido en retención tenga una justificación matemática.")
