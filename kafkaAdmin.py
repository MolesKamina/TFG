from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError

class KafkaServerAdmin:
    def __init__(self, bootstrap_servers):
        """
        Inicializa un nuevo administrador de servidor Kafka.

        Args:
            bootstrap_servers (str): Lista de servidores de Kafka para establecer la conexión.
        """
        self.admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

    def create_topics(self, topics):
        """
        Crea los topics especificados en el servidor Kafka.

        Args:
            topics (list): Lista de nombres de los topics a crear.
        """
        new_topics = [NewTopic(name, num_partitions=1, replication_factor=1) for name in topics]
        try:
            self.admin_client.create_topics(new_topics)
            print("Topics created successfully.")
        except TopicAlreadyExistsError as e:
            print(f"Error: {e}")

    def delete_topics(self, topics):
        """
        Elimina los topics especificados del servidor Kafka.

        Args:
            topics (list): Lista de nombres de los topics a eliminar.
        """
        try:
            self.admin_client.delete_topics(topics)
            print("Topics deleted successfully.")
        except UnknownTopicOrPartitionError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    bootstrap_servers = "bmoles.ddns.net:9092"
    list_topics = ['Topic1', 'Topic2', 'Topic3', 'Topic4', 'Topic5']

    admin = KafkaServerAdmin(bootstrap_servers)

    # Crear topics
    admin.create_topics(list_topics)

    # Eliminar topics
    #admin.delete_topics(list_topics)
