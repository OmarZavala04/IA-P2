# Simula un sistema simple de reconocimiento de habla
# asociando palabras habladas con su interpretación.

import random
import time

# =========================
# BASE DE PALABRAS
# =========================

# formato:
# ("palabra hablada", "significado")
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
    busca la palabra dentro de la base
    y devuelve su interpretacion
    """

    print("\nreconociendo palabra...")
    time.sleep(1)  # simula tiempo de procesamiento

    for palabra, interpretacion in palabras_habladas:

        # comparacion ignorando mayusculas
        if entrada_habla.lower() == palabra.lower():

            print("palabra reconocida:", entrada_habla)
            print("interpretacion     :", interpretacion)

            return interpretacion

    # si no se encontro
    print("palabra no reconocida.")
    return "desconocida"

# =========================
# MENU DE SELECCION
# =========================

def seleccionar_palabra():

    opciones = [palabra for palabra, _ in palabras_habladas]

    print("=== sistema de reconocimiento de habla ===\n")

    print("elige una opcion:\n")

    for i, opcion in enumerate(opciones, start=1):
        print(i, "-", opcion)

    print(len(opciones) + 1, "- aleatoria")

    eleccion = input("\nescribe el numero de tu eleccion: ")

    # validar entrada
    if eleccion.isdigit():

        eleccion = int(eleccion)

        # palabra normal
        if 1 <= eleccion <= len(opciones):
            return opciones[eleccion - 1]

        # palabra aleatoria
        elif eleccion == len(opciones) + 1:
            return random.choice(opciones)

    # si hubo error
    print("\nentrada no valida.")
    print("se elegira una palabra aleatoria...\n")

    return random.choice(opciones)

# =========================
# PROGRAMA PRINCIPAL
# =========================

palabra_hablada = seleccionar_palabra()

print("\npalabra detectada:", palabra_hablada)

resultado = reconocer_habla(palabra_hablada)

print("\nresultado final:", resultado)