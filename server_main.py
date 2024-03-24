from consumer import Consumer
from nodo import Nodo
from sensor import Sensor
from databaseManager import DatabaseManager

def process_message(message):
    sensor_id, neighbors = message
    node = Nodo(sensor_id, neighbors)
    sensor = Sensor(node)
    return sensor

def print_sensor_content(sensor):
    print(f"Sensor ID: {sensor.nodo.get_identificador()}")
    print(f"Vecinos: {sensor.nodo.get_nodos_vecinos()}")
    print()

def server_main():
    # Crear un consumidor para el tópico Topic1
    consumer = Consumer(['Topic1'], 'localhost:9092', enable_auto_commit=True)

    db_manager = DatabaseManager(host="bmoles.ddns.net", username="kafka", 
                                 password="26Kafka97*", database="proyecto_db")
    #db_manager.connect()

    # Ejecutar un bucle infinito para recibir continuamente mensajes
    while True:
        # Esperar a recibir un mensaje
        message = consumer.receive_message('Topic1')

        # Procesar el mensaje y crear el sensor
        sensor = process_message(message)

        # Mostrar mensaje de procesamiento
        #print("Mensaje recibido y procesado:")

        # Mostrar contenido del sensor
        #print_sensor_content(sensor)

        # Aquí puedes continuar con el procesamiento del sensor
        db_manager.insert_sensor_node(sensor.nodo.get_identificador(), sensor.nodo.get_nodos_vecinos())
        db_manager.insert_node_neighbor(sensor.nodo.get_identificador(), sensor.nodo.get_nodos_vecinos())

if __name__ == "__main__":
    server_main()
