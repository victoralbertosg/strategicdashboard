  
el dashboard no puede ser “bonito”; debe ser **instrumento de decisión**. diseño que conecta exactamente con la pregunta empírica.

---

# **🔷 1\. ENFOQUE DEL DASHBOARD (clave)**

Tu dashboard debe responder en segundos:

**¿A quién intervenir, por qué y cuánto dinero gano o pierdo si actúo?**

Si no responde eso → no sirve para tu tesis.

---

# **🔷 2\. ARQUITECTURA GENERAL (4 módulos)**

### **🧩 Módulo 1: Predicción**

* Probabilidad de churn por cliente  
* Clasificación (Alto / Medio / Bajo riesgo)

---

### **🧩 Módulo 2: Explicabilidad (XAI)**

* Variables que explican el churn  
* SHAP global y local

---

### **🧩 Módulo 3: Simulación económica (TU APORTE)**

* Costos vs beneficios  
* Escenarios de decisión

---

### **🧩 Módulo 4: Decisión estratégica**

* Lista priorizada de clientes  
* Recomendaciones de acción

---

# **🔷 3\. DISEÑO DE PANTALLAS (UX funcional)**

---

## **🔹 🖥️ PANTALLA 1: VISIÓN GENERAL (Executive View)**

### **Objetivo:**

Resumen para gerente

### **Componentes:**

* 📊 KPI 1: Tasa de churn (%)  
* 📊 KPI 2: Clientes en riesgo (N)  
* 💰 KPI 3: Pérdida estimada sin intervención  
* 💰 KPI 4: Ganancia potencial con modelo  
* 📈 Gráfico:  
  * Distribución de probabilidad de churn

---

## **🔹 🖥️ PANTALLA 2: MODELO PREDICTIVO**

### **Objetivo:**

Entender el comportamiento del modelo

### **Componentes:**

* Curva ROC / AUC  
* Matriz de confusión  
* Tabla de clientes:  
  * ID  
  * Probabilidad de churn  
  * Clasificación  
* Filtro:  
  * Umbral de decisión (slider 🔥)

👉 Este slider es clave para la simulación

---

## **🔹 🖥️ PANTALLA 3: EXPLICABILIDAD (XAI)**

### **Objetivo:**

Responder: ¿Por qué el cliente se va?

### **Componentes:**

### **🔸 Global**

* Feature importance (SHAP global)

### **🔸 Individual**

* Selección de cliente  
* SHAP waterfall plot

Ejemplo:

Cliente X → se va por:

* Alto costo  
* Baja interacción  
* Mala experiencia

👉 Esto convierte el modelo en **accionable**

---

## **🔹 🖥️ PANTALLA 4: SIMULACIÓN ECONÓMICA (CORE DE TESIS)**

### **Objetivo:**

Responder:

¿Cuánto gano o pierdo según mis decisiones?

---

### **🔥 Inputs (controlados por usuario)**

* 💰 Costo de retención (ej: descuento)  
* 💰 Valor del cliente (CLV)  
* ⚠️ Costo de perder cliente  
* 🎯 Umbral de intervención

---

### **📊 Outputs**

* TP (clientes salvados)  
* FP (intervenciones innecesarias)  
* FN (clientes perdidos)

---

### **💰 KPI PRINCIPAL**

**Ganancia Neta**

Ganancia \= (TP × beneficio) − (FP × costo) − (FN × pérdida)  
---

### **📈 Gráficos clave**

* Ganancia vs umbral  
* Curva de rentabilidad  
* Comparación:  
  * Sin modelo vs Con modelo

👉 ESTE gráfico es el corazón de tu tesis

---

## **🔹 🖥️ PANTALLA 5: TOMA DE DECISIONES**

### **Objetivo:**

Responder:

¿A quién debo intervenir ahora?

---

### **📋 Tabla priorizada**

| Cliente | Riesgo | Valor | Explicación | Acción |
| ----- | ----- | ----- | ----- | ----- |
| C001 | Alto | Alto | Precio alto | Ofrecer descuento |
| C002 | Medio | Alto | Baja interacción | Contacto |
| C003 | Alto | Bajo | Bajo valor | No intervenir |

---

### **🎯 Lógica de decisión**

* Alto riesgo \+ alto valor → intervenir  
* Alto riesgo \+ bajo valor → evaluar costo  
* Bajo riesgo → no intervenir

---

# **INDICADORES CLAVE** 

debe medir:

* Precisión del modelo  
* Ganancia neta  
* ROI  
* Reducción de churn  
* Número de decisiones optimizadas

---

# **LO QUE HARÁ QUE TU DASHBOARD SEA FUERTE**

✔ Integra:

* Predicción  
* Explicación  
* Dinero

✔ Permite:

* Simular decisiones

✔ Demuestra:

* Impacto real

---

# **DIFERENCIA CLAVE (esto te dará puntos en sustentación)**

| Dashboard común | Tu dashboard |
| ----- | ----- |
| Muestra churn | Optimiza decisiones |
| Muestra datos | Simula dinero |
| Es descriptivo | Es prescriptivo |

