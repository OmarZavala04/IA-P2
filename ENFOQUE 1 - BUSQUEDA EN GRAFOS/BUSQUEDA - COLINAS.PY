# búsqueda por ascensión de colinas
#
# este algoritmo intenta mejorar
# paso a paso una solución
#
# en cada movimiento:
# solamente acepta vecinos
# que tengan un valor mayor
#
# idea principal:
# avanzar siempre hacia arriba
# según una función de evaluación
#
# limitación importante:
# si ningún vecino mejora
# el estado actual,
# el algoritmo se detiene
#
# esto puede provocar
# máximos locales
#
# un máximo local:
# es una solución buena
# pero no necesariamente
# la mejor de todas


def obtener_mejor_vecino(
    estado_actual,
    conexiones,
    funcion_valor
):

    """
    estado_actual:
        nodo actual

    conexiones:
        vecinos disponibles
        para cada estado

    funcion_valor:
        evalúa qué tan bueno
        es un estado

    retorna:
        el mejor vecino
        que supere al actual

        si no existe mejora:
        retorna None
    """

    valor_actual = funcion_valor(
        estado_actual
    )

    mejor_opcion = None

    mejor_puntaje = valor_actual

    # revisar vecinos
    for vecino in conexiones.get(
        estado_actual,
        []
    ):

        valor_vecino = funcion_valor(
            vecino
        )

        # aceptar solamente mejoras
        if valor_vecino > mejor_puntaje:

            mejor_puntaje = valor_vecino

            mejor_opcion = vecino

    return mejor_opcion


def hill_climbing(
    inicio,
    conexiones,
    funcion_valor
):

    """
    inicio:
        estado inicial

    conexiones:
        movimientos posibles

    funcion_valor:
        mide la calidad
        de cada estado

    retorna:
        estado_final,
        historial
    """

    actual = inicio

    historial = [actual]

    while True:

        # buscar mejora
        siguiente = obtener_mejor_vecino(
            actual,
            conexiones,
            funcion_valor
        )

        # si no existe mejora
        # finalizar búsqueda
        if siguiente is None:

            return actual, historial

        # avanzar al nuevo estado
        actual = siguiente

        historial.append(actual)


if __name__ == "__main__":

    # conexiones entre estados
    #
    # cada estado representa
    # un número

    conexiones = {

        1: [2, 3],

        2: [4, 5],

        3: [5, 6],

        4: [7],

        5: [7, 8],

        6: [8],

        7: [9],

        8: [9, 10],

        9: [],

        10: []
    }

    # función de evaluación
    #
    # números mayores
    # representan mejores estados

    def funcion_valor(x):

        return x

    # comenzar búsqueda
    # desde el estado 1

    resultado, recorrido = hill_climbing(
        inicio=1,
        conexiones=conexiones,
        funcion_valor=funcion_valor
    )

    print("estado final encontrado:")
    print(resultado)

    print("camino recorrido:")
    print(recorrido)

    # resumen:
    #
    # - únicamente se aceptan
    #   movimientos mejores
    #
    # - si ya no existe mejora
    #   la búsqueda termina
    #
    # - no garantiza
    #   el óptimo global
    #
    # - puede detenerse
    #   en máximos locales