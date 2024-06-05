# dispositivo.py
from nodo import Nodo

class Dispositivo:
    def __init__(self, id, description, nodo: Nodo=None):
        """
        Inicializa un nuevo dispositivo que gestiona la información relacionada con 
        Sensores y Actuadores.

        Args:
            id (str): El identificador único del dispositivo.
            description (str): La descripción del dispositivo.
            nodo (Nodo): El nodo al que está asociado el dispositivo, si aplica.
        """
        self.id = id
        self.description = description
        if nodo:
            self.nodo = nodo
