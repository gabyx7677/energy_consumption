# Energy Consumption Analysis

Este proyecto analiza el consumo eléctrico en función de distintas variables ambientales, como temperatura, humedad y condiciones climáticas. El objetivo es identificar patrones, correlaciones y factores que influyen en la demanda energética mediante visualizaciones interactivas y análisis exploratorios.

## Estructura

- `app.py`: aplicación principal en Streamlit.
- `datasets/power_consumption.csv`: conjunto de datos usado para el análisis.
- `notebooks/EDA.ipynb`: exploración y visualización inicial de los datos.
- `requirements.txt`: lista de dependencias.
- `render.yaml`: configuración de despliegue en Render.

## Cómo usar

```bash
git clone https://github.com/gabyx7677/energy_consumption.git
cd energy_consumption
python -m venv energy_consumption_env
source energy_consumption_env/Scripts/activate
pip install -r requirements.txt
streamlit run app.py