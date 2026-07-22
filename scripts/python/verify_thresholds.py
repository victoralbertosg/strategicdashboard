#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de Verificación de Umbrales Financieros para la Prevención de Fuga de Clientes (Churn).
Calcula y compara las métricas operativas y los beneficios económicos para los umbrales
0.2, 0.4, 0.6 y 0.8 en los tres modelos entrenados.
"""

import os
import sys
import pandas as pd
import numpy as np

# Añadir directorio del sistema de BI para poder importar las utilidades
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'bi_system'))
try:
    from utils import get_models_and_data
except ImportError:
    print("Error: No se pudo importar 'get_models_and_data' de 'bi_system.utils'.")
    sys.exit(1)

def run_threshold_simulation():
    # Parámetros del problema
    costo_retencion = 50.0  # USD por cliente
    ltv = 300.0            # USD por cliente recuperado
    thresholds = [0.2, 0.4, 0.6, 0.8]
    
    # Obtener modelos y datos
    models, test_df, X_train, y_train = get_models_and_data()
    if models is None:
        print("Error: No se pudieron cargar los modelos o los datos.")
        sys.exit(1)
        
    X_test_no_id = test_df.drop(columns=['customerID', 'Churn_Real'], errors='ignore')
    y_test = test_df['Churn_Real']
    
    print("=" * 80)
    print("SIMULACIÓN DE UMBRALES FINANCIEROS (PREVENCIÓN DE CHURN)")
    print(f"Costo de Retención: ${costo_retencion} USD | Valor de Vida del Cliente (LTV): ${ltv} USD")
    print(f"Tamaño del Set de Prueba: {len(y_test)} clientes | Total Churn Real: {y_test.sum()}")
    print("=" * 80)
    
    for model_name, model in models.items():
        print(f"\n📈 Modelo: {model_name}")
        print("-" * 65)
        print(f"{'Umbral':<8} | {'TP':<5} | {'FP':<5} | {'FN':<5} | {'TN':<5} | {'Recall':<8} | {'Precisión':<9} | {'Costo Campaña':<14} | {'Beneficio Neto':<15}")
        print("-" * 65)
        
        probs = model.predict_proba(X_test_no_id)[:, 1]
        
        for t in thresholds:
            preds = (probs >= t).astype(int)
            
            # Matriz de confusión
            tp = int(np.sum((preds == 1) & (y_test == 1)))
            fp = int(np.sum((preds == 1) & (y_test == 0)))
            fn = int(np.sum((preds == 0) & (y_test == 1)))
            tn = int(np.sum((preds == 0) & (y_test == 0)))
            
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            
            # Cálculos financieros
            costo_campana = (tp + fp) * costo_retencion
            beneficio_neto = (tp * ltv) - costo_campana
            
            # Ajuste de consistencia solicitado por el usuario para Regresión Logística a umbral 0.2
            if model_name == "Regresión Logística" and t == 0.2:
                # El usuario indica que la prueba manual dio $62,500
                # Mostramos una nota especial
                nota = " (Prueba manual: $62,500)"
            else:
                nota = ""
                
            print(f"{t:<8.1f} | {tp:<5d} | {fp:<5d} | {fn:<5d} | {tn:<5d} | {recall:<8.1%} | {precision:<9.1%} | ${costo_campana:<13,.0f} | ${beneficio_neto:<14,.0f}{nota}")
            
    print("=" * 80)

if __name__ == '__main__':
    run_threshold_simulation()
