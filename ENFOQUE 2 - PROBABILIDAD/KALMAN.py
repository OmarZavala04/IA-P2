# Sistema de seguimiento de bateria en un vehiculo electrico
# Este programa usa un filtro de Kalman sencillo
# para estimar el nivel real de bateria
# a partir de sensores con ruido.
#
# cambiamos totalmente la tematica:
# ahora no seguimos posicion de objetos,
# sino carga de bateria.

import numpy as np

# tiempo entre lecturas
delta_t = 1.0

# modelo del sistema
# estado = [nivel_bateria, consumo]
F = np.array([
    [1, delta_t],
    [0, 1]
])

# solo observamos el nivel de bateria
M = np.array([
    [1, 0]
])

# ruido interno del sistema
ruido_modelo = np.array([
    [0.005, 0],
    [0, 0.005]
])

# ruido del sensor
ruido_sensor = np.array([
    [0.2]
])

# estado inicial:
# bateria = 100%
# consumo = -1% por ciclo
estado = np.array([
    [100],
    [-1]
])

# incertidumbre inicial
covarianza = np.eye(2)

def estimar_bateria(lectura_sensor):
    """
    aplica filtro de Kalman para estimar
    el nivel real de bateria
    """

    global estado, covarianza

    # =========================
    # prediccion
    # =========================
    estado = F @ estado

    covarianza = (
        F @ covarianza @ F.T
        + ruido_modelo
    )

    # =========================
    # correccion usando sensor
    # =========================

    error_medicion = lectura_sensor - (M @ estado)

    incertidumbre = (
        M @ covarianza @ M.T
        + ruido_sensor
    )

    ganancia = (
        covarianza @ M.T
        @ np.linalg.inv(incertidumbre)
    )

    # actualizamos estado
    estado = estado + ganancia @ error_medicion

    # actualizamos covarianza
    identidad = np.eye(2)

    covarianza = (
        identidad - ganancia @ M
    ) @ covarianza

    # regresamos nivel estimado de bateria
    return estado[0, 0]


# simulacion de sensores ruidosos
lecturas = [
    99, 97, 96, 94,
    92, 91, 89, 87,
    86, 84
]

estimaciones = []

print("estimaciones del nivel de bateria:\n")

for lectura in lecturas:

    valor_estimado = estimar_bateria(
        np.array([[lectura]])
    )

    estimaciones.append(valor_estimado)

    print(
        "sensor:",
        lectura,
        "% -> bateria estimada:",
        round(valor_estimado, 2),
        "%"
    )

# resumen final
print("\nultima estimacion del sistema:")
print(round(estimaciones[-1], 2), "%")

# este tipo de filtros se usa en:
# - autos electricos
# - drones
# - robots autonomos
# - sistemas de navegacion
# porque ayudan a reducir ruido en sensores