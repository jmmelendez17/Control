import numpy as np
import matplotlib.pyplot as plt
import control as ct
# Definir las funciones de transferencia de los sistemas
frequencies = np.logspace(-1, 3, 1000)
Gs = ct.TransferFunction([1,1], [1, 7, 20, 50, 0])
ct.root_locus(Gs)
plt.show()