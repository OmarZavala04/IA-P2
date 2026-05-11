import numpy as np
import matplotlib.pyplot as plt

# =========================
# GENERACION DE DATOS
# =========================

np.random.seed(0)

n_samples = 100

# clase 1 centrada en (1,1)
X1 = np.random.randn(n_samples, 2) + np.array([1, 1])

# clase 0 centrada en (-1,-1)
X2 = np.random.randn(n_samples, 2) + np.array([-1, -1])

X = np.vstack((X1, X2))
Y = np.array([1] * n_samples + [0] * n_samples)

# =========================
# PREPROCESAMIENTO (BIAS)
# =========================

X_biased = np.c_[np.ones((X.shape[0], 1)), X]

# =========================
# PERCEPTRON
# =========================

learning_rate = 0.1
n_iterations = 1000

weights = np.random.randn(X_biased.shape[1])

def step_function(x):
    return 1 if x >= 0 else 0

# =========================
# ENTRENAMIENTO
# =========================

for _ in range(n_iterations):
    for i in range(len(Y)):

        linear_output = np.dot(X_biased[i], weights)
        predicted = step_function(linear_output)

        error = Y[i] - predicted

        # ajuste de pesos
        weights += learning_rate * error * X_biased[i]

# =========================
# VISUALIZACION
# =========================

plt.figure(figsize=(8, 6))

plt.scatter(X[Y == 0][:, 0], X[Y == 0][:, 1], color='red', label='Clase 0')
plt.scatter(X[Y == 1][:, 0], X[Y == 1][:, 1], color='blue', label='Clase 1')

# linea de decision
x_values = np.linspace(-3, 3, 100)
y_values = -(weights[0] + weights[1] * x_values) / weights[2]

plt.plot(x_values, y_values, color='green', label='Línea de decisión')

plt.title('Perceptrón: separabilidad lineal')
plt.xlabel('x1')
plt.ylabel('x2')

plt.xlim(-3, 3)
plt.ylim(-3, 3)

plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
plt.axvline(0, color='black', linestyle='--', linewidth=0.5)

plt.legend()
plt.grid(True)

plt.show()

"""
idea clave:
- el perceptrón busca una frontera lineal
- solo funciona si los datos son separables linealmente
- si no lo son, falla (no converge bien)

esto es el primer escalón histórico hacia redes neuronales modernas
"""