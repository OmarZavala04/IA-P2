# búsqueda con vuelta atrás
#
# también conocida como:
# backtracking
#
# este algoritmo construye
# una solución paso a paso
#
# funcionamiento:
#
# - intenta asignar valores
# - verifica restricciones
# - si algo falla:
#   regresa y prueba otra opción
#
# esto evita continuar
# con soluciones inválidas
#
# es muy utilizado
# en problemas CSP
# (problemas de satisfacción
# de restricciones)


def validar_restricciones(
    asignacion,
    restricciones
):

    """
    asignacion:
        valores asignados actualmente

    restricciones:
        reglas del problema

    retorna:
        True si la asignación es válida
        False si existe conflicto
    """

    for regla in restricciones:

        if not regla(asignacion):

            return False

    return True


def algoritmo_backtracking(
    variables,
    dominios,
    restricciones,
    asignacion_actual=None
):

    """
    variables:
        lista de variables

    dominios:
        valores posibles
        para cada variable

    restricciones:
        reglas que deben cumplirse

    asignacion_actual:
        decisiones realizadas
        hasta el momento

    retorna:
        solución válida
        o None
    """

    if asignacion_actual is None:

        asignacion_actual = {}

    # si todas las variables
    # ya tienen valor
    # entonces terminamos
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

    # probar cada valor posible
    for valor in dominios[pendiente]:

        nueva_asignacion = (
            asignacion_actual.copy()
        )

        nueva_asignacion[pendiente] = valor

        # validar restricciones
        if validar_restricciones(
            nueva_asignacion,
            restricciones
        ):

            resultado = algoritmo_backtracking(
                variables,
                dominios,
                restricciones,
                nueva_asignacion
            )

            # si la solución funcionó
            # regresar resultado
            if resultado is not None:

                return resultado

        # si falla:
        # el algoritmo regresa
        # automáticamente aquí
        # y prueba otro valor

    # si ningún valor funciona
    # no existe solución
    return None


if __name__ == "__main__":

    # ejemplo:
    # asignación de horarios
    # para exámenes

    variables = [

        "mate",

        "fisica",

        "programacion"
    ]

    # días disponibles

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

    solucion = algoritmo_backtracking(
        variables,
        dominios,
        restricciones
    )

    print("solución encontrada:")
    print(solucion)

    # explicación:
    #
    # 1. asigna valor a una variable
    #
    # 2. verifica restricciones
    #
    # 3. si algo falla:
    #    regresa al paso anterior
    #
    # 4. prueba otra posibilidad
    #
    # resumen:
    #
    # - backtracking explora
    #   combinaciones válidas
    #
    # - evita continuar
    #   caminos incorrectos
    #
    # - cuando una decisión falla
    #   el algoritmo retrocede