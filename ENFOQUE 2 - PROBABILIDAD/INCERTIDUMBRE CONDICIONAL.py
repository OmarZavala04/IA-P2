"""
independencia condicional

la independencia condicional significa que:
si ya conocemos cierta informacion,
otra variable puede dejar de ser importante.

ejemplo:

variables:
- lluvia
- trafico
- llegar_tarde

si ya sabemos que hay muchisimo trafico,
entonces saber si llovio o no
tal vez ya no cambia mucho la probabilidad
de llegar tarde.

eso significa:
"llegar_tarde" es condicionalmente independiente
de "lluvia" dado "trafico".

en inteligencia artificial esto sirve para:
- simplificar calculos
- reducir combinaciones
- construir redes bayesianas
- hacer inferencia mas eficiente
"""

def prob_llegar_tarde(hay_trafico):
    """
    calcula probabilidad de llegar tarde
    dependiendo del trafico.

    parametro:
        hay_trafico:
            True  -> si hay trafico
            False -> no hay trafico

    regresa:
        probabilidad entre 0 y 1
    """

    if hay_trafico:

        # si hay trafico:
        # muy alta probabilidad de retraso
        return 0.9

    else:

        # si no hay trafico:
        # baja probabilidad de retraso
        return 0.1


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":

    # caso 1: hay trafico
    prob_con_trafico = prob_llegar_tarde(True)

    # caso 2: no hay trafico
    prob_sin_trafico = prob_llegar_tarde(False)

    print("RESULTADOS\n")

    print(
        "probabilidad de llegar tarde SI hay trafico =",
        prob_con_trafico
    )

    print(
        "probabilidad de llegar tarde SI NO hay trafico =",
        prob_sin_trafico
    )

    print("\ninterpretacion:")

    print("- el trafico cambia mucho la probabilidad")
    print("- una vez conocido el trafico,")
    print("  otras variables pueden importar menos")
    print("- eso ayuda a simplificar modelos probabilisticos")

# conceptos importantes:
#
# independencia:
#   una variable no afecta otra
#
# independencia condicional:
#   una variable deja de importar
#   DESPUES de conocer otra variable
#
# redes bayesianas:
#   usan mucho esta idea para ahorrar calculos