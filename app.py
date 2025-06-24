import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go



st.set_page_config(page_title="Análisis Energético", layout="wide")


# Sección de título general de la app
st.title("Análisis del Consumo Energético en la ciudad de San Aurelio en Colombia")


# Título de sección
st.header("1. Carga y exploración inicial del conjunto de datos")


# Descripción del objetivo general del análisis
st.write("""
Este proyecto analiza cómo varía el consumo energético en tres zonas de la ciudad de San Aurelio, en el departamento
de Arauca en Colombia a lo largo del año 2017. Se consideran variables exógenas como temperatura, humedad, velocidad del viento 
y flujos difusos de energía solar para entender su impacto sobre la demanda eléctrica. 
A partir de estos datos,por ahora se pretende hacer un análisis exploratorio de los datos para más a futuro construir modelos predictivos
robustos que permitan anticipar momentos de alta demanda y facilitar la gestión energética al estudiar las variables que afectan el consumo energético.
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
st.subheader("Curva de demanda diaria del consumo") 

st.write("""
La curva de demanda energética diaria revela patrones de comportamiento asociados al uso de la electricidad 
en diferentes zonas. Esta representación es clave para anticipar picos de consumo, optimizar la distribución 
de energía y diseñar estrategias de gestión basadas en la demanda real observada a lo largo del tiempo.
""")

if st.button("Mostrar gráfico de la curva de demanda"):
    
    # Se resamplea con base a la hora y se saca el promedio de consumo por hora
    e_c_hourly = e_c['total_pwc'].resample('h').mean().to_frame() # A df porque es una serie
    e_c_hourly['hour'] = e_c_hourly.index.hour # Se reindexa 
    curve = e_c_hourly.groupby('hour')['total_pwc'].mean()
    fig_demand_curve = px.line(
        curve,
        labels={'value': 'Desviación Estándar [W]', 'datetime': 'Fecha', 'variable': 'Zona'},
        title="Desviación Estándar Diaria del Consumo por Zona"
    )
    st.plotly_chart(fig_demand_curve, use_container_width=True)


# --- Gráfico: curva de demanda diaria día laboral - fin de semana ---
st.subheader("Curva de demanda diaria días laborales - fines de semana")

st.write("""
Al segmentar el consumo energético entre días laborales y fines de semana, se evidencian patrones distintos 
de demanda. Mientras que los días hábiles presentan una curva más estructurada con picos previsibles, 
los fines de semana muestran una reducción general en el consumo, reflejando cambios en los hábitos 
de actividad de la población. Esta diferenciación es clave para construir modelos predictivos más precisos 
y para una planificación energética que se adapte a las dinámicas sociales reales.
""")

if st.button("Mostrar gráfico de la curva de demanda weekday - weekend day"):

    
    e_c['weekday'] = e_c.index.weekday # Se crea columna con el día de la semana (0 = lunes, 6 = domingo)
    e_c['tipo_dia'] = e_c['weekday'].apply(lambda x: 'Fin de Semana' if x >= 5 else 'Laboral') # Se define si es fin de semana (sábado o domingo)
    e_c_hourly = e_c['total_pwc'].resample('h').mean().to_frame() # Se crea df basandose en el resampleo horario del consumo total (de serie a df)
    e_c_hourly['tipo_dia'] = e_c['tipo_dia'].resample('h').first() # Se resamplea por hora para suavizar y se conserva tipo de día
    e_c_hourly['hour'] = e_c_hourly.index.hour
    week_or_weekend_day = e_c_hourly.groupby(['tipo_dia', 'hour'])['total_pwc'].mean().unstack(0) # Se agrupan los promedios por hora y tipo de día
    fig_type_date_demand = px.line(
        week_or_weekend_day,
        labels={'value': 'Desviación Estándar [W]', 'datetime': 'Fecha', 'variable': 'Zona'},
        title="Desviación Estándar Diaria del Consumo por Zona"
    )
    st.plotly_chart(fig_type_date_demand, use_container_width=True)


# Título y descripción para los histogramas
st.header("3. Distribución del Consumo por Zona")

st.write("""
En esta sección se analiza la distribución de consumo energético para cada zona mediante histogramas interactivos. 
Los histogramas permiten visualizar la frecuencia de los distintos niveles de consumo, y ayudan a identificar patrones, 
asimetrías o posibles sesgos en los datos de cada zona.
""")

st.write("""
Marca la casilla si deseas visualizar los histogramas del consumo energético por zona. 
Esta vista facilita identificar la forma de la distribución y posibles diferencias entre las tres áreas analizadas.
""")

# Casilla de verificación
if st.checkbox("Mostrar histogramas de consumo por zona"):
    # Crear figura con subplots
    fig = make_subplots(rows=1, cols=3, subplot_titles=["Zona 1", "Zona 2", "Zona 3"])
    zonas = ['zone_1_pwc', 'zone_2_pwc', 'zone_3_pwc']

    for i, zona in enumerate(zonas, start=1):
        fig.add_trace(
            go.Histogram(
                x=e_c[zona],
                nbinsx=30,
                name=zona.upper(),
                marker_color='skyblue',
                opacity=0.75
            ),
            row=1, col=i
        )

    # Layout general
    fig.update_layout(
        title_text="Distribución del Consumo Energético por Zona",
        showlegend=False,
        height=400,
        bargap=0.05,
    )

    st.plotly_chart(fig, use_container_width=True)

# Conclusipon
st.header("Conclusión del Análisis")

st.write("""
El análisis exploratorio del consumo energético en la ciudad de San Aurelio revela patrones claros de demanda diaria, mensual 
y semanal, destacando una disminución consistente los fines de semana y una mayor variabilidad en ciertos períodos del año. 
La segmentación por zonas permite observar comportamientos específicos, lo que es esencial para la toma de decisiones focalizadas 
en eficiencia energética. Además, la estabilidad en algunos tramos y la alta variabilidad en otros indican la necesidad de 
modelos predictivos capaces de adaptarse a estas dinámicas. Estos hallazgos sientan las bases para construir soluciones de 
predicción robustas que optimicen la gestión del sistema eléctrico local, anticipando picos de consumo y mejorando la sostenibilidad energética.
""")

# Se muestra la conclusión general del análisis temporal del consumo energético
st.markdown("""
## **Conclusiones del Análisis Temporal del Consumo Energético**

### 1. **Consumo Diario Promedio por Zona**
- La **Zona 1** mantiene el nivel de consumo diario más alto, con una tendencia creciente hasta mediados de año y estabilización posterior.
- La **Zona 2** presenta un comportamiento estable con ligeros incrementos a mitad de año.
- La **Zona 3** evidencia un comportamiento atípico, con un aumento marcado entre junio y agosto, seguido de una caída abrupta. Esto podría indicar una anomalía operativa o cambio estructural en dicha zona.

### 2. **Consumo Mensual Promedio por Zona**
- Las tres zonas muestran crecimiento hasta agosto. La **Zona 3** desciende bruscamente luego, mientras las otras dos zonas mantienen una disminución moderada.
- Este patrón sugiere estacionalidad o un evento específico que alteró significativamente el consumo.

### 3. **Variabilidad Diaria del Consumo por Zona**
- La **Zona 1** presenta alta variabilidad pero controlada, reflejando una demanda robusta y predecible.
- La **Zona 2** mantiene variabilidad intermedia con picos aislados.
- La **Zona 3** muestra alta volatilidad durante su periodo de mayor consumo, lo que refuerza la hipótesis de un cambio relevante en su uso energético.

### 4. **Curva de Demanda Diaria (por hora)**
- El consumo sigue un patrón típico diario:
    - Mínimos entre las 2:00 y 6:00 AM.
    - Incremento sostenido desde las 7:00 AM.
    - **Pico máximo entre las 7:00 PM y 9:00 PM**, coincidiendo con el periodo de mayor actividad residencial.
- Este perfil permite identificar horas pico y diseñar estrategias de respuesta a la demanda.

---

###  **Recomendaciones Estratégicas**
- **Monitorear la Zona 3** por posibles eventos estructurales que afectan su perfil energético.
- Priorizar la **Zona 1** en decisiones de inversión y mantenimiento, dada su alta y estable demanda.
- Usar la curva horaria para diseñar **tarifas dinámicas** y estrategias de eficiencia energética.
- Considerar la **estacionalidad energética** para anticipar incrementos de demanda y planificar recursos.

""")