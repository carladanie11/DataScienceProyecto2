import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Título y descripción general
st.title("📡 Análisis del Sector de Telecomunicaciones en Argentina")
st.sidebar.title("Navegación")

# Opciones de navegación en la barra lateral
seccion = st.sidebar.radio(
    "Selecciona una sección:",
    ("Inicio", "Penetración del Servicio", "Calidad y Velocidad del Servicio", "Tecnologías de Conexión", "KPI's")
)

# Sección: Inicio
if seccion == "Inicio":
    st.write("""
    Este proyecto realiza un análisis exhaustivo del sector de telecomunicaciones en Argentina, utilizando datos del ENACOM.  
    El análisis se divide en tres áreas clave:
    
    1. **Penetración del Servicio**  
       Objetivo: Evaluar qué tan extendido está el servicio de internet en la población y en los hogares.
    
    2. **Calidad y Velocidad del Servicio**  
       Objetivo: Identificar las velocidades promedio y su distribución entre provincias.
    
    3. **Tecnologías de Conexión**  
       Objetivo: Analizar las tecnologías dominantes y su evolución.
       
    4. **KPI's**  
       Objetivo: Presentacion de KPI's.
    """)
    
    
# Sección: Penetración del Servicio
elif seccion == "Penetración del Servicio":
    st.header("1.1 Penetración del Servicio")

    st.write("""
    Esta sección analiza qué tan extendido está el servicio de internet en la población y en los hogares de Argentina. 
    Se utilizan los siguientes datasets:
    - **Penetración-población**
    - **Penetración-hogares**
    - **Penetración-totales**
    """)

    # Carga de datos
    @st.cache_data
    def cargar_datos():
        poblacion = pd.read_csv("Penetracion_poblacion_limpio.csv")
        hogares = pd.read_csv("Penetracion_hogares_limpio.csv")
        totales = pd.read_csv("Penetracion_totales_limpio.csv")
        return poblacion, hogares, totales

    penetracion_poblacion, penetracion_hogares, penetracion_totales = cargar_datos()

    # Gráfico: Penetración de Internet en la Población por Provincia
    st.subheader("Gráfico: Penetración de Internet en la Población por Provincia")
    st.write("""
    Este gráfico muestra la penetración de Internet en la población, expresada como **accesos por cada 100 habitantes**, para cada provincia de Argentina. 
    Permite visualizar cómo varía la conectividad entre las diferentes provincias, destacando tanto a las más conectadas como a aquellas con menor cobertura.
    """)

    # Filtrar y ordenar datos
    penetracion_poblacion_sorted = penetracion_poblacion.sort_values(
        by="Accesos por cada 100 hab", ascending=False
    )

    # Crear gráfico interactivo con Plotly
    fig_poblacion = px.bar(
        penetracion_poblacion_sorted,
        x="Provincia",
        y="Accesos por cada 100 hab",
        color="Provincia",  # Colorea las barras por provincia
        title="Accesos por cada 100 habitantes en las provincias",
        labels={"Accesos por cada 100 hab": "Accesos por cada 100 habitantes"},
        template="plotly",  # Estilo visual
    )

    # Mejorar diseño
    fig_poblacion.update_layout(
        xaxis_title="Provincia",
        yaxis_title="Accesos por cada 100 habitantes",
        xaxis_tickangle=90,  # Rotación de etiquetas del eje X
        title_font_size=16
    )

    # Mostrar el gráfico en el dashboard
    st.plotly_chart(fig_poblacion)

    # Gráfico: Penetración de Internet en los Hogares por Región
    st.subheader("Gráfico: Penetración de Internet en los Hogares por Región")
    st.write("""
    Este gráfico muestra la penetración de Internet en los hogares, expresada como **accesos por cada 100 hogares**, para cada provincia de Argentina. 
    Permite comparar el nivel de conectividad entre las regiones, destacando diferencias significativas.
    """)

    # Filtrar y ordenar datos
    penetracion_hogares_sorted = penetracion_hogares.sort_values(
        by="Accesos por cada 100 hogares", ascending=False
    )

    # Crear gráfico interactivo con Plotly
    fig_hogares = px.bar(
        penetracion_hogares_sorted,
        x="Provincia",
        y="Accesos por cada 100 hogares",
        color="Provincia",  # Colorea las barras por provincia
        title="Accesos por cada 100 hogares en las provincias",
        labels={"Accesos por cada 100 hogares": "Accesos por cada 100 hogares"},
        template="plotly",  # Estilo visual
    )

    # Mejorar diseño
    fig_hogares.update_layout(
        xaxis_title="Provincia",
        yaxis_title="Accesos por cada 100 hogares",
        xaxis_tickangle=90,  # Rotación de etiquetas del eje X
        title_font_size=16
    )

    # Mostrar el gráfico en el dashboard
    st.plotly_chart(fig_hogares)

    # Gráfico: Tendencias de Penetración Total a lo Largo del Tiempo
    st.subheader("Gráfico: Tendencias de Penetración Total a lo Largo del Tiempo")
    st.write("""
    Este gráfico muestra la evolución de la penetración de Internet en hogares y población a lo largo del tiempo. 
    Permite identificar patrones, crecimiento sostenido y variaciones anuales.
    """)

    # Crear gráfico interactivo de líneas con Plotly
    fig_tendencias = px.line(
        penetracion_totales,
        x="Periodo",
        y=["Accesos por cada 100 hogares", "Accesos por cada 100 hab"],
        markers=True,
        labels={"value": "Accesos por cada 100", "variable": "Indicador"},
        title="Tendencias de Accesos por cada 100 hogares y habitantes",
        template="plotly"
    )

    # Mejorar diseño
    fig_tendencias.update_layout(
        xaxis_title="Periodo",
        yaxis_title="Accesos por cada 100",
        title_font_size=16,
        legend_title_text="Indicador"
    )

    # Mostrar el gráfico en el dashboard
    st.plotly_chart(fig_tendencias)

    # Insights Significativos
    st.subheader("Insights Significativos")
    st.markdown("""
    - **Brechas Geográficas Persistentes**:
      - Regiones urbanas como *Capital Federal, Tierra del Fuego y La Pampa* lideran en accesos por cada 100 habitantes y hogares.
      - En contraste, provincias rurales como *Formosa, Chaco y San Juan* están significativamente rezagadas, reflejando desigualdades en infraestructura tecnológica y nivel de urbanización.
    - **Crecimiento Sostenido en Penetración de Internet**:
      - La penetración ha mejorado notablemente desde 2014, con valores más altos en 2024 tanto en accesos por cada 100 habitantes (cercano a 30) como por cada 100 hogares (cercano a 80).
      - Esto sugiere un progreso constante en conectividad, aunque con variaciones entre regiones y hogares.
    - **Diferencia Entre Hogares y Habitantes**:
      - Siempre hay más accesos por hogar que por habitante, indicando que mientras los hogares se conectan más, el acceso individual todavía enfrenta desafíos.
      - En 2024, la diferencia es marcada, reflejando que no todos los individuos dentro de los hogares acceden al servicio.
    - **Patrones Temporales y Efectos Contextuales**:
      - El crecimiento en conectividad muestra aceleraciones en ciertos períodos, como entre 2019 y 2021, lo cual puede estar relacionado con eventos globales (como la pandemia) que impulsaron la demanda de internet.
    """)

