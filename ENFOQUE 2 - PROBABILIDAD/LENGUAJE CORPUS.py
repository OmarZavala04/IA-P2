"""
modelo de lenguaje n-grama

un modelo n-grama aprende patrones de palabras en un texto.
la idea:
- mira grupos de palabras consecutivas
- aprende cuales palabras suelen aparecer despues de otras

ejemplo:
si muchas veces aparece:
"inteligencia artificial"

entonces despues de "inteligencia"
el modelo aprende que probablemente sigue "artificial".

si n = 2:
- usamos bigramas
- vemos 1 palabra y predecimos la siguiente

si n = 3:
- usamos trigramas
- vemos 2 palabras y predecimos la siguiente

esto se usa en:
- prediccion de texto
- autocompletado
- procesamiento de lenguaje natural
- modelos de lenguaje simples
"""

from collections import defaultdict
import random


class ModeloNGrama:
    def __init__(self, n):
        """
        n:
            tamaño del n-grama

        ejemplo:
            n=2 -> bigramas
            n=3 -> trigramas
        """

        self.n = n

        # estructura:
        # {
        #   prefijo: {
        #       palabra_siguiente: cantidad
        #   }
        # }
        self.ngramas = defaultdict(lambda: defaultdict(int))

        # vocabulario aprendido
        self.vocabulario = set()

    def entrenar(self, texto):
        """
        aprende patrones del texto
        """

        # pasamos todo a minusculas
        tokens = texto.lower().split()

        # guardamos palabras unicas
        self.vocabulario.update(tokens)

        # recorremos formando n-gramas
        for i in range(len(tokens) - self.n + 1):

            # ejemplo n=2:
            # ("la", "inteligencia")

            ngrama = tuple(tokens[i:i + self.n])

            # prefijo = todas menos la ultima
            prefijo = ngrama[:-1]

            # palabra objetivo = ultima
            siguiente = ngrama[-1]

            # contamos ocurrencia
            self.ngramas[prefijo][siguiente] += 1

    def predecir(self, prefijo_texto):
        """
        predice la siguiente palabra
        """

        prefijo = tuple(prefijo_texto.lower().split())

        # validacion
        if len(prefijo) != self.n - 1:
            raise ValueError(
                f"el prefijo debe tener {self.n - 1} palabras"
            )

        # buscamos palabras posibles
        opciones = self.ngramas[prefijo]

        if len(opciones) == 0:
            return None

        # total de ocurrencias
        total = sum(opciones.values())

        # calculamos probabilidades
        probabilidades = {}

        for palabra, conteo in opciones.items():
            probabilidades[palabra] = conteo / total

        # elegimos la mas probable
        mejor_palabra = max(
            probabilidades,
            key=probabilidades.get
        )

        return mejor_palabra, probabilidades[mejor_palabra]

    def generar_texto(self, inicio, longitud=10):
        """
        genera texto automaticamente
        usando el modelo aprendido
        """

        palabras = inicio.lower().split()

        for _ in range(longitud):

            # tomamos las ultimas n-1 palabras
            prefijo = tuple(palabras[-(self.n - 1):])

            opciones = self.ngramas.get(prefijo)

            if not opciones:
                break

            # seleccion aleatoria ponderada
            palabras_posibles = list(opciones.keys())
            pesos = list(opciones.values())

            siguiente = random.choices(
                palabras_posibles,
                weights=pesos,
                k=1
            )[0]

            palabras.append(siguiente)

        return " ".join(palabras)

    def mostrar_modelo(self):
        """
        imprime lo aprendido
        """

        print("modelo aprendido:\n")

        for prefijo, siguientes in self.ngramas.items():

            print("prefijo:", prefijo)

            total = sum(siguientes.values())

            for palabra, conteo in siguientes.items():

                prob = conteo / total

                print(
                    "   ->",
                    palabra,
                    "| veces =", conteo,
                    "| prob =", round(prob, 3)
                )

            print()


# ====================================
# ejemplo de uso
# ====================================

if __name__ == "__main__":

    texto = """
    la inteligencia artificial aprende patrones
    la inteligencia artificial ayuda en problemas
    la inteligencia humana aprende experiencia
    los modelos de lenguaje usan texto
    los modelos de lenguaje aprenden palabras
    """

    # crear modelo de bigramas
    modelo = ModeloNGrama(n=2)

    # entrenar
    modelo.entrenar(texto)

    # mostrar lo aprendido
    modelo.mostrar_modelo()

    # hacer prediccion
    prefijo = "la"

    resultado = modelo.predecir(prefijo)

    if resultado is not None:

        palabra, prob = resultado

        print("prediccion para:", prefijo)
        print(
            "siguiente palabra mas probable =",
            palabra
        )
        print(
            "probabilidad =",
            round(prob, 4)
        )

    # generar texto automatico
    print("\ntexto generado automaticamente:\n")

    generado = modelo.generar_texto(
        inicio="la",
        longitud=8
    )

    print(generado)

    print("\nexplicacion:")
    print("- el modelo aprende viendo palabras consecutivas")
    print("- usa frecuencia para calcular probabilidades")
    print("- mientras mas texto tenga, mejor aprende")
    print("- esto es la base de modelos de lenguaje mas avanzados")