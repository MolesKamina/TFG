# sensor.py
import random
from nodo import Nodo

class Sensor:
    def __init__(self, nodo: Nodo):
        self.nodo = nodo

    def generar_valor(self):
        # Generar un valor aleatorio entre 0 y 1
        return random.random()
