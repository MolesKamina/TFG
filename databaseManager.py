import mysql.connector
from datetime import datetime

class DatabaseManager:
    def __init__(self, host, username, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def close(self):
        if self.cursor:
            self.cursor.close()

    def insert_sensor_node(self, sensor_id, neighbors, description=None):
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "INSERT INTO sensor_nodes (id, description, date) VALUES (%s, %s, %s)"
            values = (sensor_id, description, current_time)
            self.execute_query(query, values)
            self.close()
        except Exception as e:
            print("Error:", e)
        for neighbor_id in neighbors:
            try:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                query = "INSERT INTO sensor_nodes (id, description, date) VALUES (%s, %s, %s)"
                values = (neighbor_id, description, current_time)
                #print(values)
                self.execute_query(query, values)
                self.close()
            except Exception as e:
                print("Error:", e)

    def insert_node_neighbor(self, sensor_id, neighbors):
        try:
            for neighbor_id in neighbors:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                query = "INSERT INTO nodes_neighbours (id_sensor_a, id_sensor_b, date) VALUES (%s, %s, %s)"
                values = (sensor_id, neighbor_id, current_time)
                self.execute_query(query, values)
            self.close()
        except Exception as e:
            print("Error:", e)
    
    def insert_sensor_data(self, sensor_id, data, date):
        try:
            query = "INSERT INTO sensor_values (id_sensor, value, date) VALUES (%s, %s, %s)"
            values = (sensor_id, data, date)
            self.execute_query(query, values)
            self.close()
        except Exception as e:
            print("Error:", e)
    
    def execute_query(self, query, values=None):
        # Ejecutar una consulta SQL
        self.cursor = self.connection.cursor()
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        self.connection.commit()
