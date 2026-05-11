# Este código simula un sistema básico de reconocimiento de palabras.
# El usuario puede seleccionar una palabra manualmente
# o dejar que el sistema elija una al azar.

import random
import time

# =========================
# BASE DE PALABRAS
# =========================

# formato:
# ("palabra", "interpretacion")
palabras_habladas = [
    ("hola", "saludo"),
    ("adios", "despedida"),
    ("gracias", "agradecimiento"),
    ("perdon", "disculpa"),
    ("si", "afirmacion"),
    ("no", "negacion")
]

# =========================
# FUNCION DE RECONOCIMIENTO
# =========================

def reconocer_habla(entrada_habla):
    """
    busca la interpretacion de la palabra
    dentro de la lista de palabras conocidas
    """

    print("\nreconociendo palabra...")
    time.sleep(1)

    for palabra, interpretacion in palabras_habladas:

        # comparar ignorando mayusculas
        if entrada_habla.lower() == palabra.lower():

            print("palabra reconocida :", entrada_habla)
            print("interpretacion     :", interpretacion)

            return interpretacion

    # si no existe coincidencia
    print("palabra no reconocida.")
    return "desconocida"

# =========================
# MENU DE OPCIONES
# =========================

def seleccionar_palabra():

    opciones = [palabra for palabra, _ in palabras_habladas]

    print("=== sistema de reconocimiento de palabras ===\n")

    print("elige una opcion:\n")

    for i, opcion in enumerate(opciones, start=1):
        print(i, "-", opcion)

    print(len(opciones) + 1, "- aleatoria")

    eleccion = input("\nescribe el numero de tu eleccion: ")

    # validar si es numero
    if eleccion.isdigit():

        eleccion = int(eleccion)

        # seleccion manual
        if 1 <= eleccion <= len(opciones):
            return opciones[eleccion - 1]

        # seleccion aleatoria
        elif eleccion == len(opciones) + 1:
            return random.choice(opciones)

    # si hubo error
    print("\nentrada invalida.")
    print("se seleccionara una palabra aleatoria...\n")

    return random.choice(opciones)

# =========================
# PROGRAMA PRINCIPAL
# =========================

palabra_hablada = seleccionar_palabra()

print("\npalabra seleccionada:", palabra_hablada)

resultado = reconocer_habla(palabra_hablada)

print("\ninterpretacion final:", resultado)