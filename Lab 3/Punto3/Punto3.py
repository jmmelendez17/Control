import streamlit as st
import numpy as np
import control as ct
import matplotlib.pyplot as plt

st.title("Calculadora de estabilidad por el criterio de Ruth")

st.write("Esta aplicación despliega el arreglo de Routh, el polinomio característico, el mapa de polos del sistemay da detalles sobre la estabilidad del mismo")

# Obtener el polinomio en orden descendente del usuario
polynomial_input = st.text_input("Por favor, ingrese su polinomio en orden descendente y separado por comas como en el ejemplo siguiente:", "1 ,2, 3, 4, 5")
coefficients = [float(coeff.strip()) for coeff in polynomial_input.split(',')]

st.write("su polinomio característico es:")
def format_polynomial_term(coeff, power):
    sign = '+' if coeff >= 0 else '-'
    coeff_abs = abs(coeff)

    if coeff_abs == 0:
        return ''
    elif power == 0:
        return f"{sign}{int(coeff_abs)}"
    elif power == 1:
        return f"{sign}{int(coeff_abs)}s"
    else:
        return f"{sign}{int(coeff_abs)}s^{power}"

def polynomial_to_latex(coefficients):
    n = len(coefficients)
    polynomial_latex = "P(s) = " + ''.join(format_polynomial_term(coefficients[i], n - i - 1) for i in range(n) if coefficients[i] != 0)

    return polynomial_latex

# Mostrar el polinomio ingresado con formato LaTeX
polynomial_latex = polynomial_to_latex(coefficients)
st.latex(polynomial_latex)


print(coefficients)
#Definir longitud del polinomio
n=len(coefficients)
epsilon = 1e-10 
CE=0
C0=0

print (n)

#Definir dimensión de la matriz
if n %2==0: 
    Longmat=int(n/2)
    z=0 #Es par
else: 
    Longmat=int((n+1)/2)
    z=1

print (Longmat)

matriz = np.zeros((n, Longmat))

print (matriz)

for j in range (0, Longmat):
    matriz[0, j] = coefficients[2*j]

    if z==1:
        for j in range (0, Longmat-1):
            matriz[1, j] = coefficients[(2*j)+1]
    else:
        for j in range (0, Longmat):
            matriz[1, j] = coefficients[(2*j)+1]



print(matriz)

for i in range (2, n):
    for j in range (0, Longmat):
        if j + 1 < Longmat:
           matriz[i,j]= ((matriz[i-1,j]*matriz[i-2,j+1])- (matriz[i-2, j] * matriz[i-1,j+1]))/matriz[i-1,j]
           CS=0 #caso especial
           if abs(matriz[i, 0]) == 0:
               if sum(matriz[i]) == 0 and Longmat > i < n-1:
                    d = i
                    C0 = 1   
                    for j in range(Longmat):
                        matriz[d, j] = matriz[d-1, j] * ((n-d) - (2*j))
                        for i in range (d+1, n):
                            for j in range (0, Longmat):
                                if j + 1 < Longmat:
                                 matriz[i,j]= ((matriz[i-1,j]*matriz[i-2,j+1])- (matriz[i-2, j] * matriz[i-1,j+1]))/matriz[i-1,j]
                                
                        
                   
                    
               else:
                 matriz[i, 0] = epsilon
                 CE=1


for i in range(2, n):
    for j in range(Longmat):
        if matriz[i, j] is None:
            matriz[i, j] = 0



# Identificar cambios de signo en la primera columna
cambios_signo_primera_columna = 0
for i in range(1, n):  # Empezamos desde la segunda fila
    if matriz[i, 0] * matriz[i - 1, 0] < 0:
        cambios_signo_primera_columna += 1



# Mostrar la matriz
# Convertir la matriz a una cadena formateada

st.write("Arreglo de Routh:")
matriz_latex = "\\begin{bmatrix}\n"
for i in range(n):
    matriz_latex += " & ".join([f"{int(np.round(matriz[i, j]))}" if not np.isnan(matriz[i, j]) else ' ' for j in range(Longmat)])
    matriz_latex += " \\\\\n"
matriz_latex += "\\end{bmatrix}"

# Mostrar la matriz en formato LaTeX
st.latex(matriz_latex)

if cambios_signo_primera_columna==0:
    st.write("No hay raices inestables en el sistema.")
else:
    st.write(f"Hay {cambios_signo_primera_columna} raiz/raíces inestables en el sistema.")

if CE==1:
    st.write("Se aplica el caso especial de Epsilon.")
else:
    if C0==1:
        st.write("Se aplica el caso especial del polinomio auxiliar")
    else:
            if CS==0:
                st.write("No se aplican casos especiales.")


print(matriz)
# Create a transfer function (you can also use state-space or other representations)
numerator = [1]  # Coefficients of the numerator polynomial
denominator = coefficients  # Coefficients of the denominator polynomial
sys = ct.TransferFunction(numerator, denominator)


# Mostrar el mapa de polos y ceros
plt.figure()
ct.pzmap(sys)

# Personalizar el gráfico
plt.grid(True)
plt.title('Mapa de polos del sistema')
plt.ylabel('Imaginario (jw)')
plt.xlabel('Real (s)')

# Mostrar el gráfico en Streamlit
st.pyplot(plt)


