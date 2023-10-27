import numpy as np
import matplotlib.pyplot as plt
import control as ct

# Definir las funciones de transferencia de los sistemas
G0 = ct.TransferFunction([20], [1])  # Cero 1
G1 = ct.TransferFunction([1, 1], [1])  # Cero 1
G2 = ct.TransferFunction([1], [1, 0])     # Polo en origen
G3 = ct.TransferFunction([1], [1, 5])     # Polo en 5
G4 = ct.TransferFunction([1], [1, 2, 10])     # Polo cuadrático

# Crear una lista de frecuencias en un rango más amplio
frequencies = np.logspace(-1, 3, 1000)

# Calcular las respuestas en frecuencia y guardar los resultados
w0, mag0, phase0 = ct.bode_plot(G0, omega=frequencies, dB=True, label='Constante',  linestyle='dashed')
w1, mag1, phase1 = ct.bode_plot(G1, omega=frequencies, dB=True, label='Cero 1')
w2, mag2, phase2 = ct.bode_plot(G2, omega=frequencies, dB=True, label='Polo en origen', linestyle='dashed')
w3, mag3, phase3 = ct.bode_plot(G3, omega=frequencies, dB=True, label='Polo en 5', linestyle='dashed')
w4, mag4, phase4 = ct.bode_plot(G4, omega=frequencies, dB=True, label='Polo cuadrático')
plt.xlabel('Frecuencia (rad/s)')
plt.ylabel('Fase (grados)')
plt.grid(True)

# Agregar leyenda
plt.legend()

# Personalizar etiquetas y título
plt.suptitle('Bosquejo de diagrama de Bode')
plt.tight_layout()
plt.subplots_adjust(top=0.88)
# Personalizar etiquetas de los ejes
plt.xlabel('Frecuencia (rad/s)')
plt.subplots_adjust(hspace=0.4)

plt.show()

# Definir las funciones de transferencia de los sistemas
Gs = ct.TransferFunction([20,20], [1, 7, 20, 50, 0])  #función completa
ws, mags, phases = ct.bode_plot(Gs, omega=frequencies, dB=True, color='purple', margins=True)
Margin1= ct.margin(Gs)


# Personalizar etiquetas y título
plt.suptitle('Diagrama de Bode')
plt.tight_layout()
plt.subplots_adjust(top=0.88)
# Personalizar etiquetas de los ejes
plt.xlabel('Frecuencia (rad/s)')
plt.subplots_adjust(hspace=0.4)

plt.show()


#Gráfica para K=40

# Definir las funciones de transferencia de los sistemas
G0 = ct.TransferFunction([40], [1])  # Cero 1
G1 = ct.TransferFunction([1, 1], [1])  # Cero 1
G2 = ct.TransferFunction([1], [1, 0])     # Polo en origen
G3 = ct.TransferFunction([1], [1, 5])     # Polo en 5
G4 = ct.TransferFunction([1], [1, 2, 10])     # Polo cuadrático

# Crear una lista de frecuencias en un rango más amplio
frequencies = np.logspace(-1, 3, 1000)

# Calcular las respuestas en frecuencia y guardar los resultados
w0, mag0, phase0 = ct.bode_plot(G0, omega=frequencies, dB=True, label='Constante',  linestyle='dashed')
w1, mag1, phase1 = ct.bode_plot(G1, omega=frequencies, dB=True, label='Cero 1')
w2, mag2, phase2 = ct.bode_plot(G2, omega=frequencies, dB=True, label='Polo en origen', linestyle='dashed')
w3, mag3, phase3 = ct.bode_plot(G3, omega=frequencies, dB=True, label='Polo en 5', linestyle='dashed')
w4, mag4, phase4 = ct.bode_plot(G4, omega=frequencies, dB=True, label='Polo cuadrático')
plt.xlabel('Frecuencia (rad/s)')
plt.ylabel('Fase (grados)')
plt.grid(True)

# Agregar leyenda
plt.legend()

# Personalizar etiquetas y título
plt.suptitle('Bosquejo de diagrama de Bode')
plt.tight_layout()
plt.subplots_adjust(top=0.88)
# Personalizar etiquetas de los ejes
plt.xlabel('Frecuencia (rad/s)')
plt.subplots_adjust(hspace=0.4)

plt.show()

# Definir las funciones de transferencia de los sistemas
Gs = ct.TransferFunction([40,40], [1, 7, 20, 50, 0])  #función completa
ws, mags, phases = ct.bode_plot(Gs, omega=frequencies, dB=True, color='purple', margins=True)
Margin2= ct.margin(Gs)

# Personalizar etiquetas y título
plt.suptitle('Diagrama de Bode')
plt.tight_layout()
plt.subplots_adjust(top=0.88)
# Personalizar etiquetas de los ejes
plt.xlabel('Frecuencia (rad/s)')
plt.subplots_adjust(hspace=0.4)

plt.show()



