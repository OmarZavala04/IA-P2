# búsqueda local:
# mínimos conflictos
#
# este algoritmo comienza
# con una asignación cualquiera
# aunque tenga errores
#
# después intenta corregir
# únicamente las variables
# que causan conflictos
#
# idea principal:
#
# - detectar problemas
# - modificar solo lo necesario
# - escoger el valor
#   que genere menos conflictos
#
# ventaja:
# funciona rápido
# en problemas grandes
#
# ejemplos:
#
# - horarios
# - sudoku
# - coloreo de mapas
# - asignación de tareas

import random


def calcular_conflictos(
    asignacion,
    restricciones
):

    """
    asignacion:
        valores actuales

    restricciones:
        reglas del problema

    retorna:
        número de conflictos
    """

    conflictos = 0

    for regla in restricciones:

        if not regla(asignacion):

            conflictos += 1

    return conflictos


def variables_conflictivas(
    asignacion,
    restricciones
):

    """
    detecta variables
    relacionadas con conflictos

    retorna:
        lista de variables problemáticas
    """

    problematicas = set()

    for regla in restricciones:

        if not regla(asignacion):

            for variable in asignacion:

                problematicas.add(variable)

    return list(problematicas)


def mejor_valor(
    variable,
    asignacion,
    dominios,
    restricciones
):

    """
    busca el valor
    que produzca menos conflictos
    """

    mejor_opcion = None

    menor_conflicto = None

    for valor in dominios[variable]:

        prueba = asignacion.copy()

        prueba[variable] = valor

        conflictos = calcular_conflictos(
            prueba,
            restricciones
        )

        if (
            mejor_opcion is None
            or conflictos < menor_conflicto
        ):

            mejor_opcion = valor

            menor_conflicto = conflictos

    return mejor_opcion


def algoritmo_minimos_conflictos(
    variables,
    dominios,
    restricciones,
    max_intentos,
    max_pasos
):

    """
    variables:
        variables del problema

    dominios:
        valores posibles

    restricciones:
        reglas que deben cumplirse

    max_intentos:
        reinicios máximos

    max_pasos:
        correcciones máximas
        por intento

    retorna:
        solución válida
        e historial
    """

    historial = []

    # varios intentos
    for _ in range(max_intentos):

        # crear asignación aleatoria
        asignacion = {}

        for variable in variables:

            asignacion[variable] = (
                random.choice(
                    dominios[variable]
                )
            )

        historial.append(
            asignacion.copy()
        )

        # intentar corregir conflictos
        for _ in range(max_pasos):

            # verificar solución
            if (
                calcular_conflictos(
                    asignacion,
                    restricciones
                ) == 0
            ):

                return (
                    asignacion,
                    historial
                )

            # detectar variables conflictivas
            conflictivas = variables_conflictivas(
                asignacion,
                restricciones
            )

            if not conflictivas:

                return (
                    asignacion,
                    historial
                )

            # escoger una variable problemática
            variable = random.choice(
                conflictivas
            )

            # buscar mejor valor
            nuevo_valor = mejor_valor(
                variable,
                asignacion,
                dominios,
                restricciones
            )

            # aplicar corrección
            asignacion[variable] = nuevo_valor

            historial.append(
                asignacion.copy()
            )

        # si falla:
        # reinicia automáticamente
        # con otra asignación aleatoria

    return None, historial


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
    # no repetir días

    def regla_dias_diferentes(
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

        regla_dias_diferentes,

        regla_programacion
    ]

    solucion, historial = (
        algoritmo_minimos_conflictos(
            variables=variables,
            dominios=dominios,
            restricciones=restricciones,
            max_intentos=10,
            max_pasos=20
        )
    )

    print("solución encontrada:")
    print(solucion)

    print("\nhistorial de cambios:")

    for paso, estado in enumerate(historial):

        print(
            "paso",
            paso,
            "->",
            estado
        )

    # resumen:
    #
    # - inicia con algo aleatorio
    #
    # - detecta conflictos
    #
    # - modifica solo variables problemáticas
    #
    # - escoge el valor
    #   que reduzca conflictos
    #
    # - si no funciona:
    #   reinicia desde cero
    #
    # - es búsqueda local
    #   no usa recursión