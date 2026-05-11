"""
incertidumbre
la incertidumbre aparece cuando no sabemos exactamente
que resultado va a ocurrir.

en inteligencia artificial esto es muy comun:
- sensores con errores
- decisiones humanas
- clima
- trafico
- fallas
- predicciones

en lugar de decir:
"esto va a pasar seguro"

decimos:
"esto tiene cierta probabilidad de pasar"

la idea de este programa es:
1. simular un evento incierto
2. repetirlo muchas veces
3. observar que los resultados cambian
4. aproximar la probabilidad real

esto muestra como la ia trabaja con probabilidades
y no siempre con certezas absolutas.
"""

import random

def evento_aleatorio():
    """
    esta funcion representa un evento incierto.

    random.random()
    genera un numero decimal entre 0 y 1.

    si el numero es menor que 0.3:
        el evento ocurre

    eso significa:
        probabilidad = 30%
    """

    numero = random.random()

    if numero < 0.3:
        return True
    else:
        return False


def medir_incertidumbre(intentos):
    """
    repetimos el experimento muchas veces
    para observar el comportamiento probabilistico.

    intentos:
        cantidad de veces que probamos el evento
    """

    ocurre = 0
    no_ocurre = 0

    for _ in range(intentos):

        resultado = evento_aleatorio()

        if resultado:
            ocurre += 1
        else:
            no_ocurre += 1

    # frecuencia aproximada
    probabilidad_aproximada = ocurre / intentos

    return {
        "ocurre": ocurre,
        "no_ocurre": no_ocurre,
        "probabilidad": probabilidad_aproximada
    }


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":

    intentos = 1000

    resultado = medir_incertidumbre(intentos)

    print("RESULTADOS DEL EXPERIMENTO\n")

    print("veces que ocurrio el evento:")
    print(resultado["ocurre"])

    print("\nveces que NO ocurrio:")
    print(resultado["no_ocurre"])

    print("\nprobabilidad aproximada:")
    print(round(resultado["probabilidad"], 3))

    print("\ninterpretacion:")
    print("- no podemos saber si ocurrira en una prueba individual")
    print("- solo podemos estimar probabilidades")
    print("- mientras mas intentos hacemos,")
    print("  mas se acerca al valor real (~0.3)")

# conceptos importantes:
#
# - incertidumbre:
#     no saber exactamente que ocurrira
#
# - probabilidad:
#     medir que tan posible es un resultado
#
# - simulacion:
#     repetir muchas veces para observar patrones
#
# - frecuencia:
#     aproximacion experimental de la probabilidad