
# heurísticas
# en búsquedas informadas utilizamos una referencia
# para decidir cuál camino parece más conveniente
# esa referencia se conoce como heurística
# la heurística representa una estimación de cercanía al objetivo
# entre menor sea el valor, se supone que estamos más cerca
# esto no asegura encontrar la mejor ruta
# pero sí ayuda a explorar primero los caminos más prometedores

def seleccionar_mejor_vecino(grafo, heuristica, nodo_actual):
    # esta función revisa los vecinos disponibles
    # desde el nodo actual y selecciona
    # el que tenga la heurística más pequeña
    #
    # grafo: estructura con las conexiones
    # heuristica: valores estimados para cada nodo
    # nodo_actual: posición donde nos encontramos

    vecinos = grafo.get(nodo_actual, [])

    # si el nodo no tiene vecinos disponibles
    # ya no es posible continuar
    if len(vecinos) == 0:
        return None

    # seleccionamos el vecino con menor valor heurístico
    mejor_opcion = min(
        vecinos,
        key=lambda nodo: heuristica.get(nodo, float("inf"))
    )

    return mejor_opcion


def busqueda_voraz(grafo, heuristica, inicio, meta):
    # esta función intenta alcanzar la meta
    # moviéndose siempre hacia el vecino
    # que parece más cercano según la heurística
    #
    # este método corresponde a una búsqueda greedy
    # por lo tanto no garantiza el camino óptimo

    actual = inicio

    recorrido = [actual]

    # conjunto para evitar ciclos
    visitados = {actual}

    while actual != meta:

        siguiente = seleccionar_mejor_vecino(
            grafo,
            heuristica,
            actual
        )

        # si no hay más opciones
        # el recorrido falla
        if siguiente is None:
            return recorrido, False

        # si ya visitamos el nodo
        # significa que estamos repitiendo caminos
        if siguiente in visitados:
            return recorrido, False

        recorrido.append(siguiente)

        visitados.add(siguiente)

        actual = siguiente

    # si el ciclo termina
    # significa que llegamos a la meta
    return recorrido, True


if __name__ == "__main__":

    # representación del grafo
    #
    # aula -> corredor, patio
    # corredor -> laboratorio, biblioteca
    # patio -> cafetería
    # laboratorio -> servidor
    # biblioteca -> cafetería
    # cafetería -> servidor

    grafo = {
        "aula": ["corredor", "patio"],
        "corredor": ["laboratorio", "biblioteca"],
        "patio": ["cafeteria"],
        "laboratorio": ["servidor"],
        "biblioteca": ["cafeteria"],
        "cafeteria": ["servidor"],
        "servidor": []
    }

    # valores heurísticos
    #
    # representan qué tan cerca creemos
    # que está cada nodo del servidor
    #
    # servidor = 0 porque ya es el objetivo
    # números pequeños indican mayor cercanía

    heuristica = {
        "servidor": 0,
        "cafeteria": 1,
        "laboratorio": 1,
        "biblioteca": 2,
        "corredor": 2,
        "patio": 2,
        "aula": 3
    }

    # búsqueda desde aula hasta servidor
    camino, encontrado = busqueda_voraz(
        grafo,
        heuristica,
        "aula",
        "servidor"
    )

    print("camino obtenido con heurística:")
    print(camino)

    print("¿se alcanzó el objetivo?")
    print(encontrado)

    # observaciones:
    #
    # heuristica["cafeteria"] = 1
    # significa que cafeteria parece cercana al servidor
    #
    # min(..., key=...)
    # selecciona el elemento con menor valor asociado
    #
    # append(x)
    # agrega un elemento al final de una lista
    #
    # add(x)
    # inserta un elemento dentro de un conjunto
