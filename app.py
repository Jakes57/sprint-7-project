import pandas as pd
import plotly.express as px
import streamlit as st
     
car_data = pd.read_csv('vehicles_us.csv')  # leer los datos

# Casilla para histograma
show_hist = st.checkbox('Mostrar histograma de odómetro')

# Casilla para gráfico de dispersión
show_scatter = st.checkbox('Mostrar gráfico de dispersión Precio vs Año del modelo')

if show_hist:
    st.write('Creación de un histograma para el conjunto de datos de anuncios de venta de coches')
    fig = px.histogram(car_data, x="odometer")
    st.plotly_chart(fig, use_container_width=True)

if show_scatter:
    st.write('Creación de un gráfico de dispersión: Precio vs Año del modelo')
    fig = px.scatter(car_data, x='model_year', y='price',
                     color='condition', title='Precio vs Año del modelo por condición')
    st.plotly_chart(fig, use_container_width=True)