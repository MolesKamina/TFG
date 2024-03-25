# sensor.py
import random
from dispositivo import Dispositivo
from nodo import Nodo

class Sensor(Dispositivo):
    def __init__(self, nodo: Nodo):
        super().__init__(nodo)

    def generar_valor(self):
        # Generar un valor aleatorio entre 0 y 1
        return random.random()