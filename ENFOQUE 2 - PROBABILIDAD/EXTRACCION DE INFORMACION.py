# Analizador simple de tickets de soporte
# Este programa usa expresiones regulares para extraer:
# - correos electronicos
# - numeros de ticket
# - horas
#
# la idea es cambiar totalmente la tematica:
# ahora simulamos mensajes de soporte tecnico.

import re

class AnalizadorTickets:
    def __init__(self, mensajes):
        self.mensajes = mensajes

    def extraer_correos(self):
        """
        busca correos electronicos dentro del texto
        ejemplo:
        soporte@gmail.com
        usuario123@hotmail.com
        """
        patron = r'\b[\w\.-]+@[\w\.-]+\.\w+\b'
        correos = re.findall(patron, self.mensajes)

        # eliminamos repetidos
        return list(set(correos))

    def extraer_tickets(self):
        """
        busca numeros de ticket tipo:
        TK-1023
        INC-5501
        """
        patron = r'\b[A-Z]{2,4}-\d{3,6}\b'
        tickets = re.findall(patron, self.mensajes)

        return list(set(tickets))

    def extraer_horas(self):
        """
        busca horas en formato:
        14:30
        09:15
        """
        patron = r'\b\d{1,2}:\d{2}\b'
        horas = re.findall(patron, self.mensajes)

        return list(set(horas))


# texto de ejemplo
mensajes = """
[09:15] El usuario reportó una falla en el sistema.
Ticket generado: TK-1023
Contacto: carlos.soporte@gmail.com

[14:30] Nueva incidencia detectada.
Numero de incidente: INC-5501
Enviar respuesta a admin.red@hotmail.com

[16:45] Seguimiento completado para TK-1023
"""

# creamos el analizador
analizador = AnalizadorTickets(mensajes)

# extraemos informacion
correos = analizador.extraer_correos()
tickets = analizador.extraer_tickets()
horas = analizador.extraer_horas()

# mostramos resultados
print("correos encontrados:")
for c in correos:
    print(" ", c)

print("\ntickets encontrados:")
for t in tickets:
    print(" ", t)

print("\nhoras encontradas:")
for h in horas:
    print(" ", h)

# este ejemplo muestra como regex puede servir
# para mineria de texto y extraccion automatica de informacion
# en sistemas reales de soporte o monitoreo