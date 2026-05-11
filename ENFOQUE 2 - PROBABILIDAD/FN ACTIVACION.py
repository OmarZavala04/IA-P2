# Comparacion de curvas de aceleracion para un videojuego
# Este programa muestra diferentes formas en que un personaje
# puede acelerar dependiendo del tipo de motor o fisica usada.
#
# cambiamos totalmente la idea:
# ahora ya no hablamos de redes neuronales,
# sino de comportamiento de movimiento en videojuegos.

import numpy as np
import matplotlib.pyplot as plt

# tiempo simulado
tiempo = np.linspace(-10, 10, 200)

# ============================
# funciones de movimiento
# ============================

def movimiento_suave(t):
    """
    aceleracion progresiva suave
    similar a un auto automatico
    """
    return 1 / (1 + np.exp(-t))

def movimiento_balanceado(t):
    """
    cambio equilibrado entre frenado y aceleracion
    """
    return np.tanh(t)

def movimiento_brusco(t):
    """
    aceleracion instantanea
    """
    return np.maximum(0, t)

def movimiento_deslizante(t, perdida=0.05):
    """
    aceleracion con pequeña inercia negativa
    """
    return np.where(t > 0, t, perdida * t)

# calculamos curvas
curva_suave = movimiento_suave(tiempo)
curva_balanceada = movimiento_balanceado(tiempo)
curva_brusca = movimiento_brusco(tiempo)
curva_deslizante = movimiento_deslizante(tiempo)

# ============================
# graficas
# ============================

plt.figure(figsize=(12, 8))

# curva suave
plt.subplot(2, 2, 1)
plt.plot(tiempo, curva_suave)
plt.title("Movimiento Suave")
plt.xlabel("Tiempo")
plt.ylabel("Velocidad")
plt.grid(True)

# curva balanceada
plt.subplot(2, 2, 2)
plt.plot(tiempo, curva_balanceada)
plt.title("Movimiento Balanceado")
plt.xlabel("Tiempo")
plt.ylabel("Velocidad")
plt.grid(True)

# curva brusca
plt.subplot(2, 2, 3)
plt.plot(tiempo, curva_brusca)
plt.title("Movimiento Brusco")
plt.xlabel("Tiempo")
plt.ylabel("Velocidad")
plt.grid(True)

# curva con deslizamiento
plt.subplot(2, 2, 4)
plt.plot(tiempo, curva_deslizante)
plt.title("Movimiento con Deslizamiento")
plt.xlabel("Tiempo")
plt.ylabel("Velocidad")
plt.grid(True)

plt.tight_layout()
plt.show()

# explicacion:
# cada curva representa una sensacion distinta de movimiento:
#
# - suave:
#   arranque gradual y controlado
#
# - balanceado:
#   cambio natural entre negativo y positivo
#
# - brusco:
#   respuesta inmediata
#
# - deslizante:
#   mantiene algo de movimiento incluso en negativo
#
# ideas parecidas se usan en:
# - videojuegos
# - simuladores
# - animacion
# - robots