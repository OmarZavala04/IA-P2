"""
filtrado probabilistico en una app de peliculas

este ejemplo usa eliminacion de variables
para calcular probabilidades en una red bayesiana.

escenario:
queremos saber la probabilidad de que
a una persona le guste una pelicula
dado que sabemos que:
- vio el trailer completo

variables:
- accion
- actores_famosos
- le_gusta
- recomienda

la idea:
calcular:

P(le_gusta | recomienda=True)

sin revisar manualmente todas las combinaciones.
"""

import itertools

# red bayesiana
red = {

    "accion": {
        "padres": [],
        "cpt": {
            (): 0.6
        }
    },

    "actores_famosos": {
        "padres": [],
        "cpt": {
            (): 0.7
        }
    },

    "le_gusta": {
        "padres": ["accion", "actores_famosos"],
        "cpt": {

            (True, True): 0.95,
            (True, False): 0.75,
            (False, True): 0.60,
            (False, False): 0.10
        }
    },

    "recomienda": {
        "padres": ["le_gusta"],
        "cpt": {

            (True,): 0.9,
            (False,): 0.2
        }
    }
}


def generar_asignaciones(lista_vars):

    for valores in itertools.product([True, False], repeat=len(lista_vars)):

        yield dict(zip(lista_vars, valores))


def crear_factor(variable, red_local):

    padres = red_local[variable]["padres"]

    variables_factor = [variable] + padres

    tabla = {}

    for asignacion in generar_asignaciones(variables_factor):

        clave_padres = tuple(asignacion[p] for p in padres)

        prob_true = red_local[variable]["cpt"][clave_padres]

        if asignacion[variable]:
            prob = prob_true
        else:
            prob = 1 - prob_true

        fila = tuple(asignacion[v] for v in variables_factor)

        tabla[fila] = prob

    return {
        "vars": variables_factor,
        "tabla": tabla
    }


def aplicar_evidencia(factor, variable, valor):

    if variable not in factor["vars"]:
        return factor

    indice = factor["vars"].index(variable)

    nuevas_vars = [v for v in factor["vars"] if v != variable]

    nueva_tabla = {}

    for fila, prob in factor["tabla"].items():

        if fila[indice] == valor:

            nueva_fila = tuple(
                x for i, x in enumerate(fila)
                if i != indice
            )

            nueva_tabla[nueva_fila] = prob

    return {
        "vars": nuevas_vars,
        "tabla": nueva_tabla
    }


def unir_factores(f1, f2):

    vars1 = f1["vars"]
    vars2 = f2["vars"]

    nuevas_vars = list(dict.fromkeys(vars1 + vars2))

    nueva_tabla = {}

    for asign in generar_asignaciones(nuevas_vars):

        fila1 = tuple(asign[v] for v in vars1)
        fila2 = tuple(asign[v] for v in vars2)

        if fila1 in f1["tabla"] and fila2 in f2["tabla"]:

            fila_total = tuple(asign[v] for v in nuevas_vars)

            nueva_tabla[fila_total] = (
                f1["tabla"][fila1] *
                f2["tabla"][fila2]
            )

    return {
        "vars": nuevas_vars,
        "tabla": nueva_tabla
    }


def eliminar_variable(factor, variable):

    if variable not in factor["vars"]:
        return factor

    indice = factor["vars"].index(variable)

    nuevas_vars = [v for v in factor["vars"] if v != variable]

    nueva_tabla = {}

    for fila, prob in factor["tabla"].items():

        fila_reducida = tuple(
            x for i, x in enumerate(fila)
            if i != indice
        )

        nueva_tabla[fila_reducida] = (
            nueva_tabla.get(fila_reducida, 0) + prob
        )

    return {
        "vars": nuevas_vars,
        "tabla": nueva_tabla
    }


def normalizar(factor, variable_obj):

    indice = factor["vars"].index(variable_obj)

    distribucion = {
        True: 0,
        False: 0
    }

    for fila, prob in factor["tabla"].items():

        valor = fila[indice]

        distribucion[valor] += prob

    total = distribucion[True] + distribucion[False]

    distribucion[True] /= total
    distribucion[False] /= total

    return distribucion


def inferencia(query, evidencia, red_local):

    # crear factores
    factores = []

    for var in red_local.keys():

        factores.append(
            crear_factor(var, red_local)
        )

    # aplicar evidencia
    for ev, val in evidencia.items():

        factores = [
            aplicar_evidencia(f, ev, val)
            for f in factores
        ]

    # variables ocultas
    ocultas = [
        v for v in red_local.keys()
        if v != query and v not in evidencia
    ]

    # eliminar variables
    for var in ocultas:

        factores_con_var = [
            f for f in factores
            if var in f["vars"]
        ]

        factores_sin_var = [
            f for f in factores
            if var not in f["vars"]
        ]

        if len(factores_con_var) == 0:
            factores = factores_sin_var
            continue

        combinado = factores_con_var[0]

        for otro in factores_con_var[1:]:

            combinado = unir_factores(combinado, otro)

        reducido = eliminar_variable(combinado, var)

        factores = factores_sin_var + [reducido]

    # multiplicar factores finales
    resultado = factores[0]

    for otro in factores[1:]:

        resultado = unir_factores(resultado, otro)

    return normalizar(resultado, query)


if __name__ == "__main__":

    # consulta:
    # probabilidad de que le guste
    # dado que la recomendo

    resultado = inferencia(
        query="le_gusta",
        evidencia={
            "recomienda": True
        },
        red_local=red
    )

    print("resultado de inferencia:\n")

    print(
        "probabilidad de le_gusta = True:",
        round(resultado[True], 4)
    )

    print(
        "probabilidad de le_gusta = False:",
        round(resultado[False], 4)
    )

    # eliminacion de variables:
    # reduce calculos innecesarios
    # sumando variables ocultas
    # para hacer inferencia mas eficiente