# Sección: Calidad y Velocidad del Servicio
elif seccion == "Calidad y Velocidad del Servicio":
    st.header("1.2 Calidad y Velocidad del Servicio")

    st.write("""
    Esta sección tiene como objetivo identificar las velocidades promedio de Internet y su distribución entre las provincias de Argentina. 
    Se exploran las siguientes hojas de datos:
    - **Velocidad_sin_Rangos**
    - **Velocidad % por prov**
    - **Totales VMD**
    - **Accesos por rangos**
    - **Totales Accesos por rango**
    """)
    
    st.write("""
    En esta área se realizaron los análisis de:
    - Distribución de velocidades
    - Análisis por provincia
    - Velocidad promedio por provincia
    """)

    # Carga de los datos
    @st.cache_data
    def cargar_datos_velocidad():
        velocidad_sin_rangos = pd.read_csv("velocidad_sin_rangos_limpio.csv")
        velocidad_por_prov = pd.read_csv("Velocidad_por_provincia_limpio.csv")
        totales_vmd = pd.read_csv("Totales_VMD_limpio.csv")
        accesos_por_rangos = pd.read_csv("accesos_por_rangos_limpio.csv")
        totales_accesos_por_rango = pd.read_csv("Totales_Accesos_por_rango_limpio.csv")
        return velocidad_sin_rangos, velocidad_por_prov, totales_vmd, accesos_por_rangos, totales_accesos_por_rango

    velocidad_sin_rangos, velocidad_por_prov, totales_vmd, accesos_por_rangos, totales_accesos_por_rango = cargar_datos_velocidad()

    # Cálculo del promedio nacional de velocidad media
    promedio_nacional = velocidad_por_prov["Mbps (Media de bajada)"].mean()
    st.write(f"**Promedio Nacional de Velocidad Media de Bajada**: {promedio_nacional:.2f} Mbps")

    # Gráfico interactivo de velocidad promedio por provincia
    st.subheader("Gráfico: Velocidad Promedio por Provincia")
    st.write("""
    Este gráfico muestra la velocidad promedio de bajada de internet por provincia. Las provincias están ordenadas de acuerdo con su velocidad media.
    """)

    # Crear gráfico interactivo con Plotly
    fig_velocidad = px.bar(
        velocidad_por_prov,
        x="Provincia",
        y="Mbps (Media de bajada)",
        color="Provincia",  # Colorea las barras por provincia
        title="Velocidad Promedio por Provincia (Mbps)",
        labels={"Mbps (Media de bajada)": "Velocidad Promedio (Mbps)", "Provincia": "Provincia"},
        template="plotly",  # Estilo visual
    )

    # Mejorar diseño del gráfico
    fig_velocidad.update_layout(
        xaxis_title="Provincia",
        yaxis_title="Velocidad Promedio (Mbps)",
        xaxis_tickangle=45,  # Rotación de etiquetas del eje X
        title_font_size=16
    )

    # Mostrar gráfico en el dashboard
    st.plotly_chart(fig_velocidad)

    # Insights Significativos
    st.subheader("Insights Significativos")
    st.markdown("""
    - **Disparidad en la calidad del servicio**:
      - Existe una gran variabilidad en las velocidades de internet entre provincias. 
      - Las velocidades promedio van desde 3.46 Mbps (mínimo) hasta 170.78 Mbps (máximo), con una desviación estándar de 43.26 Mbps.
    
    - **Diferencias regionales**:
      - Provincias más urbanizadas, como *Capital Federal* y *Buenos Aires*, lideran en velocidades promedio debido a una infraestructura avanzada.
      - Regiones rurales como *Chubut* presentan velocidades significativamente más bajas, reflejando brechas en desarrollo tecnológico e inversión.
    
    - **Distribución sesgada**:
      - La velocidad promedio nacional (61.3 Mbps) es mayor que la mediana (44.64 Mbps), indicando la influencia de algunas provincias con velocidades muy altas en el promedio general.
    
    - **Infraestructura y población**:
      - Las provincias con mayor densidad de población tienden a contar con mejores servicios, mientras que las áreas rurales enfrentan desafíos de acceso.
    
    - **Oportunidades de mejora**:
      - Las regiones con bajas velocidades ofrecen una oportunidad para inversiones estratégicas y expansión del mercado, especialmente mediante tecnologías alternativas como el internet satelital.
    """)

