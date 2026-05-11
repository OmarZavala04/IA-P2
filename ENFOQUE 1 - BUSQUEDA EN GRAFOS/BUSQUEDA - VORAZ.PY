# búsqueda voraz primero el mejor
# también conocida como:
# greedy best first search
#
# este método intenta avanzar
# hacia el nodo que aparenta
# estar más cerca del objetivo
#
# solamente utiliza la heurística
# y no considera el costo real recorrido
#
# ventaja:
# suele ser rápida
#
# desventaja:
# puede tomar decisiones engañosas
# y no siempre encuentra la mejor ruta

import heapq


def greedy_best_first(grafo, heuristica, origen, destino):

    # grafo:
    # conexiones entre nodos
    #
    # heuristica:
    # estimación de cercanía al objetivo
    #
    # origen:
    # punto de inicio
    #
    # destino:
    # nodo objetivo

    if origen == destino:
        return [origen]

    # cola de prioridad:
    # (heurística, nodo, camino)
    pendientes = []

    heapq.heappush(
        pendientes,
        (
            heuristica.get(origen, float("inf")),
            origen,
            [origen]
        )
    )

    # conjunto para evitar ciclos
    visitados = {origen}

    while pendientes:

        # obtenemos el nodo
        # con menor heurística
        _, actual, ruta = heapq.heappop(
            pendientes
        )

        # si encontramos el destino
        # terminamos la búsqueda
        if actual == destino:
            return ruta

        # exploramos los vecinos
        for vecino in grafo.get(actual, []):

            if vecino not in visitados:

                visitados.add(vecino)

                nueva_ruta = ruta + [vecino]

                # el vecino se agrega
                # usando únicamente
                # su valor heurístico
                heapq.heappush(
                    pendientes,
                    (
                        heuristica.get(
                            vecino,
                            float("inf")
                        ),
                        vecino,
                        nueva_ruta
                    )
                )

    # no fue posible llegar
    return None


if __name__ == "__main__":

    # representación del mapa
    #
    # aula -> corredor, patio
    # corredor -> laboratorio, biblioteca
    # patio -> cafetería
    # laboratorio -> servidor
    # biblioteca -> cafetería
    # cafetería -> servidor

    grafo = {

        "aula": [
            "corredor",
            "patio"
        ],

        "corredor": [
            "laboratorio",
            "biblioteca"
        ],

        "patio": [
            "cafeteria"
        ],

        "laboratorio": [
            "servidor"
        ],

        "biblioteca": [
            "cafeteria"
        ],

        "cafeteria": [
            "servidor"
        ],

        "servidor": []
    }

    # heurística:
    # estimación de cercanía
    # respecto al servidor
    #
    # números pequeños indican
    # mayor proximidad

    heuristica = {

        "servidor": 0,

        "cafeteria": 1,

        "laboratorio": 1,

        "biblioteca": 2,

        "corredor": 2,

        "patio": 2,

        "aula": 3
    }

    camino_1 = greedy_best_first(
        grafo,
        heuristica,
        "aula",
        "servidor"
    )

    print("ruta voraz desde aula a servidor:")
    print(camino_1)

    camino_2 = greedy_best_first(
        grafo,
        heuristica,
        "aula",
        "estacionamiento"
    )

    print("ruta hacia estacionamiento:")
    print(camino_2)

    # resumen:
    #
    # - siempre se elige
    #   el nodo con heurística menor
    #
    # - no toma en cuenta
    #   el costo real recorrido
    #
    # - normalmente es rápida
    #
    # - no garantiza
    #   la ruta óptima