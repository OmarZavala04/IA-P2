"""
regla de la cadena
permite descomponer una probabilidad conjunta en partes pequeñas.

idea:
p(a, b, c) = p(a) * p(b | a) * p(c | a, b)

esto es clave en IA porque:
- reduce problemas complejos
- permite construir modelos probabilísticos grandes
- es base de redes bayesianas

en vez de adivinar todo junto,
vamos construyendo paso a paso.
"""

def prob_conjunta(p_a, p_b_dado_a, p_c_dado_a_y_b):
    """
    calcula p(a,b,c) usando regla de la cadena
    """

    return p_a * p_b_dado_a * p_c_dado_a_y_b


# =========================
# EJEMPLO
# =========================

p_total = prob_conjunta(
    p_a=0.5,
    p_b_dado_a=0.4,
    p_c_dado_a_y_b=0.8
)

print("p(a, b, c) =", round(p_total, 4))
print("porcentaje:", round(p_total * 100, 2), "%")

"""
interpretacion:
cada condicion va reduciendo el espacio de posibilidades.

- primero pasa a
- luego b depende de a
- luego c depende de todo lo anterior

esto es literalmente como construyen razonamiento los modelos probabilísticos:
paso a paso, encadenando incertidumbre.
"""