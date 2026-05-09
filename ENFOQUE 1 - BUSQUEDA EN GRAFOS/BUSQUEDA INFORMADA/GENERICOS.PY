# algoritmos genéticos
#
# este método de búsqueda
# trabaja con muchas soluciones
# al mismo tiempo
#
# la idea principal es:
#
# - generar soluciones iniciales
# - evaluar cuáles son mejores
# - combinar las mejores
# - aplicar pequeñas mutaciones
# - repetir el proceso
#
# está inspirado en
# conceptos de evolución biológica
#
# se utiliza cuando:
# no conocemos la solución exacta
# pero sí podemos medir
# qué tan buena es


import random


def generar_individuo(
    longitud
):

    """
    longitud:
        cantidad de genes

    retorna:
        una solución aleatoria

    ejemplo:
        [1, 0, 1, 1, 0]
    """

    individuo = []

    for _ in range(longitud):

        gen = random.randint(0, 1)

        individuo.append(gen)

    return individuo


def funcion_fitness(
    individuo
):

    """
    individuo:
        solución a evaluar

    retorna:
        puntaje de calidad

    en este ejemplo:
    más números 1
    significan mejor solución
    """

    return sum(individuo)


def elegir_padres(
    poblacion,
    cantidad
):

    """
    poblacion:
        conjunto de soluciones

    cantidad:
        cuántos padres conservar

    retorna:
        los individuos
        con mayor fitness
    """

    ordenados = sorted(
        poblacion,
        key=lambda x: funcion_fitness(x),
        reverse=True
    )

    return ordenados[:cantidad]


def crossover(
    padre_1,
    padre_2
):

    """
    combina dos individuos
    para producir un hijo
    """

    punto_corte = random.randint(
        1,
        len(padre_1) - 1
    )

    hijo = (
        padre_1[:punto_corte]
        + padre_2[punto_corte:]
    )

    return hijo


def aplicar_mutacion(
    individuo,
    probabilidad
):

    """
    modifica genes aleatoriamente

    probabilidad:
        posibilidad de mutar
        cada posición
    """

    for i in range(len(individuo)):

        if random.random() < probabilidad:

            # invertir bit
            individuo[i] = (
                1 - individuo[i]
            )

    return individuo


def algoritmo_genetico(
    tamano_poblacion,
    longitud_individuo,
    generaciones,
    probabilidad_mutacion,
    cantidad_padres
):

    """
    tamano_poblacion:
        número de individuos

    longitud_individuo:
        tamaño de cada solución

    generaciones:
        cantidad de iteraciones

    probabilidad_mutacion:
        frecuencia de mutaciones

    cantidad_padres:
        número de mejores individuos

    retorna:
        mejor solución,
        puntaje,
        historial
    """

    # generar población inicial
    poblacion = []

    for _ in range(tamano_poblacion):

        poblacion.append(
            generar_individuo(
                longitud_individuo
            )
        )

    historial = []

    # proceso evolutivo
    for _ in range(generaciones):

        # seleccionar mejores individuos
        padres = elegir_padres(
            poblacion,
            cantidad_padres
        )

        nueva_poblacion = []

        # conservar padres
        for padre in padres:

            nueva_poblacion.append(
                padre[:]
            )

        # generar hijos nuevos
        while (
            len(nueva_poblacion)
            < tamano_poblacion
        ):

            padre_1 = random.choice(
                padres
            )

            padre_2 = random.choice(
                padres
            )

            hijo = crossover(
                padre_1,
                padre_2
            )

            hijo = aplicar_mutacion(
                hijo,
                probabilidad_mutacion
            )

            nueva_poblacion.append(
                hijo
            )

        poblacion = nueva_poblacion

        # guardar mejor individuo
        mejor_actual = max(
            poblacion,
            key=lambda x: funcion_fitness(x)
        )

        historial.append(
            (
                mejor_actual[:],
                funcion_fitness(
                    mejor_actual
                )
            )
        )

    # seleccionar mejor solución final
    mejor_final = max(
        poblacion,
        key=lambda x: funcion_fitness(x)
    )

    return (
        mejor_final,
        funcion_fitness(mejor_final),
        historial
    )


if __name__ == "__main__":

    # parámetros principales

    tamano_poblacion = 6

    longitud_individuo = 5

    generaciones = 20

    probabilidad_mutacion = 0.1

    cantidad_padres = 2

    mejor, puntaje_final, historial = algoritmo_genetico(
        tamano_poblacion,
        longitud_individuo,
        generaciones,
        probabilidad_mutacion,
        cantidad_padres
    )

    print("mejor solución encontrada:")
    print(mejor)

    print("puntaje obtenido:")
    print(puntaje_final)

    print("\nmejores individuos por generación:")

    for indice, datos in enumerate(historial):

        individuo, score = datos

        print(
            "generación",
            indice,
            "->",
            individuo,
            "fitness:",
            score
        )

    # resumen:
    #
    # - generar_individuo(...)
    #   crea soluciones aleatorias
    #
    # - funcion_fitness(...)
    #   mide la calidad
    #
    # - elegir_padres(...)
    #   selecciona las mejores soluciones
    #
    # - crossover(...)
    #   combina individuos
    #
    # - aplicar_mutacion(...)
    #   introduce variaciones aleatorias
    #
    # - algoritmo_genetico(...)
    #   repite el proceso evolutivo