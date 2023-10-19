import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from control.matlab import *
import control as ct
import numpy as np
from scipy import signal
from scipy.signal import find_peaks
from scipy.optimize import root_scalar
import math
from scipy.optimize import curve_fit

# Título de la aplicación
st.title("Análisis de respuesta experimental")

# Botón para cargar el archivo CSV
uploaded_file = st.file_uploader("Cargar un archivo CSV", type=["csv"])

df = None
amort=None
ωn=None
ζ=None
if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(uploaded_file)

    # Haz lo que quieras con el DataFrame (por ejemplo, mostrarlo)
    if df is not None:
        t = df['t'].ravel().tolist()
        y = df['y'].ravel().tolist()
        plt.plot(t, y)
        plt.xlabel('Tiempo')
        plt.ylabel('Salida')
        fig, ax = plt.subplots()
        ax.plot(t, y)
        ax.set_title('Respuesta del sistema experimental')

        # Mostrar la gráfica en Streamlit
        st.pyplot(fig)

        # Calcular si es subamortiguado o sobreamortiguado
        maxi = max(y)
        ylength = len(y)
        if maxi > y[ylength - 1]:
            amort=1
            st.text_area('Estado del sistema', 'Sistema subamortiguado')
            print(f'amort es {amort}')
        else:
            amort=2
            st.text_area('Estado del sistema', 'Sistema sobreamortiguado')
            print(f'amort es {amort}')
ωn = 0  # Inicializar ωn con un valor predeterminado
ζ= 0

if amort == 1:
    if st.button("Calcular Función de Transferencia"):
        def second_order_subamortiguado(t, Kp, wn, zeta):
            return Kp * (1 - np.exp(-zeta * wn * t) * np.cos(wn * np.sqrt(1 - zeta**2) * t))

        # Ajustar los parámetros del sistema usando curve_fit
        params, covariance = curve_fit(second_order_subamortiguado, t, y, p0=[1.0, 1.0, 0.1])

        # Extraer los parámetros ajustados
        Kp_estimado, wn_estimada, zeta_estimada = params

        # Crear una figura y graficar los datos y el modelo ajustado
        t_modelo = np.linspace(0, max(t), 100)
        respuesta_modelo = second_order_subamortiguado(t_modelo, Kp_estimado, wn_estimada, zeta_estimada)

        
        num = [wn_estimada**2]
        den = [1, 2*zeta_estimada*wn_estimada, wn_estimada**2]
        Salida=ct.tf(num,den)
        tiempo, respuesta = ct.step_response(Salida)
         # Mostrar los resultados en un solo cuadro en Streamlit
        st.write(f"Coeficiente de Amortiguamiento (ζ): {zeta_estimada}")
        st.write(f"Frecuencia Natural (ωn) (rad/s): {wn_estimada}")
        st.write("Función de Transferencia:")
        st.latex(f"G(s) = \\frac{{{wn_estimada**2}}}{{s^2 + {2*wn_estimada*zeta_estimada}s + {wn_estimada**2}}}")

        # Crear una figura y graficar los datos y el modelo ajustado
        t_modelo = np.linspace(0, max(t), 100)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(t, y, label='Datos')
        # Extender la respuesta hasta t=60 interpolando los valores
        tiempo_extension = np.linspace(0, 60, len(t))  # Cambiar el número de puntos si es necesario
        respuesta_extension = np.interp(tiempo_extension, tiempo, respuesta)
        ax.plot(tiempo_extension, respuesta_extension, 'r--', label='Modelo subamortiguado')
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Respuesta')
        ax.set_xlim(0, 60)
        ax.set_title('Respuesta experimental vs sistema caracterizado')
        ax.legend()
        ax.grid(True)

        # Mostrar la gráfica en Streamlit
        st.pyplot(fig)
        error = respuesta_extension - y
        # Calcular el cuadrado del error
        error_cuadrado = error ** 2
        # Calcular la ISE como la suma acumulativa del error cuadrado
        ise = np.sum(error_cuadrado)
        st.write(f"el error de Predicción Cuadrático de este sistema es: {ise}")
else:
    if st.button("Calcular Función de Transferencia"):
        #Cálculo utilizando el método de Stark
        ylength = len(y)
        print(f"Longitud: {ylength}")
        maxi = max(y)
        ωn = 0  # Inicializar ωn con un valor predeterminado
        ζ= 0
        # Calcula el valor de X correspondiente al porcentaje del valor final de Y
        X_15 = [t[i] for i in range(ylength) if y[i] >= (15 / 100) * y[ylength - 1]]
        X_45 = [t[i] for i in range(ylength) if y[i] >= (45 / 100) * y[ylength - 1]]
        X_75 = [t[i] for i in range(ylength) if y[i] >= (75 / 100) * y[ylength - 1]]

        Stark = (X_45[0] - X_15[0]) / (X_75[0] - X_15[0])
        ζ = (0.0805 - 5.547 * ((0.475 - Stark) ** 2)) / (Stark - 0.356)
        Fzeta = 0.708 * ((2.811) ** ζ)
        ωn = Fzeta / (X_75[0] - X_15[0])
        FZeta2 = 0.922 * ((1.66) ** ζ)
        RET = X_45[0] - (FZeta2 / ωn)

        num = [ωn**2]
        den = [1, 2*ζ*ωn, ωn**2]
        Salida=ct.tf(num,den)
        tiempo, respuesta = ct.step_response(Salida)
        funcion_transferencia = f"G(s) = {ωn**2}/(s**2 + {2*ωn*ζ}s + {ωn**2} )"

        # Mostrar los resultados en un solo cuadro en Streamlit
        st.write(f"Coeficiente de Amortiguamiento (ζ): {ζ}")
        st.write(f"Frecuencia Natural (ωn) (rad/s): {ωn}")
        st.write("Función de Transferencia:")
        st.latex(f"G(s) = \\frac{{{ωn**2}}}{{s^2 + {2*ωn*ζ}s + {ωn**2}}}")
        st.write(f"El retardo del modelo es {RET}")

        # Crear una figura y graficar los datos y el modelo ajustado
        t_modelo = np.linspace(0, max(t), 100)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(t, y, label='Datos')
        # Extender la respuesta hasta t=60 interpolando los valores
        tiempo_extension = np.linspace(0, 60, len(t))  # Cambiar el número de puntos si es necesario
        respuesta_extension = np.interp(tiempo_extension, tiempo, respuesta)
        ax.plot(tiempo_extension, respuesta_extension, 'r--', label='Modelo sobreamortiguado')
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Respuesta')
        ax.set_xlim(0, 60)
        ax.set_title('Respuesta experimental vs sistema caracterizado')
        ax.legend()
        ax.grid(True)

        # Mostrar la gráfica en Streamlit
        st.pyplot(fig)

        error = respuesta_extension - y
        # Calcular el cuadrado del error
        error_cuadrado = error ** 2
        # Calcular la ISE como la suma acumulativa del error cuadrado
        ise = np.sum(error_cuadrado)
        st.write(f"el error de Predicción Cuadrático de este sistema es: {ise}")
