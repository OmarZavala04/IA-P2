# Parcialmente observable
# pomdp = mdp pero no sabes exactamente en que estado estas
# solo tienes una creencia (probabilidades sobre estados)

def utilidad_accion_en_estado(accion, estado_real):
    """
    utilidad inmediata de hacer una accion
    en cierto estado real
    """

    tabla = {
        ("salir", "seguro"): 10,
        ("salir", "peligro"): -20,

        ("esperar", "seguro"): 1,
        ("esperar", "peligro"): 0,

        ("observar", "seguro"): -1,
        ("observar", "peligro"): -1,
    }

    return tabla[(accion, estado_real)]


def utilidad_esperada_de_accion(accion, creencia):
    """
    utilidad esperada usando la creencia actual
    """

    total = 0

    for estado in creencia:

        probabilidad = creencia[estado]

        utilidad = utilidad_accion_en_estado(
            accion,
            estado
        )

        total += probabilidad * utilidad

    return total


def mejor_accion(creencia):
    """
    revisa todas las acciones
    y escoge la de mayor utilidad esperada
    """

    acciones = [
        "salir",
        "esperar",
        "observar"
    ]

    mejor_accion_encontrada = None
    mejor_utilidad = None

    for accion in acciones:

        utilidad = utilidad_esperada_de_accion(
            accion,
            creencia
        )

        print(
            "utilidad esperada de",
            accion,
            "=",
            utilidad
        )

        if (
            mejor_accion_encontrada is None
            or
            utilidad > mejor_utilidad
        ):

            mejor_accion_encontrada = accion
            mejor_utilidad = utilidad

    return (
        mejor_accion_encontrada,
        mejor_utilidad
    )


def actualizar_creencia(
    creencia_anterior,
    observacion,
    confiabilidad_sensor
):
    """
    actualiza la creencia usando una observacion
    """

    prob_seguro = creencia_anterior["seguro"]
    prob_peligro = creencia_anterior["peligro"]

    if observacion == "parece_seguro":

        verosimilitud_seguro = confiabilidad_sensor
        verosimilitud_peligro = 1 - confiabilidad_sensor

    else:

        verosimilitud_seguro = 1 - confiabilidad_sensor
        verosimilitud_peligro = confiabilidad_sensor

    nueva_seguro_sin_norm = (
        verosimilitud_seguro
        *
        prob_seguro
    )

    nueva_peligro_sin_norm = (
        verosimilitud_peligro
        *
        prob_peligro
    )

    total = (
        nueva_seguro_sin_norm
        +
        nueva_peligro_sin_norm
    )

    if total == 0:

        nueva_seguro = 0.5
        nueva_peligro = 0.5

    else:

        nueva_seguro = (
            nueva_seguro_sin_norm
            /
            total
        )

        nueva_peligro = (
            nueva_peligro_sin_norm
            /
            total
        )

    return {
        "seguro": nueva_seguro,
        "peligro": nueva_peligro
    }


if __name__ == "__main__":

    # creencia inicial
    creencia = {
        "seguro": 0.7,
        "peligro": 0.3
    }

    print("creencia inicial:")
    print(creencia)

    # buscar mejor accion inicial
    accion_1, utilidad_1 = mejor_accion(
        creencia
    )

    print("\nmejor accion inicial:")
    print(accion_1)

    print("utilidad esperada:")
    print(utilidad_1)

    # simulacion de observacion
    observacion = "parece_peligro"

    confiabilidad = 0.8

    nueva_creencia = actualizar_creencia(
        creencia,
        observacion,
        confiabilidad
    )

    print("\ncreencia despues de observar:")
    print(nueva_creencia)

    # buscar mejor accion despues de observar
    accion_2, utilidad_2 = mejor_accion(
        nueva_creencia
    )

    print("\nmejor accion despues de observar:")
    print(accion_2)

    print("utilidad esperada:")
    print(utilidad_2)