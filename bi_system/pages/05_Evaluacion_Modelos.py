import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report
from xgboost import XGBClassifier

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

st.set_page_config(page_title="Competición de Modelos", layout="wide")
st.title("🧩 Módulo 5: Evaluación y Selección del Cerebro Digital")
st.markdown("¿Cómo sabemos que elegimos la mejor inteligencia artificial? Aquí hemos puesto a competir a las 3 metodologías matemáticas más conocidas para saber cuál es la más exacta al aprender del pasado.")

RAW_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'cleaned', 'telco_cleaned.csv')

@st.cache_resource
def train_and_evaluate_models():
    if not os.path.exists(RAW_PATH):
        return None
        
    df = pd.read_csv(RAW_PATH)
    
    # Preparación mínima y universal
    df = df.drop(columns=['customerID'], errors='ignore')
    df = pd.get_dummies(df, drop_first=True)
    
    X = df.drop(columns=['Churn'])
    y = df['Churn']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {}
    
    # 1. Regresión Logística
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train, y_train)
    lr_probs = lr.predict_proba(X_test)[:, 1]
    lr_preds = lr.predict(X_test)
    models['Regresión Logística (Clásica)'] = {
        'auc': roc_auc_score(y_test, lr_probs),
        'y_test': y_test,
        'y_pred': lr_preds,
        'y_prob': lr_probs,
        'desc': "Método estadístico robusto que busca relaciones lineales. Es el estándar de la industria por su transparencia."
    }
    
    # 2. Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_probs = rf.predict_proba(X_test)[:, 1]
    rf_preds = rf.predict(X_test)
    models['Random Forest (Votación)'] = {
        'auc': roc_auc_score(y_test, rf_probs),
        'y_test': y_test,
        'y_pred': rf_preds,
        'y_prob': rf_probs,
        'desc': "Un bosque de árboles de decisión que votan para dar un veredicto. Muy potente para captar patrones complejos."
    }
    
    # 3. XGBoost
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    xgb.fit(X_train, y_train)
    xgb_probs = xgb.predict_proba(X_test)[:, 1]
    xgb_preds = xgb.predict(X_test)
    models['XGBoost (Avanzado)'] = {
        'auc': roc_auc_score(y_test, xgb_probs),
        'y_test': y_test,
        'y_pred': xgb_preds,
        'y_prob': xgb_probs,
        'desc': "La técnica más moderna y ganadora de competencias internacionales. Aprende de sus propios errores en cada paso."
    }
    
    return models

results = train_and_evaluate_models()

if results is None:
    st.error("Datos base no encontrados para entrenar.")
else:
    tab_titles = ["🏆 Comparativa General"] + list(results.keys())
    tabs = st.tabs(tab_titles)
    
    # --- TAB: COMPARATIVA ---
    with tabs[0]:
        st.subheader("Tabla de Puntuaciones (Desempeño AUC-ROC)")
        st.markdown("El métrico **AUC-ROC** equivale a la 'nota' del examen. Mientras más cerca a 1.0 (100%), significa que comete menos errores.")
        
        auc_data = {k: v['auc'] for k, v in results.items()}
        res_df = pd.DataFrame(list(auc_data.items()), columns=['Tipo de IA', 'Puntuación (AUC)'])
        res_df = res_df.sort_values(by='Puntuación (AUC)', ascending=False).reset_index(drop=True)
        
        st.dataframe(res_df.style.highlight_max(subset=['Puntuación (AUC)'], color='lightgreen'))
        
        fig, ax = plt.subplots(figsize=(8, 4))
        res_df.plot(kind='bar', x='Tipo de IA', y='Puntuación (AUC)', ax=ax, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        ax.set_title("Comparación de Poder de Predicción")
        ax.set_ylabel("AUC-ROC Score")
        ax.set_ylim(0, 1)
        plt.xticks(rotation=15)
        st.pyplot(fig)
        
        st.success(f"**Conclusión para Gerencia:** El ganador es **{res_df.iloc[0]['Tipo de IA']}**. Este modelo garantiza la mayor precisión operativa.")

    # --- TABS: POR MODELO ---
    for i, (name, data) in enumerate(results.items(), start=1):
        with tabs[i]:
            st.subheader(f"Análisis Detallado: {name}")
            st.info(data['desc'])
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### 📊 Matriz de Confusión")
                cm = confusion_matrix(data['y_test'], data['y_pred'])
                fig_cm, ax_cm = plt.subplots(figsize=(5, 4))
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax_cm, 
                            xticklabels=['Se Queda', 'Se Va'], 
                            yticklabels=['Se Queda', 'Se Va'])
                ax_cm.set_xlabel('Predicción del Modelo')
                ax_cm.set_ylabel('Realidad del Cliente')
                st.pyplot(fig_cm)
                
                st.markdown("""
                **¿Cómo leer esto?**
                *   **Arriba-Izquierda:** Clientes que se quedaron y acertamos (Aciertos Lealtad).
                *   **Abajo-Derecha:** Clientes que se fueron y detectamos (Aciertos Fuga).
                *   **Arriba-Derecha:** 'Falsas Alarmas' (Gastamos en alguien que no se iba).
                *   **Abajo-Izquierda:** 'Fugas Sorpresa' (Gente que se fue y no vimos venir).
                """)
                
            with col2:
                st.markdown("#### 📐 Métricas de Precisión")
                report = classification_report(data['y_test'], data['y_pred'], output_dict=True)
                report_df = pd.DataFrame(report).transpose()
                st.dataframe(report_df.loc[['0', '1', 'accuracy'], ['precision', 'recall', 'f1-score']])
                
                st.markdown(f"""
                *   **AUC-ROC:** {data['auc']:.4f} (Calidad global del ranking).
                *   **Precisión (Clase Fuga):** {report['1']['precision']:.2%}. De cada 100 alertas, cuántas son reales.
                *   **Recall (Clase Fuga):** {report['1']['recall']:.2%}. Del total de gente que se va, a cuántos logramos atrapar.
                *   **Efectividad (F1):** {report['1']['f1-score']:.4f}. Balance entre precisión y cobertura.
                """)
                
                st.warning("⚠️ **Nota Técnica:** Un Recall alto es mejor para no perder clientes, pero una Precisión alta es mejor para no desperdiciar presupuesto en incentivos.")
