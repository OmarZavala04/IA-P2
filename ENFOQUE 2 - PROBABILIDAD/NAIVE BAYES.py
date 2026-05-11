# Este código implementa un clasificador Naïve Bayes Gaussiano
# SIN usar sklearn ni librerías externas de machine learning.
# Calcula:
# - probabilidades a priori
# - medias y desviaciones por clase
# - probabilidad gaussiana
# - predicción de nuevas muestras
# - precisión del modelo

import numpy as np
import pandas as pd

# ======================= DATOS =======================

data = {
    'Característica1': [1.0, 2.0, 1.5, 1.2, 2.5, 1.8, 2.2, 1.0, 1.4, 2.0],
    'Característica2': [0.5, 1.5, 1.0, 0.7, 2.0, 1.5, 1.8, 0.6, 1.1, 1.4],
    'Clase': ['A', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B']
}

df = pd.DataFrame(data)

# ======================= FUNCIONES =======================

def calcular_probabilidades_clase(df):
    """
    Calcula probabilidades a priori:
    P(clase)
    """
    probabilidades = {}

    total = len(df)

    for clase in df['Clase'].unique():
        cantidad = len(df[df['Clase'] == clase])
        probabilidades[clase] = cantidad / total

    return probabilidades


def calcular_parametros(df, clase):
    """
    Calcula media y desviación estándar
    de cada característica para una clase.
    """

    subset = df[df['Clase'] == clase]

    medias = subset[['Característica1', 'Característica2']].mean()

    desviaciones = subset[['Característica1', 'Característica2']].std()

    return medias, desviaciones


def probabilidad_gaussiana(x, media, desviacion):
    """
    Distribución normal (gaussiana)
    """

    # evitar division entre cero
    if desviacion == 0:
        desviacion = 1e-6

    exponente = np.exp(
        -((x - media) ** 2) / (2 * desviacion ** 2)
    )

    return (
        1 / (np.sqrt(2 * np.pi) * desviacion)
    ) * exponente


def predecir(df, entrada):
    """
    Predice la clase más probable
    para una entrada nueva.
    """

    probabilidades_clase = calcular_probabilidades_clase(df)

    clases = df['Clase'].unique()

    probabilidades_finales = {}

    for clase in clases:

        medias, desviaciones = calcular_parametros(df, clase)

        # comenzamos con P(clase)
        prob_total = probabilidades_clase[clase]

        # multiplicamos probabilidades gaussianas
        for i in range(len(entrada)):

            prob_total *= probabilidad_gaussiana(
                entrada[i],
                medias.iloc[i],
                desviaciones.iloc[i]
            )

        probabilidades_finales[clase] = prob_total

    # mostrar probabilidades calculadas
    print("\nProbabilidades calculadas:")
    for clase, prob in probabilidades_finales.items():
        print(clase, "->", prob)

    # regresar clase con mayor probabilidad
    return max(probabilidades_finales, key=probabilidades_finales.get)


def evaluar_modelo(df):
    """
    Evalúa el modelo usando los mismos datos.
    """

    correctos = 0
    total = len(df)

    for i in range(total):

        entrada = [
            df.iloc[i]['Característica1'],
            df.iloc[i]['Característica2']
        ]

        clase_real = df.iloc[i]['Clase']

        clase_predicha = predecir(df, entrada)

        if clase_real == clase_predicha:
            correctos += 1

    precision = correctos / total

    return precision


# ======================= PRUEBA =======================

nueva_entrada = [1.5, 1.0]

clase_predicha = predecir(df, nueva_entrada)

print("\nNueva entrada:", nueva_entrada)

print("Clase predicha:", clase_predicha)

# ======================= EVALUACIÓN =======================

precision = evaluar_modelo(df)

print("\nPrecisión aproximada del modelo:", round(precision, 4))