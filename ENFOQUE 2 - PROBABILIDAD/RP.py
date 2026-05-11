# Implementa una red bayesiana simple para almacenar
# y consultar probabilidades condicionales.

from collections import defaultdict

class RedBayesiana:

    def __init__(self):
        """
        diccionario tipo:
        {
            evento: {
                dado_evento: probabilidad
            }
        }
        """
        self.probabilidades = defaultdict(dict)

    def agregar_probabilidad(self, evento, dado_evento, probabilidad):
        """
        guarda una probabilidad condicional:
        P(evento | dado_evento)
        """

        # validacion simple
        if probabilidad < 0 or probabilidad > 1:
            print("error: la probabilidad debe estar entre 0 y 1")
            return

        self.probabilidades[evento][dado_evento] = probabilidad

    def calcular_probabilidad(self, evento, dado_evento):
        """
        devuelve:
        P(evento | dado_evento)
        """

        return self.probabilidades[evento].get(
            dado_evento,
            "probabilidad no definida"
        )

    def mostrar_probabilidades(self):
        """
        muestra todas las probabilidades guardadas
        """

        print("\n=== probabilidades registradas ===\n")

        for evento, condicionadas in self.probabilidades.items():

            for dado_evento, probabilidad in condicionadas.items():

                print(
                    "P(" + evento + " | " + dado_evento + ") =",
                    probabilidad
                )

# =========================
# CREAR RED BAYESIANA
# =========================

red = RedBayesiana()

# =========================
# AGREGAR PROBABILIDADES
# =========================

red.agregar_probabilidad("Emmanuel", "Fernanda", 0.7)
red.agregar_probabilidad("Emiliano", "Fernanda", 0.6)
red.agregar_probabilidad("Fernanda", "Emiliano", 0.8)

# =========================
# CONSULTAS
# =========================

prob1 = red.calcular_probabilidad("Emmanuel", "Fernanda")
prob2 = red.calcular_probabilidad("Emiliano", "Fernanda")
prob3 = red.calcular_probabilidad("Fernanda", "Emiliano")

# =========================
# RESULTADOS
# =========================

print("=== resultados de la red bayesiana ===\n")

print(
    "probabilidad de Emmanuel dado Fernanda =",
    prob1
)

print(
    "probabilidad de Emiliano dado Fernanda =",
    prob2
)

print(
    "probabilidad de Fernanda dado Emiliano =",
    prob3
)

# mostrar toda la red
red.mostrar_probabilidades()