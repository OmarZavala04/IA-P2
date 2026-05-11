# Generador probabilistico de recetas de cocina
# Este programa crea recetas simples usando
# reglas probabilisticas lexicalizadas.
#
# cambiamos totalmente la tematica:
# ahora no generamos oraciones gramaticales,
# sino instrucciones de cocina aleatorias.

import random

class GeneradorRecetas:
    def __init__(self):

        # estructura probabilistica de recetas
        self.reglas = {

            "RECETA": [
                ("ACCION INGREDIENTE COMPLEMENTO", 1.0)
            ],

            "ACCION": [
                ("hornea", 0.3),
                ("mezcla", 0.4),
                ("frie", 0.3)
            ],

            "INGREDIENTE": [
                ("pollo", 0.3),
                ("pasta", 0.4),
                ("vegetales", 0.3)
            ],

            "COMPLEMENTO": [
                ("con salsa picante", 0.4),
                ("con queso", 0.3),
                ("con especias", 0.3)
            ]
        }

    def generar_receta(self, simbolo="RECETA"):
        """
        genera una receta usando reglas probabilisticas
        """

        # si ya no hay mas reglas, es palabra final
        if simbolo not in self.reglas:
            return simbolo

        producciones = self.reglas[simbolo]

        # suma total de probabilidades
        total = sum(prob for _, prob in producciones)

        # numero aleatorio
        aleatorio = random.uniform(0, total)

        acumulado = 0

        # elegimos produccion segun probabilidades
        for produccion, prob in producciones:

            acumulado += prob

            if aleatorio <= acumulado:

                return " ".join(
                    self.generar_receta(s)
                    for s in produccion.split()
                )

# =========================
# PRUEBAS
# =========================

chef_virtual = GeneradorRecetas()

print("recetas generadas:\n")

for i in range(5):

    receta = chef_virtual.generar_receta()

    print(
        "receta",
        i + 1,
        "->",
        receta
    )

# ejemplos posibles:
# - mezcla pasta con queso
# - hornea pollo con especias
# - frie vegetales con salsa picante
#
# ideas parecidas se usan en:
# - generacion procedural
# - asistentes virtuales
# - videojuegos
# - sistemas de texto automatico