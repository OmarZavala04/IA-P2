# q-learning para un videojuego simple
# el personaje aprende que camino tomar
# para conseguir monedas y evitar trampas.
#
# Q[zona][accion] =
# que tan buena parece esa accion en esa zona.
#
# el personaje aprende jugando muchas veces.

import random


def escoger_movimiento(
    tabla_q,
    zona_actual,
    caminos,
    prob_random
):
    """
    escoge una accion usando e-greedy:
    - a veces explora
    - a veces usa lo mejor conocido
    """

    if len(caminos[zona_actual]) == 0:
        return None

    # explorar
    if random.random() < prob_random:
        return random.choice(
            caminos[zona_actual]
        )

    # usar mejor accion conocida
    mejor = None
    mejor_q = None

    for movimiento in caminos[zona_actual]:

        valor = tabla_q[zona_actual][movimiento]

        if (
            mejor is None or
            valor > mejor_q
        ):
            mejor = movimiento
            mejor_q = valor

    return mejor


def mejor_q_futuro(
    tabla_q,
    zona,
    caminos
):
    """
    obtiene el mejor valor Q posible
    desde una zona.
    """

    if len(caminos[zona]) == 0:
        return 0

    mejor = None

    for movimiento in caminos[zona]:

        valor = tabla_q[zona][movimiento]

        if (
            mejor is None or
            valor > mejor
        ):
            mejor = valor

    return mejor


def entrenar_jugador(
    zonas,
    caminos,
    mover,
    recompensa,
    inicio,
    alpha,
    gamma,
    exploracion,
    partidas
):
    """
    entrena al personaje muchas veces
    para que aprenda buenas decisiones.
    """

    # crear tabla Q
    tabla_q = {}

    for zona in zonas:

        tabla_q[zona] = {}

        for movimiento in caminos[zona]:

            tabla_q[zona][movimiento] = 0.0

    # entrenamiento
    for _ in range(partidas):

        zona_actual = inicio

        while True:

            accion = escoger_movimiento(
                tabla_q,
                zona_actual,
                caminos,
                exploracion
            )

            # zona final
            if accion is None:
                break

            siguiente = mover(
                zona_actual,
                accion
            )

            premio = recompensa(
                zona_actual,
                accion,
                siguiente
            )

            mejor_futuro = mejor_q_futuro(
                tabla_q,
                siguiente,
                caminos
            )

            valor_viejo = tabla_q[zona_actual][accion]

            # formula q-learning
            nuevo_valor = valor_viejo + alpha * (
                premio +
                gamma * mejor_futuro -
                valor_viejo
            )

            tabla_q[zona_actual][accion] = nuevo_valor

            zona_actual = siguiente

    return tabla_q


def mejor_camino(tabla_q, caminos):
    """
    obtiene la mejor accion
    en cada zona.
    """

    politica = {}

    for zona in caminos:

        if len(caminos[zona]) == 0:

            politica[zona] = None

        else:

            mejor_accion = None
            mejor_valor = None

            for accion in caminos[zona]:

                valor = tabla_q[zona][accion]

                if (
                    mejor_accion is None or
                    valor > mejor_valor
                ):
                    mejor_accion = accion
                    mejor_valor = valor

            politica[zona] = mejor_accion

    return politica


if __name__ == "__main__":

    # mapa del juego
    zonas = [
        "inicio",
        "cueva",
        "tesoro"
    ]

    # movimientos posibles
    caminos = {

        "inicio": [
            "entrar_cueva"
        ],

        "cueva": [
            "abrir_puerta"
        ],

        "tesoro": []
    }

    def mover(zona, accion):

        if zona == "inicio" and accion == "entrar_cueva":
            return "cueva"

        if zona == "cueva" and accion == "abrir_puerta":
            return "tesoro"

        return zona

    def recompensa(
        zona,
        accion,
        siguiente
    ):

        # premio al encontrar tesoro
        if siguiente == "tesoro":

            # variacion aleatoria
            return random.randint(15, 25)

        # pequeño costo por caminar
        return -1

    tabla_q = entrenar_jugador(
        zonas=zonas,
        caminos=caminos,
        mover=mover,
        recompensa=recompensa,
        inicio="inicio",
        alpha=0.5,
        gamma=0.9,
        exploracion=0.3,
        partidas=40
    )

    print("tabla q aprendida:")

    for zona in tabla_q:

        for accion in tabla_q[zona]:

            print(
                zona,
                ",",
                accion,
                "->",
                tabla_q[zona][accion]
            )

    politica = mejor_camino(
        tabla_q,
        caminos
    )

    print("\nmejor accion en cada zona:")

    for zona in politica:

        print(
            zona,
            "->",
            politica[zona]
        )

    # el personaje:
    # - explora caminos
    # - aprende recompensas
    # - ajusta la tabla Q
    # - termina aprendiendo
    #   las mejores decisiones