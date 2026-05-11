# Exploracion vs Explotacion
# este ejemplo muestra el dilema clasico en aprendizaje por refuerzo:
#
# - exploracion:
#     probar opciones nuevas para descubrir si son buenas
#
# - explotacion:
#     usar la opcion que actualmente parece la mejor
#
# aqui simulamos una cafeteria con varias bebidas.
# cada bebida da una "satisfaccion" diferente,
# pero el agente NO sabe cuales son las mejores al inicio.
#
# el agente debe aprender:
# - explorar algunas veces
# - explotar cuando ya tenga experiencia
#
# usamos estrategia epsilon-greedy:
# - con prob epsilon -> explorar random
# - con prob 1-epsilon -> elegir la mejor conocida


import random


def elegir_bebida(valores_estimados, bebidas, epsilon):
    """
    decide que bebida pedir.

    valores_estimados:
        dict con el promedio aprendido de cada bebida

    bebidas:
        lista de bebidas disponibles

    epsilon:
        probabilidad de explorar
    """

    # explorar
    if random.random() < epsilon:
        bebida = random.choice(bebidas)
        modo = "exploracion"

    # explotar
    else:
        bebida = max(valores_estimados, key=valores_estimados.get)
        modo = "explotacion"

    return bebida, modo


def recompensa_real(bebida):
    """
    simula la satisfaccion REAL de cada bebida.

    el agente no conoce estos valores.
    """

    if bebida == "cafe":
        return random.randint(7, 10)

    if bebida == "te":
        return random.randint(4, 8)

    if bebida == "chocolate":
        return random.randint(6, 9)

    if bebida == "matcha":
        return random.randint(2, 12)

    return 0


def actualizar_valor(valor_actual, recompensa, veces_probada):
    """
    actualiza el promedio aprendido de una bebida.

    formula:
    nuevo_promedio =
        promedio_viejo + (recompensa - promedio_viejo)/n
    """

    nuevo = valor_actual + (
        (recompensa - valor_actual) / veces_probada
    )

    return nuevo


if __name__ == "__main__":

    bebidas = ["cafe", "te", "chocolate", "matcha"]

    # valores estimados iniciales
    # al inicio no sabemos nada
    valores_estimados = {}

    for b in bebidas:
        valores_estimados[b] = 0.0

    # contador de cuantas veces probamos cada bebida
    conteos = {}

    for b in bebidas:
        conteos[b] = 0

    epsilon = 0.3
    rondas = 30

    print("aprendiendo preferencias...\n")

    for ronda in range(1, rondas + 1):

        # elegir bebida
        bebida, modo = elegir_bebida(
            valores_estimados,
            bebidas,
            epsilon
        )

        # recibir recompensa real
        recompensa = recompensa_real(bebida)

        # actualizar contador
        conteos[bebida] += 1

        # actualizar estimacion aprendida
        valores_estimados[bebida] = actualizar_valor(
            valores_estimados[bebida],
            recompensa,
            conteos[bebida]
        )

        print(
            "ronda", ronda,
            "| modo:", modo,
            "| bebida:", bebida,
            "| recompensa:", recompensa,
            "| promedio aprendido:", round(valores_estimados[bebida], 2)
        )

    print("\nvalores aprendidos finales:")

    for bebida in bebidas:
        print(
            bebida,
            "->",
            round(valores_estimados[bebida], 2),
            "(probada", conteos[bebida], "veces)"
        )

    mejor = max(valores_estimados, key=valores_estimados.get)

    print("\nmejor bebida aprendida:", mejor)

    # resumen:
    # - exploracion = probar opciones nuevas
    # - explotacion = usar la mejor conocida
    # - epsilon controla cuanto explora el agente
    # - el agente aprende promedios observando recompensas