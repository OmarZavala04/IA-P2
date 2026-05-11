"""
manto de markov (markov blanket)

el manto de markov de un nodo
es el conjunto minimo de variables
que necesito conocer para razonar sobre ese nodo
sin observar toda la red bayesiana.

idea importante:
si conozco el manto de markov de X,
entonces el resto de la red
ya no agrega informacion extra sobre X.

esto sirve para:
- reducir calculos
- hacer inferencia mas eficiente
- simplificar modelos probabilisticos
- seleccionar variables importantes

==========================================
COMO SE FORMA
==========================================

manto(X) =

    padres(X)
    +
    hijos(X)
    +
    copadres(X)

donde:

- padres:
    nodos que afectan a X

- hijos:
    nodos afectados por X

- copadres:
    otros padres de los hijos de X
"""

# ==========================================
# RED BAYESIANA SIMPLE
# ==========================================
#
#      a ----\
#              -> b -> d
#      c ----/
#
# padres de b:
#   a, c
#
# hijos de b:
#   d
#
# copadres de b:
#   ninguno
#

red = {

    "a": {
        "padres": [],
        "hijos": ["b"]
    },

    "b": {
        "padres": ["a", "c"],
        "hijos": ["d"]
    },

    "c": {
        "padres": [],
        "hijos": ["b"]
    },

    "d": {
        "padres": ["b"],
        "hijos": []
    }
}

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def padres_de(nodo, red_local):
    """
    regresa los padres directos del nodo
    """

    return red_local[nodo]["padres"]


def hijos_de(nodo, red_local):
    """
    regresa los hijos directos del nodo
    """

    return red_local[nodo]["hijos"]


def copadres_de(nodo, red_local):
    """
    regresa los otros padres
    de los hijos del nodo

    ejemplo:
        si:
            x -> h
            y -> h

        entonces:
            y es copadre de x
    """

    resultado = set()

    # revisamos cada hijo del nodo
    for hijo in hijos_de(nodo, red_local):

        # revisamos los padres de ese hijo
        for padre in padres_de(hijo, red_local):

            # evitamos agregar el mismo nodo
            if padre != nodo:
                resultado.add(padre)

    return list(resultado)


# ==========================================
# MANTO DE MARKOV
# ==========================================

def manto_de_markov(nodo, red_local):
    """
    construye el manto de markov:

        padres
        +
        hijos
        +
        copadres

    quitando duplicados
    """

    lista_padres = padres_de(
        nodo,
        red_local
    )

    lista_hijos = hijos_de(
        nodo,
        red_local
    )

    lista_copadres = copadres_de(
        nodo,
        red_local
    )

    conjunto = set(
        lista_padres
        + lista_hijos
        + lista_copadres
    )

    # por seguridad:
    # quitamos el mismo nodo
    if nodo in conjunto:
        conjunto.remove(nodo)

    return list(conjunto)


# ==========================================
# EJEMPLO
# ==========================================

nodo_objetivo = "b"

manto = manto_de_markov(
    nodo_objetivo,
    red
)

# ==========================================
# RESULTADOS
# ==========================================

print("Nodo objetivo:", nodo_objetivo)

print("\nManto de Markov:")

for elemento in manto:
    print("-", elemento)

# ==========================================
# INTERPRETACION
# ==========================================

print("\ninterpretacion:")

print("- el manto contiene toda la informacion")
print("  relevante para el nodo")

print("- conocer otros nodos fuera del manto")
print("  ya no aporta informacion adicional")

print("- esto ayuda a simplificar inferencia")
print("  en redes bayesianas")

# conceptos importantes:
#
# padres:
#   causas del nodo
#
# hijos:
#   efectos del nodo
#
# copadres:
#   otras causas compartidas de los hijos
#
# manto de markov:
#   conjunto minimo necesario
#   para razonar sobre un nodo