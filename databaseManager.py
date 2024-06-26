import mysql.connector
from datetime import datetime

class DatabaseManager:
    def __init__(self, host, username, password, database):
        """
        Inicializa una nueva instancia de DatabaseManager.

        Args:
            host (str): La dirección del host de la base de datos.
            username (str): El nombre de usuario para acceder a la base de datos.
            password (str): La contraseña para acceder a la base de datos.
            database (str): El nombre de la base de datos a la que se conectará.
        """
        self.connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        """
        Cierra la conexión con la base de datos.
        """
        if self.connection:
            self.connection.close()

    def close(self):
        """
        Cierra el cursor de la base de datos.
        """
        if self.cursor:
            self.cursor.close()

    def insert_node(self, node_id, neighbors, description=None):
        """
        Inserta un nuevo nodo en la base de datos. Tambien inserta sus vecinos como nuevos nodos
        si no se encuentran registrados en la base de datos.

        Args:
            node_id (int): Identificador del nodo a insertar.
            neighbors (list): Lista de identificadores de los vecinos del nodo.
            description (str, opcional): Descripción del nodo. Por defecto es nula.
        """
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
                self.execute_query(query, values)
                self.close()
            except Exception as e:
                print("Error:", e)

    def insert_node_neighbors(self, node_id, neighbors):
        """
        Inserta los vecinos de un nodo en la base de datos.

        Args:
            node_id (int): Identificador del nodo.
            neighbors (list): Lista de identificadores de los vecinos del nodo.
        """
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
        """
        Inserta un nuevo sensor en la base de datos.

        Args:
            sensor_id (int): Identificador del sensor.
            node_id (int): Identificador del nodo al que está asociado el sensor.
            description (str, opcional): Descripción del sensor. Por defecto es nula.
        """
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "INSERT INTO sensors (id, node_id, description, date) VALUES (%s, %s, %s, %s)"
            values = (sensor_id, node_id, description, current_time)
            self.execute_query(query, values)
            self.close()
        except Exception as e:
            print("Error:", e)

    def insert_actuator(self, actuator_id, node_id, description=None):
        """
        Inserta un nuevo actuador en la base de datos.

        Args:
            actuator_id (int): Identificador del actuador.
            node_id (int): Identificador del nodo al que está asociado el actuador.
            description (str, opcional): Descripción del actuador. Por defecto es nula.
        """
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "INSERT INTO actuators (id, node_id, description, date) VALUES (%s, %s, %s, %s)"
            values = (actuator_id, node_id, description, current_time)
            self.execute_query(query, values)
            self.close()
        except Exception as e:
            print("Error:", e)

    def insert_sensor_data(self, sensor_id, data, date):
        """
        Inserta datos de un sensor en la base de datos.

        Args:
            sensor_id (int): Identificador del sensor.
            data (float): Valor del dato del sensor.
            date (str): Fecha y hora del dato del sensor (en el formato 'YYYY-MM-DD HH:MM:SS').
        """
        try:
            query = "INSERT INTO sensor_values (id_sensor, value, date) VALUES (%s, %s, %s)"
            values = (sensor_id, data, date)
            self.execute_query(query, values)
            self.close()
        except Exception as e:
            print("Error:", e)
    
    def insert_node_action(self, node_id, action, date):
        """
        Inserta una acción realizada por un nodo en la base de datos.

        Args:
            node_id (int): Identificador del nodo.
            action (str): Acción realizada por el nodo.
            date (str): Fecha y hora de la acción (en el formato 'YYYY-MM-DD HH:MM:SS').
        """
        try:
            query = "INSERT INTO nodes_actions (node_id, action, date) VALUES (%s, %s, %s)"
            values = (node_id, action, date)
            self.execute_query(query, values)
            self.close()
        except Exception as e:
            print("Error:", e)

    def extract_actuators(self, id_nodes):
        """
        Extrae los actuadores asociados a una lista de nodos.

        Args:
            id_nodes (list): Lista de identificadores de los nodos.

        Returns:
            actuators (list): Lista de identificadores de los actuadores asociados a los nodos.
        """
        try:
            placeholders = ', '.join(['%s' for _ in id_nodes])
            query = f"""
            SELECT id FROM actuators
            WHERE node_id IN ({placeholders})
            """
            actuators = self.execute_query(query, values=id_nodes, select=True)
            return actuators
        except Exception as e:
            print("Error:", e)
    
    def extract_nodes(self):
        """
        Extrae todos los nodos de la base de datos.

        Returns:
            nodes (list): Lista de identificadores de los nodos.
        """
        try:
            query = "SELECT id FROM nodes"
            nodes = self.execute_query(query, select=True)
            self.close()
            return nodes
        except Exception as e:
            print("Error:", e)
    
    def extract_nodes_action(self, node_ids, date):
        """
        Extrae las acciones realizadas por una lista de nodos en una fecha específica.

        Args:
            node_ids (list): Lista de identificadores de los nodos.
            date (str): Fecha de las acciones (en el formato 'YYYY-MM-DD').

        Returns:
            nodes (list): Lista de tuplas que contienen el identificador del nodo, la acción realizada y la fecha de la acción.
        """
        try:
            node_placeholders = ', '.join(['%s' for _ in node_ids])
            values = tuple(node_ids) + (date,)
            query = f"""
            SELECT node_id, action, date
            FROM nodes_actions
            WHERE node_id IN ({node_placeholders})
            AND DATE(date) = %s                                                           
            """
            nodes = self.execute_query(query, values, select=True)
            self.close()
            return nodes
        except Exception as e:
            print("Error:", e)


    def extract_nodes_values(self, node_ids, date):
        """
        Extrae los valores de los sensores asociados a una lista de nodos en una fecha específica.

        Args:
            node_ids (list): Lista de identificadores de los nodos.
            date (str): Fecha de los valores (en el formato 'YYYY-MM-DD').

        Returns:
            nodes_values (list): Lista de tuplas que contienen el identificador del nodo, el valor del sensor y la fecha del valor.
        """
        try:
            node_placeholders = ', '.join(['%s' for _ in node_ids])
            values = tuple(node_ids) + (date,)
            query = f"""
            SELECT node_id, value, A.date
            FROM sensor_values A
            INNER JOIN sensors B
            ON A.id_sensor = B.id
            WHERE node_id IN ({node_placeholders})
            AND DATE(A.date) = %s
            """
            nodes_values = self.execute_query(query, values, select=True)
            self.close()
            return nodes_values
        except Exception as e:
            print("Error:", e)

    def extract_all_nodes_values(self, node_ids, date):
        """
        Extrae los valores de los sensores asociados a una lista de nodos en todos los días anteriores a una fecha específica.

        Args:
            node_ids (list): Lista de identificadores de los nodos.
            date (datetime): Fecha límite (los valores se extraerán para todos los días anteriores a esta fecha).

        Returns:
            nodes_values (list): Lista de tuplas que contienen el identificador del nodo, el valor del sensor y la fecha del valor.
        """
        try:
            node_placeholders = ', '.join(['%s' for _ in node_ids])
            values = tuple(node_ids) + (date,)
            query = f"""
            SELECT node_id, value, A.date
            FROM sensor_values A
            INNER JOIN sensors B
            ON A.id_sensor = B.id
            WHERE node_id IN ({node_placeholders})
            AND DATE(A.date) < %s
            """
            nodes_values = self.execute_query(query, values, select=True)
            self.close()
            return nodes_values
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

