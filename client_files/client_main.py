from producer import Producer
import os
import re

def read_sensor_file(filename):
    sensors_data = []
    with open(filename, 'r') as file:
        for line in file:
            sensor_id, neighbors = re.split(r'\s+', line.strip(), maxsplit=1)
            neighbors = neighbors.split(',')
            sensors_data.append((sensor_id, neighbors))
            print(sensors_data)
    return sensors_data

def client_process(sensor_file, topic):
    # Leer el archivo de sensores
    sensors_data = read_sensor_file(sensor_file)

    # Configurar el productor de Kafka
    producer = Producer([topic], 'bmoles.ddns.net:9092')

    # Enviar mensajes al tópico Topic1
    for data in sensors_data:
        message = data
        print(message)
        producer.send_message(topic, message)
        print(f"Mensaje enviado al tópico {topic}: {message}")

if __name__ == "__main__":
    # Definir el nombre del archivo de sensores y el tópico
    sensor_file = "sensors.txt"
    topic = "Topic1"

    # Verificar si el archivo de sensores existe
    if not os.path.exists(sensor_file):
        print(f"El archivo de sensores '{sensor_file}' no existe.")
    else:
        # Procesar los sensores y enviar mensajes
        client_process(sensor_file, topic)
