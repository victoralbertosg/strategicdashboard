import os
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score, f1_score
import shap

CLEANED_DIR = 'data/cleaned'
MODEL_DIR = 'scripts/python/models'

def train_and_evaluate():
    os.makedirs(MODEL_DIR, exist_ok=True)
    data_path = os.path.join(CLEANED_DIR, 'telco_cleaned.csv')
    
    if not os.path.exists(data_path):
        raise FileNotFoundError("Dataset limpio no encontrado. Corra data_prep.py primero.")
        
    df = pd.read_csv(data_path)
    
    # Conservamos el ID para el output final, pero lo quitamos de características
    df_features = df.drop(columns=['customerID'])
    
    # Codificar variables categóricas
    # Para XGBoost, las variables tipo Category o numéricas funcionarán mejor.
    # Convertiremos Object a categórico
    obj_cols = df_features.select_dtypes(include=['object']).columns
    
    encoder_dict = {}
    for col in obj_cols:
        le = LabelEncoder()
        df_features[col] = le.fit_transform(df_features[col].astype(str))
        encoder_dict[col] = le
        
    # Guardar los encoders si los necesitamos en prod
    with open(os.path.join(MODEL_DIR, 'label_encoders.pkl'), 'wb') as f:
        pickle.dump(encoder_dict, f)
        
    X = df_features.drop(columns=['Churn'])
    y = df_features['Churn']
    
    # Train/Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Entrenando modelo XGBoost...")
    model = xgb.XGBClassifier(
        n_estimators=100, 
        max_depth=5, 
        learning_rate=0.1, 
        use_label_encoder=False, 
        eval_metric='logloss',
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    print("Modelo entrenado. Calculando métricas en Conjunto de Prueba:")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    auc = roc_auc_score(y_test, y_prob)
    f1 = f1_score(y_test, y_pred)
    
    print(classification_report(y_test, y_pred))
    print(f"ROC-AUC: {auc:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    # Generar salidas de Predicciones y SHAP (XAI) acopladas al ID original 
    # para ser consumidas estáticamente por el Dashboard de BI (Streamlit)
    print("Calculando SHAP Values para Inteligencia Artificial Explicable...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    # Creamos un dataframe que una ID, valores reales, probabildiades y SHAP
    test_indices = X_test.index
    df_results = df.loc[test_indices, ['customerID', 'Churn']].copy()
    df_results.rename(columns={'Churn': 'True_Churn'}, inplace=True)
    df_results['Predicted_Prob'] = y_prob
    df_results['Predicted_Class'] = y_pred
    
    # Añadimos los features originales y sus valores SHAP
    # Guardamos los shap como sufijo _SHAP
    shap_df = pd.DataFrame(shap_values, columns=[str(c) + '_SHAP' for c in X.columns], index=test_indices)
    
    # Cruce definitivo final (Dataset enriquecido para BI)
    final_bi_df = pd.concat([df_results, X_test, shap_df], axis=1)
    
    bi_output_path = os.path.join(CLEANED_DIR, 'bi_ready_predictions.csv')
    final_bi_df.to_csv(bi_output_path, index=False)
    print(f"\nDatos Listos para Inteligencia de Negocios exportados en: {bi_output_path}")

    # Guardar modelo
    model_path = os.path.join(MODEL_DIR, 'xgb_churn_model.json')
    model.save_model(model_path)
    print(f"Modelo guardado en {model_path}")

if __name__ == '__main__':
    train_and_evaluate()
