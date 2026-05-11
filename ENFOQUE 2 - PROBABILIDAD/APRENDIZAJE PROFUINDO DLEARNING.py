# red neuronal para clasificar frutas
# esta red aprende si una fruta probablemente es "manzana" o "naranja"
# usando:
# - peso
# - color
# - textura
#
# salida:
# 1 = manzana
# 0 = naranja

import numpy as np

# funcion tanh
def tanh(x):
    return np.tanh(x)

# derivada de tanh
def derivada_tanh(x):
    return 1 - np.tanh(x) ** 2

# funcion sigmoide
def sigmoide(x):
    return 1 / (1 + np.exp(-x))

# derivada sigmoide
def derivada_sigmoide(x):
    return x * (1 - x)


class ClasificadorFrutas:

    def __init__(self, entradas, ocultas, salidas):

        # pesos entrada -> oculta
        self.w1 = np.random.randn(entradas, ocultas) * 0.1

        # bias capa oculta
        self.b1 = np.zeros((1, ocultas))

        # pesos oculta -> salida
        self.w2 = np.random.randn(ocultas, salidas) * 0.1

        # bias salida
        self.b2 = np.zeros((1, salidas))

    def forward(self, X):

        # capa oculta
        self.z1 = np.dot(X, self.w1) + self.b1
        self.a1 = tanh(self.z1)

        # capa salida
        self.z2 = np.dot(self.a1, self.w2) + self.b2
        self.salida = sigmoide(self.z2)

        return self.salida

    def backward(self, X, y, salida, lr):

        # error salida
        error_salida = y - salida

        # delta salida
        delta_salida = error_salida * derivada_sigmoide(salida)

        # error oculto
        error_oculto = delta_salida.dot(self.w2.T)

        # delta oculto
        delta_oculto = error_oculto * derivada_tanh(self.z1)

        # actualizar pesos salida
        self.w2 += self.a1.T.dot(delta_salida) * lr
        self.b2 += np.sum(delta_salida, axis=0, keepdims=True) * lr

        # actualizar pesos entrada
        self.w1 += X.T.dot(delta_oculto) * lr
        self.b1 += np.sum(delta_oculto, axis=0, keepdims=True) * lr

    def entrenar(self, X, y, epocas, lr):

        for epoca in range(epocas):

            salida = self.forward(X)

            self.backward(X, y, salida, lr)

            # imprimir error
            if epoca % 200 == 0:

                loss = np.mean((y - salida) ** 2)

                print("epoca", epoca, "- error:", round(loss, 5))

    def clasificar(self, X):

        prob = self.forward(X)

        return np.where(prob >= 0.5, 1, 0)


if __name__ == "__main__":

    # dataset:
    #
    # [peso, color, textura]
    #
    # peso:
    # 0 = ligero
    # 1 = pesado
    #
    # color:
    # 0 = naranja
    # 1 = rojo
    #
    # textura:
    # 0 = lisa
    # 1 = rugosa

    X = np.array([
        [1, 1, 0],  # manzana
        [1, 1, 0],  # manzana
        [0, 0, 1],  # naranja
        [0, 0, 1],  # naranja
        [1, 1, 1],  # manzana rara
        [0, 0, 0]   # naranja lisa
    ])

    # 1 = manzana
    # 0 = naranja
    y = np.array([
        [1],
        [1],
        [0],
        [0],
        [1],
        [0]
    ])

    # crear red
    red = ClasificadorFrutas(
        entradas=3,
        ocultas=4,
        salidas=1
    )

    # entrenar
    red.entrenar(
        X,
        y,
        epocas=2000,
        lr=0.05
    )

    # predicciones
    print("\npredicciones finales:")

    resultados = red.forward(X)

    for i in range(len(X)):

        print(
            "entrada:",
            X[i],
            "-> probabilidad:",
            round(float(resultados[i][0]), 4)
        )

    # nueva fruta
    nueva_fruta = np.array([[1, 1, 0]])

    pred = red.clasificar(nueva_fruta)

    print("\nnueva fruta:", nueva_fruta[0])

    if pred[0][0] == 1:
        print("clasificacion: manzana")
    else:
        print("clasificacion: naranja")

    # la red aprende ajustando pesos
    # usando propagacion hacia adelante
    # y retropropagacion del error