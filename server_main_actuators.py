from consumer import Consumer
from nodo import Nodo
from actuador import Actuador
from databaseManager import DatabaseManager

def process_message(message):
    actuator_id, node_id, description = message
    actuador = Actuador(actuator_id, description, Nodo(node_id))
    return actuador

def server_main_nodes():
    # Crear un consumidor para el tópico Topic4
    # Este consumidor recibirá información de actuadores
    consumer = Consumer(['Topic4'], 'bmoles.ddns.net:9092', enable_auto_commit=True)

    db_manager = DatabaseManager(host="bmoles.ddns.net", username="kafka", 
                                 password="26Kafka97*", database="proyecto_db")

    # Ejecutar un bucle infinito para recibir continuamente mensajes
    while True:
        # Esperar a recibir un mensaje
        message = consumer.receive_message('Topic4')

        # Procesar el mensaje y crear el actuador
        actuador = process_message(message)

        # Aquí puedes continuar con el procesamiento del sensor
        db_manager.insert_actuator(actuador.get_id(), actuador.get_nodo().get_identificador(), 
                                   actuador.get_description())

if __name__ == "__main__":
    server_main_nodes()
