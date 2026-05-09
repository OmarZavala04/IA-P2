# búsqueda por temple simulado
#
# este algoritmo intenta encontrar
# una buena solución dentro
# de un conjunto de estados
#
# diferencia con ascensión de colinas:
#
# - hill climbing solo acepta
#   movimientos mejores
#
# - temple simulado puede aceptar
#   temporalmente soluciones peores
#
# ¿por qué aceptar algo peor?
#
# para evitar quedar atrapado
# en máximos locales
#
# el algoritmo utiliza
# una temperatura
#
# al inicio:
# la temperatura es alta
# y permite más exploración
#
# después:
# la temperatura disminuye
# y el algoritmo se vuelve
# más estricto


import random
import math


def vecino_aleatorio(
    actual,
    conexiones
):

    """
    actual:
        estado actual

    conexiones:
        vecinos posibles
        para cada estado

    retorna:
        un vecino aleatorio
        o None si no existen vecinos
    """

    opciones = conexiones.get(
        actual,
        []
    )

    if len(opciones) == 0:
        return None

    # seleccionar vecino al azar
    return random.choice(opciones)


def algoritmo_temple_simulado(
    inicio,
    conexiones,
    funcion_valor,
    temperatura_inicial,
    factor_enfriamiento,
    iteraciones_maximas
):

    """
    inicio:
        estado inicial

    conexiones:
        movimientos posibles

    funcion_valor:
        mide qué tan bueno es un estado

    temperatura_inicial:
        temperatura al comenzar

    factor_enfriamiento:
        velocidad con la que
        disminuye la temperatura

    iteraciones_maximas:
        cantidad máxima de pasos

    retorna:
        mejor_estado,
        historial
    """

    actual = inicio

    mejor_estado = actual

    historial = [actual]

    temperatura = temperatura_inicial

    for _ in range(iteraciones_maximas):

        vecino = vecino_aleatorio(
            actual,
            conexiones
        )

        # si no hay vecinos
        # termina el proceso
        if vecino is None:
            break

        valor_actual = funcion_valor(actual)

        valor_vecino = funcion_valor(vecino)

        # si el vecino es mejor
        # se acepta inmediatamente
        if valor_vecino > valor_actual:

            actual = vecino

        else:

            # diferencia negativa
            diferencia = (
                valor_vecino
                - valor_actual
            )

            # probabilidad de aceptar
            # un movimiento peor
            if temperatura > 0:

                probabilidad = math.exp(
                    diferencia / temperatura
                )

            else:
                probabilidad = 0

            # número aleatorio entre 0 y 1
            numero = random.random()

            # aceptar el movimiento
            # dependiendo de la probabilidad
            if numero < probabilidad:

                actual = vecino

        # guardar historial
        historial.append(actual)

        # actualizar mejor estado global
        if (
            funcion_valor(actual)
            > funcion_valor(mejor_estado)
        ):

            mejor_estado = actual

        # disminuir temperatura
        temperatura = (
            temperatura
            * factor_enfriamiento
        )

        # detener si la temperatura
        # es demasiado baja
        if temperatura <= 0.0001:
            break

    return mejor_estado, historial


if __name__ == "__main__":

    # conexiones entre estados
    #
    # cada estado es un número

    conexiones = {

        3: [4, 5, 6],

        4: [5, 7],

        5: [6, 7],

        6: [7, 8],

        7: [8, 9],

        8: [9, 10],

        9: [10],

        10: []
    }

    # función de evaluación
    #
    # valores mayores
    # representan mejores estados

    def funcion_valor(x):
        return x

    mejor, recorrido = algoritmo_temple_simulado(
        inicio=3,
        conexiones=conexiones,
        funcion_valor=funcion_valor,
        temperatura_inicial=10.0,
        factor_enfriamiento=0.9,
        iteraciones_maximas=50
    )

    print("mejor estado encontrado:")
    print(mejor)

    print("historial de estados visitados:")
    print(recorrido)

    # resumen:
    #
    # - temperatura alta:
    #   permite explorar más
    #
    # - temperatura baja:
    #   reduce movimientos riesgosos
    #
    # - math.exp(...)
    #   calcula la probabilidad
    #   de aceptar estados peores
    #
    # - random.random()
    #   decide aleatoriamente
    #   si el movimiento se acepta