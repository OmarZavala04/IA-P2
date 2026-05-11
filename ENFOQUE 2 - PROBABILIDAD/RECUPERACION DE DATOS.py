# Este código implementa un sistema simple de recuperación de documentos.
# El sistema busca documentos que contengan todas las palabras
# escritas en una consulta.

import numpy as np

class DocumentRetrieval:

    def __init__(self):

        # =========================
        # BASE DE DOCUMENTOS
        # =========================

        self.documentos = {
            1: "El perro juega en el parque.",
            2: "El gato duerme en la casa.",
            3: "Los pájaros cantan en la mañana.",
            4: "El perro y el gato son amigos.",
            5: "Los niños juegan en el parque."
        }

    def buscar(self, consulta):
        """
        busca documentos que contengan
        todas las palabras de la consulta
        """

        # convertir consulta a minusculas
        consulta_palabras = consulta.lower().split()

        resultados = []

        # recorrer documentos
        for id_doc, doc in self.documentos.items():

            texto = doc.lower()

            # verificar si TODAS las palabras existen
            if all(palabra in texto for palabra in consulta_palabras):

                resultados.append(id_doc)

        return resultados

    def mostrar_documentos(self):
        """
        muestra todos los documentos almacenados
        """

        print("=== documentos disponibles ===\n")

        for id_doc, texto in self.documentos.items():

            print("documento", id_doc, "->", texto)

# =========================
# CREAR SISTEMA
# =========================

sistema_recuperacion = DocumentRetrieval()

# mostrar documentos
sistema_recuperacion.mostrar_documentos()

# =========================
# CONSULTA
# =========================

consulta = "perro parque"

print("\nconsulta realizada:", consulta)

# buscar resultados
resultados = sistema_recuperacion.buscar(consulta)

# =========================
# RESULTADOS
# =========================

print("\n=== documentos encontrados ===\n")

if len(resultados) == 0:

    print("no se encontraron documentos.")

else:

    for doc_id in resultados:

        print(
            "documento",
            doc_id,
            "->",
            sistema_recuperacion.documentos[doc_id]
        )