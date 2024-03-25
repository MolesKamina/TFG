from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError

class KafkaServerAdmin:
    def __init__(self, bootstrap_servers):
        self.admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

    def create_topics(self, topics):
        new_topics = [NewTopic(name, num_partitions=1, replication_factor=1) for name in topics]
        try:
            self.admin_client.create_topics(new_topics)
            print("Topics created successfully.")
        except TopicAlreadyExistsError as e:
            print(f"Error: {e}")

    def delete_topics(self, topics):
        try:
            self.admin_client.delete_topics(topics)
            print("Topics deleted successfully.")
        except UnknownTopicOrPartitionError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    bootstrap_servers = "bmoles.ddns.net:9092"  # Adjust this according to your Kafka configuration
    list_topics = ['Topic1', 'Topic2', 'Topic3']  # List of topics to create or delete

    admin = KafkaServerAdmin(bootstrap_servers)

    # Crear temas
    admin.create_topics(list_topics)

    # Eliminar temas
    #admin.delete_topics(list_topics)
