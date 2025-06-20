import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Se carga el dataset
power_consuption = pd.read_csv('datasets/power_consumption.csv')

# Se muestra el título de la app
st.title('Consumo eléctrico')

# Se muestra el DataFrame en la aplicación
st.dataframe(power_consuption)

st.text('se supone que asi sirve no?')


st.set_page_config(page_title="App Eléctricidad", layout="wide")

st.title("Análisis de consumo electrico")
st.write("Bienvenido a la aplicación de Streamlit desplegada con Render.")


