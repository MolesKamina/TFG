# sensor.py
import random
from dispositivo import Dispositivo
from nodo import Nodo

class Sensor(Dispositivo):
    def __init__(self, id, description, nodo: Nodo=None):
        super().__init__(id, description, nodo)

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_nodo(self):
        return self.nodo

    def generar_valor(self, node_behavior=0, date=None):
        # Switch case para determinar el comportamiento según el nodo
        if node_behavior == 1:
            # Comportamiento predeterminado (actual)
            return self._generar_valor_default(date)
        # elif node_behavior == 2:
        #     # Comportamiento especial para el nodo 2
        #     return self._generar_valor_nodo2(date)
        # elif node_behavior == 3:
        #     # Comportamiento especial para el nodo 3
        #     return self._generar_valor_nodo3(date)
        else:
            raise ValueError("Comportamiento de nodo no válido")

    def _generar_valor_default(self, date):
        if "Temperatura" in self.description:
            # Generar un valor aleatorio simulando un sensor de temperatura
            return round(random.uniform(15.0, 25.0), 1)  # Rango normal de temperaturas entre 15°C y 25°C
        elif "Movimiento" in self.description:
            # Utilizar la lógica del método get_value para simular un sensor de movimiento
            if date is None:
                raise ValueError("Debe proporcionar una fecha para generar el valor de movimiento")
            
            if date.weekday() >= 5:  # 5 es sábado, 6 es domingo
                # Si es fin de semana, asignar un valor fijo de 0
                return 0.0
            # Chequear si la hora está entre las 9:00 y las 17:00
            elif 9 <= date.hour < 17:
                value = 1.0
            else:
                value = 0.0

            # Aleatoriamente, con 0.1 de posibilidades, cambiar el valor por uno random entre 0 y 1
            if random.random() < 0.1:
                value = random.uniform(0, 1)

            return value