# sensor.py
import random
from dispositivo import Dispositivo
from nodo import Nodo

class Sensor(Dispositivo):
    def __init__(self, id, description, nodo: Nodo=None):
        self.id = id
        self.description = description
        if nodo:
            super().__init__(nodo)

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_nodo(self):
        return self.nodo

    def generar_valor(self):
        # Generar un valor aleatorio entre 0 y 1
        return random.random()