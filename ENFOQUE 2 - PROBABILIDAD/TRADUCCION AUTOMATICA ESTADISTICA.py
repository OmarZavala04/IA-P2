# Este código implementa un traductor simple palabra por palabra
# usando un diccionario como base para la traducción.

class TraductorEstadistico:
    def __init__(self):
        # diccionario base de traducción
        self.diccionario = {
            'hola': 'hello',
            'adios': 'goodbye',
            'gracias': 'thank you',
            'por': 'for',
            'favor': 'please',
            'si': 'yes',
            'no': 'no'
        }

    def traducir(self, frase):
        """
        traduce palabra por palabra.
        si no encuentra la palabra, la deja igual.
        """
        palabras = frase.lower().split()
        traduccion = []

        for palabra in palabras:
            traduccion.append(
                self.diccionario.get(palabra, palabra)
            )

        return ' '.join(traduccion)


# =========================
# USO DEL TRADUCTOR
# =========================

traductor = TraductorEstadistico()

frase_original = "hola gracias por favor"
frase_traducida = traductor.traducir(frase_original)

print("frase original:", frase_original)
print("frase traducida:", frase_traducida)

"""
mejora aplicada:
- se corrige "por favor" (antes no funcionaba como frase)
- ahora todo se pasa a minusculas para evitar errores
- se mantiene la idea de traduccion palabra por palabra

idea importante:
esto NO es traducción real moderna.
es un modelo tipo "bolsa de palabras":
- no entiende contexto
- no entiende gramática
- solo reemplaza tokens

los traductores reales usan:
- modelos neuronales
- embeddings
- transformers
"""