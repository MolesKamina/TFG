from consumer import Consumer
from nodo import Nodo
#from sensor import Sensor
from databaseManager import DatabaseManager

def process_message(message):
    node_id, neighbors = message
    node = Nodo(node_id, neighbors)
    #sensor = Sensor(node)
    return node

def server_main_nodes():
    # Crear un consumidor para el tópico Topic1
    # Este consumidor recibirá información de nodos (su ID y nodos vecinos)
    consumer = Consumer(['Topic1'], 'bmoles.ddns.net:9092', enable_auto_commit=True)

    db_manager = DatabaseManager(host="bmoles.ddns.net", username="kafka", 
                                 password="26Kafka97*", database="proyecto_db")
    #db_manager.connect()

    # Ejecutar un bucle infinito para recibir continuamente mensajes
    while True:
        # Esperar a recibir un mensaje
        message = consumer.receive_message('Topic1')

        # Procesar el mensaje y crear el nodo
        node = process_message(message)

        # Aquí puedes continuar con el procesamiento del nodo
        db_manager.insert_node(node.get_identificador(), node.get_nodos_vecinos())
        db_manager.insert_node_neighbors(node.get_identificador(), node.get_nodos_vecinos())

if __name__ == "__main__":
    server_main_nodes()
