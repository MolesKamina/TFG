from datetime import datetime
import pandas as pd
import random
from databaseManager import DatabaseManager
from multiprocessing import Process
from itertools import groupby
from operator import itemgetter
import sys

# Función para dividir una lista de días en 4 listas equitativas
def split_days_into_lists(total_days):
    num_lists = 4
    days_per_list = total_days // num_lists
    remainder = total_days % num_lists

    day_lists = []
    start_day = 0

    for i in range(num_lists):
        end_day = start_day + days_per_list
        if remainder > 0:
            end_day += 1
            remainder -= 1

        day_lists.append(list(range(start_day, end_day)))
        start_day = end_day

    return day_lists

# Función para procesar una lista de días
def process_day_list(date_input, day_list):
    for i in day_list:
        process_sensor_data(date_input, i)

# Lista de valores de sensor
sensor_values = list(range(1, 17))

# Función para obtener el valor del sensor basado en la fecha
def get_value(date):
    if date.weekday() >= 5:  # 5 es sábado, 6 es domingo
        # Si es fin de semana, asignar un valor aleatorio entre 0 y 1
        value = 0.0
    # Chequear si la fecha está entre las 9:00 y las 17:00
    else:
        if 9 <= date.hour < 17:
            value = 1.0
        else:
            value = 0.0
        
    # Aleatoriamente, con 0.1 de posibilidades, cambiar el valor por uno random entre 0 y 1
    if random.random() < 0.1:
        value = random.uniform(0, 1)
        
    return value

# Función para procesar los datos de los sensores y añadirlos a la base de datos
def process_sensor_data(date_str, num_day):
    db = DatabaseManager(host="bmoles.ddns.net", username="kafka", 
                             password="26Kafka97*", database="proyecto_db")
    
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    current_date = date_obj - pd.Timedelta(days=num_day)
    insert_sensor_data_for_day(db, current_date)

# Función para insertar datos de sensor para un día específico
def insert_sensor_data_for_day(db, date):
    # Recorrer los intervalos de 5 minutos durante el día
    for j in range(0, 1440, 5):  # 1440 minutos en un día
        current_time = date + pd.Timedelta(minutes=j)
        for sensor_id in sensor_values:
            data_value = get_value(current_time)
            db.insert_sensor_data(sensor_id, data_value, current_time)

if __name__ == "__main__":
    # Comprobar el número de argumentos
    if len(sys.argv) != 3:
        print("Uso: python script.py <fecha> <num_dias>")
        sys.exit(1)

    # Obtener los argumentos de la línea de comandos
    date_input = sys.argv[1]
    num_days = int(sys.argv[2])

    # Dividir los días en 4 listas
    day_lists = split_days_into_lists(num_days)

    processes = []

    for day_list in day_lists:
        p = Process(target=process_day_list, args=(date_input, day_list))
        processes.append(p)
        p.start()

    # Esperar a que todos los procesos terminen
    for p in processes:
        p.join()