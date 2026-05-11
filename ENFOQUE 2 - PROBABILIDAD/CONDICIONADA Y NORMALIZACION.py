"""
probabilidad condicionada y normalizacion

queremos calcular:
¿cual es la probabilidad de que el ruido sea un gato
sabiendo que la ventana esta cerrada?

normalizar significa ajustar valores para que las
probabilidades finales sumen exactamente 1.
"""

# =========================
# probabilidades iniciales
# =========================

# creencias antes de tener evidencia
p_gato = 0.6
p_viento = 0.4

print("=== probabilidades iniciales ===")
print("probabilidad de gato   =", p_gato)
print("probabilidad de viento =", p_viento)

# =========================
# nueva evidencia
# =========================

print("\nla ventana esta cerrada...\n")

# valores "crudos" despues de observar la evidencia
p_gato_dado_ventana = 0.9
p_viento_dado_ventana = 0.2

print("valores sin normalizar:")
print("gato   =", p_gato_dado_ventana)
print("viento =", p_viento_dado_ventana)

# =========================
# normalizacion
# =========================

# sumamos los valores
suma_cruda = p_gato_dado_ventana + p_viento_dado_ventana

# ajustamos para que sumen 1
p_gato_normalizado = p_gato_dado_ventana / suma_cruda
p_viento_normalizado = p_viento_dado_ventana / suma_cruda

# =========================
# resultados finales
# =========================

print("\n=== probabilidades normalizadas ===")
print("prob(gato | ventana cerrada)   =", round(p_gato_normalizado, 4))
print("prob(viento | ventana cerrada) =", round(p_viento_normalizado, 4))

# mostrar en porcentaje
print("\nen porcentaje:")
print("gato   =", round(p_gato_normalizado * 100, 2), "%")
print("viento =", round(p_viento_normalizado * 100, 2), "%")

# comprobacion
suma_final = p_gato_normalizado + p_viento_normalizado

print("\nsuma final =", round(suma_final, 4))

if round(suma_final, 4) == 1.0:
    print("la normalizacion fue correcta")
else:
    print("hay un error en la normalizacion")