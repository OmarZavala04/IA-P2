# Simulador de trafico urbano
# Este programa genera autos en posiciones aleatorias
# dentro de una ciudad ficticia.
#
# cada punto representa un vehiculo:
# - posicion X/Y = ubicacion en la ciudad
# - color = nivel de congestion
# - tamaño = cantidad de pasajeros

import numpy as np
import matplotlib.pyplot as plt

# =========================
# GENERACION DE VEHICULOS
# =========================

np.random.seed(7)

cantidad_autos = 120

# posiciones en el mapa
pos_x = np.random.rand(cantidad_autos) * 50
pos_y = np.random.rand(cantidad_autos) * 50

# nivel de congestion de cada auto
# valores altos = trafico pesado
congestion = np.random.rand(cantidad_autos)

# cantidad de pasajeros
pasajeros = (np.random.rand(cantidad_autos) * 300) + 20

# =========================
# VISUALIZACION
# =========================

plt.figure(figsize=(11, 7))

grafica = plt.scatter(
    pos_x,
    pos_y,
    c=congestion,
    s=pasajeros,
    alpha=0.6,
    cmap="plasma"
)

# detalles del mapa
plt.title("Mapa de Trafico Urbano Inteligente")
plt.xlabel("Zona Este/Oeste")
plt.ylabel("Zona Norte/Sur")

plt.grid(True)

# barra lateral de colores
barra = plt.colorbar(grafica)
barra.set_label("Nivel de Congestion")

plt.show()

# =========================
# DATOS EXTRA
# =========================

print("cantidad de vehiculos analizados:")
print(cantidad_autos)

print("\npromedio de congestion:")
print(round(np.mean(congestion), 2))

print("\npromedio de pasajeros por vehiculo:")
print(round(np.mean(pasajeros), 2))

# este tipo de visualizacion se parece
# a sistemas usados en:
# - monitoreo de trafico
# - ciudades inteligentes
# - simulaciones urbanas
# - mapas de movilidad