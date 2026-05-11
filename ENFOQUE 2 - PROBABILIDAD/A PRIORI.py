"""
probabilidad a priori
tambien se dice prior es lo que tu crees antes de ver nueva informacion.

ejemplo:
si tengo una bolsa con dulces y aun no saco ninguno,
puedo calcular que tan probable es sacar cada color
solo viendo cuantos hay de cada uno.

vamos a:
1. contar dulces de cada color
2. calcular probabilidades a priori
3. imprimir resultados en decimal y porcentaje
"""

# cantidad de dulces por color
rojos = 3
azules = 1

# total de dulces
total = rojos + azules

# probabilidades a priori
prob_rojo_apriori = rojos / total
prob_azul_apriori = azules / total

# mostrar resultados
print("=== probabilidades a priori ===\n")

print("dulces rojos :", rojos)
print("dulces azules:", azules)
print("total dulces :", total)

print("\nprobabilidad de sacar rojo =", prob_rojo_apriori)
print("probabilidad de sacar azul =", prob_azul_apriori)

# convertir a porcentaje
print("\nen porcentaje:")
print("rojo =", round(prob_rojo_apriori * 100, 2), "%")
print("azul =", round(prob_azul_apriori * 100, 2), "%")

# comprobacion
suma_probs = prob_rojo_apriori + prob_azul_apriori

print("\nsuma total de probabilidades =", suma_probs)

if suma_probs == 1:
    print("la distribucion es valida")
else:
    print("la distribucion NO es valida")