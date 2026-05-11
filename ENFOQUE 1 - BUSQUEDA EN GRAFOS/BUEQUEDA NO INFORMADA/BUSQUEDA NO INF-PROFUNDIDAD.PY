# búsqueda A*
# este algoritmo intenta encontrar
# una ruta eficiente hacia el objetivo
#
# para decidir qué nodo explorar utiliza:
#
# f(n) = g(n) + h(n)
#
# g(n) -> costo acumulado real
# h(n) -> estimación faltante hasta la meta
#
# el algoritmo siempre prioriza
# el nodo con menor valor de f

import heapq


def busqueda_a_estrella(grafo, heuristica, origen, destino):

    # heuristica:
    # estimación de distancia al objetivo
    #
    # origen:
    # nodo inicial
    #
    # destino:
    # nodo que queremos alcanzar
    #
    # retorna:
    # (ruta, costo_total)
    # o (None, None) si no existe camino

    if origen == destino:
        return [origen], 0

    # diccionario con el costo real
    # acumulado para cada nodo
    costos_reales = {
        origen: 0
    }

    # cola de prioridad:
    # (valor_f, nodo_actual, camino)
    pendientes = []

    f_inicial = (
        costos_reales[origen]
        + heuristica.get(origen, float("inf"))
    )

    heapq.heappush(
        pendientes,
        (f_inicial, origen, [origen])
    )

    explorados = set()

    while pendientes:

        f_actual, nodo_actual, ruta_actual = heapq.heappop(
            pendientes
        )

        # si llegamos al destino
        # terminamos la búsqueda
        if nodo_actual == destino:
            return ruta_actual, costos_reales[nodo_actual]

        # evitamos volver a procesar nodos
        if nodo_actual in explorados:
            continue

        explorados.add(nodo_actual)

        # revisamos las conexiones vecinas
        for vecino, costo in grafo.get(
            nodo_actual,
            {}
        ).items():

            # nuevo costo acumulado
            nuevo_costo = (
                costos_reales[nodo_actual]
                + costo
            )

            # si es la primera vez
            # o encontramos una ruta mejor
            if (
                vecino not in costos_reales
                or nuevo_costo < costos_reales[vecino]
            ):

                costos_reales[vecino] = nuevo_costo

                nueva_ruta = ruta_actual + [vecino]

                # cálculo de f(n)
                valor_f = (
                    nuevo_costo
                    + heuristica.get(
                        vecino,
                        float("inf")
                    )
                )

                heapq.heappush(
                    pendientes,
                    (
                        valor_f,
                        vecino,
                        nueva_ruta
                    )
                )

    # no fue posible llegar al destino
    return None, None


# comentario sobre AO*
#
# AO* se utiliza en grafos AND-OR
# donde algunos pasos requieren
# completar varias acciones relacionadas
#
# normalmente en cursos introductorios
# solo se revisa la teoría general
# y no suele implementarse en código


if __name__ == "__main__":

    # grafo con costos de desplazamiento

    grafo = {

        "hogar": {
            "mercado": 2,
            "jardin": 5
        },

        "mercado": {
            "universidad": 2,
            "clinica": 5
        },

        "universidad": {
            "empresa": 4
        },

        "jardin": {
            "clinica": 2
        },

        "clinica": {
            "empresa": 3
        },

        "empresa": {}
    }

    # heurística:
    # estimación de cercanía
    # respecto al nodo "empresa"

    heuristica = {

        "empresa": 0,

        "clinica": 2,

        "universidad": 3,

        "jardin": 4,

        "mercado": 4,

        "hogar": 6
    }

    ruta, costo_total = busqueda_a_estrella(
        grafo,
        heuristica,
        "hogar",
        "empresa"
    )

    print("ruta calculada con A*:")
    print(ruta)

    print("costo total:")
    print(costo_total)

    ruta2, costo_total2 = busqueda_a_estrella(
        grafo,
        heuristica,
        "hogar",
        "aeropuerto"
    )

    print("ruta hacia aeropuerto:")
    print(ruta2)

    print("costo total:")
    print(costo_total2)

    # resumen:
    #
    # g(n) -> costo recorrido
    # h(n) -> estimación restante
    # f(n) -> suma de ambos valores
    #
    # A* prioriza el nodo
    # con el menor valor de f