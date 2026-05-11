"""
mcmc (markov chain monte carlo)

mcmc sirve para aproximar probabilidades
cuando calcularlas exactamente seria demasiado caro.

idea general:
- tenemos una distribucion objetivo
- no sabemos calcularla facil
- entonces generamos MUCHAS muestras
- contamos que tan seguido aparece cada estado

si un estado aparece mucho:
-> probablemente tiene alta probabilidad

si aparece poco:
-> probablemente tiene baja probabilidad

esto se usa mucho en:
- redes bayesianas
- inteligencia artificial probabilistica
- inferencia bayesiana
- fisica estadistica
- machine learning

aqui implementamos:
metropolis-hastings
que es uno de los algoritmos mcmc mas famosos
"""

import random
import matplotlib.pyplot as plt


# ==========================================
# distribucion objetivo
# ==========================================

"""
esta es la distribucion que queremos aproximar.

no importa si suma exactamente 1.
mcmc solo necesita pesos relativos.
"""

objetivo = {
    "estado_a": 0.1,
    "estado_b": 0.4,
    "estado_c": 0.5
}


def prob_objetivo(estado):
    """
    regresa el peso/probabilidad del estado
    """
    return objetivo[estado]


# ==========================================
# propuesta de nuevos estados
# ==========================================

def proponer_estado(actual, todos_estados):
    """
    propone un nuevo estado aleatorio

    esto es como:
    "quiero intentar moverme a otro estado"
    """

    candidatos = [
        e for e in todos_estados
        if e != actual
    ]

    return random.choice(candidatos)


# ==========================================
# algoritmo metropolis-hastings
# ==========================================

def metropolis_hastings(iteraciones,
                        estado_inicial):

    """
    algoritmo principal mcmc

    pasos:
    1. tengo estado actual
    2. propongo candidato
    3. calculo razon de aceptacion
    4. acepto o rechazo
    5. guardo el estado final
    """

    estado_actual = estado_inicial

    historial = [estado_actual]

    todos_estados = list(objetivo.keys())

    for i in range(iteraciones):

        # ==========================
        # proponer nuevo estado
        # ==========================

        candidato = proponer_estado(
            estado_actual,
            todos_estados
        )

        # ==========================
        # calcular probabilidades
        # ==========================

        p_actual = prob_objetivo(estado_actual)
        p_candidato = prob_objetivo(candidato)

        # ==========================
        # razon de aceptacion
        # ==========================

        if p_actual == 0:

            razon = 1.0

        else:

            razon = p_candidato / p_actual

        # ==========================
        # decidir si aceptamos
        # ==========================

        aceptar = (
            random.random()
            < min(1.0, razon)
        )

        if aceptar:
            estado_actual = candidato

        # guardar muestra
        historial.append(estado_actual)

    return historial


# ==========================================
# estimar distribucion
# ==========================================

def estimar_distribucion(muestras):
    """
    cuenta frecuencia de cada estado
    """

    conteo = {}

    for estado in muestras:

        conteo[estado] = (
            conteo.get(estado, 0)
            + 1
        )

    total = len(muestras)

    distribucion = {}

    for estado, veces in conteo.items():

        distribucion[estado] = veces / total

    return distribucion


# ==========================================
# visualizar resultados
# ==========================================

def graficar_distribuciones(real, aproximada):
    """
    compara distribucion real vs aproximada
    """

    estados = list(real.keys())

    valores_reales = [
        real[e]
        for e in estados
    ]

    valores_aprox = [
        aproximada.get(e, 0)
        for e in estados
    ]

    x = range(len(estados))

    plt.figure(figsize=(8, 5))

    plt.bar(
        [i - 0.2 for i in x],
        valores_reales,
        width=0.4,
        label="real"
    )

    plt.bar(
        [i + 0.2 for i in x],
        valores_aprox,
        width=0.4,
        label="aproximada"
    )

    plt.xticks(x, estados)

    plt.ylabel("probabilidad")
    plt.title("mcmc - distribucion real vs aproximada")

    plt.legend()
    plt.grid(True)

    plt.show()


# ==========================================
# ejecutar simulacion
# ==========================================

if __name__ == "__main__":

    muestras = metropolis_hastings(
        iteraciones=5000,
        estado_inicial="estado_a"
    )

    aproximacion = estimar_distribucion(muestras)

    print("distribucion aproximada con mcmc:\n")

    for estado, prob in aproximacion.items():

        print(
            estado,
            "->",
            round(prob, 4)
        )

    print("\ndistribucion objetivo real:\n")

    for estado, prob in objetivo.items():

        print(
            estado,
            "->",
            prob
        )

    # graficar
    graficar_distribuciones(
        objetivo,
        aproximacion
    )

    print("\nexplicacion:")
    print("- mcmc no calcula todo exacto")
    print("- genera muestras poco a poco")
    print("- los estados mas visitados son mas probables")
    print("- mientras mas iteraciones, mejor aproximacion")
    print("- metropolis-hastings acepta movimientos probables")
    print("- movimientos poco probables a veces tambien se aceptan")