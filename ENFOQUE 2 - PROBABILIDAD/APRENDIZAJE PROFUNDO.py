# perceptron multicapa para recomendar peliculas
# este ejemplo usa una red neuronal sencilla con:
# - capa de entrada
# - capa oculta
# - capa de salida
# aprende si a una persona probablemente le gustara una pelicula
# segun:
# [accion, romance, duracion_larga]

import numpy as np

# funcion leaky relu
def leaky_relu(x):
    return np.where(x > 0, x, x * 0.01)

# derivada de leaky relu
def derivada_leaky_relu(x):
    return np.where(x > 0, 1, 0.01)

# funcion sigmoide
def sigmoide(x):
    return 1 / (1 + np.exp(-x))

# derivada de sigmoide
def derivada_sigmoide(x):
    return x * (1 - x)

class RedPeliculas:

    def __init__(self, entradas, ocultas, salidas):

        # pesos entrada -> oculta
        self.w1 = np.random.randn(entradas, ocultas) * 0.1

        # bias oculta
        self.b1 = np.zeros((1, ocultas))

        # pesos oculta -> salida
        self.w2 = np.random.randn(ocultas, salidas) * 0.1

        # bias salida
        self.b2 = np.zeros((1, salidas))

    def forward(self, X):

        # capa oculta
        self.z1 = np.dot(X, self.w1) + self.b1
        self.a1 = leaky_relu(self.z1)

        # capa salida
        self.z2 = np.dot(self.a1, self.w2) + self.b2
        self.salida = sigmoide(self.z2)

        return self.salida

    def backward(self, X, y, salida, lr):

        # error salida
        error_salida = y - salida

        # delta salida
        delta_salida = error_salida * derivada_sigmoide(salida)

        # error capa oculta
        error_oculta = delta_salida.dot(self.w2.T)

        # delta capa oculta
        delta_oculta = error_oculta * derivada_leaky_relu(self.z1)

        # actualizar pesos salida
        self.w2 += self.a1.T.dot(delta_salida) * lr
        self.b2 += np.sum(delta_salida, axis=0, keepdims=True) * lr

        # actualizar pesos entrada
        self.w1 += X.T.dot(delta_oculta) * lr
        self.b1 += np.sum(delta_oculta, axis=0, keepdims=True) * lr

    def entrenar(self, X, y, epochs, lr):

        for epoca in range(epochs):

            salida = self.forward(X)

            self.backward(X, y, salida, lr)

            # mostrar error cada cierto tiempo
            if epoca % 200 == 0:

                loss = np.mean((y - salida) ** 2)

                print("epoca", epoca, "- error:", round(loss, 5))

    def predecir(self, X):

        salida = self.forward(X)

        # convertir a 0 o 1
        return np.where(salida >= 0.5, 1, 0)


if __name__ == "__main__":

    # dataset:
    # [accion, romance, larga]
    #
    # ejemplo:
    # [1,0,1] = pelicula de accion, no romance, larga
    #
    # salida:
    # 1 = le gusta
    # 0 = no le gusta

    X = np.array([
        [1, 0, 1],
        [1, 0, 0],
        [0, 1, 1],
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]
    ])

    y = np.array([
        [1],
        [1],
        [0],
        [0],
        [1],
        [0]
    ])

    # crear red
    red = RedPeliculas(
        entradas=3,
        ocultas=5,
        salidas=1
    )

    # entrenar
    red.entrenar(
        X,
        y,
        epochs=2000,
        lr=0.05
    )

    # probar
    print("\npredicciones finales:")

    predicciones = red.forward(X)

    for i in range(len(X)):

        print(
            "entrada:",
            X[i],
            "-> prob gustar:",
            round(float(predicciones[i][0]), 4)
        )

    # prueba nueva
    nueva = np.array([[1, 1, 0]])

    resultado = red.predecir(nueva)

    print("\nprueba nueva pelicula:", nueva[0])

    if resultado[0][0] == 1:
        print("prediccion: probablemente SI le guste")
    else:
        print("prediccion: probablemente NO le guste")

    # idea:
    # la red aprende patrones ajustando pesos
    # durante el entrenamiento
    # usando propagacion hacia adelante y retropropagacion