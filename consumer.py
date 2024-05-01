from kafka import KafkaConsumer
from message_client import MessageClient
from json import loads

class Consumer(MessageClient):
    def __init__(self, topic_list, bootstrap_servers, enable_auto_commit):
        """
        Inicializa un nuevo cliente consumidor de mensajes.

        Args:
            topic_list (list): Lista de topics a los que el cliente se suscribirá.
            bootstrap_servers (str): Lista de servidores para establecer la conexión.
            enable_auto_commit (bool): Indicador para habilitar o deshabilitar el commit automático de offsets.
        """
        super().__init__(topic_list, bootstrap_servers, enable_auto_commit, False)

    def receive_message(self, topic):
        """
        Recibe un mensaje del topic especificado.

        Args:
            topic (str): El topic del cual se quiere recibir el mensaje.

        Returns:
            str: El contenido del mensaje recibido.
        """
        return super().receive_message(topic)