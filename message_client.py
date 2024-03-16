# message_client.py
# En esta clase se va a gestionar el envío y recepción de mensajes.
# Únicamente se encargará de gestionar ese "puente" entre todos los actores
# Tendrá dos métodos principales, aunque se podrán programar más a conveniencia
# El método send_message se encargará de enviar un mensaje, y el método receive_message de recibirlo
# Internamente se programará para que se utilice un servidor externo para gestionar este servicio

class MessageClient:
    def __init__(self, topic_list, bootstrap_servers, enable_auto_commit):
        self.topic_list = topic_list
        self.bootstrap_servers = bootstrap_servers
        self.enable_auto_commit = enable_auto_commit

    def send_message(self, topic, message_content):
        # Método para enviar mensajes
        pass

    def receive_message(self, topic):
        # Método para recibir mensajes
        pass