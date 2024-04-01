from databaseManager import DatabaseManager
from producer import Producer 
import pandas as pd
from multiprocessing import Process

def format_output(data):
    """
    Formatea la salida de una consulta SQL para su uso en otras consultas.

    Args:
        data (list): Lista de tuplas con los resultados de la consulta.

    Returns:
        formatted_output: Tupla con los elementos de la primera columna de cada tupla de la lista de resultados.
    """
    formatted_output = tuple(item[0] for item in data)
    return formatted_output

def send_values(df, producer, topic):
    """
    Envía los valores de un DataFrame a un topic mediante el productor.

    Args:
        df (DataFrame): DataFrame con los datos a enviar.
        producer (Producer): Instancia del productor para enviar los mensajes.
        topic (str): Nombre del topic al que se enviarán los mensajes.
    """
    for index, row in df.iterrows():
        node_id = row['node_id']
        action = row['action']
        date = row['date']
        message = f"{node_id},{action},{date}"
        producer.send_message(topic, message)

if __name__ == "__main__":
    # Este programa extrae datos de la base de datos, los formatea y los envía a un servidor Kafka.
    date = "2024-03-25"
    db_manager = DatabaseManager(host="bmoles.ddns.net", username="kafka", 
                                password="26Kafka97*", database="proyecto_db")
    topic = "Topic5"
    producer = Producer([topic], 'bmoles.ddns.net:9092')
    processes = []
    
    # Obtener lista de nodos:
    nodes = db_manager.extract_nodes()

    # Formatear el resultado para utilizarlo en otras consultas.
    nodes_formatted = format_output(nodes)

    # Obtener los valores almacenados en la tabla nodes_actions para la fecha dada y los nodos encontrados.
    nodes_action = db_manager.extract_nodes_action(nodes_formatted, date)

    # Crea un DataFrame con los resultados de la consulta SQL
    df = pd.DataFrame(nodes_action, columns=['node_id', 'action', 'date'])

    # Obtiene el número de nodos únicos en el DataFrame.
    node_count = df['node_id'].nunique()

    # Para cada número único de nodo, crea un DataFrame de salida con la acción 'FIN' y la fecha mínima, y lo concatena al DataFrame principal 'df'.
    for i in range(node_count):
        exit_df = pd.DataFrame([[str(i), 'FIN', pd.Timestamp.min]], columns=['node_id', 'action', 'date'])
        df = pd.concat([df, exit_df], ignore_index=True)
    
    # Agrupa los datos del DataFrame 'df' por 'node_id'.
    group_by_node_id = df.groupby('node_id')
    
    # Para cada grupo de nodos, crea un proceso que enviará los valores del grupo al productor mediante la función 'send_values'.
    for node_id, group_df in group_by_node_id:
        p = Process(target=send_values, args=(group_df, producer, topic))
        processes.append(p)
        p.start()

    # Espera a que todos los procesos se completen antes de continuar.
    for p in processes:
        p.join()