"""
ponderacion de verosimilitud (likelihood weighting)

esta tecnica aproxima:
p(query | evidencia)

usando muestreo ponderado en redes bayesianas.

idea:
- las variables de evidencia NO se samplean
- se fijan al valor observado
- cada muestra recibe un peso
- el peso indica que tan compatible fue con la evidencia
"""

import random

# ======================= RED BAYESIANA =======================

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
        "cpt": {

            (True,  True):  0.9,
            (True,  False): 0.8,

            (False, True):  0.6,
            (False, False): 0.05
        }
    },

    "sudor": {
        "padres": ["fiebre"],
        "cpt": {

            (True,):  0.85,
            (False,): 0.1
        }
    }
}

# orden topológico:
# padres primero
orden_vars = [
    "virus",
    "clima_frio",
    "fiebre",
    "sudor"
]

# ======================= FUNCIONES =======================

def prob_true_de_nodo(
    nodo,
    asignacion,
    red_local
):
    """
    devuelve:
    p(nodo = true | padres)
    """

    padres = red_local[nodo]["padres"]

    clave = tuple(
        asignacion[p]
        for p in padres
    )

    return red_local[nodo]["cpt"][clave]


def samplear_likelihood_weighting(
    red_local,
    orden,
    evidencia
):
    """
    genera:
    - una muestra
    - un peso asociado
    """

    asignacion = {}

    peso = 1.0

    for nodo in orden:

        p_true = prob_true_de_nodo(
            nodo,
            asignacion,
            red_local
        )

        # ================= EVIDENCIA =================

        if nodo in evidencia:

            valor_obs = evidencia[nodo]

            # fijamos el valor
            asignacion[nodo] = valor_obs

            # actualizar peso
            if valor_obs is True:
                peso *= p_true
            else:
                peso *= (1 - p_true)

        # ================= SAMPLE NORMAL =================

        else:

            asignacion[nodo] = (
                random.random() < p_true
            )

    return asignacion, peso


def likelihood_weighting(
    query_var,
    evidencia,
    red_local,
    orden,
    n_muestras
):
    """
    aproxima:
    p(query_var | evidencia)
    """

    peso_true = 0.0
    peso_false = 0.0

    muestras_guardadas = []

    for _ in range(n_muestras):

        asignacion, peso = samplear_likelihood_weighting(
            red_local,
            orden,
            evidencia
        )

        # guardar algunas muestras
        if len(muestras_guardadas) < 5:
            muestras_guardadas.append(
                (asignacion.copy(), peso)
            )

        # acumular pesos
        if asignacion[query_var] is True:
            peso_true += peso
        else:
            peso_false += peso

    # ================= NORMALIZACIÓN =================

    total = peso_true + peso_false

    if total == 0:
        return {
            True: 0.0,
            False: 0.0
        }, muestras_guardadas

    resultado = {

        True: peso_true / total,

        False: peso_false / total
    }

    return resultado, muestras_guardadas


# ======================= EJECUCIÓN =======================

resultado, muestras = likelihood_weighting(

    query_var="fiebre",

    evidencia={
        "sudor": True
    },

    red_local=red,

    orden=orden_vars,

    n_muestras=5000
)

# ======================= MOSTRAR MUESTRAS =======================

print("algunas muestras generadas:\n")

for i, (muestra, peso) in enumerate(muestras, start=1):

    print("muestra", i)

    print("valores ->", muestra)

    print("peso    ->", round(peso, 6))

    print()

# ======================= RESULTADO FINAL =======================

print("resultado aproximado:\n")

print(
    "p(fiebre = true | sudor = true)  ->",
    round(resultado[True], 4)
)

print(
    "p(fiebre = false | sudor = true) ->",
    round(resultado[False], 4)
)