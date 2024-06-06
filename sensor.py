# sensor.py

import random
from dispositivo import Dispositivo
from nodo import Nodo

class Sensor(Dispositivo):
    def __init__(self, id, description, nodo: Nodo=None):
        """
        Inicializa un nuevo Sensor

        Args:
            id (str): El identificador único del Sensor.
            description (str): La descripción del Sensor.
            nodo (Nodo): El nodo al que está asociado el Sensor, si aplica.
        """
        super().__init__(id, description, nodo)
        self.ultimo_valor_temperatura = None  # Almacena el último valor de temperatura generado

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_nodo(self):
        return self.nodo

    def generar_valor(self, node_behavior=0, date=None):
        if node_behavior == 1:
            return self._generar_valor_default(date)
        elif node_behavior == 2:
            return self._generar_valor_behavior2(date)
        else:
            raise ValueError("Comportamiento de nodo no válido")

    def _generar_valor_default(self, date):
        if date is None:
            raise ValueError("Debe proporcionar una fecha para generar el valor del sensor")
        if "Temperatura" in self.description:
            if self.ultimo_valor_temperatura is None:
                if 9 <= date.hour < 17 and date.weekday() < 5:
                    # Valor inicial en horario laboral
                    self.ultimo_valor_temperatura = round(random.uniform(21.0, 23.0), 1)  # Temperatura de oficina con aire acondicionado
                else:
                    # Valor inicial fuera del horario laboral
                    self.ultimo_valor_temperatura = round(random.uniform(15.0, 25.0), 1)  # Rango normal de temperaturas

            else:
                if 9 <= date.hour < 17 and date.weekday() < 5:
                    # Ajustar valor en horario laboral
                    self.ultimo_valor_temperatura += round(random.uniform(-0.5, 0.5), 1)
                    # Asegurar que el valor permanece dentro del rango de temperatura de oficina
                    if self.ultimo_valor_temperatura < 21.0:
                        self.ultimo_valor_temperatura = 21.0
                    elif self.ultimo_valor_temperatura > 23.0:
                        self.ultimo_valor_temperatura = 23.0
                else:
                    # Ajustar valor fuera del horario laboral
                    self.ultimo_valor_temperatura += round(random.uniform(-1.0, 1.0), 1)
                    # Asegurar que el valor permanece dentro de un rango razonable
                    if self.ultimo_valor_temperatura < 15.0:
                        self.ultimo_valor_temperatura = 15.0
                    elif self.ultimo_valor_temperatura > 25.0:
                        self.ultimo_valor_temperatura = 25.0

            return self.ultimo_valor_temperatura
        elif "Movimiento" in self.description:
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
    
    def _generar_valor_behavior2(self, date):
        if date is None:
            raise ValueError("Debe proporcionar una fecha para generar el valor del sensor")
        if "Iluminación" in self.description:
            if 15 <= date.hour < 19:
                return 1.0  # Simular que hay iluminación de 3 a 7 de la tarde
            else:
                return 0.0  # No hay iluminación fuera de ese horario

        elif "Temperatura" in self.description:
            return round(random.uniform(15.0, 25.0), 1)  # Generar temperatura sin control horario