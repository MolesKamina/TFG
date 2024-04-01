class MessageClient:
    def __init__(self, topic_list, bootstrap_servers, enable_auto_commit):
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

    def send_message(self, topic, message_content):
        """
        Envía un mensaje al topic especificado.

        Args:
            topic (str): El topic al que se enviará el mensaje.
            message_content (str): El contenido del mensaje a enviar.
        """
        # Método para enviar mensajes
        pass

    def receive_message(self, topic):
        """
        Recibe un mensaje del topic especificado.

        Args:
            topic (str): El topic del cual se quiere recibir el mensaje.

        Returns:
            str: El contenido del mensaje recibido.
        """
        # Método para recibir mensajes
        pass