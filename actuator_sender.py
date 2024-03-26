from datetime import datetime
from databaseManager import DatabaseManager
from producer import Producer

def format_output(data):
    formatted_output = tuple(item[0] for item in data)
    return formatted_output


if __name__ == "__main__":
    date = "2024-03-25"  # Especifica la fecha en formato YYYY-MM-DD
    db_manager = DatabaseManager(host="bmoles.ddns.net", username="kafka", 
                                password="26Kafka97*", database="proyecto_db")
    
    # Obtener lista de nodos:
    nodes = db_manager.extract_nodes()
    print(nodes)

    # Formatear el resultado para utilizarlo en otras consultas
    nodes_formatted = format_output(nodes)
    print(nodes_formatted)

    # Obtener lista de los actuadores "conectados" a los nodos
    #actuadores = db_manager.extract_actuators(nodes_formatted)
    #print(actuadores)

    # Obtener los valores almacenados en la tabla nodes_actions para la fecha dada y los nodos encontrados
    nodes_action = db_manager.extract_nodes_action(nodes_formatted, date)
    print(nodes_action)
