import pandas as pd
import plotly.express as px
import streamlit as st

# Encabezado y presentación
st.title("Listados de Vehículos USA 1900–2020")

st.markdown("""
Esta aplicación web permite explorar y visualizar datos de anuncios de venta de vehículos usados en Estados Unidos.  
Interactúa con los gráficos para conocer mejor el mercado de autos en los Estados Unidos.
""")

# Cargar datos
car_data = pd.read_csv('vehicles_us.csv')

# Mostrar el dataframe completo de forma interactiva
st.subheader("Datos de los anuncios")
st.dataframe(car_data)

# Crear Titulo Visualizaciones
st.subheader("Visualizaciones Pre-hechas")

# Casilla para histograma
show_hist = st.checkbox('Mostrar histograma de odómetro')

# Casilla para gráfico de dispersión
show_scatter = st.checkbox('Mostrar gráfico de dispersión Precio vs Año del modelo')

# Casilla para gráfico de pastel
show_pie = st.checkbox('Mostrar gráfico de pastel: distribución de vehículos por rango de precio')

if show_hist:
    st.write('Creación de un histograma para el conjunto de datos de anuncios de venta de coches')
    fig = px.histogram(car_data, x="odometer")
    st.plotly_chart(fig, use_container_width=True)

if show_scatter:
    st.write('Creación de un gráfico de dispersión: Precio vs Año del modelo')
    fig = px.scatter(car_data, x='model_year', y='price',
                     color='condition', title='Precio vs Año del modelo por condición')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Crea tu propia gráfica de barras")

if show_pie:
    st.write('Distribución de vehículos por rango de precio')

    # Slider para seleccionar rango de precios
    min_price = int(car_data['price'].min())
    max_price = int(car_data['price'].max())
    price_range = st.slider('Selecciona el rango de precios:', min_value=min_price, max_value=max_price, value=(min_price, max_price))

    # Filtrar el DataFrame según el rango seleccionado
    filtered_data = car_data[(car_data['price'] >= price_range[0]) & (car_data['price'] <= price_range[1])]

    if filtered_data.empty:
        st.warning("No hay datos para ese rango de precio. Intenta con otro rango.")
    else:
        # Definir bins dinámicos basados en el rango seleccionado
        bins = list(range(price_range[0], price_range[1] + 1, max(1000, (price_range[1] - price_range[0]) // 6)))
        if bins[-1] < price_range[1]:
            bins.append(price_range[1])

        labels = [f"{bins[i]} - {bins[i+1]}" for i in range(len(bins)-1)]

        # Crear columna de rangos de precio
        filtered_data['price_range'] = pd.cut(filtered_data['price'], bins=bins, labels=labels, include_lowest=True)

        # Contar marcas por rango de precio
        grouped = filtered_data.groupby('price_range')['model'].value_counts().reset_index(name='count')

        # Obtener la marca más común por rango de precio
        top_brands = grouped.loc[grouped.groupby('price_range')['count'].idxmax()]

        fig = px.pie(top_brands, values='count', names='model',
                     title='Vehículo más común por rango de precio')

        st.plotly_chart(fig, use_container_width=True)

# Crear Titulo Grafico Personalizado de Barras
st.subheader("Crea tu propia visualización")

# Seleccionar columnas para el eje X e Y
x_col = st.selectbox("Selecciona la columna para el eje X:", car_data.columns)
y_col = st.selectbox("Selecciona la columna para el eje Y:", car_data.columns)

# Botón para generar la gráfica
if st.button("Generar gráfica de barras"):
    st.write(f"Mostrando comparación de '{y_col}' agrupado por '{x_col}'")

    try:
        # Agrupar datos y graficar
        grouped = car_data.groupby(x_col)[y_col].mean().reset_index()

        fig = px.bar(grouped, x=x_col, y=y_col,
                     labels={x_col: x_col.capitalize(), y_col: f"Promedio de {y_col}"},
                     title=f"Promedio de {y_col} por {x_col}")
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"No se pudo generar la gráfica: {e}")