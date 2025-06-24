# Energy Consumption Analysis

Este proyecto analiza el consumo eléctrico en función de distintas variables ambientales, como temperatura, humedad y condiciones climáticas. El objetivo es identificar patrones, correlaciones y factores que influyen en la demanda energética mediante visualizaciones interactivas y análisis exploratorios.

## Estructura

- `app.py`: aplicación principal en Streamlit.
- `datasets/power_consumption.csv`: conjunto de datos usado para el análisis.
- `notebooks/EDA.ipynb`: exploración y visualización inicial de los datos.
- `requirements.txt`: lista de dependencias.
- `render.yaml`: configuración de despliegue en Render.

# 📊 Análisis Temporal del Consumo Energético

Este proyecto explora el comportamiento del consumo energético en tres zonas a lo largo de un año, utilizando herramientas de análisis de datos, visualización y despliegue web con **Python y Streamlit**.

## 🚀 Objetivo

Identificar patrones diarios, mensuales y horarios en el consumo eléctrico para:
- Detectar anomalías o eventos críticos.
- Entender la estacionalidad del consumo.
- Evaluar la estabilidad de la demanda.
- Proponer estrategias de optimización energética.

## 🛠️ Herramientas utilizadas

- **Python** (Pandas, Numpy, Plotly, Seaborn, Scikit-learn)
- **Streamlit** para visualización interactiva
- **Git y GitHub** para control de versiones
- **Render** como plataforma de despliegue

## 📈 Visualizaciones clave

- **Consumo Diario Promedio por Zona**
- **Consumo Mensual Promedio por Zona**
- **Variabilidad Diaria del Consumo**
- **Curva de Demanda Diaria (por hora)**

Todas las gráficas se generan automáticamente desde el backend de datos preprocesados. El usuario puede activar las visualizaciones mediante botones en la interfaz de Streamlit.

## 🧠 Conclusiones principales

- La **Zona 1** es la de mayor y más estable demanda.
- La **Zona 3** presenta anomalías críticas que deben ser monitoreadas.
- El **consumo energético presenta estacionalidad clara**, con picos en horas de la noche.
- La curva diaria sugiere oportunidades para políticas de eficiencia o tarifas dinámicas.

## 🌐 Despliegue

Puedes ver la app en línea en Render:  
📍 https://energy-consumption-vce7.onrender.com