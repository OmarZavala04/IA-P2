# salto atras dirigido por conflictos
# es parecido a backtracking, pero mas inteligente.
# cuando encuentra un conflicto, intenta brincar directo
# a la variable que lo causo.

def revisar_reglas(asignacion):
    """
    revisa si la asignacion actual rompe alguna regla
    """

    # regla 1:
    # no puede haber dos examenes el mismo dia
    materias = list(asignacion.keys())

    for i in range(len(materias)):
        for j in range(i + 1, len(materias)):

            m1 = materias[i]
            m2 = materias[j]

            # conflicto: mismo dia
            if asignacion[m1] == asignacion[m2]:
                return False, ("same_day", m2)

    # regla 2:
    # prog no puede ser lunes
    if "prog" in asignacion:

        if asignacion["prog"] == "lunes":
            return False, ("prog_lunes", "prog")

    return True, None


def salto_atras_conflictos(variables, dominios):

    # guardamos posicion de cada variable
    # esto ayuda a saber hasta donde brincar
    indice_variable = {}

    for i, var in enumerate(variables):
        indice_variable[var] = i

    # historial para ver que hizo el algoritmo
    historial_debug = []

    def intentar(index, asignacion_actual):

        # si ya asignamos todas las variables
        # ya encontramos solucion
        if index == len(variables):
            return asignacion_actual.copy(), None

        var_actual = variables[index]

        # por defecto:
        # salto atras normal
        mejor_salto = index - 1

        # probar cada valor posible
        for valor in dominios[var_actual]:

            asignacion_actual[var_actual] = valor

            ok, conflicto = revisar_reglas(asignacion_actual)

            historial_debug.append(
                f"probando {var_actual} = {valor} -> {'ok' if ok else 'conflicto'}"
            )

            if ok:

                # seguir con siguiente variable
                solucion, salto = intentar(
                    index + 1,
                    asignacion_actual
                )

                # si encontramos solucion final
                if solucion is not None:
                    return solucion, None

                # si el conflicto viene de mas atras
                # propagamos el salto
                if salto is not None and salto < index:

                    del asignacion_actual[var_actual]

                    return None, salto

            else:

                tipo_conflicto, variable_conflictiva = conflicto

                if tipo_conflicto == "same_day":

                    # brincar a variable que causo el choque
                    salto_conflicto = indice_variable[variable_conflictiva]

                elif tipo_conflicto == "prog_lunes":

                    salto_conflicto = indice_variable["prog"]

                else:

                    salto_conflicto = index - 1

                # guardar salto mas lejano
                if salto_conflicto < mejor_salto:
                    mejor_salto = salto_conflicto

            # quitar intento actual
            del asignacion_actual[var_actual]

        # no hubo solucion desde esta variable
        return None, mejor_salto

    solucion_final, _ = intentar(0, {})

    return solucion_final, historial_debug


if __name__ == "__main__":

    # variables = materias
    variables = [
        "mate",
        "fisica",
        "prog"
    ]

    # dominios = dias posibles
    dominios = {

        "mate": [
            "lunes",
            "miercoles",
            "viernes"
        ],

        "fisica": [
            "lunes",
            "miercoles",
            "viernes"
        ],

        "prog": [
            "lunes",
            "miercoles",
            "viernes"
        ]
    }

    solucion, debug = salto_atras_conflictos(
        variables,
        dominios
    )

    print("solucion encontrada:")
    print(solucion)

    print("\npasos del algoritmo:")

    for linea in debug:
        print(linea)