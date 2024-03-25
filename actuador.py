from dispositivo import Dispositivo
from nodo import Nodo

class Actuador(Dispositivo):
    def __init__(self, nodo: Nodo):
        super().__init__(nodo)

    def ejecutar_accion(self, accion):
        # Simular ejecución de una acción
        print(f"Ejecutando acción {accion} en el nodo {self.nodo.get_identificador()}")
