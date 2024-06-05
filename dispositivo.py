# dispositivo.py
from nodo import Nodo

class Dispositivo:
    def __init__(self, id, description, nodo: Nodo=None):
        """
        Inicializa un nuevo dispositivo asociado a un nodo. La clase Dispositivo es la clase 
        encargada de gestionar el apartado de nodos en el sistema.

        Args:
            nodo (Nodo): El nodo al que está asociado el dispositivo.
        """
        self.id = id
        self.description = description
        if nodo:
            self.nodo = nodo
