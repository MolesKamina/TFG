# Este programa será el cerebro del sistema. Funciona de la siguiente manera:
# Recibe como argumento una fecha, y realiza la siguiente acción:
# 1: Descarga de la base de datos los siguientes valores: Una lista de IDs de nodos, y una lista de toda la información existente para esos nodos. La información obtenida tendrá el siguiente formato: node_id, value
# 2: Una vez se tenga toda esa información, se procede a llamar a una función, encargada de preparar un plan de acción con estas tablas.
# 3: 
from databaseManager import DatabaseManager
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class Planificador:
    def __init__(self, database_manager, date=None):
        self.database_manager = database_manager
        self.date = date
        nodes = self.database_manager.extract_nodes()
        self.nodes_formatted = self.format_output(nodes)

    def set_date(self, date):
        self.date = date

    def format_output(self, data):
        formatted_output = tuple(item[0] for item in data)
        return formatted_output

    def light_plan(self):
        list_values = self.database_manager.extract_nodes_values(self.nodes_formatted, self.date)

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
        return grouped_df
    
    def temperature_plan(self, movement_df):
        # Convertir la cadena de texto de la fecha a un objeto de fecha
        date_obj = datetime.strptime(self.date, "%Y-%m-%d")

        # Obtener la fecha de una semana antes
        previous_week_date = date_obj - pd.Timedelta(days=7)

        # Inicializar una lista para almacenar todos los valores de la semana anterior
        all_week_values = []

        # Iterar sobre cada día de la semana anterior
        for i in range(7):
            # Calcular la fecha del día actual de la semana anterior
            current_day_date = previous_week_date + pd.Timedelta(days=i)
            
            # Extraer valores de los sensores de temperatura del día actual
            list_values = self.database_manager.extract_nodes_values(self.nodes_formatted, current_day_date)
            
            # Agregar los valores del día actual a la lista de todos los valores de la semana
            all_week_values.extend(list_values)

        # Convertir la lista de valores de la semana en un array de NumPy
        dataset = np.array(all_week_values, dtype=[('node_id', 'U10'), ('value', float), ('date', 'M8[us]')])

    def set_plan(self):
        if self.date is None:
            raise ValueError("La fecha no ha sido especificada")
        movement_df = self.light_plan()
        self.temperature_plan(movement_df)
