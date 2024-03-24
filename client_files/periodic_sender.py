import os
import re
import time
from datetime import datetime
from multiprocessing import Process
from producer import Producer
from sensor import Sensor
from nodo import Nodo

def generate_and_send_values(sensor, topic, n_iterations):
    for i in range(n_iterations):
        # Generar un valor aleatorio
        value = sensor.generar_valor()

        # Obtener la fecha actual
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Formatear el mensaje
        message = f"{sensor.nodo.get_identificador()},{value},{current_time}"

        # Enviar mensaje al tópico Topic2
        producer.send_message(topic, message)
        print(f"Mensaje enviado al tópico {topic}: {message}")

        # Esperar 1 segundo antes de enviar el próximo mensaje
        time.sleep(1)

if __name__ == "__main__":
    # Definir el nombre del archivo de sensores y el tópico
    sensor_file = "sensors.txt"
    topic = "Topic2"

    # Verificar si el archivo de sensores existe
    if not os.path.exists(sensor_file):
        print(f"El archivo de sensores '{sensor_file}' no existe.")
    else:
        # Leer el archivo de sensores y crear una lista de sensores
        sensors = []
        with open(sensor_file, 'r') as file:
            for line in file:
                sensor_id, neighbors = re.split(r'\s+', line.strip(), maxsplit=1)
                neighbors = neighbors.split(',')
                node = Nodo(sensor_id, neighbors)
                sensors.append(Sensor(node))
                #print(sensors_data)

        # Configurar el productor de Kafka
        producer = Producer([topic], 'bmoles.ddns.net:9092')

        # Definir el número de iteraciones
        n_iterations = 100  # Cambia este valor según tus necesidades

        # Crear un proceso para cada sensor
        processes = []
        for sensor in sensors:
            p = Process(target=generate_and_send_values, args=(sensor, topic, n_iterations))
            processes.append(p)
            p.start()

        # Esperar a que todos los procesos terminen
        for p in processes:
            p.join()
