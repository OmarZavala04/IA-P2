# Algoritmo EM (Expectation Maximization)
# ejemplo:
# clasificacion de clientes en una cafeteria.
#
# cada cliente tiene:
# - tiempo_promedio_en_tienda
# - dinero_gastado
#
# queremos descubrir automaticamente tipos de clientes:
# - clientes rapidos
# - clientes tranquilos
# - clientes premium
#
# usamos una mezcla de gaussianas
# y el algoritmo EM para aprender:
# - centros de grupos
# - dispersion
# - porcentaje de clientes por grupo
#
# EM funciona asi:
#
# E-step:
#   calculamos que tan probable es que cada cliente
#   pertenezca a cada grupo.
#
# M-step:
#   actualizamos parametros de los grupos usando esas probabilidades.
#
# repetimos varias veces.


import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs


# =========================================================
# 1. GENERAR DATOS SINTETICOS
# =========================================================

np.random.seed(10)

X, _ = make_blobs(
    n_samples=450,
    centers=3,
    cluster_std=1.0,
    random_state=10
)

# visualizacion inicial
plt.figure(figsize=(7, 5))

plt.scatter(
    X[:, 0],
    X[:, 1],
    alpha=0.6
)

plt.title("Clientes Generados")

plt.xlabel("Tiempo en Tienda")
plt.ylabel("Dinero Gastado")

plt.grid(True)

plt.show()


# =========================================================
# 2. INICIALIZAR PARAMETROS
# =========================================================

def inicializar_modelo(X, numero_grupos):

    cantidad_datos, dimensiones = X.shape

    # medias aleatorias
    medias = X[
        np.random.choice(
            cantidad_datos,
            numero_grupos,
            replace=False
        )
    ]

    # covarianzas iniciales
    covarianzas = np.array([
        np.eye(dimensiones)
        for _ in range(numero_grupos)
    ])

    # pesos iniciales iguales
    pesos = np.ones(numero_grupos) / numero_grupos

    return medias, covarianzas, pesos


# =========================================================
# 3. FUNCION GAUSSIANA MULTIVARIADA
# =========================================================

def gaussiana_multivariable(X, media, cov):

    dimensiones = len(media)

    inversa = np.linalg.inv(cov)

    diferencia = X - media

    exponente = np.einsum(
        "ij,jk,ik->i",
        diferencia,
        inversa,
        diferencia
    )

    denominador = np.sqrt(
        ((2 * np.pi) ** dimensiones)
        * np.linalg.det(cov)
    )

    return np.exp(-0.5 * exponente) / denominador


# =========================================================
# 4. ALGORITMO EM
# =========================================================

def entrenar_em(X, numero_grupos, iteraciones=40):

    cantidad_datos, dimensiones = X.shape

    medias, covarianzas, pesos = inicializar_modelo(
        X,
        numero_grupos
    )

    for paso in range(iteraciones):

        # =================================================
        # E-STEP
        # =================================================
        responsabilidades = np.zeros(
            (cantidad_datos, numero_grupos)
        )

        for grupo in range(numero_grupos):

            responsabilidades[:, grupo] = (
                pesos[grupo]
                * gaussiana_multivariable(
                    X,
                    medias[grupo],
                    covarianzas[grupo]
                )
            )

        # normalizar probabilidades
        suma = responsabilidades.sum(axis=1)[:, np.newaxis]

        suma[suma == 0] = 1e-10

        responsabilidades /= suma


        # =================================================
        # M-STEP
        # =================================================

        N_k = responsabilidades.sum(axis=0)

        for grupo in range(numero_grupos):

            # actualizar media
            medias[grupo] = (
                responsabilidades[:, grupo][:, np.newaxis]
                * X
            ).sum(axis=0) / N_k[grupo]

            # actualizar covarianza
            diferencia = X - medias[grupo]

            covarianzas[grupo] = np.dot(
                (responsabilidades[:, grupo][:, np.newaxis]
                 * diferencia).T,
                diferencia
            ) / N_k[grupo]

            # evitar problemas numericos
            covarianzas[grupo] += np.eye(dimensiones) * 1e-6

        # actualizar pesos
        pesos = N_k / cantidad_datos

    return medias, covarianzas, pesos, responsabilidades


# =========================================================
# 5. ENTRENAR MODELO
# =========================================================

numero_grupos = 3

medias, covarianzas, pesos, responsabilidades = entrenar_em(
    X,
    numero_grupos
)

# cluster final = grupo con mayor responsabilidad
clusters = np.argmax(
    responsabilidades,
    axis=1
)


# =========================================================
# 6. VISUALIZAR RESULTADOS
# =========================================================

plt.figure(figsize=(7, 5))

plt.scatter(
    X[:, 0],
    X[:, 1],
    c=clusters,
    cmap="coolwarm",
    alpha=0.7
)

# dibujar medias
plt.scatter(
    medias[:, 0],
    medias[:, 1],
    color="black",
    marker="X",
    s=250,
    label="Centros EM"
)

plt.title("Agrupamiento usando EM")

plt.xlabel("Tiempo en Tienda")
plt.ylabel("Dinero Gastado")

plt.legend()

plt.grid(True)

plt.show()


# =========================================================
# 7. MOSTRAR RESULTADOS
# =========================================================

print("\nCENTROS APRENDIDOS:\n")

for i, media in enumerate(medias):

    print(
        "grupo", i,
        "->",
        np.round(media, 2)
    )

print("\nPESOS DE CADA GRUPO:\n")

for i, peso in enumerate(pesos):

    print(
        "grupo", i,
        "->",
        round(peso, 3)
    )

print("\nCOVARIANZAS:\n")

for i, cov in enumerate(covarianzas):

    print("\ngrupo", i)
    print(np.round(cov, 2))


# resumen:
# - EM aprende grupos probabilisticos
# - cada punto puede pertenecer parcialmente a varios grupos
# - E-step calcula responsabilidades
# - M-step actualiza parametros
# - esto se usa mucho en clustering probabilistico