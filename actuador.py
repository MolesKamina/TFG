from dispositivo import Dispositivo
from nodo import Nodo

class Actuador(Dispositivo):
    def __init__(self, id, description, nodo: Nodo):
        self.id = id
        self.description = description
        super().__init__(nodo)

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_nodo(self):
        return self.nodo

    def ejecutar_accion(self, accion):
        # Simular ejecución de una acción
        print(f"Ejecutando acción {accion} en el nodo {self.get_id()}")