# Sección 1.3 Tecnologías de Conexión
elif seccion == "Tecnologías de Conexión":
    st.header("1.3 Tecnologías de Conexión")

    st.write("""
    Esta sección analiza las tecnologías de conexión dominantes en Argentina y su evolución en el tiempo. 
    Se busca identificar tendencias en el uso de tecnologías como Fibra Óptica, ADSL, Cablemódem, entre otras.
    """)

    # Incluir las hojas relevantes y los análisis realizados
    st.write("""
    **Hojas relevantes:**
    - Accesos_tecnologia_localidad
    - Totales Accesos Por Tecnología
    - Accesos Por Tecnología

    En esta área se realizaron los análisis de:
    - Tecnologías Más Utilizadas
    - Tecnologías dominantes
    - Evolución del Uso de Tecnologías
    """)

    # Carga de datos
    @st.cache_data
    def cargar_tecnologias_datos():
        accesos_tecnologia_localidad = pd.read_csv("Accesos_tecnologia_localidad_limpio.csv")
        totales_accesos_por_tecnologia = pd.read_csv("Totales_Accesos_Por_Tecnologia_limpio.csv")
        accesos_por_tecnologia = pd.read_csv("Accesos_Por_Tecnologia_limpio.csv")
        return accesos_tecnologia_localidad, totales_accesos_por_tecnologia, accesos_por_tecnologia

    accesos_tecnologia_localidad, totales_accesos_por_tecnologia, accesos_por_tecnologia = cargar_tecnologias_datos()

    # Gráfico: Evolución del Uso de Tecnologías
    st.subheader("Gráfico: Evolución del Uso de Tecnologías")
    st.write("""
    Este gráfico muestra la evolución temporal del uso de diferentes tecnologías de conexión a Internet 
    en Argentina desde el año 2014 hasta 2024, por trimestre.
    """)

    # Seleccionar las columnas relevantes de tecnologías
    columnas_tecnologias = [
        col for col in totales_accesos_por_tecnologia.columns 
        if col not in ['Año', 'Trimestre']
    ]

    # Sumar accesos por tecnología y periodo (año-trimestre)
    tendencias = totales_accesos_por_tecnologia.groupby(['Año', 'Trimestre'])[columnas_tecnologias].sum().reset_index()

    # Crear una columna combinada para periodo (Año-Trimestre)
    tendencias['Periodo'] = tendencias['Año'].astype(str) + "-T" + tendencias['Trimestre'].astype(str)

    # Transformar el DataFrame para Plotly (long format)
    tendencias_melted = tendencias.melt(id_vars='Periodo', value_vars=columnas_tecnologias, 
                                        var_name='Tecnología', value_name='Cantidad de Accesos')

    # Crear gráfico interactivo con Plotly
    fig_tecnologias = px.line(
        tendencias_melted,
        x='Periodo',
        y='Cantidad de Accesos',
        color='Tecnología',
        markers=True,
        title="Tendencia Temporal de las Tecnologías de Conexión (2014-2024)",
        labels={'Cantidad de Accesos': 'Accesos Totales', 'Periodo': 'Periodo (Año-Trimestre)'},
        template="plotly"
    )

    # Mejorar el diseño
    fig_tecnologias.update_layout(
        xaxis_title="Periodo (Año-Trimestre)",
        yaxis_title="Cantidad de Accesos",
        legend_title="Tecnología",
        title_font_size=16,
        xaxis_tickangle=45
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_tecnologias)

    # Insights Significativos
    st.subheader("Insights Significativos")
    st.write("""
    A partir del análisis realizado, los siguientes insights se destacan como los más relevantes:
    """)

    # Detallar cada insight con markdown
    st.markdown("""
    - **Predominio del Cablemódem**:
        - **Proporción**: Representa el 48% de los accesos acumulados, destacándose como la tecnología más utilizada en todo el país.
        - **Razón de su éxito**: Esto se debe a su disponibilidad, rendimiento confiable y costos accesibles para usuarios finales.

    - **Declive de tecnologías antiguas**:
        - **ADSL**: Disminución sostenida de accesos (un 79% menos entre 2014 y 2024 Q1), reflejando una transición hacia tecnologías más modernas como la fibra óptica.
        - **Dial-up**: Casi obsoleto, con una adopción mínima.

    - **Crecimiento de Fibra Óptica**:
        - **Explosión en adopción**: Aumentó más de 27 veces entre 2014 Q1 (150,323) y 2024 Q2 (4.1 millones).
        - **Concentración urbana**: Su crecimiento es más notable en regiones urbanas con mayor infraestructura tecnológica.

    - **Persistencia del Wireless**:
        - Aunque minoritario, su adopción sigue aumentando, especialmente en áreas rurales o regiones de difícil acceso donde otras tecnologías no son viables.

    - **Provincias líderes en modernización**:
        - **Buenos Aires y Capital Federal**: Estas provincias tienen los mayores accesos a fibra óptica, reflejando inversiones tecnológicas y demanda en áreas urbanas.
    """)

 
