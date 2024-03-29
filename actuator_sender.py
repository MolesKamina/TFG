from datetime import datetime
from databaseManager import DatabaseManager
from producer import Producer
import pandas as pd
from multiprocessing import Process

def format_output(data):
    formatted_output = tuple(item[0] for item in data)
    return formatted_output

def send_values(df, producer, topic):
    for index, row in df.iterrows():
        node_id = row['node_id']
        action = row['action']
        date = row['date']
        message = f"{node_id},{action},{date}"
        #print(message)
        producer.send_message(topic, message)

if __name__ == "__main__":
    date = "2024-03-25"  # Especifica la fecha en formato YYYY-MM-DD
    db_manager = DatabaseManager(host="bmoles.ddns.net", username="kafka", 
                                password="26Kafka97*", database="proyecto_db")
    topic = "Topic5"
    producer = Producer([topic], 'bmoles.ddns.net:9092')
    processes = []
    
    # Obtener lista de nodos:
    nodes = db_manager.extract_nodes()
    print(nodes)

    # Formatear el resultado para utilizarlo en otras consultas
    nodes_formatted = format_output(nodes)
    print(nodes_formatted)

    # Obtener los valores almacenados en la tabla nodes_actions para la fecha dada y los nodos encontrados
    nodes_action = db_manager.extract_nodes_action(nodes_formatted, date)

    df = pd.DataFrame(nodes_action, columns=['node_id', 'action', 'date'])

    node_count = df['node_id'].nunique()
    print(node_count)

    for i in range(node_count):
        exit_df = pd.DataFrame([[str(i), 'FIN', pd.Timestamp.min]], columns=['node_id', 'action', 'date'])
        df = pd.concat([df, exit_df], ignore_index=True)

    #print(df)
    group_by_node_id = df.groupby('node_id')
    
    for node_id, group_df in group_by_node_id:
        p = Process(target=send_values, args=(group_df, producer, topic))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    #df = pd.DataFrame(columns=['node_id', 'action', 'date'])

