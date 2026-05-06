import os
import pandas as pd
import numpy as np

RAW_DIR = 'data/raw'
CLEANED_DIR = 'data/cleaned'
DATA_URL = 'https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv'

def setup_directories():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(CLEANED_DIR, exist_ok=True)

def fetch_data():
    raw_path = os.path.join(RAW_DIR, 'Telco_Customer_Churn.csv')
    if not os.path.exists(raw_path):
        print("Descargando dataset de IBM Telco Churn...")
        df = pd.read_csv(DATA_URL)
        df.to_csv(raw_path, index=False)
        print(f"Dataset guardado en {raw_path}")
    else:
        print("Dataset ya se encuentra descargado en data/raw/")
        df = pd.read_csv(raw_path)
    return df

def clean_data(df):
    print("Iniciando proceso de limpieza...")
    
    # 1. 'TotalCharges' a numérico (hay espacios en blanco para nuevos clientes)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].replace(' ', np.nan))
    
    # Rellenar nulos con 0 para los clientes que no han tenido cargos aún
    df['TotalCharges'] = df['TotalCharges'].fillna(0)
    
    # 2. Codificar 'Churn' a variable binaria
    if 'Churn' in df.columns:
        df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
        
    # 3. Eliminar ID (se puede mantener para cruzar en BI, así que lo guardamos en el index o como columna aparte)
    # Lo mantenemos porque para el Dashboard en Streamlit la granularidad por clienteID es útil
    
    cleaned_path = os.path.join(CLEANED_DIR, 'telco_cleaned.csv')
    df.to_csv(cleaned_path, index=False)
    print(f"Dataset procesado y guardado en {cleaned_path}")
    
    print("\nResumen de Transformaciones:")
    print(df.info())
    print("\nDistribución de Churn:")
    print(df['Churn'].value_counts(normalize=True).round(3))
    
    return df

if __name__ == '__main__':
    setup_directories()
    df_raw = fetch_data()
    df_clean = clean_data(df_raw)
    print("ETL completado. Listo para la Fase 3 de Entrenamiento de Modelo y BI.")
