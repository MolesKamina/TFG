from consumer import Consumer
from nodo import Nodo
from sensor import Sensor
from databaseManager import DatabaseManager

def process_message(message):
    sensor_id, node_id, description = message
    sensor = Sensor(sensor_id, description, Nodo(node_id))
    return sensor

def server_main_nodes():
    # Crear un consumidor para el tópico Topic3
    # Este consumidor recibirá información de sensores
    consumer = Consumer(['Topic3'], 'bmoles.ddns.net:9092', enable_auto_commit=True)

    db_manager = DatabaseManager(host="bmoles.ddns.net", username="kafka", 
                                 password="26Kafka97*", database="proyecto_db")
    #db_manager.connect()

    # Ejecutar un bucle infinito para recibir continuamente mensajes
    while True:
        # Esperar a recibir un mensaje
        message = consumer.receive_message('Topic3')

        # Procesar el mensaje y crear el sensor
        sensor = process_message(message)

        # Aquí puedes continuar con el procesamiento del sensor
        db_manager.insert_sensor(sensor.get_id(), sensor.get_nodo().get_identificador(), sensor.get_description())

if __name__ == "__main__":
    server_main_nodes()
