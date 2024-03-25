import os
import time
from datetime import datetime
from multiprocessing import Process
from producer import Producer
from sensor import Sensor
from fileReader import FileReader

def generate_and_send_values(sensor_data, topic, n_iterations):
    for i in range(n_iterations):
        # Generar un valor aleatorio
        sensor_id, node_id, sensor_descr = sensor_data
        sen = Sensor(sensor_id, node_id, sensor_descr)
        value = sen.generar_valor()

        # Obtener la fecha actual
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Formatear el mensaje
        message = f"{sen.get_id()},{value},{current_time}"

        # Enviar mensaje al tópico correspondiente
        producer.send_message(topic, message)
        print(f"Mensaje enviado al tópico {topic}: {message}")

        # Esperar 1 segundo antes de enviar el próximo mensaje
        time.sleep(1)

if __name__ == "__main__":
    # Definir el nombre del archivo de sensores y el tópico
    sensor_file = "sensors.txt"
    topic = "Topic2"
    fr = FileReader()

    # Verificar si el archivo de sensores existe
    if not os.path.exists(sensor_file):
        print(f"El archivo de sensores '{sensor_file}' no existe.")
    else:
        # Leer el archivo de sensores y crear una lista de sensores

        sensors_data = fr.read_sensor_file(sensor_file)

        # Configurar el productor de Kafka
        producer = Producer([topic], 'bmoles.ddns.net:9092')

        # Definir el número de iteraciones
        n_iterations = 100

        # Crear un proceso para cada sensor
        processes = []
        for s in sensors_data:
            p = Process(target=generate_and_send_values, args=(s, topic, n_iterations))
            processes.append(p)
            p.start()

        # Esperar a que todos los procesos terminen
        for p in processes:
            p.join()