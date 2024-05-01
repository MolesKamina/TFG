from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import dumps, loads

class MessageClient:
    def __init__(self, topic_list, bootstrap_servers, enable_auto_commit, type: bool):
        """
        Inicializa un nuevo cliente de mensajes.

        Args:
            topic_list (list): Lista de topics a los que el cliente se suscribirá.
            bootstrap_servers (str): Lista de servidores para establecer la conexión.
            enable_auto_commit (bool): Indicador para habilitar o deshabilitar el commit automático de offsets.
        """
        self.topic_list = topic_list
        self.bootstrap_servers = bootstrap_servers
        self.enable_auto_commit = enable_auto_commit
        self.producer = None
        self.consumer = None
        if type:
            self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers, 
                value_serializer=lambda x: dumps(x).encode('utf-8'))
        else:
            self.consumer = KafkaConsumer(
                *topic_list,
                bootstrap_servers=bootstrap_servers,
                enable_auto_commit=enable_auto_commit,
                value_deserializer=lambda x: loads(x.decode('utf-8'))
            ) 

    def open(self):
        if self.producer is None:
            self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers, 
                                          value_serializer=lambda x: dumps(x).encode('utf-8'))

    def close(self):
        if self.producer is not None:
            self.producer.close()
            self.producer = None

    def send_message(self, topic, message_content):
        self.open()  # Abre el productor si aún no está abierto
        self.producer.send(topic, message_content)

        # Es importante llamar a flush para asegurarse de que el mensaje se envíe
        self.producer.flush()

    def receive_message(self, topic):
        for message in self.consumer:
            if message.topic == topic:
                return message.value