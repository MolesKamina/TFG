#from kafka import KafkaProducer
from message_client import MessageClient
#from json import dumps

class Producer(MessageClient):
    def __init__(self, bootstrap_servers, enable_auto_commit=True):
        """
        Inicializa un nuevo cliente productor de mensajes.

        Args:
            topic_list (list): Lista de topics a los que el cliente se suscribirá.
            bootstrap_servers (str): Lista de servidores para establecer la conexión.
            enable_auto_commit (bool): Indicador para habilitar o deshabilitar el commit automático de offsets.
        """
        super().__init__(None, bootstrap_servers, enable_auto_commit, True)

    def open(self):
        super().open()

    def close(self):
        super().close()

    def send_message(self, topic, message_content):
        super().send_message(topic, message_content)