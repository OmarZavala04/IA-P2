# Agrupamiento de canciones por energia y ritmo
# este ejemplo usa K-means para agrupar canciones
# automaticamente segun sus caracteristicas.
#
# la idea:
# cada cancion tiene:
# - energia
# - ritmo
#
# el algoritmo intentara encontrar grupos similares
# sin que nosotros le digamos cuales canciones pertenecen a cada grupo.
#
# esto es aprendizaje NO supervisado.


import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans


# =========================================================
# 1. GENERAR DATOS SINTETICOS
# =========================================================

# semilla para reproducibilidad
np.random.seed(7)

# grupo 1 -> musica tranquila
tranquila = np.random.normal(
    loc=[2, 3],
    scale=[0.5, 0.5],
    size=(80, 2)
)

# grupo 2 -> musica energetica
energetica = np.random.normal(
    loc=[8, 8],
    scale=[0.7, 0.7],
    size=(80, 2)
)

# grupo 3 -> musica intermedia
intermedia = np.random.normal(
    loc=[5, 6],
    scale=[0.6, 0.6],
    size=(80, 2)
)

# unimos todos los datos
X = np.vstack([
    tranquila,
    energetica,
    intermedia
])


# =========================================================
# 2. VISUALIZAR DATOS ORIGINALES
# =========================================================

plt.figure(figsize=(7, 5))

plt.scatter(
    X[:, 0],
    X[:, 1],
    color="gray",
    alpha=0.6
)

plt.title("Canciones Antes del Agrupamiento")

plt.xlabel("Energia")
plt.ylabel("Ritmo")

plt.grid(True)

plt.show()


# =========================================================
# 3. ENTRENAR K-MEANS
# =========================================================

numero_clusters = 3

modelo = KMeans(
    n_clusters=numero_clusters,
    random_state=7
)

modelo.fit(X)

# etiquetas de cluster
clusters = modelo.labels_

# centros encontrados
centros = modelo.cluster_centers_


# =========================================================
# 4. VISUALIZAR RESULTADOS
# =========================================================

plt.figure(figsize=(7, 5))

plt.scatter(
    X[:, 0],
    X[:, 1],
    c=clusters,
    cmap="plasma",
    alpha=0.7
)

# dibujar centros
plt.scatter(
    centros[:, 0],
    centros[:, 1],
    color="black",
    marker="X",
    s=250,
    label="Centros"
)

plt.title("Agrupamiento de Canciones con K-means")

plt.xlabel("Energia")
plt.ylabel("Ritmo")

plt.legend()

plt.grid(True)

plt.show()


# =========================================================
# 5. MOSTRAR CENTROS
# =========================================================

print("centros encontrados:\n")

for i, centro in enumerate(centros):

    print(
        "cluster", i,
        "-> energia:",
        round(centro[0], 2),
        "| ritmo:",
        round(centro[1], 2)
    )


# resumen:
# - k-means agrupa datos similares automaticamente
# - no necesita etiquetas reales
# - encuentra centros de grupos
# - cada punto pertenece al cluster mas cercano
# - aqui agrupamos canciones segun energia y ritmo