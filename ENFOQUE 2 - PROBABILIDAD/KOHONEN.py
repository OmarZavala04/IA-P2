"""
mapa autoorganizado de kohonen (som)
un som (self-organizing map) aprende a agrupar datos parecidos
sin que le digamos etiquetas.

la idea:
- cada neurona del mapa tiene pesos
- llega un dato
- buscamos la neurona mas parecida (bmu = best matching unit)
- ajustamos esa neurona y sus vecinas para parecerse mas al dato

con muchas iteraciones:
- neuronas cercanas representan datos parecidos
- el mapa se "organiza solo"

esto es aprendizaje no supervisado.
"""

import numpy as np
import matplotlib.pyplot as plt


class SOM:
    def __init__(self, filas, columnas, dimension_entrada,
                 learning_rate=0.5, radio=2, epochs=100):

        """
        filas, columnas:
            tamaño del mapa 2d

        dimension_entrada:
            cantidad de valores de cada dato

        learning_rate:
            que tanto se ajustan los pesos

        radio:
            tamaño de vecindad

        epochs:
            cuantas veces entrenamos
        """

        self.filas = filas
        self.columnas = columnas
        self.dimension_entrada = dimension_entrada

        self.learning_rate_inicial = learning_rate
        self.radio_inicial = radio
        self.epochs = epochs

        # pesos aleatorios para cada neurona
        self.pesos = np.random.rand(
            filas,
            columnas,
            dimension_entrada
        )

    def distancia(self, a, b):
        """
        distancia euclidiana entre dos vectores
        """
        return np.linalg.norm(a - b)

    def encontrar_bmu(self, dato):
        """
        encuentra la neurona mas parecida al dato
        (best matching unit)
        """

        mejor_distancia = None
        mejor_pos = None

        for i in range(self.filas):
            for j in range(self.columnas):

                d = self.distancia(dato, self.pesos[i][j])

                if (mejor_distancia is None) or (d < mejor_distancia):
                    mejor_distancia = d
                    mejor_pos = (i, j)

        return mejor_pos

    def actualizar_pesos(self, dato, bmu, epoch):
        """
        ajusta los pesos de la neurona ganadora
        y sus vecinas
        """

        # learning rate decreciente
        lr = self.learning_rate_inicial * (1 - epoch / self.epochs)

        # radio decreciente
        radio_actual = self.radio_inicial * (1 - epoch / self.epochs)

        for i in range(self.filas):
            for j in range(self.columnas):

                # distancia de la neurona actual a la bmu
                dist_mapa = np.linalg.norm(
                    np.array([i, j]) - np.array(bmu)
                )

                # solo actualizamos vecinas cercanas
                if dist_mapa <= radio_actual:

                    # influencia segun distancia
                    influencia = np.exp(
                        -(dist_mapa ** 2) / (2 * (radio_actual ** 2 + 1e-5))
                    )

                    # regla de actualizacion
                    self.pesos[i][j] += (
                        influencia *
                        lr *
                        (dato - self.pesos[i][j])
                    )

    def entrenar(self, datos):
        """
        entrenamiento principal del som
        """

        for epoch in range(self.epochs):

            # mezclamos datos
            np.random.shuffle(datos)

            for dato in datos:

                # encontrar neurona ganadora
                bmu = self.encontrar_bmu(dato)

                # ajustar pesos
                self.actualizar_pesos(dato, bmu, epoch)

            # imprimir progreso
            if epoch % 10 == 0:
                print("epoch", epoch, "completada")

    def visualizar_mapa(self):
        """
        muestra el mapa aprendido
        usando colores
        """

        plt.figure(figsize=(8, 8))

        # si los datos son 3d o mas,
        # usamos solo las primeras 3 dimensiones como rgb
        if self.dimension_entrada >= 3:
            imagen = self.pesos[:, :, :3]
        else:
            # si son 2d agregamos una dimension falsa
            imagen = np.zeros((self.filas, self.columnas, 3))
            imagen[:, :, :self.dimension_entrada] = self.pesos

        plt.imshow(imagen)
        plt.title("mapa autoorganizado (som)")
        plt.axis("off")
        plt.show()


# ===========================
# ejemplo de uso
# ===========================

if __name__ == "__main__":

    # generamos datos artificiales
    # 3 grupos distintos

    grupo1 = np.random.normal(
        loc=[0.2, 0.2],
        scale=0.05,
        size=(100, 2)
    )

    grupo2 = np.random.normal(
        loc=[0.8, 0.3],
        scale=0.05,
        size=(100, 2)
    )

    grupo3 = np.random.normal(
        loc=[0.5, 0.8],
        scale=0.05,
        size=(100, 2)
    )

    datos = np.vstack([grupo1, grupo2, grupo3])

    # mostramos datos originales
    plt.scatter(datos[:, 0], datos[:, 1], alpha=0.6)
    plt.title("datos originales")
    plt.grid(True)
    plt.show()

    # crear som
    som = SOM(
        filas=10,
        columnas=10,
        dimension_entrada=2,
        learning_rate=0.5,
        radio=3,
        epochs=100
    )

    # entrenar
    som.entrenar(datos)

    # visualizar resultado
    som.visualizar_mapa()

    print("\nentrenamiento terminado")
    print("- neuronas cercanas representan datos parecidos")
    print("- el mapa se organizo solo segun los patrones")
    print("- esto es aprendizaje no supervisado")