import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import load_data
from sklearn.metrics import confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt

st.set_page_config(page_title="Predicciones", layout="wide")

st.title("🧩 Módulo 1: Aciertos del Sistema Predictivo")
st.markdown("Esta sección demuestra **qué tan preciso es nuestro 'adivino' digital**. Comparamos lo que el sistema alertó vs lo que sabemos que realmente ocurrirá.")

df = load_data()
if df is None:
    st.error("Faltan datos.")
    st.stop()

st.sidebar.markdown("### 🎚️ Nivel de Sensibilidad")
st.sidebar.markdown('Puede hacer que el sistema sea más "paranoico" o más "relajado".')
threshold = st.sidebar.slider("¿Desde qué porcentaje de riesgo debemos alertar?", 0.0, 1.0, 0.5, 0.01)

df['Intervencion'] = (df['Predicted_Prob'] >= threshold).astype(int)

st.subheader("📊 Fiabilidad de las Alertas")
st.markdown("Estos gráficos nos indican si estamos listos para confiar nuestro dinero al sistema.")
col1, col2 = st.columns(2)

fpr, tpr, _ = roc_curve(df['True_Churn'], df['Predicted_Prob'])
roc_auc = auc(fpr, tpr)

fig, ax = plt.subplots(figsize=(5,4))
ax.plot(fpr, tpr, color='darkorange', lw=2, label=f'Nota del sistema: {roc_auc:.2f} / 1.0')
ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Adivinanza al azar')
ax.set_xlabel('Falsas Alarmas (Errores)')
ax.set_ylabel('Alertas Correctas (Aciertos)')
ax.set_title('Capacidad Total de Acierto')
ax.legend(loc="lower right")
col1.pyplot(fig)
col1.caption("Curva de Rendimiento: Cuanto más hacia la esquina superior izquierda esté la línea naranja, mejor predice el sistema. Un 0.5 es tirar una moneda; 1.0 es perfección.")

cm = confusion_matrix(df['True_Churn'], df['Intervencion'])
fig2, ax2 = plt.subplots(figsize=(5,4))
ax2.matshow(cm, cmap='Blues', alpha=0.3)
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax2.text(x=j, y=i,s=cm[i, j], va='center', ha='center', size='xx-large')
ax2.set_xlabel('Lo que el SISTEMA DIJO')
ax2.set_ylabel('Lo que REALMENTE PASÓ')
ax2.set_title('Resumen de Éxitos y Fracasos')
# Set ticks to human readable
ax2.set_xticks([0,1])
ax2.set_yticks([0,1])
ax2.set_xticklabels(['Se queda', 'Se va'])
ax2.set_yticklabels(['Se queda', 'Se va'])
col2.pyplot(fig2)
col2.caption("Matriz de Confusión: La diagonal principal (arriba a la izq y abajo a la der) son nuestros **aciertos absolutos**.")

st.divider()

st.subheader("📋 Lista Clasificada de Clientes")
st.markdown("Observe individualmente qué grupo de riesgo se ha asignado a cada uno.")
df['Nivel de Alerta'] = pd.cut(df['Predicted_Prob'], bins=[0, 0.3, 0.7, 1.0], labels=['Tranquilo', 'Cuidado', 'Peligro Inminente'])
st.dataframe(df[['customerID', 'Predicted_Prob', 'Nivel de Alerta']].sort_values(by='Predicted_Prob', ascending=False).head(50))
