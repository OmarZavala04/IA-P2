"""
red bayesiana
una red bayesiana es una forma de representar causas y efectos con probabilidad.
se dibuja como nodos (variables) conectados con flechas (quien causa a quien).

mejora:
- ahora la red puede hacer inferencias simples
- podemos calcular probabilidades usando evidencia
- agregamos simulacion aleatoria para ver ejemplos

ejemplo:
si alguien tiene tos,
¿que tan probable es que tenga cancer?
"""

import random

# =========================
# DEFINICION DE LA RED
# =========================

nodos = ["fumar", "cancer", "tos"]

padres = {
    "fumar": [],
    "cancer": ["fumar"],
    "tos": ["fumar", "cancer"]
}

# =========================
# PROBABILIDADES
# =========================

# p(fumar=true)
p_fumar = 0.3

def p_cancer_dado_fumar(fuma):
    """
    p(cancer=true | fuma)
    """
    if fuma:
        return 0.2
    else:
        return 0.01

def p_tos_dado_fumar_y_cancer(fuma, tiene_cancer):
    """
    p(tos=true | fuma, cancer)
    """
    if tiene_cancer:
        return 0.9
    elif fuma:
        return 0.5
    else:
        return 0.1

# =========================
# FUNCIONES AUXILIARES
# =========================

def evento(probabilidad):
    """
    genera True o False segun una probabilidad
    ejemplo:
    evento(0.7) -> 70% True
    """
    return random.random() < probabilidad

def generar_persona():
    """
    genera una persona aleatoria usando la red bayesiana
    """
    fuma = evento(p_fumar)

    cancer = evento(
        p_cancer_dado_fumar(fuma)
    )

    tos = evento(
        p_tos_dado_fumar_y_cancer(fuma, cancer)
    )

    return {
        "fumar": fuma,
        "cancer": cancer,
        "tos": tos
    }

# =========================
# INFERENCIA SIMPLE
# =========================

def estimar_probabilidad_cancer_dado_tos(n_muestras=10000):
    """
    aproximamos:
    p(cancer=true | tos=true)

    usando simulacion
    """

    casos_con_tos = 0
    casos_con_tos_y_cancer = 0

    for _ in range(n_muestras):

        persona = generar_persona()

        if persona["tos"]:
            casos_con_tos += 1

            if persona["cancer"]:
                casos_con_tos_y_cancer += 1

    if casos_con_tos == 0:
        return 0

    return casos_con_tos_y_cancer / casos_con_tos

# =========================
# MOSTRAR INFORMACION
# =========================

print("nodos de la red:")
print(nodos)

print("\npadres:")
for nodo, p in padres.items():
    print(nodo, "->", p)

print("\nprobabilidades base:")
print("p(fumar=true) =", p_fumar)
print("p(cancer=true | fuma=true) =", p_cancer_dado_fumar(True))
print("p(cancer=true | fuma=false) =", p_cancer_dado_fumar(False))

print("\nejemplos de personas generadas:")
for i in range(5):
    print("persona", i + 1, "->", generar_persona())

# =========================
# CONSULTA BAYESIANA
# =========================

resultado = estimar_probabilidad_cancer_dado_tos()

print("\nresultado aproximado:")
print("p(cancer=true | tos=true) =", round(resultado, 4))

print("""
interpretacion:
- si aparece tos, la probabilidad de cancer aumenta
- eso pasa porque en la red:
  fumar influye en cancer
  y cancer influye en tos
- la red bayesiana conecta causas y efectos
- usamos probabilidad porque no hay certeza absoluta
""")