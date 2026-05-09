# Iteracion de politicas
# una politica dice que accion tomar en cada estado

def evaluar_politica(
    estados,
    politica,
    acciones_por_estado,
    transicion,
    recompensa,
    descuento,
    pasos_eval
):
    """
    calcula el valor de cada estado
    siguiendo la politica actual
    """

    # iniciar todos los valores en 0
    valores = {}

    for estado in estados:
        valores[estado] = 0

    # aproximacion iterativa
    for _ in range(pasos_eval):

        nuevos_valores = {}

        for estado in estados:

            accion = politica[estado]

            # estado terminal
            if accion is None:

                nuevos_valores[estado] = 0

            else:

                siguiente_estado = transicion(
                    estado,
                    accion
                )

                recompensa_actual = recompensa(
                    estado,
                    accion
                )

                # ecuacion de bellman para politica fija
                valor = (
                    recompensa_actual
                    +
                    descuento
                    *
                    valores[siguiente_estado]
                )

                nuevos_valores[estado] = valor

        valores = nuevos_valores

    return valores


def mejorar_politica(
    estados,
    acciones_por_estado,
    transicion,
    recompensa,
    descuento,
    valores_actuales
):
    """
    intenta mejorar la politica actual
    escogiendo la mejor accion en cada estado
    """

    nueva_politica = {}

    for estado in estados:

        acciones = acciones_por_estado[estado]

        # estado terminal
        if len(acciones) == 0:

            nueva_politica[estado] = None

        else:

            mejor_accion = None
            mejor_score = None

            # probar todas las acciones
            for accion in acciones:

                siguiente_estado = transicion(
                    estado,
                    accion
                )

                recompensa_actual = recompensa(
                    estado,
                    accion
                )

                score = (
                    recompensa_actual
                    +
                    descuento
                    *
                    valores_actuales[siguiente_estado]
                )

                if (
                    mejor_accion is None
                    or
                    score > mejor_score
                ):

                    mejor_accion = accion
                    mejor_score = score

            nueva_politica[estado] = mejor_accion

    return nueva_politica


def politicas_iguales(
    politica_1,
    politica_2
):
    """
    revisa si dos politicas son iguales
    """

    for estado in politica_1:

        if politica_1[estado] != politica_2[estado]:
            return False

    return True


def iteracion_de_politicas(
    estados,
    acciones_por_estado,
    transicion,
    recompensa,
    descuento,
    pasos_eval,
    pasos_mejora
):
    """
    alterna:
    1) evaluar politica
    2) mejorar politica
    """

    # politica inicial simple
    politica = {}

    for estado in estados:

        acciones = acciones_por_estado[estado]

        if len(acciones) == 0:

            politica[estado] = None

        else:

            politica[estado] = acciones[0]

    # ciclo principal
    for _ in range(pasos_mejora):

        # evaluar politica actual
        valores = evaluar_politica(
            estados,
            politica,
            acciones_por_estado,
            transicion,
            recompensa,
            descuento,
            pasos_eval
        )

        # mejorar politica
        nueva_politica = mejorar_politica(
            estados,
            acciones_por_estado,
            transicion,
            recompensa,
            descuento,
            valores
        )

        # si ya no cambia, terminar
        if politicas_iguales(
            politica,
            nueva_politica
        ):

            return (
                nueva_politica,
                valores
            )

        politica = nueva_politica

    return politica, valores


if __name__ == "__main__":

    # estados del problema
    estados = [
        "a",
        "b",
        "c"
    ]

    # acciones posibles por estado
    acciones_por_estado = {
        "a": ["ir_b", "ir_c"],
        "b": ["ir_c"],
        "c": []
    }

    # funcion de transicion
    def transicion(estado, accion):

        if estado == "a" and accion == "ir_b":
            return "b"

        if estado == "a" and accion == "ir_c":
            return "c"

        if estado == "b" and accion == "ir_c":
            return "c"

        if estado == "c":
            return "c"

        return estado

    # recompensas inmediatas
    def recompensa(estado, accion):

        if estado == "a" and accion == "ir_b":
            return 5

        if estado == "a" and accion == "ir_c":
            return 10

        if estado == "b" and accion == "ir_c":
            return 2

        return 0

    descuento = 0.9

    politica_final, valores_finales = iteracion_de_politicas(
        estados,
        acciones_por_estado,
        transicion,
        recompensa,
        descuento,
        pasos_eval=10,
        pasos_mejora=10
    )

    print("politica final:")

    for estado in estados:

        print(
            estado,
            "->",
            politica_final[estado]
        )

    print("\nvalores finales:")

    for estado in estados:

        print(
            estado,
            "->",
            valores_finales[estado]
        )