import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report, roc_curve

from utils import load_data, init_global_controls, get_models_and_data

st.set_page_config(page_title="Competición de Modelos", layout="wide")
init_global_controls()

st.title("🧩 Módulo 5: Evaluación y Selección del Cerebro Digital")
st.markdown("Aquí comparamos el desempeño de diferentes inteligencias artificiales para asegurar que estamos usando la más precisa.")

models, test_df, X_train, y_train = get_models_and_data()

if models is None:
    st.error("Datos base no encontrados para entrenar.")
else:
    # Calcular métricas para todos los modelos para la comparativa
    results = {}
    # MUY IMPORTANTE: Solo quitar customerID y Churn_Real. TotalCharges SÍ es un feature.
    X_test_no_id = test_df.drop(columns=['customerID', 'Churn_Real'], errors='ignore')
    y_test = test_df['Churn_Real']
    
    for name, model in models.items():
        probs = model.predict_proba(X_test_no_id)[:, 1]
        preds = (probs >= st.session_state.umbral).astype(int)
        results[name] = {
            'auc': roc_auc_score(y_test, probs),
            'y_test': y_test,
            'y_pred': preds,
            'y_prob': probs,
            'desc': f"Modelo {name} evaluado con umbral del {st.session_state.umbral*100:.0f}%."
        }
    
    # Ordenar por AUC
    sorted_names = sorted(results.keys(), key=lambda x: results[x]['auc'], reverse=True)
    
    tab_titles = ["🏆 Comparativa General"] + sorted_names
    tabs = st.tabs(tab_titles)
    
    with tabs[0]:
        st.subheader("Cuadro de Mando de Modelos")
        best_model = sorted_names[0]
        st.markdown(f"El modelo con mejor desempeño actual es **{best_model}**.")
        
        if st.session_state.current_model_name == best_model:
            st.success(f"✅ Usted está usando el mejor modelo disponible: **{best_model}**")
        else:
            st.warning(f"⚠️ El modelo activo actual es **{st.session_state.current_model_name}**, pero **{best_model}** tiene mejores resultados históricos.")
            if st.button(f"Cambiar a {best_model} ahora"):
                st.session_state.current_model_name = best_model
                st.rerun()

        # Tabla de comparación
        auc_data = {k: v['auc'] for k, v in results.items()}
        res_df = pd.DataFrame(list(auc_data.items()), columns=['Tipo de IA', 'Puntuación (AUC)'])
        res_df = res_df.sort_values(by='Puntuación (AUC)', ascending=False).reset_index(drop=True)
        st.dataframe(res_df.style.highlight_max(subset=['Puntuación (AUC)'], color='lightgreen'))
        
        # Gráfico ROC
        fig_roc, ax_roc = plt.subplots(figsize=(8, 4))
        for name in sorted_names:
            fpr, tpr, _ = roc_curve(results[name]['y_test'], results[name]['y_prob'])
            ax_roc.plot(fpr, tpr, label=f"{name} (AUC: {results[name]['auc']:.3f})")
        
        ax_roc.plot([0, 1], [0, 1], 'k--', alpha=0.5)
        ax_roc.set_title("Curva de Calidad: ¿Qué modelo separa mejor a los clientes?")
        ax_roc.legend()
        st.pyplot(fig_roc)

        # LEYENDA AUC
        with st.expander("📚 ¿Qué significa la Puntuación AUC? (Explicación para no técnicos)"):
            st.markdown("""
            **Imagine que el AUC es la 'nota de examen' de la IA (de 0 a 1.0):**
            
            *   **1.0 (100%):** Perfección absoluta. La IA nunca se equivoca. (Casi imposible en la vida real).
            *   **0.80 - 0.90:** **Excelente.** La IA tiene un olfato muy fino para detectar quién se va.
            *   **0.70 - 0.80:** **Bueno.** Útil para tomar decisiones masivas.
            *   **0.50:** **Azar.** Es lo mismo que lanzar una moneda al aire.
            
            *Si un modelo tiene 0.84, significa que en el 84% de las veces, si le ponemos a un cliente fiel y a uno que se va enfrente, sabrá identificar correctamente quién es quién.*
            """)

    # Análisis por modelo
    for i, name in enumerate(sorted_names, start=1):
        data = results[name]
        with tabs[i]:
            st.subheader(f"Detalle: {name}")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Matriz de Confusión")
                cm = confusion_matrix(data['y_test'], data['y_pred'])
                fig_cm, ax_cm = plt.subplots(figsize=(5, 4))
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax_cm, 
                            xticklabels=['Leal', 'Fuga'], 
                            yticklabels=['Leal', 'Fuga'])
                ax_cm.set_xlabel('Predicción del Modelo')
                ax_cm.set_ylabel('Realidad')
                st.pyplot(fig_cm)
                
            with col2:
                st.markdown("#### Métricas Operativas")
                report = classification_report(data['y_test'], data['y_pred'], output_dict=True)
                acc = report['accuracy']
                prec = report['1']['precision']
                rec = report['1']['recall']
                
                st.metric("Precisión (No dar falsas alarmas)", f"{prec:.1%}")
                st.metric("Cobertura (No dejar que nadie se escape)", f"{rec:.1%}")
                
                st.info(f"""
                **Análisis:** 
                Con el umbral actual del **{st.session_state.umbral*100:.0f}%**, este modelo detecta al **{rec:.1%}** de los clientes que realmente se van. El resto (**{1-rec:.1%}**) son 'fugas sorpresa' que el modelo no detectó.
                """)
