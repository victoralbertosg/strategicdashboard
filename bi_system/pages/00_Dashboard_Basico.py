import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Configuraciones de página
st.set_page_config(page_title="Telco Churn BI Dashboard", page_icon="📶", layout="wide")

# Rutas de datos
DATA_PATH = 'data/cleaned/bi_ready_predictions.csv'

@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        return df
    else:
        return None

def main():
    st.title("📶 Dashboard de Inteligencia de Negocios - Retención Predictiva")
    st.markdown("Sistema de apoyo a la toma de decisiones. Integra predicciones de Machine Learning, interpretabilidad de resultados (XAI) y simulación de rentabilidad económica.")

    df = load_data()
    
    if df is None:
        st.warning(f"⚠️ No se encontró el dataset en '{DATA_PATH}'. Por favor ejecuta primero los scripts ETL y de Entrenamiento MLOps.")
        return

    # Paneles de control y simulación
    st.sidebar.header("🎯 Parámetros Estratégicos")
    riesgo_threshold = st.sidebar.slider("Umbral de Riesgo (Probabilidad de Churn)", 0.0, 1.0, 0.5, 0.05)
    
    # KPIs Rápidos
    total_customers = len(df)
    high_risk_customers = len(df[df['Predicted_Prob'] >= riesgo_threshold])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes Evaluados (Batch)", f"{total_customers:,}")
    col2.metric("Clientes de Alto Riesgo", f"{high_risk_customers:,}")
    col3.metric("% de Cartera en Riesgo", f"{(high_risk_customers/total_customers)*100:.1f} %")

    st.divider()

    # ----------------------------------------------------
    # SECCIÓN 1: EVALUACIÓN DE IMPACTO FINANCIERO
    # ----------------------------------------------------
    st.header("1. Evaluación de Impacto Financiero")
    st.markdown("Analice el rendimiento económico de la campaña de retención sugerida por el modelo. Compara la acción de intervenir prospectos de alto riesgo (Escenario B) frente a la inacción ante la falta de sistema predictivo (Escenario A).")
    
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        costo_retencion = st.number_input("Costo de Retención por Cliente (Ej. Beneficio otorgado) [$]", value=50)
    with c_col2:
        ingreso_salvado = st.number_input("Valor Económico del Cliente (LTV/Facturación a salvar) [$]", value=300)

    df['Intervencion'] = (df['Predicted_Prob'] >= riesgo_threshold).astype(int)
    
    TP = len(df[(df['Intervencion'] == 1) & (df['True_Churn'] == 1)])
    FP = len(df[(df['Intervencion'] == 1) & (df['True_Churn'] == 0)])
    FN = len(df[(df['Intervencion'] == 0) & (df['True_Churn'] == 1)])
    
    # Cálculos comparativos (similares a la página de simulación)
    inversion_total = (TP + FP) * costo_retencion
    ingreso_recuperado = TP * ingreso_salvado
    
    ganancia_neta = ingreso_recuperado - inversion_total
    perdida_residual = FN * ingreso_salvado

    r_col1, r_col2 = st.columns(2)
    r_col1.metric("Ganancia Neta (Aporte Económico del Modelo)", f"${ganancia_neta:,.2f}")
    r_col1.caption("Cálculo: Ingresos recuperados de retenciones exitosas menos la inversión total de la campaña.")
    r_col2.metric("Fuga Monetaria Residual (Fugas No Detectadas)", f"${perdida_residual:,.2f}", delta_color="inverse")

    st.divider()

    # ----------------------------------------------------
    # SECCIÓN 2: EXPLICABILIDAD (SHAP VALUES)
    # ----------------------------------------------------
    st.header("2. Inteligencia Artificial Explicable (XAI)")
    st.markdown("Analice los factores causales que impulsan el desgaste en clientes de alto riesgo.")
    
    # Filtro de clientes afectados
    risk_df = df[df['Predicted_Prob'] >= riesgo_threshold].copy()
    
    if len(risk_df) > 0:
        st.dataframe(risk_df[['customerID', 'Predicted_Prob', 'True_Churn']].sort_values(by='Predicted_Prob', ascending=False).head(10))
        
        selected_client = st.selectbox("Seleccione un ID de Cliente para ver causas anatómicas del Riesgo:", risk_df['customerID'])
        
        if selected_client:
            client_data = risk_df[risk_df['customerID'] == selected_client].iloc[0]
            
            # Extraemos las columnas SHAP
            shap_cols = [c for c in client_data.index if str(c).endswith('_SHAP')]
            shap_values = client_data[shap_cols].copy()
            # Quitamos el sufijo para visualizar
            shap_values.index = [c.replace('_SHAP', '') for c in shap_cols]
            
            # Ordenamos por magnitud impacto absoluto
            shap_values_sorted = shap_values.sort_values()
            
            fig, ax = plt.subplots(figsize=(8, 4))
            # Coloreamos rojo si empuja a churn, verde si retiene
            colors = ['red' if val > 0 else 'green' for val in shap_values_sorted.values]
            shap_values_sorted.plot(kind='barh', color=colors, ax=ax)
            ax.set_title(f"Impacto de Variables (SHAP) para el cliente {selected_client}")
            ax.set_xlabel("Impacto en probabilidad de Churn (Log-Odds)")
            st.pyplot(fig)
            st.caption("🔴 Rojo: Factores que empujan al cliente a abandonar | 🟢 Verde: Factores que retienen al cliente")
            
    else:
        st.info("No hay clientes que superen el umbral de riesgo actual.")

if __name__ == '__main__':
    main()
