import math
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Título de la aplicación
# Título de la aplicación
st.title("Análisis de respuesta en frecuencia")

st.write("Esta aplicación permite encontrar la función de transferencia de un sistema de control a partir del análisis de su respuesta en frecuencia.")

# Botón para cargar el archivo CSV
uploaded_file = st.file_uploader("Cargar un archivo CSV", type=["csv"])

# Selector para el tipo de frecuencia (Hz o Rad/s)
freq_type = st.selectbox("Unidades de frecuencia", ["Hz", "Rad/s"])

if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(uploaded_file)

    # Haz lo que quieras con el DataFrame (por ejemplo, mostrarlo)
    if df is not None:
        Mag = df['Mag'].ravel().tolist()
        Phase = df['Phase'].ravel().tolist()
        Frec = df['W'].ravel().tolist()

        # Convierte las frecuencias a radianes por segundo si es necesario
        if freq_type == "Hz":
            Frec = np.deg2rad(Frec)

        # Crear la figura para magnitud
        fig_mag, ax_mag = plt.subplots()
        ax_mag.semilogx(Frec, Mag)
        ax_mag.set_ylabel('Magnitud')
        ax_mag.set_xlabel(f'Frecuencia ({freq_type})')
        ax_mag.set_title('Respuesta del sistema experimental (Magnitud)')

        # Crear la figura para fase
        fig_phase, ax_phase = plt.subplots()
        ax_phase.semilogx(Frec, Phase)
        ax_phase.set_xlabel(f'Frecuencia ({freq_type})')
        ax_phase.set_ylabel('Fase (grados)')
        ax_phase.set_title('Respuesta del sistema experimental (Fase)')

        # Mostrar la gráfica en Streamlit
        if st.button("Graficar"):
            # Mostrar la gráfica en Streamlit
            st.pyplot(fig_mag)
            st.pyplot(fig_phase)