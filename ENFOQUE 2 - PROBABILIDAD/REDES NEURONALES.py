# Este código implementa una red neuronal multicapa (MLP) para clasificación
# en un conjunto de datos sintético "moons", mostrando la evolución de pérdida y precisión.

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers

# =========================
# GENERACION DE DATOS
# =========================

X, y = make_moons(n_samples=1000, noise=0.1, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# normalizar ayuda a la red a aprender mas estable
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# =========================
# MODELO MLP
# =========================

model = keras.Sequential([
    layers.Dense(8, activation='relu', input_shape=(2,)),
    layers.Dense(4, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# =========================
# ENTRENAMIENTO
# =========================

history = model.fit(
    X_train,
    y_train,
    epochs=100,
    batch_size=10,
    validation_split=0.2,
    verbose=0  # menos ruido en consola
)

# =========================
# EVALUACION
# =========================

loss, accuracy = model.evaluate(X_test, y_test, verbose=0)

print(f'Precision del modelo en test: {accuracy:.2f}')

# =========================
# VISUALIZACION
# =========================

plt.figure(figsize=(12, 4))

# perdida
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='val')
plt.title('Pérdida durante entrenamiento')
plt.xlabel('Epocas')
plt.ylabel('Loss')
plt.legend()

# accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='train')
plt.plot(history.history['val_accuracy'], label='val')
plt.title('Precisión durante entrenamiento')
plt.xlabel('Epocas')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()