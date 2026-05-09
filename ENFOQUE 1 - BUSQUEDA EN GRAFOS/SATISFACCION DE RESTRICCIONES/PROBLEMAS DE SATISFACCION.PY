# búsqueda tabú
#
# este método es similar
# a la ascensión de colinas
# pero incorpora memoria
#
# problema de hill climbing:
# puede quedarse atrapado
# repitiendo los mismos estados
#
# para evitarlo se usa
# una lista tabú
#
# la lista tabú almacena
# estados recientes que
# temporalmente no se pueden usar


def seleccionar_vecino_valido(
    estado_actual,
    conexiones,
    funcion_valor,
    lista_tabu
):

    # estado_actual:
    # nodo donde nos encontramos
    #
    # conexiones:
    # vecinos disponibles
    #
    # funcion_valor:
    # evalúa qué tan bueno es un estado
    #
    # lista_tabu:
    # estados prohibidos temporalmente
    #
    # retorna:
    # el mejor vecino permitido
    # o None si no existe uno válido

    mejor_candidato = None

    mejor_puntaje = None

    for vecino in conexiones.get(
        estado_actual,
        []
    ):

        # ignoramos estados tabú
        if vecino in lista_tabu:
            continue

        puntaje = funcion_valor(vecino)

        # seleccionamos el vecino
        # con mayor valor
        if (
            mejor_candidato is None
            or puntaje > mejor_puntaje
        ):

            mejor_candidato = vecino

            mejor_puntaje = puntaje

    return mejor_candidato


def algoritmo_tabu(
    inicio,
    conexiones,
    funcion_valor,
    limite_tabu,
    iteraciones_maximas
):

    # inicio:
    # estado inicial
    #
    # conexiones:
    # posibles movimientos
    #
    # funcion_valor:
    # mide la calidad de cada estado
    #
    # limite_tabu:
    # tamaño máximo de memoria tabú
    #
    # iteraciones_maximas:
    # cantidad máxima de movimientos
    #
    # retorna:
    # (mejor_estado, historial)

    actual = inicio

    # mejor estado encontrado
    mejor_global = actual

    historial = [actual]

    # estructuras de memoria tabú
    tabu = {actual}

    cola_tabu = [actual]

    for _ in range(iteraciones_maximas):

        siguiente = seleccionar_vecino_valido(
            actual,
            conexiones,
            funcion_valor,
            tabu
        )

        # si no hay movimientos válidos
        # termina la búsqueda
        if siguiente is None:
            break

        # avanzar al siguiente estado
        actual = siguiente

        historial.append(actual)

        # agregar a lista tabú
        tabu.add(actual)

        cola_tabu.append(actual)

        # controlar tamaño máximo
        if len(cola_tabu) > limite_tabu:

            estado_viejo = cola_tabu.pop(0)

            if estado_viejo in tabu:
                tabu.remove(estado_viejo)

        # actualizar mejor solución global
        if (
            funcion_valor(actual)
            > funcion_valor(mejor_global)
        ):

            mejor_global = actual

    return mejor_global, historial


if __name__ == "__main__":

    # conexiones entre estados
    #
    # números mayores
    # representan mejores soluciones

    conexiones = {

        3: [4, 5, 6],

        4: [5, 6],

        5: [4, 6, 7],

        6: [5, 7, 8],

        7: [6, 8, 9],

        8: [7, 9],

        9: [8]
    }

    # función de evaluación
    #
    # mientras mayor sea el número
    # mejor es el estado

    def funcion_valor(x):
        return x

    # parámetros principales:
    #
    # inicio = 3
    #
    # limite_tabu = 3
    # cantidad máxima de estados prohibidos
    #
    # iteraciones_maximas = 10
    # número máximo de movimientos

    mejor_estado, recorrido = algoritmo_tabu(
        inicio=3,
        conexiones=conexiones,
        funcion_valor=funcion_valor,
        limite_tabu=3,
        iteraciones_maximas=10
    )

    print("mejor estado encontrado:")
    print(mejor_estado)

    print("historial de movimientos:")
    print(recorrido)

    # resumen:
    #
    # - la memoria tabú evita
    #   regresar inmediatamente
    #   a estados recientes
    #
    # - esto reduce ciclos repetitivos
    #
    # - mejor_global almacena
    #   la mejor solución encontrada