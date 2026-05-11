# simulador simple de sensores en una casa inteligente
# este ejemplo usa una pequeña red neuronal SIN entrenamiento
# solamente hace propagacion hacia adelante.
#
# entradas:
# [temperatura_alta, movimiento_detectado, luz_apagada]
#
# la red calcula:
# - activacion de capa intermedia
# - salida final
#
# idea:
# decidir si se debe activar la alarma inteligente.

import numpy as np

# funcion de activacion softplus
def softplus(x):
    return np.log(1 + np.exp(x))

# derivada softplus
def derivada_softplus(x):
    return 1 / (1 + np.exp(-x))


# clase de nodo
class Nodo:

    def __init__(self, entradas):

        # pesos aleatorios
        self.pesos = np.random.uniform(-1, 1, entradas)

        # bias aleatorio
        self.bias = np.random.uniform(-1, 1)

    def calcular(self, datos):

        suma = np.dot(datos, self.pesos) + self.bias

        return softplus(suma)


# capa de nodos
class Bloque:

    def __init__(self, cantidad_nodos, entradas_por_nodo):

        self.nodos = []

        for _ in range(cantidad_nodos):

            self.nodos.append(
                Nodo(entradas_por_nodo)
            )

    def procesar(self, datos):

        resultados = []

        for nodo in self.nodos:

            resultados.append(
                nodo.calcular(datos)
            )

        return np.array(resultados)


if __name__ == "__main__":

    # dataset:
    #
    # [temperatura_alta, movimiento, oscuridad]
    #
    # 1 = si
    # 0 = no

    entradas = np.array([
        [1, 1, 1],
        [0, 1, 1],
        [1, 0, 0],
        [0, 0, 1]
    ])

    # capa intermedia
    capa_intermedia = Bloque(
        cantidad_nodos=3,
        entradas_por_nodo=3
    )

    # capa final
    capa_final = Bloque(
        cantidad_nodos=1,
        entradas_por_nodo=3
    )

    print("simulacion de propagacion:\n")

    for dato in entradas:

        # salida capa intermedia
        salida_intermedia = capa_intermedia.procesar(dato)

        # salida final
        salida_final = capa_final.procesar(salida_intermedia)

        print("entrada:", dato)
        print(" salida intermedia:", salida_intermedia)
        print(" salida final:", salida_final)

        # interpretacion simple
        if salida_final[0] > 1.0:
            print(" decision: activar alarma\n")
        else:
            print(" decision: no activar alarma\n")

    # este ejemplo solo calcula salidas
    # no hay entrenamiento ni ajuste de pesos
    # solamente propagacion hacia adelante