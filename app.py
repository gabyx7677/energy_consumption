import streamlit as st
import pandas as pd

# Se carga el dataset
vehicles_us = pd.read_csv('vehicles_us.csv')

# Se muestra el título de la app
st.title('Análisis de Vehículos en EE.UU.')

# Se muestra el DataFrame en la aplicación
st.dataframe(vehicles_us)

st.text('se supone que asi sirve no?')