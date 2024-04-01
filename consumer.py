from kafka import KafkaConsumer
from message_client import MessageClient
from json import loads

class Consumer(MessageClient):
    def __init__(self, topic_list, bootstrap_servers, enable_auto_commit):
        """
        Inicializa un nuevo consumidor de Kafka.

        Args:
            topic_list (list): Lista de topics a los que el consumidor se suscribirá.
            bootstrap_servers (str): Lista de servidores de Kafka para establecer la conexión.
            enable_auto_commit (bool): Indicador para habilitar o deshabilitar el commit automático de offsets.
        """
        super().__init__(topic_list, bootstrap_servers, enable_auto_commit)
        self.consumer = KafkaConsumer(
            *topic_list,
            bootstrap_servers=bootstrap_servers,
            enable_auto_commit=enable_auto_commit,
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )

    def receive_message(self, topic):
        """
        Recibe un mensaje del topic especificado.

        Args:
            topic (str): El topic del cual se quiere recibir el mensaje.

        Returns:
            message: El mensaje recibido.
        """
        for message in self.consumer:
            if message.topic == topic:
                return message.value