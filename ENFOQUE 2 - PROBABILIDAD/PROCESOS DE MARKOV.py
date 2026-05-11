# Este código simula un proceso de Markov con 3 estados,
# genera una secuencia de estados a lo largo de varios pasos
# y visualiza la evolución del proceso.

import numpy as np
import matplotlib.pyplot as plt

class ProcesoDeMarkov:
    def __init__(self, matriz_transicion):
        """
        matriz_transicion:
            matriz donde cada fila representa:
            probabilidad de pasar de un estado a otro

        ejemplo:
            fila 0 -> probabilidades saliendo del estado 0
        """

        self.matriz_transicion = matriz_transicion
        self.n_estados = matriz_transicion.shape[0]

    def simular(self, estado_inicial, n_pasos):
        """
        genera una secuencia de estados

        estado_inicial:
            estado donde inicia el proceso

        n_pasos:
            cantidad de transiciones a simular
        """

        estados = [estado_inicial]
        estado_actual = estado_inicial

        for _ in range(n_pasos):

            # elegimos el siguiente estado
            # usando las probabilidades de la fila actual
            estado_actual = np.random.choice(
                self.n_estados,
                p=self.matriz_transicion[estado_actual]
            )

            estados.append(estado_actual)

        return estados

# ==========================================
# MATRIZ DE TRANSICION
# ==========================================
# ejemplo con 3 estados:
#
# estado 0:
#   10% quedarse en 0
#   60% ir a 1
#   30% ir a 2
#
# estado 1:
#   40% ir a 0
#   40% quedarse en 1
#   20% ir a 2
#
# estado 2:
#   30% ir a 0
#   30% ir a 1
#   40% quedarse en 2

matriz_transicion = np.array([
    [0.1, 0.6, 0.3],
    [0.4, 0.4, 0.2],
    [0.3, 0.3, 0.4]
])

# ==========================================
# CREACION DEL MODELO
# ==========================================

markov = ProcesoDeMarkov(matriz_transicion)

# ==========================================
# SIMULACION
# ==========================================

estado_inicial = 0
n_pasos = 100

secuencia_estados = markov.simular(
    estado_inicial,
    n_pasos
)

# ==========================================
# MOSTRAR RESULTADOS
# ==========================================

print("Secuencia generada de estados:\n")
print(secuencia_estados)

# ==========================================
# VISUALIZACION
# ==========================================

plt.figure(figsize=(12, 5))

plt.plot(
    secuencia_estados,
    marker='o',
    linestyle='-',
    color='purple'
)

plt.title("Simulación de un Proceso de Markov")
plt.xlabel("Paso de tiempo")
plt.ylabel("Estado")

plt.yticks([0, 1, 2])

plt.grid(True)

plt.show()

# - un proceso de Markov solo depende del estado actual
#   para decidir el siguiente estado
#
# - la matriz de transicion define todas las probabilidades
#
# - cada simulacion puede generar resultados diferentes
#   porque el proceso es aleatorio