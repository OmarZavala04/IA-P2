"""
inferencia por enumeracion

la inferencia por enumeracion es una tecnica usada
en redes bayesianas para calcular probabilidades condicionales.

queremos calcular cosas como:

    P(X | evidencia)

ejemplo:
    P(fiebre | sudor = True)

la idea es:
1. probar todas las combinaciones posibles
   de variables desconocidas
2. calcular probabilidades
3. sumar resultados
4. normalizar

esto funciona,
pero puede volverse lento si hay demasiadas variables.
"""

# ==========================================
# RED BAYESIANA
# ==========================================
# cada nodo tiene:
# - padres
# - tabla CPT:
#   probabilidad condicional del nodo

red = {

    "virus": {
        "padres": [],
        "cpt": {
            (): 0.1
        }
    },

    "clima_frio": {
        "padres": [],
        "cpt": {
            (): 0.3
        }
    },

    "fiebre": {
        "padres": ["virus", "clima_frio"],

        # P(fiebre = True | virus, clima_frio)

        "cpt": {

            (True,  True ): 0.9,
            (True,  False): 0.8,
            (False, True ): 0.6,
            (False, False): 0.05
        }
    },

    "sudor": {
        "padres": ["fiebre"],

        # P(sudor = True | fiebre)

        "cpt": {

            (True,): 0.85,
            (False,): 0.1
        }
    }
}

# orden de recorrido de variables
orden_vars = [
    "virus",
    "clima_frio",
    "fiebre",
    "sudor"
]

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def prob_var_true(var, evidencia, red_local):
    """
    regresa:

        P(var = True | padres)

    usando la CPT del nodo
    """

    padres = red_local[var]["padres"]

    clave = tuple(
        evidencia[p]
        for p in padres
    )

    return red_local[var]["cpt"][clave]


def prob_de_var(var, valor, evidencia, red_local):
    """
    calcula:

        P(var = valor | padres)

    si valor = False:
        usamos:
            1 - P(True)
    """

    p_true = prob_var_true(
        var,
        evidencia,
        red_local
    )

    if valor is True:
        return p_true
    else:
        return 1 - p_true


# ==========================================
# ENUMERACION RECURSIVA
# ==========================================

def enumerar_todo(vars_restantes, evidencia, red_local):
    """
    calcula probabilidad conjunta total

    si una variable no tiene valor,
    probamos:
        True
        False

    y sumamos ambos casos
    """

    # caso base
    if len(vars_restantes) == 0:
        return 1.0

    # tomamos primera variable
    v = vars_restantes[0]

    resto = vars_restantes[1:]

    # si ya conocemos su valor
    if v in evidencia:

        p = prob_de_var(
            v,
            evidencia[v],
            evidencia,
            red_local
        )

        return p * enumerar_todo(
            resto,
            evidencia,
            red_local
        )

    # si NO conocemos su valor
    else:

        total = 0.0

        for val in [True, False]:

            nueva_evidencia = evidencia.copy()

            nueva_evidencia[v] = val

            p = prob_de_var(
                v,
                val,
                nueva_evidencia,
                red_local
            )

            total += p * enumerar_todo(
                resto,
                nueva_evidencia,
                red_local
            )

        return total


# ==========================================
# NORMALIZACION
# ==========================================

def normalizar(distribucion):
    """
    hace que todas las probabilidades sumen 1
    """

    suma = sum(distribucion.values())

    return {
        k: v / suma
        for k, v in distribucion.items()
    }


# ==========================================
# CONSULTA PRINCIPAL
# ==========================================

def preguntar(
    variable_objetivo,
    evidencia,
    red_local,
    orden
):
    """
    calcula:

        P(variable_objetivo | evidencia)

    regresa:
        {
            True: probabilidad,
            False: probabilidad
        }
    """

    distribucion = {}

    for valor in [True, False]:

        evidencia_tmp = evidencia.copy()

        evidencia_tmp[variable_objetivo] = valor

        distribucion[valor] = enumerar_todo(
            orden,
            evidencia_tmp,
            red_local
        )

    return normalizar(distribucion)


# ==========================================
# EJEMPLO
# ==========================================

# queremos calcular:
#
# P(fiebre | sudor = True)

resultado = preguntar(
    variable_objetivo="fiebre",
    evidencia={"sudor": True},
    red_local=red,
    orden=orden_vars
)

# ==========================================
# MOSTRAR RESULTADOS
# ==========================================

print("Resultado de inferencia por enumeracion:\n")

print(
    "P(fiebre = True | sudor = True) =",
    round(resultado[True], 4)
)

print(
    "P(fiebre = False | sudor = True) =",
    round(resultado[False], 4)
)

# ==========================================
# INTERPRETACION
# ==========================================

print("\ninterpretacion:")

print("- si hay sudor, la probabilidad de fiebre aumenta")
print("- el algoritmo revisa todas las combinaciones posibles")
print("- luego suma probabilidades y normaliza")
print("- esto permite hacer inferencia probabilistica")

# conceptos importantes:
#
# red bayesiana:
#   modelo probabilistico con dependencias
#
# evidencia:
#   informacion conocida
#
# inferencia:
#   calcular probabilidades desconocidas
#
# enumeracion:
#   probar todas las combinaciones posibles