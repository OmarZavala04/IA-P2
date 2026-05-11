# valor de la informacion
# ahora cambiamos el escenario:
# un agricultor decide si sembrar un cultivo delicado o uno resistente.
# puede consultar un pronostico avanzado del clima antes de decidir.

# estados posibles del clima:
# - "buen_clima"
# - "mal_clima"

# decisiones:
# - "cultivo_delicado" (gana mucho si clima es bueno, pierde mucho si es malo)
# - "cultivo_resistente" (gana menos pero es mas seguro)


def utilidad_cosecha(resultado):
    """
    asigna utilidad segun lo que paso al final
    """

    tabla = {
        "delicado_bueno": 120,
        "delicado_malo": -100,
        "resistente_bueno": 60,
        "resistente_malo": 30
    }

    return tabla[resultado]


def decision_sin_pronostico(prob_buen_clima, prob_mal_clima):
    """
    decide directamente sin informacion adicional
    """

    # utilidad esperada cultivo delicado
    ue_delicado = (
        prob_buen_clima * utilidad_cosecha("delicado_bueno") +
        prob_mal_clima  * utilidad_cosecha("delicado_malo")
    )

    # utilidad esperada cultivo resistente
    ue_resistente = (
        prob_buen_clima * utilidad_cosecha("resistente_bueno") +
        prob_mal_clima  * utilidad_cosecha("resistente_malo")
    )

    if ue_delicado >= ue_resistente:
        return "delicado", ue_delicado
    else:
        return "resistente", ue_resistente


def decision_con_pronostico(
    prob_buen_clima,
    prob_mal_clima,
    costo_pronostico,
    precision
):
    """
    usa informacion del pronostico antes de decidir
    """

    # prob de que el sistema diga "buen clima"
    prob_dice_bueno = (
        prob_buen_clima * precision +
        prob_mal_clima  * (1 - precision)
    )

    prob_dice_malo = 1 - prob_dice_bueno

    # si el sistema dice "buen clima" -> elegimos delicado
    if prob_dice_bueno > 0:

        prob_real_bueno = (
            prob_buen_clima * precision
        ) / prob_dice_bueno

        prob_real_malo = (
            prob_mal_clima * (1 - precision)
        ) / prob_dice_bueno

    else:
        prob_real_bueno = 0
        prob_real_malo = 0

    ue_si_bueno = (
        prob_real_bueno * utilidad_cosecha("delicado_bueno") +
        prob_real_malo  * utilidad_cosecha("delicado_malo")
    )

    # si dice "mal clima" -> elegimos resistente
    ue_si_malo = (
        prob_buen_clima * utilidad_cosecha("resistente_bueno") +
        prob_mal_clima  * utilidad_cosecha("resistente_malo")
    )

    # utilidad total considerando ambas posibilidades
    ue_total = (
        prob_dice_bueno * ue_si_bueno +
        prob_dice_malo  * ue_si_malo
    )

    # restamos costo de obtener info
    ue_total -= costo_pronostico

    return ue_total


if __name__ == "__main__":

    # probabilidades del clima
    prob_buen_clima = 0.7
    prob_mal_clima = 0.3

    # sin informacion
    decision, utilidad_base = decision_sin_pronostico(
        prob_buen_clima,
        prob_mal_clima
    )

    print("sin pronostico:")
    print(" decision:", decision)
    print(" utilidad esperada:", utilidad_base)

    # con informacion
    costo_pronostico = 10
    precision = 0.85

    utilidad_con_info = decision_con_pronostico(
        prob_buen_clima,
        prob_mal_clima,
        costo_pronostico,
        precision
    )

    print("\ncon pronostico:")
    print(" utilidad esperada:", utilidad_con_info)

    # valor de la informacion
    valor = utilidad_con_info - utilidad_base

    print("\nvalor de la informacion:", valor)

    # - si valor > 0 conviene usar el pronostico
    # - si valor <= 0 no vale la pena pagar por esa informacion