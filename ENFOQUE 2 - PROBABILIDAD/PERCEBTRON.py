# Este código implementa un perceptrón simple para clasificar
# dos clases en un conjunto de datos 2D.
# Además:
# - calcula precisión
# - muestra pérdidas
# - grafica la frontera de decisión

import numpy as np
import matplotlib.pyplot as plt

# ======================= GENERACIÓN DE DATOS =======================

np.random.seed(0)

n_samples = 100

# Datos aleatorios 2D
X = np.random.randn(n_samples, 2)

# Regla de clasificación:
# clase 1 si x1 + x2 > 0
# clase 0 en otro caso
Y = np.array([
    1 if x[0] + x[1] > 0 else 0
    for x in X
])

# ======================= SESGO =======================

# Agregar columna de 1s para bias
X_biased = np.c_[
    np.ones((X.shape[0], 1)),
    X
]

# ======================= PARÁMETROS =======================

learning_rate = 0.1
n_iterations = 100

# Pesos aleatorios iniciales
weights = np.random.randn(X_biased.shape[1])

# Guardar errores por época
errores_por_epoca = []

# ======================= FUNCIONES =======================

def step_function(x):
    """
    Función escalón
    """
    return 1 if x >= 0 else 0


def predict(x):
    """
    Predicción de una muestra
    """
    salida_lineal = np.dot(x, weights)
    return step_function(salida_lineal)


# ======================= ENTRENAMIENTO =======================

for epoch in range(n_iterations):

    errores = 0

    for i in range(n_samples):

        # salida lineal
        linear_output = np.dot(
            X_biased[i],
            weights
        )

        # predicción
        predicted = step_function(linear_output)

        # error
        error = Y[i] - predicted

        if error != 0:
            errores += 1

        # actualización de pesos
        update = learning_rate * error

        weights += update * X_biased[i]

    errores_por_epoca.append(errores)

    # mostrar progreso
    if epoch % 10 == 0:
        print(
            f"Epoch {epoch} | "
            f"Errores: {errores}"
        )

# ======================= EVALUACIÓN =======================

predicciones = []

for x in X_biased:
    predicciones.append(predict(x))

predicciones = np.array(predicciones)

precision = np.mean(predicciones == Y)

print("\nPrecisión final:", round(precision, 4))

print("\nPesos aprendidos:")
print(weights)

# ======================= VISUALIZACIÓN =======================

plt.figure(figsize=(10, 7))

# Clase 0
plt.scatter(
    X[Y == 0][:, 0],
    X[Y == 0][:, 1],
    color='red',
    label='Clase 0'
)

# Clase 1
plt.scatter(
    X[Y == 1][:, 0],
    X[Y == 1][:, 1],
    color='blue',
    label='Clase 1'
)

# ======================= FRONTERA DE DECISIÓN =======================

x_values = np.linspace(-3, 3, 200)

# ecuación:
# w0 + w1*x + w2*y = 0
# despejando y:
# y = -(w0 + w1*x) / w2

y_values = -(
    weights[0] +
    weights[1] * x_values
) / weights[2]

plt.plot(
    x_values,
    y_values,
    color='green',
    linewidth=2,
    label='Línea de Decisión'
)

# ======================= CONFIGURACIÓN =======================

plt.title("Perceptrón - Clasificación Binaria")

plt.xlabel("Característica 1")

plt.ylabel("Característica 2")

plt.legend()

plt.grid(True)

plt.show()

# ======================= ERROR DURANTE ENTRENAMIENTO =======================

plt.figure(figsize=(8, 5))

plt.plot(
    errores_por_epoca,
    marker='o'
)

plt.title("Errores por Época")

plt.xlabel("Época")

plt.ylabel("Cantidad de errores")

plt.grid(True)

plt.show()