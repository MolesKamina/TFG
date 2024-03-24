from kafka import KafkaConsumer
from message_client import MessageClient
from json import loads

class Consumer(MessageClient):
    def __init__(self, topic_list, bootstrap_servers, enable_auto_commit):
        super().__init__(topic_list, bootstrap_servers, enable_auto_commit)
        self.consumer = KafkaConsumer(
            *topic_list,
            bootstrap_servers=bootstrap_servers,
            enable_auto_commit=enable_auto_commit,
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )

    def receive_message(self, topic):
        for message in self.consumer:
            if message.topic == topic:
                return message.value