# Sección: KPI's

# KPI 1 - Aumento del 2% en el acceso al servicio de internet por provincia
if seccion == "KPI's":
    st.header("📊 KPI: Aumentar en un 2% el acceso al servicio de internet por provincia")

    st.write("""
    Este gráfico muestra un objetivo clave: aumentar en un **2%** el acceso al servicio de internet para el próximo trimestre, 
    expresado en términos de accesos por cada 100 hogares para cada provincia. La comparación incluye el acceso actual y el acceso planificado.
    """)

    # Cargar datos
    @st.cache_data
    def cargar_kpi_data():
        return pd.read_csv("Penetracion_hogares_limpio.csv")

    penetracion_hogares = cargar_kpi_data()

    # Filtrar datos más recientes (año 2024, trimestre 2)
    acceso_actual = penetracion_hogares[
        (penetracion_hogares['Año'] == 2024) & (penetracion_hogares['Trimestre'] == 2)
    ].copy()

    # Calcular nuevo acceso y KPI
    acceso_actual['Nuevo_acceso'] = acceso_actual['Accesos por cada 100 hogares'] * 1.02
    acceso_actual['KPI (%)'] = (
        (acceso_actual['Nuevo_acceso'] - acceso_actual['Accesos por cada 100 hogares']) /
        acceso_actual['Accesos por cada 100 hogares']
    ) * 100

    # Gráfico interactivo con Plotly
    fig_kpi = go.Figure()

    # Barras de Acceso Actual
    fig_kpi.add_trace(go.Bar(
        x=acceso_actual['Provincia'],
        y=acceso_actual['Accesos por cada 100 hogares'],
        name="Acceso Actual",
        marker_color="skyblue"
    ))

    # Barras de Nuevo Acceso (Planificado)
    fig_kpi.add_trace(go.Bar(
        x=acceso_actual['Provincia'],
        y=acceso_actual['Nuevo_acceso'],
        name="Acceso Planificado (2%)",
        marker_color="orange"
    ))

    # Diseño del gráfico
    fig_kpi.update_layout(
        title="Incremento Planificado del 2% en el Próximo Trimestre",
        xaxis_title="Provincia",
        yaxis_title="Accesos por cada 100 Hogares",
        barmode="group",  # Barras agrupadas
        xaxis_tickangle=45,
        template="plotly",
        legend_title_text="Categoría"
    )

    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig_kpi)

    # Tabla con resultados detallados
    st.subheader("📋 Datos Detallados por Provincia")
    st.dataframe(acceso_actual[['Provincia', 'Accesos por cada 100 hogares', 'Nuevo_acceso', 'KPI (%)']])
      
    
        # KPI 2 - Crecimiento Trimestral de Accesos por Tecnología
    st.header("📊 KPI: Crecimiento Trimestral de Accesos por Tecnología")

    st.write("""
    Este gráfico muestra el crecimiento trimestral de accesos para cada tecnología de conexión, calculando la variación porcentual 
    de accesos entre trimestres para tecnologías como ADSL, Cablemodem, Fibra Óptica, Wireless y Otros.
    """)

    # Cargar datos
    @st.cache_data
    def cargar_datos_crecimiento():
        return pd.read_csv("Accesos_Por_Tecnologia_limpio.csv")

    accesos_por_tecnologia = cargar_datos_crecimiento()

    # Preparar los datos
    tasas_crecimiento = accesos_por_tecnologia[['Año', 'Trimestre', 
                                                'ADSL', 'Cablemodem', 
                                                'Fibra óptica', 'Wireless', 
                                                'Otros']].copy()

    # Calcular el crecimiento trimestral
    tasas_crecimiento = tasas_crecimiento.sort_values(by=['Año', 'Trimestre'])
    tasas_crecimiento['ADSL_Crecimiento'] = tasas_crecimiento['ADSL'].pct_change() * 100
    tasas_crecimiento['Cablemodem_Crecimiento'] = tasas_crecimiento['Cablemodem'].pct_change() * 100
    tasas_crecimiento['Fibra_Crecimiento'] = tasas_crecimiento['Fibra óptica'].pct_change() * 100
    tasas_crecimiento['Wireless_Crecimiento'] = tasas_crecimiento['Wireless'].pct_change() * 100
    tasas_crecimiento['Otros_Crecimiento'] = tasas_crecimiento['Otros'].pct_change() * 100

    # Crear columna 'Periodo'
    tasas_crecimiento['Periodo'] = tasas_crecimiento['Año'].astype(str) + " T" + tasas_crecimiento['Trimestre'].astype(str)

    # Eliminar filas NaN
    tasas_crecimiento = tasas_crecimiento.dropna(subset=['ADSL_Crecimiento', 'Cablemodem_Crecimiento', 
                                                        'Fibra_Crecimiento', 'Wireless_Crecimiento', 
                                                        'Otros_Crecimiento'])

    # Gráfico interactivo con Plotly
    fig_crecimiento = go.Figure()

    # Añadir trazas para cada tecnología
    fig_crecimiento.add_trace(go.Scatter(
        x=tasas_crecimiento['Periodo'], y=tasas_crecimiento['ADSL_Crecimiento'],
        mode='lines+markers', name='ADSL', line=dict(color='blue')
    ))
    fig_crecimiento.add_trace(go.Scatter(
        x=tasas_crecimiento['Periodo'], y=tasas_crecimiento['Cablemodem_Crecimiento'],
        mode='lines+markers', name='Cablemodem', line=dict(color='green')
    ))
    fig_crecimiento.add_trace(go.Scatter(
        x=tasas_crecimiento['Periodo'], y=tasas_crecimiento['Fibra_Crecimiento'],
        mode='lines+markers', name='Fibra Óptica', line=dict(color='red')
    ))
    fig_crecimiento.add_trace(go.Scatter(
        x=tasas_crecimiento['Periodo'], y=tasas_crecimiento['Wireless_Crecimiento'],
        mode='lines+markers', name='Wireless', line=dict(color='cyan')
    ))
    fig_crecimiento.add_trace(go.Scatter(
        x=tasas_crecimiento['Periodo'], y=tasas_crecimiento['Otros_Crecimiento'],
        mode='lines+markers', name='Otros', line=dict(color='magenta')
    ))

    # Configurar diseño del gráfico
    fig_crecimiento.update_layout(
        title="Crecimiento Trimestral de Accesos por Tecnología",
        xaxis_title="Periodo",
        yaxis_title="Crecimiento (%)",
        xaxis=dict(tickangle=45),
        legend_title="Tecnologías",
        template="plotly",
        hovermode="x unified"
    )

    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig_crecimiento)
    
        # Observaciones para KPI 2
    st.subheader("📌 Observaciones por Tecnología")
    st.markdown("""
    **ADSL (azul):** Mantiene valores cercanos al 0% de crecimiento, lo que sugiere estancamiento o disminución en su adopción.

    **Cablemodem (verde):** Tiene variaciones más regulares y picos moderados, lo que indica un crecimiento estable en ciertos períodos.

    **Fibra óptica (rojo):** Muestra un crecimiento significativo y algunos picos extremos (por encima de los 3.5 millones de %), probablemente por un aumento súbito en su adopción en algunos períodos o por un error en los datos.

    **Wireless (celeste):** Registra crecimientos pequeños pero constantes, con algunos picos moderados.

    **Otros (morado):** Tiene variaciones más planas y cercanas a 0, lo que indica un crecimiento muy bajo.
    """)

    st.markdown("""
    ### Tendencias Notables:
    - **Fibra óptica:** Domina el gráfico por sus picos pronunciados, reflejando una transición hacia esta tecnología en algunos períodos específicos.
    - **ADSL y Otros:** Están en declive o crecimiento insignificante, indicando que están siendo reemplazados por tecnologías más modernas como la fibra óptica.
    - **Cablemodem y Wireless:** Tienen un crecimiento más estable, reflejando su adopción continua pero no tan acelerada como la fibra óptica.
    """)
    
    