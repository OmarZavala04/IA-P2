# Mdp proceso de decision de markov
# un mdp describe una decision por pasos:
# - tengo un estado actual
# - elijo una accion
# - recibo una recompensa
# - paso a un nuevo estado (con cierta probabilidad)
# meta:
# elegir una politica (que accion tomar en cada estado)
# para maximizar la recompensa total esperada a largo plazo.

def iteracion_de_valores_mdp(
    estados,
    acciones_por_estado,
    transicion_prob,
    recompensa,
    descuento,
    pasos_max
):
    """
    iteracion de valores para mdp con transiciones probabilisticas
    """

    # valores iniciales
    valores = {}

    for estado in estados:
        valores[estado] = 0

    # repetimos actualizacion
    for paso in range(pasos_max):

        nuevos_valores = {}

        print("\npaso de iteracion:", paso + 1)

        for estado in estados:

            acciones = acciones_por_estado[estado]

            # estado terminal
            if len(acciones) == 0:

                nuevos_valores[estado] = 0

                print(
                    " estado",
                    estado,
                    "es terminal -> valor = 0"
                )

            else:

                mejor_valor = None

                # probamos cada accion
                for accion in acciones:

                    recompensa_inmediata = recompensa(
                        estado,
                        accion
                    )

                    valor_futuro = 0

                    # suma(probabilidad * valor_estado_siguiente)
                    for siguiente_estado, probabilidad in transicion_prob(
                        estado,
                        accion
                    ):

                        valor_futuro += (
                            probabilidad *
                            valores[siguiente_estado]
                        )

                    # q-valor esperado
                    q_valor = (
                        recompensa_inmediata +
                        descuento * valor_futuro
                    )

                    print(
                        " estado:",
                        estado,
                        "| accion:",
                        accion,
                        "| q:",
                        q_valor
                    )

                    # guardamos mejor accion
                    if (
                        mejor_valor is None or
                        q_valor > mejor_valor
                    ):
                        mejor_valor = q_valor

                nuevos_valores[estado] = mejor_valor

        valores = nuevos_valores

        print(" valores actuales:", valores)

    return valores


def politica_optima_mdp(
    estados,
    acciones_por_estado,
    transicion_prob,
    recompensa,
    descuento,
    valores
):
    """
    calcula la mejor accion para cada estado
    """

    politica = {}

    for estado in estados:

        acciones = acciones_por_estado[estado]

        # estado terminal
        if len(acciones) == 0:

            politica[estado] = None

        else:

            mejor_accion = None
            mejor_q = None

            # evaluamos acciones
            for accion in acciones:

                recompensa_inmediata = recompensa(
                    estado,
                    accion
                )

                valor_futuro = 0

                for siguiente_estado, probabilidad in transicion_prob(
                    estado,
                    accion
                ):

                    valor_futuro += (
                        probabilidad *
                        valores[siguiente_estado]
                    )

                q_valor = (
                    recompensa_inmediata +
                    descuento * valor_futuro
                )

                print(
                    "politica -> estado:",
                    estado,
                    "| accion:",
                    accion,
                    "| q:",
                    q_valor
                )

                if (
                    mejor_accion is None or
                    q_valor > mejor_q
                ):
                    mejor_accion = accion
                    mejor_q = q_valor

            politica[estado] = mejor_accion

    return politica


if __name__ == "__main__":

    # estados posibles
    estados = ["a", "b", "c"]

    # acciones posibles en cada estado
    acciones_por_estado = {
        "a": ["ir_b", "ir_c"],
        "b": ["ir_c"],
        "c": []
    }

    # transiciones probabilisticas
    def transicion_prob(estado, accion):

        # desde a a b
        if estado == "a" and accion == "ir_b":

            # 80% llego a b
            # 20% fallo y termino en c
            return [
                ("b", 0.8),
                ("c", 0.2)
            ]

        # desde a directo a c
        if estado == "a" and accion == "ir_c":

            return [
                ("c", 1.0)
            ]

        # desde b a c
        if estado == "b" and accion == "ir_c":

            return [
                ("c", 1.0)
            ]

        # estado terminal
        if estado == "c":

            return [
                ("c", 1.0)
            ]

        # fallback
        return [
            (estado, 1.0)
        ]

    # recompensas inmediatas
    def recompensa(estado, accion):

        if estado == "a" and accion == "ir_b":
            return 5

        if estado == "a" and accion == "ir_c":
            return 10

        if estado == "b" and accion == "ir_c":
            return 2

        return 0

    # descuento del futuro
    descuento = 0.9

    # calculamos valores
    valores = iteracion_de_valores_mdp(
        estados,
        acciones_por_estado,
        transicion_prob,
        recompensa,
        descuento,
        pasos_max=10
    )

    print("\nvalores finales:")
    for estado in estados:
        print(
            estado,
            "->",
            valores[estado]
        )

    # calculamos politica optima
    politica = politica_optima_mdp(
        estados,
        acciones_por_estado,
        transicion_prob,
        recompensa,
        descuento,
        valores
    )

    print("\npolitica optima:")

    for estado in estados:
        print(
            estado,
            "->",
            politica[estado]
        )

    # - mdp usa probabilidades en las transiciones
    # - iteracion de valores calcula que tan bueno es cada estado
    # - politica optima escoge la accion con mejor valor esperado