# Este código implementa una red neuronal simple de 2 capas para resolver XOR
# usando retropropagación del error (backpropagation)

import numpy as np

# =========================
# FUNCIONES DE ACTIVACION
# =========================

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# =========================
# DATOS XOR
# =========================

X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y = np.array([[0], [1], [1], [0]])

# =========================
# INICIALIZACION
# =========================

np.random.seed(42)

input_size = X.shape[1]
hidden_size = 2
output_size = y.shape[1]

weights_input_hidden = np.random.rand(input_size, hidden_size)
weights_hidden_output = np.random.rand(hidden_size, output_size)

learning_rate = 0.1

# =========================
# ENTRENAMIENTO
# =========================

for epoch in range(10000):

    # -------- forward --------
    hidden_input = np.dot(X, weights_input_hidden)
    hidden_output = sigmoid(hidden_input)

    output_input = np.dot(hidden_output, weights_hidden_output)
    predicted_output = sigmoid(output_input)

    # -------- error --------
    error = y - predicted_output

    # -------- backprop --------
    d_output = error * sigmoid_derivative(predicted_output)

    error_hidden = d_output.dot(weights_hidden_output.T)
    d_hidden = error_hidden * sigmoid_derivative(hidden_output)

    # -------- update --------
    weights_hidden_output += hidden_output.T.dot(d_output) * learning_rate
    weights_input_hidden += X.T.dot(d_hidden) * learning_rate


# =========================
# RESULTADO
# =========================

print("salidas finales de la red:")
print(np.round(predicted_output, 3))

"""
interpretacion:
la red aprende XOR, que NO es linealmente separable.

lo importante:
- una sola capa no puede resolver XOR
- la capa oculta crea una representación intermedia
- backprop ajusta pesos minimizando error

esto es base de deep learning:
forward -> error -> backward -> ajuste
"""