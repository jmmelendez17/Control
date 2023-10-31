import math
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import control as ct
# Título de la aplicación
# Título de la aplicación
st.title("Análisis de respuesta en frecuencia")

st.write("Esta aplicación permite encontrar las características de la respuesta en frecuencia de un sistema de control a partir de su caracterización.")

# Botón para cargar el archivo CSV
uploaded_file = st.file_uploader("Cargar un archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(uploaded_file)

    # Haz lo que quieras con el DataFrame (por ejemplo, mostrarlo)
    if df is not None:
        Mag = ct.mag2db(df['Mag'].ravel().tolist())
        Phase = df['Phase'].ravel().tolist()
        Frec = df['W'].ravel().tolist()

        #frecuencia y pico de resonancia
        maxi=np.max(Mag)
        prueba=maxi - Mag[0] #Mira si hay resonancia
        if prueba > 0.2:
            indice_del_pico = np.argmax(Mag)
            frecuencia_del_pico = round(Frec[indice_del_pico], 3)
            Pico=round(maxi, 3)

        #Margen de ganancia 
        # Inicializar variables para almacenar la frecuencia y la magnitud correspondiente
        frecuencia_con_fase_minus_180 = None
        magnitud_en_frecuencia = None

        for i, fase in enumerate(Phase):
            if abs(fase + 180) < 1 and abs(fase + 180) > -1 :
                frecuencia_con_fase_minus_180 = Frec[i]
                magnitud_en_frecuencia = Mag[i]
                break
        
        if magnitud_en_frecuencia is not None:
            gainmar=round(0-magnitud_en_frecuencia, 3)
        else:
            gainmar= None

        #Margen de fase 
        # Inicializar variables para almacenar la frecuencia y la fase correspondiente
        frecuencia_con_mag_1 = None
        Fase_en_frec= None

        for i, magnitud in enumerate(Mag):
            if magnitud <= 0:
                frecuencia_con_mag_1 = round(Frec[i], 3)
                Fase_en_frec= round(Phase[i], 3)
                break
        
        phasenmar=round(180+Fase_en_frec,3)

        ##Constantes de error
        Kp = Mag[0]  # Error de posición
        Kv = (Mag[0] * Frec[0])  # Error de velocidad
        Ka = (Mag[0] * Frec[0]** 2)  # Error de aceleración
        print(Kp)
        print(Kv)
        print(Ka)
        # Crear la figura para magnitud
        fig_mag, ax_mag = plt.subplots()
        ax_mag.semilogx(Frec, Mag, color='purple', label='Magnitud del sistema')
        ax_mag.set_ylabel('Magnitud (dB)')
        ax_mag.set_xlabel('frecuencia (rad/s)')
        ax_mag.set_title('Respuesta del sistema experimental (Magnitud)')
        if frecuencia_del_pico is not None:
            ax_mag.vlines(x=frecuencia_del_pico, ymin=Mag[len(Mag)-1], ymax=Pico, linestyles='dashed', color='red', label='Frecuencia de resonancia')
        if frecuencia_con_mag_1 is not None:
            ax_mag.hlines(y=0, xmin=0, xmax=frecuencia_con_mag_1- 0.02, linestyles='dashed', color='Blue', label='Ancho de banda')
        if  frecuencia_con_fase_minus_180 is not None:
            ax_mag.vlines(x=frecuencia_con_fase_minus_180, ymin=0, ymax=magnitud_en_frecuencia, linestyles='dashed', color='Green', label='Margen de ganancia')
        ax_mag.legend()
        ax_mag.grid(which='both', linestyle='--')

        # Crear la figura para fase
        fig_phase, ax_phase = plt.subplots()
        ax_phase.semilogx(Frec, Phase, color='Purple', label='Fase del sistema')
        ax_phase.set_xlabel('frecuencia (rad/s)')
        ax_phase.set_ylabel('Fase (grados)')
        ax_phase.set_title('Respuesta del sistema experimental (Fase)')
        if frecuencia_con_mag_1 is not None:
            ax_phase.vlines(x=frecuencia_con_mag_1, ymin=-180, ymax=Fase_en_frec, linestyles='dashed', color='Green', label='Margen de fase')
            ax_phase.hlines(y=-180, xmin=0, xmax=frecuencia_con_mag_1, linestyles='dashed', color='Green')
        ax_phase.legend()
        ax_phase.grid(which='both', linestyle='--')


        # Mostrar la gráfica en Streamlit
        if st.button("Graficar"):
            # Mostrar la gráfica en Streamlit
            st.pyplot(fig_mag)
            st.pyplot(fig_phase)

            st.write(f"El ancho de banda del sistema es de {frecuencia_con_mag_1} rad/s")
            if prueba > 0.2:
                st.write(f"Existe un pico de resonancia de {Pico} dB y se encuentra en {frecuencia_del_pico} rad/s:")
            else:
                st.write("No Existe un picode resonancia")

            st. write(f"El margen de fase del sistema es de {phasenmar} grados")

            if gainmar is not None:
                st. write(f"El margen de ganancia del sistema es de {gainmar} dB")
            else:
                st.write("el margen de ganancia tiende a infinito")
            
            if Kp>20:
                st.write("La constante de error estático de posición es aproximadamente infinito")
            else:
                if Kp< 0.01:
                    st.write("La constante de error estático de posición es aproximadamente 0")
                else:
                    st.write(f"la constante de error estática de posición es {round(Kp, 3)}")
            if Kv>20:
                st.write("La constante de error estático de velocidad es aproximadamente infinito")
            else:
                if Kv< 0.01:
                    st.write("La constante de error estático de velocidad es aproximadamente 0")
                else:
                    st.write(f"la constante de error estática de velocidad es {round(Kv, 3)}")
            if Ka>20:
                st.write("La constante de error estático de aceleración es aproximadamente infinito")
            else:
                if Ka< 0.01:
                    st.write("La constante de error estático de aceleración es aproximadamente 0")
                else:
                    st.write(f"la constante de error estática de aceleración es {round(Ka, 3)}")

            