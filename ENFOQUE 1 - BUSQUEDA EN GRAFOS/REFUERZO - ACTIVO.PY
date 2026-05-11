# aprendizaje por refuerzo activo
# aqui el agente SI decide que accion tomar.
# aprende probando acciones y viendo recompensas.
#
# escenario:
# un robot explorador busca baterias en una estacion espacial.
#
# puede:
# - avanzar
# - tomar atajo
#
# algunas rutas dan mas energia
# pero otras pueden fallar.

import random


def elegir_accion(
    tabla_q,
    lugar,
    acciones,
    epsilon
):
    """
    estrategia e-greedy:
    - a veces explora
    - a veces usa lo mejor aprendido
    """

    if random.random() < epsilon:
        return random.choice(
            acciones[lugar]
        )

    mejor_accion = None
    mejor_valor = None

    for accion in acciones[lugar]:

        valor = tabla_q[lugar][accion]

        if (
            mejor_accion is None or
            valor > mejor_valor
        ):
            mejor_accion = accion
            mejor_valor = valor

    return mejor_accion


def mejor_q(
    tabla_q,
    lugar,
    acciones
):
    """
    obtiene el mejor valor futuro posible
    desde un lugar.
    """

    if len(acciones[lugar]) == 0:
        return 0

    mejor = None

    for accion in acciones[lugar]:

        valor = tabla_q[lugar][accion]

        if (
            mejor is None or
            valor > mejor
        ):
            mejor = valor

    return mejor


def mover(
    lugar,
    accion
):
    """
    define a donde llega el robot
    segun la accion.
    """

    if lugar == "inicio":

        if accion == "camino_seguro":
            return "pasillo"

        if accion == "atajo":
            # el atajo puede fallar
            if random.random() < 0.5:
                return "trampa"

            return "energia"

    if lugar == "pasillo":
        return "energia"

    return "final"


def recompensa(
    siguiente
):
    """
    recompensa segun el lugar alcanzado.
    """

    tabla = {

        "pasillo": 2,

        # gran premio
        "energia": 20,

        # mala decision
        "trampa": -15,

        "final": 0
    }

    return tabla.get(
        siguiente,
        0
    )


def entrenar_robot(
    estados,
    acciones,
    inicio,
    episodios,
    alpha,
    gamma,
    epsilon
):
    """
    entrena al robot usando q-learning.
    """

    # tabla Q inicial
    tabla_q = {}

    for estado in estados:

        tabla_q[estado] = {}

        for accion in acciones[estado]:

            tabla_q[estado][accion] = 0.0

    # entrenamiento
    for _ in range(episodios):

        lugar_actual = inicio

        while lugar_actual != "final":

            if len(acciones[lugar_actual]) == 0:
                break

            accion = elegir_accion(
                tabla_q,
                lugar_actual,
                acciones,
                epsilon
            )

            siguiente = mover(
                lugar_actual,
                accion
            )

            r = recompensa(
                siguiente
            )

            valor_viejo = tabla_q[lugar_actual][accion]

            mejor_futuro = mejor_q(
                tabla_q,
                siguiente,
                acciones
            )

            # formula q-learning
            nuevo_valor = valor_viejo + alpha * (
                r +
                gamma * mejor_futuro -
                valor_viejo
            )

            tabla_q[lugar_actual][accion] = nuevo_valor

            lugar_actual = siguiente

    return tabla_q


def politica_final(
    tabla_q,
    acciones
):
    """
    obtiene la mejor accion
    en cada estado.
    """

    politica = {}

    for estado in acciones:

        if len(acciones[estado]) == 0:

            politica[estado] = None

        else:

            mejor_accion = None
            mejor_valor = None

            for accion in acciones[estado]:

                valor = tabla_q[estado][accion]

                if (
                    mejor_accion is None or
                    valor > mejor_valor
                ):
                    mejor_accion = accion
                    mejor_valor = valor

            politica[estado] = mejor_accion

    return politica


if __name__ == "__main__":

    estados = [
        "inicio",
        "pasillo",
        "energia",
        "trampa",
        "final"
    ]

    acciones = {

        "inicio": [
            "camino_seguro",
            "atajo"
        ],

        "pasillo": [
            "seguir"
        ],

        "energia": [],

        "trampa": [],

        "final": []
    }

    tabla_q = entrenar_robot(
        estados=estados,
        acciones=acciones,
        inicio="inicio",
        episodios=80,
        alpha=0.5,
        gamma=0.9,
        epsilon=0.3
    )

    print("tabla q aprendida:\n")

    for estado in tabla_q:

        for accion in tabla_q[estado]:

            print(
                estado,
                ",",
                accion,
                "->",
                tabla_q[estado][accion]
            )

    politica = politica_final(
        tabla_q,
        acciones
    )

    print("\nmejor accion aprendida:\n")

    for estado in politica:

        print(
            estado,
            "->",
            politica[estado]
        )

    # el robot:
    # - prueba acciones
    # - recibe recompensas
    # - aprende de experiencia
    # - termina descubriendo
    #   que acciones convienen mas