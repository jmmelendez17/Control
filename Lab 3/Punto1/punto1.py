import matplotlib.pyplot as plt
from scipy import signal
import control as ct
import numpy as np

# Definir el rango de valores de a
a_values = np.linspace(0, 150, 400)  # Puedes ajustar los límites y el número de puntos

# Calcular K en función de a
K_values = 2 * (2 * np.sqrt(64 * a_values**2 - 232 * a_values + 289) - 16 * a_values + 29)

# Crear el gráfico
plt.figure(figsize=(10, 6))
plt.plot(a_values, K_values, color='purple', label='Valores estables del sistema')
plt.fill_between(a_values, K_values, color='lightblue', alpha=0.5, label='Parejas estables de K-a')
plt.xlabel('Valores de a')
plt.ylabel('Valores de K')
plt.xlim([0, 15])
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
plt.title('Validación de estabilidad K-a')
plt.legend()
plt.grid(True)
plt.show()

#Sistema estable 
a1= 1
K1= 2 * (2 * np.sqrt(64 * a1**2 - 232 * a1 + 289) - 16 * a1+ 29) -50

numerator = [K1,K1*a1 ]  # Coefficients of the numerator polynomial
denominator = [1, 8, 17, 10+K1, K1*a1]  # Coefficients of the denominator polynomial
sys1 = ct.TransferFunction(numerator, denominator)
print(sys1)

# Plot poles and zeros
plt.figure()
ct.pzmap(sys1)

# Customize plot (optional)
plt.grid(True)
plt.title('Mapa de polos y ceros')
plt.ylabel('Imaginario (jw)')
plt.xlabel('real (s)')
plt.show()

# Definir el vector de tiempo
t = np.linspace(0, 100, 10000)
# Generar el escalón unitario
escalon = np.ones_like(t)
# Calcular la respuesta al escalón
time, response = ct.step_response(sys1, T=t)
# Crear el gráfico
plt.figure()
plt.plot(t, response, label='Respuesta del sistema', color='purple', linestyle= 'dashed')
plt.plot(t, escalon, label='Escalón unitario', color='green')
plt.xlim([0,15])
plt.grid(True)
plt.title('Respuesta al escalón de un sistema de control estable')
plt.ylabel('Respuesta')
plt.xlabel('Tiempo (s)')
plt.legend()
plt.show()


#Sistema inestable 
a1= 1
K1= 2 * (2 * np.sqrt(64 * a1**2 - 232 * a1 + 289) - 16 * a1+ 29) + 20

numerator = [K1,K1*a1 ]  # Coefficients of the numerator polynomial
denominator = [1, 8, 17, 10+K1, K1*a1]  # Coefficients of the denominator polynomial
sys2 = ct.TransferFunction(numerator, denominator)
print(sys2)

# Plot poles and zeros
plt.figure()
ct.pzmap(sys2)

# Customize plot (optional)
plt.grid(True)
plt.title('Mapa de polos y ceros')
plt.ylabel('Imaginario (jw)')
plt.xlabel('real (s)')
plt.show()

# Definir el vector de tiempo
t = np.linspace(0, 100, 10000)
# Generar el escalón unitario
escalon = np.ones_like(t)
# Calcular la respuesta al escalón
time, response = ct.step_response(sys2, T=t)
# Crear el gráfico
plt.figure()
plt.plot(t, response, label='Respuesta del sistema', color='purple', linestyle= 'dashed')
plt.plot(t, escalon, label='Escalón unitario', color='green')
plt.ylim([-20,20])
plt.xlim([0,15])
plt.grid(True)
plt.title('Respuesta al escalón de un sistema de control estable')
plt.ylabel('Respuesta')
plt.xlabel('Tiempo (s)')
plt.legend()
plt.show()

