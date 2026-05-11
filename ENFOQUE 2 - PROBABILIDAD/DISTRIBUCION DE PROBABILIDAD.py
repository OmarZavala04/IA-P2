"""
distribucion de probabilidad aplicada a musica

una distribucion de probabilidad sirve para representar
que tan probable es que ocurra cada opcion.

en este ejemplo:
vamos a simular una app de musica
que intenta predecir que genero escuchara una persona despues.

cada genero tiene cierta probabilidad.

la suma de todas las probabilidades
debe ser igual a 1.
"""

# distribucion de probabilidad de gustos musicales

distribucion_musica = {
    "rock": 0.25,
    "pop": 0.30,
    "electronica": 0.15,
    "rap": 0.20,
    "jazz": 0.10
}

print("probabilidad de escuchar cada genero musical:\n")

# recorrer distribucion
for genero, probabilidad in distribucion_musica.items():

    porcentaje = probabilidad * 100

    print(
        "genero:",
        genero,
        "-> probabilidad =",
        probabilidad,
        "(",
        porcentaje,
        "% )"
    )

# comprobar suma total
suma = 0

for valor in distribucion_musica.values():

    suma += valor

print("\nsuma total de probabilidades:", suma)

# verificar si esta correcta
if abs(suma - 1.0) < 0.0001:

    print("la distribucion es valida")

else:

    print("la distribucion NO es valida")


# simulacion simple:
# escoger el genero mas probable

genero_mas_probable = None
prob_mayor = -1

for genero, probabilidad in distribucion_musica.items():

    if probabilidad > prob_mayor:

        prob_mayor = probabilidad
        genero_mas_probable = genero

print("\ngenero mas probable que escuche el usuario:")
print(genero_mas_probable, "con probabilidad de", prob_mayor)

# en IA las distribuciones de probabilidad
# se usan para:
# - predicciones
# - clasificacion
# - sistemas expertos
# - modelos bayesianos
# - aprendizaje automatico