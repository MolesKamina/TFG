from consumer import Consumer
#from nodo import Nodo
#from sensor import Sensor
from databaseManager import DatabaseManager

def process_message(message):
    sensor_id, value, timestamp = message.split(',')
    # Procesar el mensaje según tus necesidades
    return sensor_id, value, timestamp

def server_receiver():
    # Crear un consumidor para el tópico Topic2
    consumer = Consumer(['Topic2'], 'localhost:9092', enable_auto_commit=True)
    db_manager = DatabaseManager(host="bmoles.ddns.net", username="kafka", 
                                 password="26Kafka97*", database="proyecto_db")

    # Ejecutar un bucle infinito para recibir continuamente mensajes
    while True:
        # Esperar a recibir un mensaje
        message = consumer.receive_message('Topic2')

        # Procesar el mensaje
        sensor_id, value, timestamp = process_message(message)

        # Insertar la información en la base de datos
        db_manager.insert_sensor_data(sensor_id, value, timestamp)

if __name__ == "__main__":
    server_receiver()
