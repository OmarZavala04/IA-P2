# Redes de Boltzmann
# una red de boltzmann es una red neuronal probabilistica
# usada para aprender patrones y distribuciones de datos.
#
# funciona con neuronas binarias:
# cada neurona puede estar en:
#   1  -> activa
#  -1  -> inactiva
#
# la red intenta encontrar estados de baja energia,
# parecida a una red de Hopfield,
# pero aqui las activaciones tienen aleatoriedad.
#
# la probabilidad de activacion depende de:
# - pesos entre neuronas
# - temperatura
# - energia total del sistema
#
# este ejemplo:
# - crea una red pequeña
# - inicializa pesos aleatorios
# - actualiza estados probabilisticamente
# - calcula energia de la red
# - muestra como evoluciona el sistema

import numpy as np
import random

class RedBoltzmann:
    def __init__(self, num_neuronas):
        """
        num_neuronas:
            cantidad de neuronas en la red
        """

        self.num_neuronas = num_neuronas

        # matriz de pesos aleatorios
        self.pesos = np.random.uniform(-1, 1, (num_neuronas, num_neuronas))

        # quitamos conexiones consigo misma
        np.fill_diagonal(self.pesos, 0)

        # hacemos simetrica la matriz
        # (w_ij = w_ji)
        self.pesos = (self.pesos + self.pesos.T) / 2

        # estado inicial aleatorio (-1 o 1)
        self.estado = np.random.choice([-1, 1], size=num_neuronas)

    def energia(self):
        """
        calcula la energia total de la red

        formula:
        E = -1/2 * sum(w_ij * s_i * s_j)
        """

        e = 0

        for i in range(self.num_neuronas):
            for j in range(self.num_neuronas):
                e += self.pesos[i][j] * self.estado[i] * self.estado[j]

        return -0.5 * e

    def probabilidad_activacion(self, i, temperatura):
        """
        calcula la probabilidad de que la neurona i
        se active usando funcion sigmoide

        temperatura:
            controla el azar
            alta temperatura -> mas aleatoriedad
            baja temperatura -> mas estable
        """

        suma = np.dot(self.pesos[i], self.estado)

        # funcion sigmoide
        p = 1 / (1 + np.exp(-2 * suma / temperatura))

        return p

    def actualizar_neurona(self, i, temperatura):
        """
        actualiza una neurona usando probabilidad
        """

        p = self.probabilidad_activacion(i, temperatura)

        # activacion probabilistica
        if random.random() < p:
            self.estado[i] = 1
        else:
            self.estado[i] = -1

    def ejecutar(self, pasos, temperatura):
        """
        ejecuta varias iteraciones de actualizacion
        """

        print("estado inicial:", self.estado)
        print("energia inicial:", round(self.energia(), 4))
        print()

        for paso in range(pasos):

            # elegimos neurona aleatoria
            i = random.randint(0, self.num_neuronas - 1)

            # actualizamos
            self.actualizar_neurona(i, temperatura)

            # mostramos estado actual
            print("paso", paso + 1)
            print("estado:", self.estado)
            print("energia:", round(self.energia(), 4))
            print()

# ============================
# programa principal
# ============================

if __name__ == "__main__":

    # crear red de boltzmann con 6 neuronas
    red = RedBoltzmann(num_neuronas=6)

    # ejecutar simulacion
    pasos = 15
    temperatura = 2.0

    red.ejecutar(
        pasos=pasos,
        temperatura=temperatura
    )

    # - la red cambia estados buscando configuraciones
    #   de menor energia
    #
    # - como hay aleatoriedad, a veces acepta estados peores
    #   temporalmente
    #
    # - esto ayuda a explorar diferentes configuraciones
    #   y evitar quedarse atrapada rapidamente