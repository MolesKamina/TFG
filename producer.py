from kafka import KafkaProducer
from message_client import MessageClient
from json import dumps

class Producer(MessageClient):
    def __init__(self, topic_list, bootstrap_servers, enable_auto_commit=True):
        super().__init__(topic_list, bootstrap_servers, enable_auto_commit)
        self.producer = None
        self.bootstrap_servers = bootstrap_servers

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

        # No cerramos el productor aquí para permitir reutilizarlo
