# Seguimiento de temperatura en un invernadero
# Este programa simula sensores con ruido y aplica
# una estimacion suavizada para calcular la temperatura real.
#
# la idea es cambiar completamente la tematica:
# ahora en vez de "estado dinamico abstracto",
# tenemos un sistema de monitoreo agricola.

import numpy as np
import matplotlib.pyplot as plt

# cantidad de mediciones
n_mediciones = 60

# arreglos para guardar datos
temperatura_real = np.zeros(n_mediciones)
lecturas_sensor = np.zeros(n_mediciones)
temperatura_estimacion = np.zeros(n_mediciones)

# parametros del sistema
variacion_clima = 0.4      # cambios reales del ambiente
ruido_sensor = 1.2         # error del sensor

# valores iniciales
temperatura_real[0] = 22
estimacion_actual = 22
error_estimacion = 1.0

# simulacion
for t in range(1, n_mediciones):

    # temperatura real cambia poco a poco
    cambio = np.random.normal(0, variacion_clima)
    temperatura_real[t] = temperatura_real[t - 1] + cambio

    # sensor mide con ruido
    lectura = temperatura_real[t] + np.random.normal(0, ruido_sensor)
    lecturas_sensor[t] = lectura

    # calculo de confianza (ganancia)
    confianza = error_estimacion / (error_estimacion + ruido_sensor)

    # corregimos la estimacion usando la lectura del sensor
    estimacion_actual = estimacion_actual + confianza * (
        lectura - estimacion_actual
    )

    temperatura_estimacion[t] = estimacion_actual

    # actualizamos error estimado
    error_estimacion = (1 - confianza) * error_estimacion + variacion_clima

# graficas
plt.figure(figsize=(10, 5))

plt.plot(
    temperatura_real,
    label="temperatura real"
)

plt.plot(
    lecturas_sensor,
    linestyle="dashed",
    label="sensor con ruido"
)

plt.plot(
    temperatura_estimacion,
    linewidth=2,
    label="temperatura estimada"
)

plt.title("Monitoreo Inteligente de Temperatura")
plt.xlabel("Tiempo")
plt.ylabel("Temperatura °C")
plt.legend()
plt.grid(True)

plt.show()

# resultados numericos finales
print("ultima temperatura real:")
print(round(temperatura_real[-1], 2), "°C")

print("\nultima lectura del sensor:")
print(round(lecturas_sensor[-1], 2), "°C")

print("\nestimacion final del sistema:")
print(round(temperatura_estimacion[-1], 2), "°C")

# este ejemplo representa una idea parecida
# a filtros usados en robots, drones,
# estaciones meteorologicas y sensores industriales