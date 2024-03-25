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

    def insert_node(self, node_id, neighbors, description=None):
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "INSERT INTO nodes (id, description, date) VALUES (%s, %s, %s)"
            values = (node_id, description, current_time)
            self.execute_query(query, values)
            self.close()
        except Exception as e:
            print("Error:", e)

        for neighbor_id in neighbors:
            try:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                query = "INSERT INTO nodes (id, description, date) VALUES (%s, %s, %s)"
                values = (neighbor_id, description, current_time)
                #print(values)
                self.execute_query(query, values)
                self.close()
            except Exception as e:
                print("Error:", e)

    def insert_node_neighbors(self, node_id, neighbors):
        try:
            for neighbor_id in neighbors:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                query = "INSERT INTO nodes_neighbors (id_node_a, id_node_b, date) VALUES (%s, %s, %s)"
                values = (node_id, neighbor_id, current_time)
                self.execute_query(query, values)
            self.close()
        except Exception as e:
            print("Error:", e)
    
    def insert_sensor(self, sensor_id, node_id,  description=None):
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "INSERT INTO sensors (id, node_id, description, date) VALUES (%s, %s, %s, %s)"
            values = (sensor_id, node_id, description, current_time)
            print(query)
            print(values)
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
    
    def execute_query(self, query, values=None, select=False):
        """
        Ejecuta una consulta SQL en la base de datos.

        Args:
            query (str): La consulta SQL a ejecutar.
            values (tuple, opcional): Valores para los parámetros de la consulta, si los hay.
            select (bool, opcional): Indica si la consulta es un SELECT. Por defecto, es False.

        Returns:
            result (list or None): La lista de resultados si select=True, None en caso contrario.
        """
        self.cursor = self.connection.cursor()

        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)

            if select:
                result = self.cursor.fetchall()
                return result
            else:
                self.connection.commit()
        except Exception as e:
            print("Error:", e)
        finally:
            self.close()

