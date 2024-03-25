from databaseManager import DatabaseManager
def create_tables(databaseManager):
    queries = []
    queries.append("""CREATE TABLE IF NOT EXISTS nodes (
                        id VARCHAR(255) PRIMARY KEY,
                        description TEXT,
                        date DATETIME
                    )""")
    queries.append("""CREATE TABLE IF NOT EXISTS sensors (
                            id VARCHAR(255) PRIMARY KEY, 
                            node_id VARCHAR(255),
                            description TEXT,
                            date DATETIME,
                            FOREIGN KEY (node_id) REFERENCES nodes(id)
                        )""")
    queries.append("""CREATE TABLE IF NOT EXISTS nodes_neighbors (
                            id_node_a VARCHAR(255),
                            id_node_b VARCHAR(255),
                            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (id_node_a) REFERENCES nodes(id),
                            FOREIGN KEY (id_node_b) REFERENCES nodes(id),
                            PRIMARY KEY (id_node_a, id_node_b)
                        )""")
    queries.append("""CREATE TABLE IF NOT EXISTS sensor_values (
                            value_id INT AUTO_INCREMENT PRIMARY KEY,
                            id_sensor VARCHAR(255),
                            value FLOAT,
                            date DATETIME,
                            FOREIGN KEY (id_sensor) REFERENCES sensors(id)
                        )""")
    for query in queries:
        databaseManager.execute_query(query)

if __name__ == "__main__":
    db_manager = DatabaseManager(host="bmoles.ddns.net", username="kafka", 
                                 password="26Kafka97*", database="proyecto_db")
    create_tables(db_manager)
