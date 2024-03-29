# Este programa será el cerebro del sistema. Funciona de la siguiente manera:
# Recibe como argumento una fecha, y realiza la siguiente acción:
# 1: Descarga de la base de datos los siguientes valores: Una lista de IDs de nodos, y una lista de toda la información existente para esos nodos. La información obtenida tendrá el siguiente formato: node_id, value
# 2: Una vez se tenga toda esa información, se procede a llamar a una función, encargada de preparar un plan de acción con estas tablas.
# 3: 
from databaseManager import DatabaseManager
import numpy as np
import pandas as pd
import datetime

class Planificador:
    def __init__(self, database_manager, date=None):
        self.database_manager = database_manager
        self.date = date

    def set_date(self, date):
        self.date = date

    def format_output(self, data):
        formatted_output = tuple(item[0] for item in data)
        return formatted_output

    def set_plan(self):
        if self.date is None:
            raise ValueError("La fecha no ha sido especificada")

        nodes = self.database_manager.extract_nodes()

        nodes_formatted = self.format_output(nodes)

        list_values = self.database_manager.extract_nodes_values(nodes_formatted, self.date)

        #Convertir a formato de matriz de NumPy
        dataset = np.array(list_values, dtype=[('node_id', 'U10'), ('value', float), ('date', 'M8[us]')])

        df = pd.DataFrame(dataset, columns=['node_id', 'value', 'date'])
        df['date'] = pd.to_datetime(df['date'])
        grouped_df = df.groupby(['node_id', 'date']).agg({'value': 'mean'}).reset_index()
        grouped_df['action'] = grouped_df['value'].apply(lambda x: 'Apagar' if x < 0.5 else 'Encender')

        for index, row in grouped_df.iterrows():
            node_id = row['node_id']
            action = row['action']
            date = row['date']
            self.database_manager.insert_node_action(node_id, action, date)
