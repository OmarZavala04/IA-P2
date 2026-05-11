# Generador procedural de misiones para videojuego RPG
# Este programa usa reglas probabilisticas
# para crear misiones aleatorias.
#
# cambiamos completamente la tematica:
# ahora ya no generamos oraciones,
# sino eventos y misiones de fantasia.

import random

class GeneradorMisiones:
    def __init__(self):

        # reglas del generador
        # cada categoria tiene opciones con probabilidades
        self.reglas = {

            "MISION": [
                (["OBJETIVO", "LUGAR"], 0.7),
                (["OBJETIVO", "ENEMIGO", "LUGAR"], 0.3)
            ],

            "OBJETIVO": [
                (["rescata"], 0.3),
                (["protege"], 0.2),
                (["encuentra"], 0.3),
                (["destruye"], 0.2)
            ],

            "ENEMIGO": [
                (["al dragon"], 0.3),
                (["a los bandidos"], 0.4),
                (["al hechicero oscuro"], 0.3)
            ],

            "LUGAR": [
                (["en el bosque antiguo"], 0.4),
                (["en la fortaleza abandonada"], 0.3),
                (["en las montañas heladas"], 0.3)
            ]
        }

    def generar(self, simbolo="MISION"):
        """
        genera texto usando reglas probabilisticas
        """

        # si ya es palabra terminal
        if simbolo not in self.reglas:
            return simbolo

        opciones = self.reglas[simbolo]

        # separamos reglas y probabilidades
        producciones, probabilidades = zip(*opciones)

        # elegimos segun peso probabilistico
        seleccion = random.choices(
            producciones,
            weights=probabilidades,
            k=1
        )[0]

        # expansion recursiva
        return " ".join(
            self.generar(s)
            for s in seleccion
        )

# =========================
# PRUEBA DEL GENERADOR
# =========================

generador = GeneradorMisiones()

print("misiones generadas:\n")

for i in range(5):

    mision = generador.generar()

    print(
        "mision",
        i + 1,
        "->",
        mision
    )

# este tipo de sistemas se usa en:
# - videojuegos RPG
# - generacion procedural
# - chatbots narrativos
# - IA para historias dinamicas