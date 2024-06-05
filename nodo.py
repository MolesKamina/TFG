# nodo.py

class Nodo:
    def __init__(self, identificador, nodos_vecinos=None):
        self.identificador = identificador
        self.nodos_vecinos = nodos_vecinos if nodos_vecinos is not None else []

    def get_identificador(self):
        return self.identificador

    def get_nodos_vecinos(self):
        return self.nodos_vecinos
    