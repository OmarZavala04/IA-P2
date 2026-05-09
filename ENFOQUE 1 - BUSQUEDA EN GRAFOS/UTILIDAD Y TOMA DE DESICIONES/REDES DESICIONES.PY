# Red de decision para elegir transporte
# una red de decision mezcla:
# - decisiones
# - probabilidad
# - utilidad
# para escoger la mejor opcion posible.

# escenario:
# necesito decidir como ir al trabajo:
# - motocicleta
# - autobus
#
# dependiendo de la decision,
# pueden pasar diferentes situaciones:
# - llegar rapido
# - llegar tarde
# - tener averia
#
# cada resultado tiene una utilidad distinta.


def valor_resultado(resultado):
    """
    asigna una utilidad a cada resultado final.
    """

    tabla = {

        # motocicleta
        "moto_rapido": 90,
        "moto_tarde": 20,
        "moto_averia": -80,

        # autobus
        "bus_rapido": 60,
        "bus_tarde": 10,
        "bus_lleno": -20
    }

    return tabla[resultado]


def calcular_utilidad(decision, escenarios):
    """
    calcula la utilidad esperada
    de una decision.
    """

    utilidad_total = 0

    for resultado, probabilidad in escenarios[decision]:

        utilidad = valor_resultado(resultado)

        utilidad_total += (
            utilidad * probabilidad
        )

    return utilidad_total


def elegir_transporte(opciones, escenarios):
    """
    revisa todas las opciones
    y escoge la mejor.
    """

    mejor_opcion = None
    mejor_utilidad = None

    for opcion in opciones:

        ue = calcular_utilidad(
            opcion,
            escenarios
        )

        print(
            "utilidad esperada de",
            opcion,
            "=",
            ue
        )

        if (
            mejor_opcion is None or
            ue > mejor_utilidad
        ):

            mejor_opcion = opcion
            mejor_utilidad = ue

    return mejor_opcion, mejor_utilidad


if __name__ == "__main__":

    # decisiones posibles
    opciones = [
        "motocicleta",
        "autobus"
    ]

    # resultados posibles segun la decision
    escenarios = {

        "motocicleta": [

            # llego rapido normalmente
            ("moto_rapido", 0.7),

            # trafico
            ("moto_tarde", 0.2),

            # falla mecanica
            ("moto_averia", 0.1)
        ],

        "autobus": [

            # llego rapido
            ("bus_rapido", 0.4),

            # mucho trafico
            ("bus_tarde", 0.4),

            # autobus lleno
            ("bus_lleno", 0.2)
        ]
    }

    mejor, utilidad = elegir_transporte(
        opciones,
        escenarios
    )

    print(
        "\nmejor opcion:",
        mejor
    )

    print(
        "utilidad esperada:",
        utilidad
    )

    # el proceso es:
    # decision -> posibles resultados ->
    # probabilidades -> utilidad esperada
    #
    # despues se elige la mejor opcion.