import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np



st.set_page_config(page_title="Análisis Energético Tetuán", layout="wide")


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
    e_c['total_pwc'] = e_c['zone_1_pwc'] + e_c['zone_2_pwc'] + e_c['zone_3_pwc']  # Se crea una nueva columna con la suma de la demanda por zona
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


# Sección de análisis temporal del consumo energético
st.header("2. Análisis Temporal del Consumo Energético")


# --- Gráfico: Consumo Diario Promedio por Zona ---
st.subheader("Consumo Diario Promedio por Zona")

st.write("""
Este gráfico muestra la evolución diaria del consumo energético promedio para cada una de las tres zonas analizadas. 
Al observar los patrones diarios se pueden detectar tendencias, estacionalidades o anomalías que ocurren a lo largo del año.
""")

if st.button("Mostrar gráfico de consumo diario promedio"):
    daily_avg = e_c.resample('D').mean()[['zone_1_pwc', 'zone_2_pwc', 'zone_3_pwc']]
    fig_daily = px.line(
        daily_avg,
        labels={'value': 'Consumo [W]', 'datetime': 'Fecha', 'variable': 'Zona'},
        title="Consumo Diario Promedio por Zona"
    )
    st.plotly_chart(fig_daily, use_container_width=True)


# --- Gráfico: Consumo Mensual Promedio por Zona ---
st.subheader("Consumo Mensual Promedio por Zona")

st.write("""
Este gráfico presenta el promedio mensual de consumo eléctrico por zona. Su objetivo es ayudar a identificar 
periodos del año con mayor o menor demanda, facilitando la planificación energética estacional.
""")

if st.button("Mostrar gráfico de consumo mensual promedio"):
    monthly_avg = e_c.resample('M').mean()[['zone_1_pwc', 'zone_2_pwc', 'zone_3_pwc']]
    fig_monthly = px.line(
        monthly_avg,
        labels={'value': 'Consumo [W]', 'datetime': 'Mes', 'variable': 'Zona'},
        title="Consumo Mensual Promedio por Zona"
    )
    st.plotly_chart(fig_monthly, use_container_width=True)


# --- Gráfico: Desviación Estándar Diaria del Consumo ---
st.subheader("Variabilidad Diaria del Consumo por Zona")

st.write("""
A través de este gráfico se muestra la desviación estándar diaria del consumo energético por zona. 
Este indicador permite evaluar qué tan estable o variable ha sido el consumo día a día, detectando posibles fluctuaciones.
""")

if st.button("Mostrar gráfico de variabilidad diaria del consumo"):
    daily_std = e_c.resample('D').std()[['zone_1_pwc', 'zone_2_pwc', 'zone_3_pwc']]
    fig_std = px.line(
        daily_std,
        labels={'value': 'Desviación Estándar [W]', 'datetime': 'Fecha', 'variable': 'Zona'},
        title="Desviación Estándar Diaria del Consumo por Zona"
    )
    st.plotly_chart(fig_std, use_container_width=True)


# --- Gráfico: curva de demanda diaria del Consumo ---
st.subheader("Curva de demanda diaria del consumo de Zona") # REVISAAAR

st.write("""
A través de este gráfico se muestra la desviación estándar diaria del consumo energético por zona. 
Este indicador permite evaluar qué tan estable o variable ha sido el consumo día a día, detectando posibles fluctuaciones.
""")

if st.button("Mostrar gráfico de la curva de demanda diaria del consumo"):
    
    # Se resamplea con base a la hora y se saca el promedio de consumo por hora
    e_c_hourly = e_c['total_pwc'].resample('h').mean()
    e_c_hourly = e_c_hourly.to_frame() # Se convierte a dataframe
    e_c_hourly['hour'] = e_c_hourly.index.hour # Se reindexa 
    curve = e_c_hourly.groupby('hour')['total_pwc'].mean()
    fig_demand_curve = px.line(
        curve,
        labels={'value': 'Desviación Estándar [W]', 'datetime': 'Fecha', 'variable': 'Zona'},
        title="Desviación Estándar Diaria del Consumo por Zona"
    )
    st.plotly_chart(fig_demand_curve, use_container_width=True)


# --- Gráfico: curva de demanda diaria día laboral - fin de semana ---
st.subheader("Curva de demanda diaria del consumo de Zona") # REVISAAAR

st.write("""
A través de este gráfico se muestra la desviación estándar diaria del consumo energético por zona. 
Este indicador permite evaluar qué tan estable o variable ha sido el consumo día a día, detectando posibles fluctuaciones.
""")

if st.button("Mostrar gráfico de la curva de demanda diaria del consumo"):

    
    e_c['weekday'] = e_c.index.weekday # Se crea columna con el día de la semana (0 = lunes, 6 = domingo)
    e_c['tipo_dia'] = e_c['weekday'].apply(lambda x: 'Fin de Semana' if x >= 5 else 'Laboral') # Se define si es fin de semana (sábado o domingo)
    e_c['total_pwc'] = e_c['zone_1_pwc'] + e_c['zone_2_pwc'] + e_c['zone_3_pwc'] # Se asegura tener la suma total de energía por fila
    e_c_hourly['tipo_dia'] = e_c['tipo_dia'].resample('h').first() # Se resamplea por hora para suavizar y se conserva tipo de día
    e_c_hourly['hour'] = e_c_hourly.index.hour
    week_or_weekend_day = e_c_hourly.groupby(['tipo_dia', 'hour'])['total_pwc'].mean().unstack(0) # Se agrupan los promedios por hora y tipo de día
    fig_type_date_demand = px.line(
        week_or_weekend_day,
        labels={'value': 'Desviación Estándar [W]', 'datetime': 'Fecha', 'variable': 'Zona'},
        title="Desviación Estándar Diaria del Consumo por Zona"
    )
    st.plotly_chart(fig_type_date_demand, use_container_width=True)