# Teoria de la utilidad: funcion de utilidad
# la utilidad representa que tan conveniente es un resultado.
# en este ejemplo una empresa debe decidir
# si enviar productos por envio rapido o envio economico.

# cada decision puede terminar en diferentes resultados:
# - entrega exitosa
# - retraso
# - perdida del paquete

# cada resultado tiene:
# - una utilidad
# - una probabilidad de ocurrir

# la idea:
# calcular utilidad esperada de cada estrategia
# y escoger la mejor.


def obtener_utilidad(evento):
    """
    asigna utilidad a cada posible resultado

    entre mas alto el numero, mejor fue el resultado
    """

    utilidades = {

        # envio rapido
        "rapido_entrega_ok": 90,
        "rapido_retraso": 20,
        "rapido_perdido": -80,

        # envio economico
        "economico_entrega_ok": 60,
        "economico_retraso": 10,
        "economico_perdido": -40
    }

    return utilidades[evento]


def calcular_utilidad_esperada(
    decision,
    escenarios_probables
):
    """
    calcula:

    utilidad_esperada =
    suma(probabilidad * utilidad)
    """

    utilidad_total = 0

    for evento, probabilidad in escenarios_probables[decision]:

        utilidad = obtener_utilidad(evento)

        contribucion = (
            probabilidad *
            utilidad
        )

        utilidad_total += contribucion

        print(
            " decision:",
            decision,
            "| evento:",
            evento,
            "| contribucion:",
            contribucion
        )

    return utilidad_total


def seleccionar_mejor_opcion(
    opciones,
    escenarios_probables
):
    """
    compara utilidad esperada de todas las opciones
    """

    mejor_opcion = None
    mejor_utilidad = None

    for opcion in opciones:

        print("\ncalculando para:", opcion)

        utilidad = calcular_utilidad_esperada(
            opcion,
            escenarios_probables
        )

        print(
            " utilidad esperada total de",
            opcion,
            "=",
            utilidad
        )

        if (
            mejor_opcion is None or
            utilidad > mejor_utilidad
        ):
            mejor_opcion = opcion
            mejor_utilidad = utilidad

    return mejor_opcion, mejor_utilidad


if __name__ == "__main__":

    # decisiones posibles
    opciones = [
        "envio_rapido",
        "envio_economico"
    ]

    # escenarios y probabilidades
    escenarios_probables = {

        "envio_rapido": [

            # llega bien
            ("rapido_entrega_ok", 0.85),

            # llega tarde
            ("rapido_retraso", 0.10),

            # se pierde
            ("rapido_perdido", 0.05)
        ],

        "envio_economico": [

            # llega bien
            ("economico_entrega_ok", 0.60),

            # llega tarde
            ("economico_retraso", 0.30),

            # se pierde
            ("economico_perdido", 0.10)
        ]
    }

    # buscamos mejor decision
    mejor, utilidad = seleccionar_mejor_opcion(
        opciones,
        escenarios_probables
    )

    print("\nmejor estrategia:")

    print(
        " opcion elegida ->",
        mejor
    )

    print(
        " utilidad esperada ->",
        utilidad
    )

    # - la utilidad representa que tan bueno es un resultado
    # - cada resultado tiene cierta probabilidad
    # - utilidad esperada = suma(probabilidad * utilidad)
    # - la mejor decision es la que da mayor utilidad esperada