from producer import Producer
from fileReader import FileReader
import os

def publisher_process(data, topic):
    # Configurar el productor de Kafka
    producer = Producer([topic], 'bmoles.ddns.net:9092')

    # Enviar mensajes al tópico Topic1
    for d in data:
        message = d
        #print(message)
        producer.send_message(topic, message)
        print(f"Mensaje enviado al tópico {topic}: {message}")

if __name__ == "__main__":
    # Definir el nombre del archivo de nodos, sensores y los tópicos
    node_file = "nodes.txt"
    sensor_file = "sensors.txt"
    actuators_file = "actuators.txt"

    node_topic = "Topic1"
    sensor_topic = "Topic3"
    actuators_topic = "Topic4"
    fr = FileReader()

    # Verificar si el archivo de nodos existe
    if not os.path.exists(node_file):
        print(f"El archivo de nodos '{node_file}' no existe.")
    else:
        # Procesar los nodos y enviar mensajes
        nodes_data = fr.read_node_file(node_file)
        publisher_process(nodes_data, node_topic)

    # Verificar si el archivo de sensores existe
    if not os.path.exists(sensor_file):
        print(f"El archivo de sensores '{sensor_file}' no existe.")
    else:
        # Procesar los sensores y enviar mensajes
        sensors_data = fr.read_sensor_file(sensor_file)
        publisher_process(sensors_data, sensor_topic)

    # Verificar si el archivo de actuadores existe
    if not os.path.exists(actuators_file):
        print(f"El archivo de sensores '{actuators_file}' no existe.")
    else:
        # Procesar los sensores y enviar mensajes
        actuators_data = fr.read_actuators_file(actuators_file)
        publisher_process(actuators_data, actuators_topic)