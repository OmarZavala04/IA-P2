# Este código implementa un clasificador SVM usando kernel RBF
# sobre un conjunto de datos sintético en forma de media luna.
# Además muestra la frontera de decisión del modelo.

import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# ======================= GENERACIÓN DE DATOS =======================

# Generamos datos tipo "moons"
X, y = make_moons(
    n_samples=300,
    noise=0.2,
    random_state=42
)

# División entrenamiento / prueba
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ======================= MODELO SVM =======================

# Kernel RBF = Radial Basis Function
svm_model = SVC(
    kernel='rbf',
    gamma='scale',
    C=1.0
)

# Entrenamiento
svm_model.fit(X_train, y_train)

# Predicciones
predicciones = svm_model.predict(X_test)

# ======================= EVALUACIÓN =======================

accuracy = svm_model.score(X_test, y_test)

print("Precisión del modelo:", round(accuracy, 4))

print("\nMatriz de confusión:")
print(confusion_matrix(y_test, predicciones))

print("\nReporte de clasificación:")
print(classification_report(y_test, predicciones))

# ======================= VISUALIZACIÓN =======================

# Crear malla para frontera de decisión
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1

xx, yy = np.meshgrid(
    np.linspace(x_min, x_max, 500),
    np.linspace(y_min, y_max, 500)
)

# Predicción sobre toda la malla
Z = svm_model.predict(
    np.c_[xx.ravel(), yy.ravel()]
)

Z = Z.reshape(xx.shape)

# ======================= GRÁFICA =======================

plt.figure(figsize=(10, 7))

# Frontera de decisión
plt.contourf(
    xx,
    yy,
    Z,
    alpha=0.3,
    cmap='viridis'
)

# Datos de prueba
plt.scatter(
    X_test[:, 0],
    X_test[:, 1],
    c=predicciones,
    cmap='viridis',
    edgecolor='black',
    s=60,
    label='Datos de prueba'
)

# Datos de entrenamiento
plt.scatter(
    X_train[:, 0],
    X_train[:, 1],
    c=y_train,
    cmap='coolwarm',
    marker='x',
    alpha=0.5,
    label='Entrenamiento'
)

plt.title("Clasificación usando SVM con Kernel RBF")
plt.xlabel("Característica 1")
plt.ylabel("Característica 2")

plt.legend()
plt.grid(True)

plt.show()