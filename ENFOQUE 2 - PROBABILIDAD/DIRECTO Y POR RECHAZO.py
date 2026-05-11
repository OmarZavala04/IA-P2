"""
muestreo directo y muestreo por rechazo
en redes bayesianas a veces calcular p(x | evidencia) exacto es caro.
en lugar de hacer toda la matematica exacta,
podemos aproximar la probabilidad generando muchos casos falsos del mundo.
esto se llama muestreo (sampling).
"""

import random

# ========================= RED BAYESIANA =========================

red = {
    "virus": {
        "padres": [],
        "cpt": {(): 0.1}
    },

    "clima_frio": {
        "padres": [],
        "cpt": {(): 0.3}
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

# orden correcto para samplear
orden_vars = ["virus", "clima_frio", "fiebre", "sudor"]

# ========================= FUNCIONES =========================

def prob_true_de_nodo(nodo, asignacion, red_local):
    """
    regresa p(nodo = true | padres)
    """
    padres = red_local[nodo]["padres"]
    clave = tuple(asignacion[p] for p in padres)
    return red_local[nodo]["cpt"][clave]


def samplear_una_vez(red_local, orden):
    """
    genera una muestra completa de la red
    """
    asignacion = {}

    for nodo in orden:
        p_true = prob_true_de_nodo(nodo, asignacion, red_local)

        # generar true/false aleatoriamente
        asignacion[nodo] = (random.random() < p_true)

    return asignacion


def cumple_evidencia(muestra, evidencia):
    """
    revisa si una muestra cumple la evidencia
    """
    for var, val in evidencia.items():
        if muestra[var] != val:
            return False

    return True


def muestreo_directo(red_local, orden, n_muestras):
    """
    genera muchas muestras completas
    """
    muestras = []

    for _ in range(n_muestras):
        muestras.append(samplear_una_vez(red_local, orden))

    return muestras


def muestreo_por_rechazo(
    red_local,
    orden,
    n_muestras,
    query_var,
    evidencia
):
    """
    aproxima:
    p(query_var | evidencia)

    usando rejection sampling
    """

    cuenta_true = 0
    cuenta_false = 0
    rechazadas = 0

    for _ in range(n_muestras):

        # generar muestra
        muestra = samplear_una_vez(red_local, orden)

        # verificar evidencia
        if not cumple_evidencia(muestra, evidencia):
            rechazadas += 1
            continue

        # contar resultados validos
        if muestra[query_var] is True:
            cuenta_true += 1
        else:
            cuenta_false += 1

    total_validas = cuenta_true + cuenta_false

    # evitar division entre cero
    if total_validas == 0:
        return {
            True: 0.0,
            False: 0.0
        }

    return {
        True: cuenta_true / total_validas,
        False: cuenta_false / total_validas
    }


# ========================= EJECUCION =========================

# generar muestras normales
muestras = muestreo_directo(
    red_local=red,
    orden=orden_vars,
    n_muestras=5
)

print("muestras generadas:\n")

for i, m in enumerate(muestras, start=1):
    print("muestra", i, "->", m)

# consulta probabilistica
resultado = muestreo_por_rechazo(
    red_local=red,
    orden=orden_vars,
    n_muestras=5000,
    query_var="fiebre",
    evidencia={"sudor": True}
)

print("\nprob aproximada con muestreo por rechazo:")
print("fiebre = true  ->", round(resultado[True], 4))
print("fiebre = false ->", round(resultado[False], 4))