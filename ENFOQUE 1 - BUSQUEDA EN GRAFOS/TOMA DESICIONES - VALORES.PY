# Planeacion de rutas con iteracion de valores
# imaginemos un robot repartidor en una ciudad.
# el robot quiere llegar a la "entrega"
# ganando la mayor cantidad de puntos posibles.
# cada lugar tiene diferentes caminos y costos.
# la idea:
# calcular que tan bueno es estar en cada lugar
# suponiendo que el robot siempre elegira el mejor camino despues.

# formula:
# valor(lugar) =
# recompensa inmediata +
# descuento * mejor valor futuro posible

def calcular_valores(lugares, movimientos, siguiente_lugar, ganancia, descuento, iteraciones):
    """
    calcula el valor aproximado de cada lugar.

    lugares:
        lista de lugares

    movimientos:
        dict lugar -> lista de movimientos posibles

    siguiente_lugar(lugar, movimiento):
        dice a donde llego

    ganancia(lugar, movimiento):
        puntos inmediatos del movimiento

    descuento:
        que tanto importa el futuro

    iteraciones:
        cuantas veces se actualizan los valores
    """

    # empezamos suponiendo que todos valen 0
    valores = {}

    for lugar in lugares:
        valores[lugar] = 0

    # repetimos varias veces
    for _ in range(iteraciones):

        nuevos = {}

        for lugar in lugares:

            opciones = movimientos[lugar]

            # si no hay movimientos posibles
            # es un lugar final
            if len(opciones) == 0:
                nuevos[lugar] = 0

            else:
                posibles_valores = []

                # revisamos cada movimiento
                for mov in opciones:

                    destino = siguiente_lugar(lugar, mov)

                    recompensa_actual = ganancia(lugar, mov)

                    # valor estimado:
                    # recompensa actual +
                    # valor futuro descontado
                    valor_estimado = (
                        recompensa_actual +
                        descuento * valores[destino]
                    )

                    posibles_valores.append(valor_estimado)

                # nos quedamos con el mejor movimiento
                nuevos[lugar] = max(posibles_valores)

        valores = nuevos

    return valores


def mejor_ruta(lugares, movimientos, siguiente_lugar, ganancia, valores, descuento):
    """
    decide cual es el mejor movimiento
    en cada lugar.
    """

    politica = {}

    for lugar in lugares:

        opciones = movimientos[lugar]

        if len(opciones) == 0:

            politica[lugar] = None

        else:

            mejor_movimiento = None
            mejor_puntaje = None

            for mov in opciones:

                destino = siguiente_lugar(lugar, mov)

                puntaje = (
                    ganancia(lugar, mov) +
                    descuento * valores[destino]
                )

                if (
                    mejor_movimiento is None or
                    puntaje > mejor_puntaje
                ):
                    mejor_movimiento = mov
                    mejor_puntaje = puntaje

            politica[lugar] = mejor_movimiento

    return politica


if __name__ == "__main__":

    # lugares del mapa
    lugares = [
        "bodega",
        "cruce",
        "entrega"
    ]

    # movimientos posibles
    movimientos = {
        "bodega": [
            "camino_rapido",
            "camino_largo"
        ],

        "cruce": [
            "seguir"
        ],

        "entrega": []
    }

    def siguiente_lugar(lugar, movimiento):

        if lugar == "bodega" and movimiento == "camino_rapido":
            return "entrega"

        if lugar == "bodega" and movimiento == "camino_largo":
            return "cruce"

        if lugar == "cruce" and movimiento == "seguir":
            return "entrega"

        return lugar

    def ganancia(lugar, movimiento):

        # camino rapido:
        # llega directo pero gasta mucha bateria
        if lugar == "bodega" and movimiento == "camino_rapido":
            return 8

        # camino largo:
        # tarda mas pero recoge otro paquete
        if lugar == "bodega" and movimiento == "camino_largo":
            return 5

        # seguir desde cruce hasta entrega
        if lugar == "cruce" and movimiento == "seguir":
            return 6

        return 0

    factor_descuento = 0.9

    valores = calcular_valores(
        lugares,
        movimientos,
        siguiente_lugar,
        ganancia,
        factor_descuento,
        iteraciones=10
    )

    print("valor estimado de cada lugar:")

    for lugar in lugares:
        print(
            lugar,
            "->",
            valores[lugar]
        )

    politica = mejor_ruta(
        lugares,
        movimientos,
        siguiente_lugar,
        ganancia,
        valores,
        factor_descuento
    )

    print("\nmejor movimiento en cada lugar:")

    for lugar in lugares:
        print(
            lugar,
            "->",
            politica[lugar]
        )

    # el algoritmo:
    # - calcula que tan conveniente es cada lugar
    # - considera recompensa actual y futuro
    # - despues escoge el mejor movimiento posible