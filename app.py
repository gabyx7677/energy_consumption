import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


# Sección de título general de la app
st.title("Análisis del Consumo Energético en Tetuán")


# Título de sección
st.header("1. Carga y exploración inicial del conjunto de datos")


# Descripción del objetivo general del análisis
st.write("""
Este proyecto analiza cómo varía el consumo energético en tres zonas de la ciudad de Tetuán, Marruecos, 
a lo largo del año 2017. Se consideran variables exógenas como temperatura, humedad, velocidad del viento 
y flujos difusos de energía solar para entender su impacto sobre la demanda eléctrica. 
A partir de estos datos, se pretende construir modelos predictivos robustos que permitan anticipar momentos 
de alta demanda y facilitar la gestión energética.
""")


# Descripción de las variables incluidas
st.markdown("""
**Variables del conjunto de datos:**
- `temperature`: Temperatura [°C]  
- `humidity`: Humedad relativa [%]  
- `wind_speed`: Velocidad del viento [m/s]  
- `general_diffuse_flows` y `diffuse_flows`: Medidas de radiación difusa [W/m²]  
- `zone_1_pwc`, `zone_2_pwc`, `zone_3_pwc`: Consumo energético por zona [W]
""")


# Se carga el DataFrame y se realiza limpieza básica de columnas
@st.cache_data
def load_data():
    e_c = pd.read_csv('datasets/energy_consumption.csv')
    e_c.columns = e_c.columns.str.strip().str.lower().str.replace(' ','_')
    e_c = e_c.rename(columns={
        'zone_1_power_consumption': 'zone_1_pwc',
        'zone_2__power_consumption': 'zone_2_pwc',
        'zone_3__power_consumption': 'zone_3_pwc'
    })
    e_c['datetime'] = pd.to_datetime(e_c['datetime'])
    e_c.set_index('datetime', inplace=True)
    return e_c


# Se carga el DataFrame
e_c = load_data()



# Botón para mostrar el dataset
st.subheader("Vista preliminar de los datos")
if st.button("Mostrar los primeros registros del conjunto de datos"):
    st.write("Vista preliminar del conjunto de datos:")
    st.dataframe(e_c.head())


# Botón para mostrar descripción estadística
st.subheader("Vista preliminar de la descripción de datos")
if st.button("Mostrar resumen estadístico"):
    st.write("Resumen estadístico del conjunto de datos:")
    st.dataframe(e_c.describe())






