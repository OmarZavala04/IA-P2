# propagación de restricciones
#
# esta técnica intenta
# eliminar valores imposibles
# antes de realizar
# toda la búsqueda
#
# idea principal:
#
# si un valor ya no puede
# cumplir restricciones
# se elimina del dominio
#
# esto reduce:
#
# - prueba y error
# - combinaciones inútiles
# - tiempo de búsqueda
#
# en este ejemplo
# usamos una versión
# del algoritmo AC-3
#
# AC-3:
# consistencia de arcos
#
# revisa pares de variables
# y elimina valores incompatibles

from collections import deque


def son_compatibles(
    variable_x,
    valor_x,
    variable_y,
    dominio_y,
    restriccion_binaria
):

    """
    verifica si un valor de X
    puede combinarse
    con al menos un valor de Y
    """

    for valor_y in dominio_y:

        if restriccion_binaria(
            variable_x,
            valor_x,
            variable_y,
            valor_y
        ):

            return True

    return False


def revisar_arco(
    variable_x,
    variable_y,
    dominios,
    restriccion_binaria
):

    """
    limpia el dominio de X
    usando información de Y

    retorna:
        True si hubo cambios
        False si no cambió nada
    """

    dominio_x = dominios[variable_x]

    dominio_y = dominios[variable_y]

    eliminar = []

    for valor_x in dominio_x:

        compatible = son_compatibles(
            variable_x,
            valor_x,
            variable_y,
            dominio_y,
            restriccion_binaria
        )

        if not compatible:

            eliminar.append(valor_x)

    # eliminar valores inválidos
    if eliminar:

        for valor in eliminar:

            dominio_x.remove(valor)

        return True

    return False


def algoritmo_ac3(
    variables,
    dominios,
    vecinos,
    restriccion_binaria
):

    """
    variables:
        variables del problema

    dominios:
        valores posibles

    vecinos:
        variables conectadas

    restriccion_binaria:
        regla entre pares
        de variables

    retorna:
        True si es consistente
        False si algún dominio
        queda vacío
    """

    cola = deque()

    # agregar todos los arcos
    for x in variables:

        for y in vecinos[x]:

            cola.append((x, y))

    # procesar cola
    while cola:

        x, y = cola.popleft()

        cambio = revisar_arco(
            x,
            y,
            dominios,
            restriccion_binaria
        )

        # si hubo cambios
        if cambio:

            # dominio vacío
            # significa imposible
            if len(dominios[x]) == 0:

                return False

            # volver a revisar vecinos
            for z in vecinos[x]:

                if z != y:

                    cola.append((z, x))

    return True


if __name__ == "__main__":

    # ejemplo:
    # coloreo de mapas

    variables = [

        "a",

        "b",

        "c"
    ]

    dominios = {

        "a": [
            "rojo",
            "verde"
        ],

        "b": [
            "rojo",
            "verde"
        ],

        "c": [
            "rojo",
            "verde"
        ]
    }

    # conexiones:
    #
    # a conectado con b
    # b conectado con a y c
    # c conectado con b

    vecinos = {

        "a": ["b"],

        "b": [
            "a",
            "c"
        ],

        "c": ["b"]
    }

    # regla:
    # vecinos no pueden
    # compartir color

    def restriccion_binaria(
        x,
        valor_x,
        y,
        valor_y
    ):

        if (
            (x == "a" and y == "b")
            or
            (x == "b" and y == "a")
        ):

            return valor_x != valor_y

        if (
            (x == "b" and y == "c")
            or
            (x == "c" and y == "b")
        ):

            return valor_x != valor_y

        return True

    consistente = algoritmo_ac3(
        variables,
        dominios,
        vecinos,
        restriccion_binaria
    )

    print("¿es consistente?:")
    print(consistente)

    print("\ndominios finales:")

    for variable in variables:

        print(
            variable,
            "->",
            dominios[variable]
        )

    # explicación:
    #
    # - AC-3 revisa pares
    #   de variables
    #
    # - elimina valores
    #   incompatibles
    #
    # - si un dominio queda vacío:
    #   no existe solución
    #
    # ventaja:
    #
    # reduce combinaciones
    # antes de buscar
    #
    # esto hace más eficiente
    # el problema CSP