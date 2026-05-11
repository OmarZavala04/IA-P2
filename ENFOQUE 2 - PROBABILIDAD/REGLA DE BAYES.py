"""
regla de bayes
la regla de bayes sirve para actualizar creencias con evidencia nueva.

idea central:
- tienes una creencia inicial (prior)
- llega evidencia (prueba positiva)
- actualizas la creencia (posterior)

esto evita errores tipo:
"salí positivo = seguro estoy enfermo"
"""

def prob_bayes(prior_enfermo, sens_prueba, falso_positivo):
    """
    calcula p(enfermo | positivo)
    usando regla de bayes
    """

    p_enfermo = prior_enfermo
    p_sano = 1 - p_enfermo

    p_positivo_dado_enfermo = sens_prueba
    p_positivo_dado_sano = falso_positivo

    # bayes numerador
    numerador = p_positivo_dado_enfermo * p_enfermo

    # prob total de positivo
    denominador = (
        p_positivo_dado_enfermo * p_enfermo +
        p_positivo_dado_sano * p_sano
    )

    if denominador == 0:
        return 0

    return numerador / denominador


# =========================
# EJEMPLO
# =========================

resultado = prob_bayes(
    prior_enfermo=0.01,
    sens_prueba=0.90,
    falso_positivo=0.05
)

print("p(enfermo | positivo) =", round(resultado, 4))
print("en porcentaje:", round(resultado * 100, 2), "%")

"""
interpretacion:
aunque la prueba sea buena (90% sensibilidad),
si la enfermedad es rara (1%),
muchos positivos son falsos positivos.

esto es base en:
- diagnostico medico
- IA probabilistica
- filtros de spam
- deteccion de fraude

bayes = actualizar creencias sin caer en intuiciones engañosas
"""