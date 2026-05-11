# aprendizaje por refuerzo pasivo
# aqui el agente NO decide acciones.
# ya existe una politica fija y el agente solo aprende
# que tan buenos son los estados mientras sigue esa politica.
#
# escenario:
# un dron reparte paquetes siguiendo rutas automaticas.
# el dron no elige caminos.
# solamente aprende:
# "que tan conveniente es terminar en cada zona"

import random


def mover(zona_actual):
    """
    politica fija del dron.
    no decide, siempre sigue la misma ruta.
    """

    if zona_actual == "almacen":
        return "avenida"

    if zona_actual == "avenida":

        # a veces llega rapido
        # a veces hay trafico
        if random.random() < 0.7:
            return "cliente"

        return "trafico"

    if zona_actual == "trafico":
        return "cliente"

    return "fin"


def recompensa(zona):
    """
    recompensa inmediata
    de entrar a cada zona.
    """

    tabla = {

        # salir cuesta bateria
        "almacen": -1,

        # avanzar normalmente
        "avenida": 2,

        # trafico hace perder tiempo
        "trafico": -4,

        # entregar paquete da puntos
        "cliente": 15,

        # final
        "fin": 0
    }

    return tabla[zona]


def aprendizaje_pasivo(
    estados,
    inicio,
    episodios,
    alpha,
    gamma
):
    """
    aprende el valor de cada estado
    siguiendo una politica fija.
    """

    # valores iniciales
    valores = {}

    for estado in estados:
        valores[estado] = 0.0

    # entrenamiento
    for _ in range(episodios):

        estado_actual = inicio

        while estado_actual != "fin":

            siguiente = mover(
                estado_actual
            )

            r = recompensa(
                siguiente
            )

            # formula:
            # V(s) = V(s) + alpha * (
            # recompensa +
            # gamma * V(siguiente)
            # - V(s)
            # )

            valor_viejo = valores[estado_actual]

            valor_nuevo = valor_viejo + alpha * (
                r +
                gamma * valores[siguiente] -
                valor_viejo
            )

            valores[estado_actual] = valor_nuevo

            estado_actual = siguiente

    return valores


if __name__ == "__main__":

    estados = [
        "almacen",
        "avenida",
        "trafico",
        "cliente",
        "fin"
    ]

    valores_aprendidos = aprendizaje_pasivo(
        estados=estados,
        inicio="almacen",
        episodios=50,
        alpha=0.4,
        gamma=0.9
    )

    print("valores aprendidos:")

    for estado in valores_aprendidos:

        print(
            estado,
            "->",
            valores_aprendidos[estado]
        )

    # el dron:
    # - no elige acciones
    # - solo sigue una politica fija
    # - aprende que tan buenos son los estados
    #   usando experiencia