# búsqueda online
#
# este tipo de búsqueda funciona
# cuando el agente no conoce
# el mapa completo desde el inicio
#
# el agente solamente conoce:
# - dónde se encuentra
# - qué vecinos tiene el nodo actual
#
# conforme avanza descubre
# nuevas conexiones y las almacena
#
# este enfoque es útil
# en entornos desconocidos
# o mapas explorados en tiempo real


def explorar_estado(
    actual,
    mundo_completo,
    memoria_agente,
    visitados
):

    """
    actual:
        posición actual del agente

    mundo_completo:
        grafo verdadero con todas las conexiones

    memoria_agente:
        conocimiento acumulado por el agente

        ejemplo:
        {
            "A": ["B", "C"],
            "B": ["D"]
        }

    visitados:
        lugares explorados previamente

    retorna:
        vecinos disponibles
        que aún no han sido visitados
    """

    # obtener vecinos reales
    vecinos_reales = mundo_completo.get(
        actual,
        []
    )

    # guardar descubrimientos
    memoria_agente[actual] = vecinos_reales[:]

    # filtrar vecinos no visitados
    disponibles = []

    for vecino in vecinos_reales:

        if vecino not in visitados:
            disponibles.append(vecino)

    return disponibles


def algoritmo_online(
    inicio,
    meta,
    mundo_completo,
    limite_pasos
):

    """
    inicio:
        nodo inicial

    meta:
        objetivo final

    mundo_completo:
        mapa real del entorno

    limite_pasos:
        límite máximo de movimientos

    retorna:
        recorrido,
        memoria_aprendida,
        éxito
    """

    actual = inicio

    recorrido = [actual]

    # memoria vacía inicialmente
    memoria_aprendida = {}

    # estados visitados
    visitados = {actual}

    for _ in range(limite_pasos):

        # verificar objetivo
        if actual == meta:
            return (
                recorrido,
                memoria_aprendida,
                True
            )

        # descubrir vecinos
        opciones = explorar_estado(
            actual,
            mundo_completo,
            memoria_aprendida,
            visitados
        )

        # si no existen opciones nuevas
        # el agente queda bloqueado
        if len(opciones) == 0:

            return (
                recorrido,
                memoria_aprendida,
                False
            )

        # estrategia básica:
        # avanzar al primer vecino disponible
        siguiente = opciones[0]

        actual = siguiente

        visitados.add(actual)

        recorrido.append(actual)

    # si se alcanza el límite
    # sin llegar a la meta
    return (
        recorrido,
        memoria_aprendida,
        False
    )


if __name__ == "__main__":

    # mapa verdadero del entorno
    #
    # el programa sí conoce
    # todas las conexiones
    #
    # el agente las descubre
    # poco a poco

    mundo_completo = {

        "A": ["B", "C"],

        "B": ["D"],

        "C": ["D", "E"],

        "D": ["F"],

        "E": ["F"],

        "F": []
    }

    # búsqueda desde A hasta F
    # sin conocer el mapa completo

    camino, memoria, encontrado = algoritmo_online(
        inicio="A",
        meta="F",
        mundo_completo=mundo_completo,
        limite_pasos=10
    )

    print("recorrido realizado:")
    print(camino)

    print("memoria aprendida:")

    for lugar, vecinos in memoria.items():

        print(
            " ",
            lugar,
            "->",
            vecinos
        )

    print("¿objetivo alcanzado?:")
    print(encontrado)

    # resumen:
    #
    # - el agente descubre
    #   el entorno paso a paso
    #
    # - memoria_aprendida almacena
    #   la información encontrada
    #
    # - no existe un plan completo
    #   desde el inicio
    #
    # - las decisiones se toman
    #   durante la exploración