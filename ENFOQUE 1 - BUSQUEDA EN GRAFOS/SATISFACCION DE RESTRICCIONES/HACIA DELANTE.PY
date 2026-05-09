# comprobación hacia delante
#
# también conocida como:
# forward checking
#
# idea principal:
#
# cuando asigno un valor
# reviso inmediatamente
# si las demás variables
# todavía tienen opciones válidas
#
# si alguna variable
# se queda sin posibilidades:
# cancelo ese camino
# antes de seguir
#
# ventaja:
# detecta errores temprano
#
# diferencia:
#
# - backtracking normal:
#   descubre errores más tarde
#
# - forward checking:
#   revisa el futuro antes
#   de continuar


def validar_restricciones(
    asignacion,
    restricciones
):

    """
    asignacion:
        valores actuales

    restricciones:
        reglas del problema

    retorna:
        True si todo es válido
        False si existe conflicto
    """

    for regla in restricciones:

        if not regla(asignacion):

            return False

    return True


def filtrar_dominio(
    variable_objetivo,
    asignacion_parcial,
    dominios,
    restricciones
):

    """
    revisa qué valores
    siguen siendo posibles
    para una variable
    """

    valores_validos = []

    for valor in dominios[variable_objetivo]:

        prueba = (
            asignacion_parcial.copy()
        )

        prueba[variable_objetivo] = valor

        if validar_restricciones(
            prueba,
            restricciones
        ):

            valores_validos.append(valor)

    return valores_validos


def algoritmo_forward_checking(
    variables,
    dominios,
    restricciones,
    asignacion_actual=None
):

    """
    variables:
        variables del problema

    dominios:
        opciones posibles

    restricciones:
        reglas que deben cumplirse

    asignacion_actual:
        decisiones tomadas

    retorna:
        solución válida
        o None
    """

    if asignacion_actual is None:

        asignacion_actual = {}

    print(
        "asignación actual:",
        asignacion_actual
    )

    # verificar solución completa
    if (
        len(asignacion_actual)
        == len(variables)
    ):

        return asignacion_actual

    # seleccionar variable pendiente
    for variable in variables:

        if variable not in asignacion_actual:

            pendiente = variable

            break

    # probar valores posibles
    for valor in dominios[pendiente]:

        nueva_asignacion = (
            asignacion_actual.copy()
        )

        nueva_asignacion[pendiente] = valor

        print(
            " probando",
            pendiente,
            "=",
            valor
        )

        # verificar restricciones actuales
        if not validar_restricciones(
            nueva_asignacion,
            restricciones
        ):

            print(
                "  conflicto detectado"
            )

            continue

        consistente = True

        # comprobación hacia delante
        #
        # revisar si las variables
        # restantes aún tienen opciones
        for otra_variable in variables:

            if (
                otra_variable
                not in nueva_asignacion
            ):

                dominio_restante = (
                    filtrar_dominio(
                        otra_variable,
                        nueva_asignacion,
                        dominios,
                        restricciones
                    )
                )

                print(
                    "   dominio restante para",
                    otra_variable,
                    "->",
                    dominio_restante
                )

                # si no quedan opciones
                # este camino ya no sirve
                if len(dominio_restante) == 0:

                    print(
                        "   sin opciones para",
                        otra_variable
                    )

                    consistente = False

                    break

        # si falla:
        # probar otro valor
        if not consistente:

            continue

        # continuar búsqueda
        resultado = algoritmo_forward_checking(
            variables,
            dominios,
            restricciones,
            nueva_asignacion
        )

        if resultado is not None:

            return resultado

    return None


if __name__ == "__main__":

    # ejemplo:
    # horarios de exámenes

    variables = [

        "mate",

        "fisica",

        "programacion"
    ]

    dominios = {

        "mate": [
            "lunes",
            "miercoles"
        ],

        "fisica": [
            "lunes",
            "miercoles"
        ],

        "programacion": [
            "lunes",
            "miercoles"
        ]
    }

    # restricción:
    # no repetir días

    def regla_dias_unicos(
        asignacion
    ):

        dias = []

        for materia in asignacion:

            dias.append(
                asignacion[materia]
            )

        return (
            len(dias)
            == len(set(dias))
        )

    # restricción:
    # programación no puede ser lunes

    def regla_programacion(
        asignacion
    ):

        if "programacion" in asignacion:

            return (
                asignacion["programacion"]
                != "lunes"
            )

        return True

    restricciones = [

        regla_dias_unicos,

        regla_programacion
    ]

    solucion = algoritmo_forward_checking(
        variables,
        dominios,
        restricciones
    )

    print(
        "\nsolución encontrada:"
    )

    print(solucion)

    print("\nproceso terminado")

    # resumen:
    #
    # - asigna valores paso a paso
    #
    # - revisa restricciones actuales
    #
    # - revisa si el futuro
    #   sigue teniendo opciones
    #
    # - si una variable
    #   se queda sin valores:
    #   cancela ese camino
    #
    # - suele ser más rápido
    #   que backtracking puro