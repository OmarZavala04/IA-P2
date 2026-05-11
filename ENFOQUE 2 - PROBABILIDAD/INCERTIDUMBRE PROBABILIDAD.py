# Distribución Binomial
# este programa calcula y grafica la probabilidad
# de obtener cierta cantidad de caras
# al lanzar una moneda varias veces.
#
# la distribucion binomial sirve cuando:
# - hay varios intentos
# - cada intento tiene solo 2 resultados posibles
#     exito / fracaso
#     cara / cruz
#     aprobado / reprobado
#
# en este caso:
# - exito = obtener cara
# - probabilidad de cara = 0.5
#
# la distribucion binomial responde:
# "¿que tan probable es obtener exactamente k caras
#  despues de n lanzamientos?"

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# ==========================================
# PARAMETROS DEL EXPERIMENTO
# ==========================================

n_lanzamientos = 10

# probabilidad de obtener cara
probabilidad_exito = 0.5

# posibles cantidades de caras:
# 0,1,2,...,10
x = np.arange(0, n_lanzamientos + 1)

# ==========================================
# CALCULO DE PROBABILIDADES
# ==========================================

# binom.pmf calcula:
# P(X = k)
#
# es decir:
# probabilidad de obtener exactamente k exitos

probabilidades = binom.pmf(
    x,
    n_lanzamientos,
    probabilidad_exito
)

# ==========================================
# MOSTRAR RESULTADOS
# ==========================================

print("Distribucion Binomial\n")

for caras, prob in zip(x, probabilidades):

    print(
        "caras:",
        caras,
        "-> probabilidad:",
        round(prob, 4)
    )

# ==========================================
# GRAFICA
# ==========================================

plt.figure(figsize=(10, 6))

# grafica de tallos
plt.stem(
    x,
    probabilidades,
    basefmt=" "
)

plt.xlabel("Numero de caras")
plt.ylabel("Probabilidad")

plt.title(
    "Distribucion Binomial\n"
    "Probabilidad de obtener k caras"
)

plt.grid(True)

plt.show()

# ==========================================
# INTERPRETACION
# ==========================================

print("\ninterpretacion:")
print("- el valor mas probable suele estar cerca de la mitad")
print("- obtener exactamente 5 caras es muy comun")
print("- obtener 0 o 10 caras es mucho menos probable")
print("- la distribucion binomial modela eventos repetidos")
print("  con probabilidades constantes")

# conceptos importantes:
#
# n:
#   numero de intentos
#
# p:
#   probabilidad de exito
#
# k:
#   cantidad de exitos
#
# binom.pmf:
#   probability mass function
#   calcula P(X = k)