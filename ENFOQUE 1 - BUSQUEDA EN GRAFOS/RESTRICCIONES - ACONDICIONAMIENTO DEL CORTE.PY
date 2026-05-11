# acondicionamiento del corte
#
# esta técnica se utiliza
# en problemas con restricciones
# muy conectadas entre sí
#
# algunas variables generan
# más conflictos que otras
#
# idea principal:
#
# 1. elegir variables problemáticas
# 2. fijar primero sus valores
# 3. resolver el resto normalmente
#
# esto divide el problema grande
# en subproblemas más simples


def validar_asignacion(
    asignacion,
    restricciones
):

    """
    asignacion:
        valores actuales asignados

    restricciones:
        lista de reglas

    retorna:
        True si todo es válido
        False si existe conflicto
    """

    for regla in restricciones:

        if not regla(asignacion):
            return False

    return True


def backtracking_basico(
    variables,
    dominios,
    restricciones,
    asignacion_actual=None
):

    """
    variables:
        variables pendientes

    dominios:
        valores posibles

    restricciones:
        reglas del problema

    asignacion_actual:
        asignaciones realizadas

    retorna:
        solución válida
        o None
    """

    if asignacion_actual is None:
        asignacion_actual = {}

    # verificar solución completa
    if (
        len(asignacion_actual)
        == len(variables)
    ):

        if validar_asignacion(
            asignacion_actual,
            restricciones
        ):

            return asignacion_actual.copy()

        return None

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

        # validar parcialmente
        if validar_asignacion(
            nueva_asignacion,
            restricciones
        ):

            resultado = backtracking_basico(
                variables,
                dominios,
                restricciones,
                nueva_asignacion
            )

            if resultado is not None:
                return resultado

    return None


def generar_combinaciones_cutset(
    variables_cutset,
    dominios,
    restricciones,
    base=None
):

    """
    variables_cutset:
        variables críticas

    dominios:
        valores posibles

    restricciones:
        reglas del problema

    base:
        asignación parcial

    retorna:
        lista de combinaciones válidas
    """

    if base is None:
        base = {}

    # si todas las variables
    # del cutset ya fueron asignadas
    if (
        len(base)
        == len(variables_cutset)
    ):

        if validar_asignacion(
            base,
            restricciones
        ):

            return [base.copy()]

        return []

    indice = len(base)

    variable_actual = (
        variables_cutset[indice]
    )

    resultados = []

    for valor in dominios[variable_actual]:

        nueva = base.copy()

        nueva[variable_actual] = valor

        # validar combinación parcial
        if validar_asignacion(
            nueva,
            restricciones
        ):

            siguientes = generar_combinaciones_cutset(
                variables_cutset,
                dominios,
                restricciones,
                nueva
            )

            resultados.extend(siguientes)

    return resultados


def condicionamiento_cutset(
    variables,
    dominios,
    restricciones,
    variables_cutset
):

    """
    variables:
        todas las variables

    dominios:
        valores permitidos

    restricciones:
        reglas del problema

    variables_cutset:
        variables conflictivas
        que se fijan primero

    retorna:
        solución válida
        o None
    """

    # generar opciones válidas
    # para las variables críticas
    opciones_cutset = (
        generar_combinaciones_cutset(
            variables_cutset,
            dominios,
            restricciones
        )
    )

    # resolver el resto
    for asignacion_cutset in opciones_cutset:

        restantes = [

            v
            for v in variables

            if v not in asignacion_cutset
        ]

        solucion = backtracking_basico(
            restantes,
            dominios,
            restricciones,
            asignacion_cutset.copy()
        )

        if solucion is not None:
            return solucion

    return None


if __name__ == "__main__":

    # variables del problema
    #
    # ejemplo:
    # materias de exámenes

    variables = [
        "mate",
        "fisica",
        "programacion"
    ]

    # dominios posibles
    #
    # días disponibles

    dominios = {

        "mate": [
            "lunes",
            "miercoles",
            "viernes"
        ],

        "fisica": [
            "lunes",
            "miercoles",
            "viernes"
        ],

        "programacion": [
            "lunes",
            "miercoles",
            "viernes"
        ]
    }

    # restricción:
    # no repetir día

    def regla_dias_distintos(
        asignacion
    ):

        dias = list(
            asignacion.values()
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

        regla_dias_distintos,

        regla_programacion
    ]

    # variables críticas
    #
    # se resolverán primero

    variables_cutset = [
        "mate"
    ]

    solucion = condicionamiento_cutset(
        variables=variables,
        dominios=dominios,
        restricciones=restricciones,
        variables_cutset=variables_cutset
    )

    print("solución encontrada:")
    print(solucion)

    # resumen:
    #
    # - las variables del cutset
    #   se asignan primero
    #
    # - después se resuelve
    #   el resto del problema
    #
    # - esto divide el problema
    #   en partes más simples
    #
    # - útil en CSP complejos