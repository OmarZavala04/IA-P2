# Busqueda de la Politica
# una politica dice que accion tomar en cada estado.
#
# en aprendizaje por refuerzo y planeacion,
# muchas veces queremos encontrar directamente
# la mejor politica posible.
#
# aqui NO calculamos valores de estados como en value iteration.
# aqui probamos distintas politicas y vemos cual funciona mejor.
#
# idea del ejemplo:
#
# un robot repartidor puede estar en:
# - "inicio"
# - "pasillo"
# - "meta"
#
# en cada estado puede elegir acciones.
# algunas dan mejores recompensas que otras.
#
# vamos a:
# 1. generar varias politicas aleatorias
# 2. simularlas
# 3. medir recompensa total
# 4. quedarnos con la mejor politica encontrada


import random


def ejecutar_politica(
    politica,
    estado_inicial,
    transicion,
    recompensa,
    pasos_max
):
    """
    ejecuta una politica y acumula recompensa total.

    politica:
        dict estado -> accion

    estado_inicial:
        donde empieza el agente

    transicion:
        funcion que calcula siguiente estado

    recompensa:
        funcion que calcula recompensa inmediata

    pasos_max:
        maximo de pasos permitidos
    """

    estado = estado_inicial
    recompensa_total = 0

    for _ in range(pasos_max):

        # si llegamos a meta terminamos
        if estado == "meta":
            break

        accion = politica[estado]

        siguiente = transicion(estado, accion)

        r = recompensa(estado, accion, siguiente)

        recompensa_total += r

        estado = siguiente

    return recompensa_total


def generar_politica_aleatoria(estados, acciones_disponibles):
    """
    crea una politica random:
    para cada estado escoge una accion aleatoria.
    """

    politica = {}

    for estado in estados:

        acciones = acciones_disponibles[estado]

        if len(acciones) == 0:
            politica[estado] = None
        else:
            politica[estado] = random.choice(acciones)

    return politica


def buscar_mejor_politica(
    estados,
    acciones_disponibles,
    estado_inicial,
    transicion,
    recompensa,
    intentos,
    pasos_max
):
    """
    prueba muchas politicas aleatorias
    y se queda con la mejor.
    """

    mejor_politica = None
    mejor_score = None

    for intento in range(intentos):

        politica = generar_politica_aleatoria(
            estados,
            acciones_disponibles
        )

        score = ejecutar_politica(
            politica,
            estado_inicial,
            transicion,
            recompensa,
            pasos_max
        )

        print(
            "intento", intento + 1,
            "| politica:", politica,
            "| recompensa:", score
        )

        if (mejor_politica is None) or (score > mejor_score):
            mejor_politica = politica
            mejor_score = score

    return mejor_politica, mejor_score


if __name__ == "__main__":

    estados = [
        "inicio",
        "pasillo",
        "meta"
    ]

    acciones_disponibles = {

        "inicio": [
            "caminar",
            "atajo"
        ],

        "pasillo": [
            "seguir",
            "regresar"
        ],

        "meta": []
    }

    def transicion(estado, accion):

        if estado == "inicio":

            if accion == "caminar":
                return "pasillo"

            if accion == "atajo":
                # el atajo puede salir bien o mal
                if random.random() < 0.5:
                    return "meta"
                else:
                    return "pasillo"

        if estado == "pasillo":

            if accion == "seguir":
                return "meta"

            if accion == "regresar":
                return "inicio"

        return estado


    def recompensa(estado, accion, siguiente):

        # llegar a meta da recompensa grande
        if siguiente == "meta":
            return 100

        # regresar pierde tiempo
        if accion == "regresar":
            return -20

        # caminar normal cuesta poquito
        return -1


    mejor_politica, mejor_score = buscar_mejor_politica(
        estados=estados,
        acciones_disponibles=acciones_disponibles,
        estado_inicial="inicio",
        transicion=transicion,
        recompensa=recompensa,
        intentos=20,
        pasos_max=10
    )

    print("\n==========================")
    print("MEJOR POLITICA ENCONTRADA")
    print("==========================")

    for estado in mejor_politica:
        print(
            estado,
            "->",
            mejor_politica[estado]
        )

    print("\nrecompensa total:", mejor_score)

    # resumen:
    # - una politica dice que hacer en cada estado
    # - aqui probamos muchas politicas distintas
    # - simulamos su rendimiento
    # - elegimos la que obtuvo mayor recompensa
    # - esto es una forma simple de busqueda de politica