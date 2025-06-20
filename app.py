import streamlit as st
import pandas as pd
import plotly_express
import numpy as np

# Se carga el dataset
vehicles_us = pd.read_csv('datasets/power_consuption.csv')

# Se muestra el título de la app
st.title('Análisis de Vehículos en EE.UU.')

# Se muestra el DataFrame en la aplicación
st.dataframe(vehicles_us)

st.text('se supone que asi sirve no?')


st.set_page_config(page_title="App Vehículos", layout="wide")

st.title("Análisis de Vehículos")
st.write("Bienvenido a la aplicación de Streamlit desplegada con Render.")