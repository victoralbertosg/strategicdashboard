import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
import shap

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'cleaned', 'telco_cleaned.csv')

@st.cache_resource
def get_models_and_data():
    if not os.path.exists(DATA_PATH):
        return None, None, None, None
        
    df_raw = pd.read_csv(DATA_PATH)
    df = df_raw.drop(columns=['customerID'], errors='ignore')
    
    # Preprocesamiento consistente
    obj_cols = df.select_dtypes(include=['object']).columns
    for col in obj_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
    
    X = df.drop(columns=['Churn'])
    y = df['Churn']
    
    # Split consistente (80/20) con semilla 42
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    models = {}
    
    # 1. Regresión Logística
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train, y_train)
    models['Regresión Logística'] = lr
    
    # 2. Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    models['Random Forest'] = rf
    
    # 3. XGBoost
    xgb_m = XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, use_label_encoder=False, eval_metric='logloss', random_state=42)
    xgb_m.fit(X_train, y_train)
    models['XGBoost'] = xgb_m
    
    # Recuperar IDs originales y cargos para el set de prueba
    test_indices = X_test.index
    test_df = X_test.copy()
    test_df['customerID'] = df_raw.loc[test_indices, 'customerID'].values
    test_df['Churn_Real'] = y_test.values
    # TotalCharges ya está en X_test porque estaba en X. 
    # Aseguramos que sea consistente con los datos crudos por si acaso.
    if 'TotalCharges' in df_raw.columns:
        test_df['TotalCharges'] = df_raw.loc[test_indices, 'TotalCharges'].values
    
    return models, test_df, X_train, y_train

def init_global_controls():
    """Inicializa los controles de la barra lateral y los guarda en session_state"""
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        models, _, _, _ = get_models_and_data()
        if models:
            model_options = list(models.keys())
            if 'current_model_name' not in st.session_state:
                st.session_state.current_model_name = 'XGBoost'
            
            st.session_state.current_model_name = st.selectbox(
                "Modelo Activo:",
                options=model_options,
                index=model_options.index(st.session_state.current_model_name),
                help="Cambie el modelo para ver cómo varían las predicciones y el riesgo."
            )
            
            if 'umbral' not in st.session_state:
                st.session_state.umbral = 0.5
            
            st.session_state.umbral = st.slider(
                "Umbral de Riesgo:",
                min_value=0.1,
                max_value=0.9,
                value=float(st.session_state.umbral),
                step=0.05,
                format="%.2f",
                help="Ajuste la sensibilidad. Un umbral bajo detecta más fugas."
            )
            
            st.divider()
            st.markdown(f"**Resumen:**\n- IA: `{st.session_state.current_model_name}`\n- Umbral: `{st.session_state.umbral*100:.0f}%`")

def load_data():
    """Función de compatibilidad que devuelve el dataframe con las predicciones del modelo seleccionado"""
    if 'current_model_name' not in st.session_state:
        st.session_state.current_model_name = 'XGBoost'
    if 'umbral' not in st.session_state:
        st.session_state.umbral = 0.5
        
    models, test_df, X_train, y_train = get_models_and_data()
    if models is None:
        return None
        
    model = models[st.session_state.current_model_name]
    # MUY IMPORTANTE: Solo quitar customerID y Churn_Real. 
    # TotalCharges SÍ se usó para entrenar y debe estar en la predicción.
    X_test_no_id = test_df.drop(columns=['customerID', 'Churn_Real'], errors='ignore')
    
    # Generar predicciones dinámicas
    probs = model.predict_proba(X_test_no_id)[:, 1]
    preds = (probs >= st.session_state.umbral).astype(int)
    
    # Crear dataframe final para consumo
    df_result = test_df.copy()
    df_result['Predicted_Prob'] = probs
    df_result['Predicted_Class'] = preds
    
    return df_result

@st.cache_resource
def get_current_shap_values(model_name):
    models, test_df, X_train, _ = get_models_and_data()
    model = models[model_name]
    # Sincronización de columnas con el entrenamiento
    X_test_no_id = test_df.drop(columns=['customerID', 'Churn_Real'], errors='ignore')
    
    if model_name in ['XGBoost', 'Random Forest']:
        explainer = shap.TreeExplainer(model)
        shap_vals = explainer.shap_values(X_test_no_id)
        if isinstance(shap_vals, list):
            shap_vals = shap_vals[1]
    else: # Regresión Logística
        explainer = shap.LinearExplainer(model, X_train)
        shap_vals = explainer.shap_values(X_test_no_id)

    return shap_vals, X_test_no_id.columns.tolist()

def paginate_dataframe(df, page_size=10, key="pagination"):
    """Maneja la paginación de un dataframe y devuelve (df_sliced, render_func)"""
    total_pages = (len(df) // page_size) + (1 if len(df) % page_size > 0 else 0)
    
    if total_pages <= 1:
        return df, lambda: None

    # Estado de la página
    state_key = f"{key}_page_val"
    if state_key not in st.session_state:
        st.session_state[state_key] = 1

    curr_page = st.session_state[state_key]
    start_idx = (curr_page - 1) * page_size
    end_idx = start_idx + page_size
    df_sliced = df.iloc[start_idx:end_idx]

    def render_controls():
        st.write("---")
        c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 3, 1, 1, 2])
        
        def set_page(val):
            st.session_state[state_key] = val

        with c1:
            if st.button("⏮", key=f"{key}_first"): set_page(1)
        with c2:
            if st.button("◀", key=f"{key}_prev"): set_page(max(1, st.session_state[state_key] - 1))
        
        with c3:
            new_page = st.number_input(
                f"Página (de {total_pages})",
                min_value=1,
                max_value=total_pages,
                value=st.session_state[state_key],
                key=f"{key}_input",
                label_visibility="collapsed"
            )
            if new_page != st.session_state[state_key]:
                st.session_state[state_key] = new_page

        with c4:
            if st.button("▶", key=f"{key}_next"): set_page(min(total_pages, st.session_state[state_key] + 1))
        with c5:
            if st.button("⏭", key=f"{key}_last"): set_page(total_pages)
        
        with c6:
            st.markdown(f"**Pág: {st.session_state[state_key]} / {total_pages}**")

    return df_sliced, render_controls
