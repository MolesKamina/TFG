from kafka import KafkaProducer
from message_client import MessageClient
from json import dumps

class Producer(MessageClient):
    def __init__(self, topic_list, bootstrap_servers, enable_auto_commit):
        super().__init__(topic_list, bootstrap_servers, enable_auto_commit)
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                       value_serializer=lambda x:
                         dumps(x).encode('utf-8'))

    def send_message(self, topic, message_content):
        self.producer.send(topic, message_content.encode('utf-8'))