# problemas de satisfacción
# de restricciones
#
# también llamados:
# CSP
#
# un CSP tiene:
#
# - variables
# - dominios
# - restricciones
#
# variables:
# cosas que debo decidir
#
# dominios:
# valores posibles
# para cada variable
#
# restricciones:
# reglas que deben cumplirse
#
# ejemplos reales:
#
# - horarios
# - sudoku
# - asignación de salones
# - coloreo de mapas
# - distribución de tareas
#
# ejemplo:
# organizar exámenes


def validar_restricciones(
    asignacion,
    restricciones
):

    """
    asignacion:
        decisiones actuales

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


def resolver_csp(
    variables,
    dominios,
    restricciones,
    asignacion_actual=None
):

    """
    variables:
        variables del problema

    dominios:
        valores posibles

    restricciones:
        reglas que deben cumplirse

    asignacion_actual:
        decisiones tomadas
        hasta el momento

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

        return asignacion_actual

    # buscar variable pendiente
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

        # validar restricciones
        if validar_restricciones(
            nueva_asignacion,
            restricciones
        ):

            resultado = resolver_csp(
                variables,
                dominios,
                restricciones,
                nueva_asignacion
            )

            if resultado is not None:

                return resultado

    # si ningún valor funciona
    return None


if __name__ == "__main__":

    # variables:
    # materias

    variables = [

        "mate",

        "fisica",

        "programacion"
    ]

    # dominios:
    # días posibles

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
    # no repetir día

    def regla_dias_distintos(
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

        regla_dias_distintos,

        regla_programacion
    ]

    solucion = resolver_csp(
        variables,
        dominios,
        restricciones
    )

    print("horario encontrado:")

    print(solucion)

    # ejemplo posible:
    #
    # {
    #   "mate": "lunes",
    #   "fisica": "miercoles",
    #   "programacion": "viernes"
    # }
    #
    # explicación:
    #
    # - cada variable recibe un valor
    #
    # - el algoritmo prueba opciones
    #
    # - si una regla falla:
    #   intenta otra combinación
    #
    # resumen:
    #
    # - variables:
    #   lo que debo decidir
    #
    # - dominios:
    #   opciones posibles
    #
    # - restricciones:
    #   reglas obligatorias
    #
    # - el algoritmo busca
    #   una combinación válida