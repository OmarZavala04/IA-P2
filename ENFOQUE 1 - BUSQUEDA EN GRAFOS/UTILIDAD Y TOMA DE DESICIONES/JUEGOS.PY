# teoria de juegos: equilibrios y mecanismos
# en teoria de juegos hay varios jugadores.
# cada jugador escoge una accion/estrategia.
# lo que ganas depende de lo que haces tu y lo que hace el otro.
# equilibrio de nash:
# una combinacion de estrategias donde
# ningun jugador gana mas cambiando SOLO su propia estrategia.

def mejor_respuesta_para_a(eleccion_b, estrategias, pagos):

    # aqui guardamos todas las mejores respuestas posibles
    # porque puede haber empate
    mejores = []

    # empezamos con utilidad muy baja
    mejor_utilidad = float("-inf")

    for opcion_a in estrategias:

        utilidad_a, _ = pagos[opcion_a][eleccion_b]

        # si encontramos algo mejor
        if utilidad_a > mejor_utilidad:

            mejor_utilidad = utilidad_a

            # reiniciamos lista
            mejores = [opcion_a]

        # si empata con la mejor utilidad
        elif utilidad_a == mejor_utilidad:

            mejores.append(opcion_a)

    return mejores


def mejor_respuesta_para_b(eleccion_a, estrategias, pagos):

    mejores = []

    mejor_utilidad = float("-inf")

    for opcion_b in estrategias:

        _, utilidad_b = pagos[eleccion_a][opcion_b]

        if utilidad_b > mejor_utilidad:

            mejor_utilidad = utilidad_b

            mejores = [opcion_b]

        elif utilidad_b == mejor_utilidad:

            mejores.append(opcion_b)

    return mejores


def es_equilibrio_de_nash(a_juega, b_juega, estrategias, pagos):

    # mejores respuestas posibles de cada jugador
    mejores_a = mejor_respuesta_para_a(
        b_juega,
        estrategias,
        pagos
    )

    mejores_b = mejor_respuesta_para_b(
        a_juega,
        estrategias,
        pagos
    )

    # para ser equilibrio:
    # ambos deben estar jugando una mejor respuesta
    return (a_juega in mejores_a) and (b_juega in mejores_b)


if __name__ == "__main__":

    # estrategias posibles
    estrategias = [
        "cooperar",
        "traicionar"
    ]

    # pagos[a][b] = (utilidad_a, utilidad_b)

    pagos = {

        "cooperar": {

            "cooperar": (-1, -1),

            "traicionar": (-10, 0)

        },

        "traicionar": {

            "cooperar": (0, -10),

            "traicionar": (-5, -5)

        }
    }

    print("\nRESULTADOS:\n")

    # probamos todas las combinaciones posibles
    for a_juega in estrategias:

        for b_juega in estrategias:

            util_a, util_b = pagos[a_juega][b_juega]

            equilibrio = es_equilibrio_de_nash(
                a_juega,
                b_juega,
                estrategias,
                pagos
            )

            print(
                "A:",
                a_juega,
                "| B:",
                b_juega,
                "| utilidad A:",
                util_a,
                "| utilidad B:",
                util_b,
                "| equilibrio de nash?:",
                equilibrio
            )

    print("\nMEJORES RESPUESTAS:\n")

    # mostramos mejores respuestas de A
    for accion_b in estrategias:

        print(
            "si B juega",
            accion_b,
            "-> mejores respuestas de A:",
            mejor_respuesta_para_a(
                accion_b,
                estrategias,
                pagos
            )
        )

    print()

    # mostramos mejores respuestas de B
    for accion_a in estrategias:

        print(
            "si A juega",
            accion_a,
            "-> mejores respuestas de B:",
            mejor_respuesta_para_b(
                accion_a,
                estrategias,
                pagos
            )
        )