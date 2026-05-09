# Red bayesiana dinamica
# una dbn modela como cambia algo conforme pasa el tiempo.
# en este ejemplo modelaremos el estado de una bateria de dron.
# estado_hoy -> estado_manana

# estados posibles:
# - "alta"
# - "media"
# - "baja"

# idea:
# 1. tengo una creencia del estado actual de la bateria
# 2. tengo probabilidades de como cambia al siguiente ciclo
# 3. calculo la probabilidad del estado futuro


def calcular_estado_siguiente(creencia_actual, modelo_transicion):
    """
    calcula la creencia del siguiente instante

    creencia_actual:
        probabilidad actual de cada estado

    ejemplo:
    {
        "alta": 0.5,
        "media": 0.3,
        "baja": 0.2
    }

    modelo_transicion:
        probabilidades de pasar de un estado a otro

    ejemplo:
    {
        "alta": {
            "alta": 0.6,
            "media": 0.3,
            "baja": 0.1
        },
        ...
    }

    regresa:
        nueva distribucion de probabilidades
    """

    nueva_creencia = {}

    # para cada estado futuro posible
    for estado_futuro in creencia_actual:

        prob_total = 0

        # sumamos contribucion de cada estado actual
        for estado_actual in creencia_actual:

            prob_actual = creencia_actual[estado_actual]

            prob_cambio = modelo_transicion[
                estado_actual
            ][
                estado_futuro
            ]

            prob_total += (
                prob_actual *
                prob_cambio
            )

        nueva_creencia[estado_futuro] = prob_total

    return nueva_creencia


def imprimir_creencia(titulo, creencia):
    """
    imprime una creencia de forma mas clara
    """

    print("\n" + titulo)

    for estado in creencia:

        porcentaje = creencia[estado] * 100

        print(
            " ",
            estado,
            "->",
            round(porcentaje, 2),
            "%"
        )


if __name__ == "__main__":

    # creencia inicial:
    # el dron probablemente tiene bateria alta
    creencia_hoy = {
        "alta": 0.5,
        "media": 0.3,
        "baja": 0.2
    }

    # modelo de transicion
    # ejemplo:
    # si la bateria esta alta:
    # 60% sigue alta
    # 30% baja a media
    # 10% baja mucho

    modelo_transicion = {

        "alta": {
            "alta": 0.6,
            "media": 0.3,
            "baja": 0.1
        },

        "media": {
            "alta": 0.1,
            "media": 0.6,
            "baja": 0.3
        },

        "baja": {
            "alta": 0.0,
            "media": 0.2,
            "baja": 0.8
        }
    }

    imprimir_creencia(
        "estado estimado de la bateria hoy:",
        creencia_hoy
    )

    # calculamos siguiente estado
    creencia_manana = calcular_estado_siguiente(
        creencia_hoy,
        modelo_transicion
    )

    imprimir_creencia(
        "estado estimado de la bateria despues:",
        creencia_manana
    )

    # simulamos otro paso mas
    creencia_despues = calcular_estado_siguiente(
        creencia_manana,
        modelo_transicion
    )

    imprimir_creencia(
        "estado estimado despues de otro ciclo:",
        creencia_despues
    )

    # - una dbn conecta estados entre tiempos diferentes
    # - usa probabilidades de transicion
    # - sirve para predecir estados futuros
    # - aqui se uso para estimar el desgaste de bateria