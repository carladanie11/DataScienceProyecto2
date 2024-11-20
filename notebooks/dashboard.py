import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Telecomunicaciones Argentina",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("📡 Dashboard de Telecomunicaciones en Argentina")
st.markdown("---")

# Función para cargar datos
@st.cache_data
def load_data():
    penetracion_poblacion = pd.read_csv("Penetracion_poblacion_limpio.csv")
    penetracion_hogares = pd.read_csv("Penetracion_hogares_limpio.csv")
    velocidad_provincia = pd.read_csv("Velocidad_por_provincia_limpio.csv")
    accesos_tecnologia = pd.read_csv("Accesos_Por_Tecnologia_limpio.csv")
    return penetracion_poblacion, penetracion_hogares, velocidad_provincia, accesos_tecnologia

# Cargar datos
try:
    penetracion_poblacion, penetracion_hogares, velocidad_provincia, accesos_tecnologia = load_data()
    st.success("Datos cargados exitosamente")
except Exception as e:
    st.error(f"Error al cargar los datos: {str(e)}")
    st.stop()

# Sidebar con filtros generales
st.sidebar.title("Filtros")
st.sidebar.markdown("---")

# Selector de área de análisis
area_analisis = st.sidebar.selectbox(
    "Seleccionar Área de Análisis",
    ["Penetración del Servicio", "Calidad y Velocidad", "Tecnologías de Conexión"]
)

# Filtros específicos según el área seleccionada
if area_analisis == "Penetración del Servicio":
    st.header("📊 Análisis de Penetración del Servicio")
    
    # Pestañas para diferentes visualizaciones
    tab1, tab2, tab3 = st.tabs(["Por Población", "Por Hogares", "Comparativa"])
    
    with tab1:
        st.subheader("Penetración por Población")
        
        # Filtros
        provincias = st.multiselect(
            "Seleccionar Provincias",
            options=sorted(penetracion_poblacion['Provincia'].unique()),
            default=["Capital Federal", "Buenos Aires", "Córdoba"]
        )
        
        # Gráfico de barras de penetración por población
        fig_poblacion = px.bar(
            penetracion_poblacion[penetracion_poblacion['Provincia'].isin(provincias)],
            x='Provincia',
            y='Accesos por cada 100 hab',
            color='Provincia',
            title='Accesos por cada 100 habitantes por Provincia'
        )
        st.plotly_chart(fig_poblacion, use_container_width=True)
        
        # KPI
        col1, col2 = st.columns(2)
        with col1:
            promedio_nacional = penetracion_poblacion['Accesos por cada 100 hab'].mean()
            st.metric("Promedio Nacional de Accesos", f"{promedio_nacional:.2f}")
        with col2:
            max_penetracion = penetracion_poblacion['Accesos por cada 100 hab'].max()
            st.metric("Máxima Penetración", f"{max_penetracion:.2f}")
    
    with tab2:
        st.subheader("Penetración por Hogares")
        
        # Gráfico de calor por provincia
        fig_heatmap = px.density_heatmap(
            penetracion_hogares,
            x='Provincia',
            y='Accesos por cada 100 hogares',
            title='Distribución de Accesos por Hogares'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Métricas de hogares
        col1, col2 = st.columns(2)
        with col1:
            promedio_hogares = penetracion_hogares['Accesos por cada 100 hogares'].mean()
            st.metric("Promedio de Accesos por Hogar", f"{promedio_hogares:.2f}")
        with col2:
            max_hogares = penetracion_hogares['Accesos por cada 100 hogares'].max()
            st.metric("Máximo Accesos por Hogar", f"{max_hogares:.2f}")

elif area_analisis == "Calidad y Velocidad":
    st.header("🚀 Análisis de Calidad y Velocidad")
    
    # Filtros para velocidad
    provincia_velocidad = st.selectbox(
        "Seleccionar Provincia",
        options=sorted(velocidad_provincia['Provincia'].unique())
    )
    
    # Gráfico de velocidad promedio
    fig_velocidad = px.line(
        velocidad_provincia[velocidad_provincia['Provincia'] == provincia_velocidad],
        x='Año',
        y='Mbps (Media de bajada)',
        title=f'Evolución de Velocidad Media en {provincia_velocidad}'
    )
    st.plotly_chart(fig_velocidad, use_container_width=True)
    
    # Métricas de velocidad
    col1, col2, col3 = st.columns(3)
    with col1:
        velocidad_actual = velocidad_provincia[
            velocidad_provincia['Provincia'] == provincia_velocidad
        ]['Mbps (Media de bajada)'].iloc[-1]
        st.metric("Velocidad Actual", f"{velocidad_actual:.2f} Mbps")
    
    with col2:
        velocidad_promedio = velocidad_provincia[
            velocidad_provincia['Provincia'] == provincia_velocidad
        ]['Mbps (Media de bajada)'].mean()
        st.metric("Velocidad Promedio", f"{velocidad_promedio:.2f} Mbps")
    
    with col3:
        cambio_velocidad = ((velocidad_actual - velocidad_promedio) / velocidad_promedio) * 100
        st.metric("Cambio vs Promedio", f"{cambio_velocidad:.1f}%")

else:  # Tecnologías de Conexión
    st.header("🔌 Análisis de Tecnologías de Conexión")
    
    # Convertir año a string para el selectbox
    accesos_tecnologia['Año'] = accesos_tecnologia['Año'].astype(str)
    
    # Filtros
    año_seleccionado = st.selectbox(
        "Seleccionar Año",
        options=sorted(accesos_tecnologia['Año'].unique(), reverse=True)
    )
    
    trimestre_seleccionado = st.selectbox(
        "Seleccionar Trimestre",
        options=sorted(accesos_tecnologia['Trimestre'].unique())
    )
    
    # Filtrar datos
    datos_filtrados = accesos_tecnologia[
        (accesos_tecnologia['Año'] == año_seleccionado) &
        (accesos_tecnologia['Trimestre'] == trimestre_seleccionado)
    ]
    
    # Crear gráfico de distribución de tecnologías
    tecnologias = ['ADSL', 'Cablemodem', 'Fibra óptica', 'Wireless', 'Otros']
    valores = datos_filtrados[tecnologias].iloc[0]
    
    fig_tecnologias = px.pie(
        values=valores,
        names=tecnologias,
        title=f'Distribución de Tecnologías ({año_seleccionado} - T{trimestre_seleccionado})'
    )
    st.plotly_chart(fig_tecnologias, use_container_width=True)
    
    # Tabla de métricas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tecnología Dominante", 
                 tecnologias[valores.argmax()],
                 f"{(valores.max() / valores.sum() * 100):.1f}% del total")
    with col2:
        st.metric("Total de Accesos",
                 f"{valores.sum():,.0f}",
                 f"{((valores.sum() - accesos_tecnologia[tecnologias].iloc[0].sum()) / accesos_tecnologia[tecnologias].iloc[0].sum() * 100):.1f}% vs primer registro")

# Footer
st.markdown("---")
st.markdown("Dashboard creado para el análisis del sector de telecomunicaciones en Argentina")