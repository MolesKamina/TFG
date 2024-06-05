from dispositivo import Dispositivo
from nodo import Nodo

class Actuador(Dispositivo):
    def __init__(self, id, description, nodo: Nodo):
        """
        Inicializa un nuevo actuador.

        Args:
            id (str): Identificador único del actuador.
            description (str): Descripción del actuador.
            nodo (Nodo): Nodo al que está asociado el actuador.
        """
        super().__init__(id, description, nodo)

    def get_id(self):
        """
        Obtiene el identificador del actuador.

        Returns:
            str: Identificador del actuador.
        """
        return self.id

    def get_description(self):
        """
        Obtiene la descripción del actuador.

        Returns:
            str: Descripción del actuador.
        """
        return self.description

    def get_nodo(self):
        """
        Obtiene el nodo al que está asociado el actuador.

        Returns:
            Nodo: Nodo asociado al actuador.
        """
        return self.nodo

    def ejecutar_accion(self, action, date):
        """
        Ejecuta una acción en el actuador.

        Args:
            accion (str): Acción a ejecutar.
            fecha (str): Fecha de la acción (en formato 'YYYY-MM-DD HH:MM:SS').
        """
        # Simula la ejecución de una acción
        print(f"Ejecutando acción {action}, fecha: {date} en el actuador {self.get_id()}")
