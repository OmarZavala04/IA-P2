# Este código genera un proceso estacionario de ruido blanco,
# calcula estadísticas básicas y visualiza la señal en el tiempo.

import numpy as np
import matplotlib.pyplot as plt

# =========================
# PARÁMETROS DEL PROCESO
# =========================

n_muestras = 1000          # cantidad de datos
media = 0                  # media teorica
desviacion_estandar = 1    # desviacion estandar teorica

# =========================
# GENERACIÓN DEL RUIDO BLANCO
# =========================

# np.random.normal(media, desviacion, cantidad)
# genera numeros aleatorios siguiendo una distribucion normal
ruido_blanco = np.random.normal(
    media,
    desviacion_estandar,
    n_muestras
)

# =========================
# VISUALIZACIÓN
# =========================

plt.figure(figsize=(12, 5))

plt.plot(
    ruido_blanco,
    color='blue',
    alpha=0.7,
    label='Ruido Blanco'
)

plt.title('Proceso Estacionario - Ruido Blanco')
plt.xlabel('Tiempo')
plt.ylabel('Valor')
plt.grid(True)
plt.legend()

plt.show()

# =========================
# ESTADÍSTICAS
# =========================

media_calculada = np.mean(ruido_blanco)
varianza_calculada = np.var(ruido_blanco)
desviacion_calculada = np.std(ruido_blanco)

# =========================
# RESULTADOS
# =========================

print("=== estadisticas del proceso ===\n")

print("media teorica               =", media)
print("media calculada             =", round(media_calculada, 4))

print("\nvarianza calculada          =", round(varianza_calculada, 4))

print("\ndesviacion estandar teorica =", desviacion_estandar)
print("desviacion calculada        =", round(desviacion_calculada, 4))

# =========================
# INTERPRETACIÓN
# =========================

print("\ninterpretacion:")
print("- el ruido blanco cambia aleatoriamente en cada instante")
print("- un proceso estacionario mantiene propiedades estadisticas similares en el tiempo")
print("- la media suele estar cerca de 0")
print("- la varianza mide que tanto se dispersan los datos")