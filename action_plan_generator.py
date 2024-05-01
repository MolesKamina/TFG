import numpy as np
import pandas as pd
from databaseManager import DatabaseManager
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC


class ActionPlanGenerator:
    def __init__(self, database_manager: DatabaseManager, date):
        self.database_manager = database_manager
        self.date = date
        nodes = self.database_manager.extract_nodes()
        self.nodes_formatted = self.format_output(nodes)
        self.df = None

        dataset = self.extract_values(self.database_manager, self.date)
        self.df = self.prepare_dataframe(dataset)
        self.model = None
        self.le = None

    def format_output(self, data):
        formatted_output = tuple(item[0] for item in data)
        return formatted_output

    def extract_values_motion(self):
        values = self.database_manager.extract_all_nodes_values(self.nodes_formatted, self.date)
        dataset = np.array(values, dtype=[('node_id', 'U10'), ('value', float), ('date', 'M8[us]')])
        self.df = self.prepare_dataframe(dataset)
    
    def extract_values_temperature(self):
        values = self.database_manager.extract_all_nodes_values(self.nodes_formatted, self.date)
        dataset = np.array(values, dtype=[('node_id', 'U10'), ('value', float), ('date', 'M8[us]')])
        self.df = self.prepare_dataframe(dataset)

    def extract_values(self, db_manager, date):
        all_values = db_manager.extract_all_nodes_values(self.nodes_formatted, date)

        dataset = np.array(all_values, dtype=[('node_id', 'U10'), ('value', float), ('date', 'M8[us]')])
    
        return dataset

    def prepare_dataframe(self, dataset):
        # Convertimos el dataset a un DataFrame
        df = pd.DataFrame(dataset, columns=['node_id', 'value', 'date'])

        # Añadimos una columna 'weekday' que indica el día de la semana
        df['weekday'] = df['date'].dt.dayofweek
        df['action'] = df['value']

        # Añadimos columnas 'hour' y 'minute' que contienen la hora y los minutos de la columna 'date'
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        return df

    def train_model(self):
        print("Comenzando plan...")
        # Preparamos los datos de entrada para el modelo
        X = self.df[['node_id', 'weekday', 'hour', 'minute']]
        y = self.df['value']  # La columna 'action' será el objetivo del modelo

        # Codificamos la variable objetivo
        self.le = LabelEncoder()
        y_encoded = self.le.fit_transform(y)

        # Entrenamos un clasificador SVM
        svm_classifier = SVC()
        svm_classifier.fit(X, y_encoded)

        self.model = svm_classifier
        print("Plan finalizado...")

    def generate_action_plan(self):
        print("Generando acciones...")
        # Generamos los intervalos de tiempo para el día objetivo
        intervals = pd.date_range(start=self.date, end=pd.Timestamp(self.date).replace(hour=23, minute=45), freq='15T')

        # Generamos el plan de acción para el día objetivo
        action_plan = pd.DataFrame(columns=['node_id', 'date', 'weekday', 'hour', 'minute', 'action'])


        for node_id in self.df['node_id'].unique():
            for interval in intervals:
                # Obtener la hora, los minutos y el día de la semana del intervalo
                hour = interval.hour
                minute = interval.minute
                weekday = interval.dayofweek
                
                # Predicción de la acción utilizando el modelo entrenado
                prediction = self.model.predict([[node_id, weekday, hour, minute]])
                action = self.le.inverse_transform(prediction)[0]

                # Añadir la predicción al plan de acción
                aux_df = pd.DataFrame([[node_id, interval, weekday, hour, minute, action]], columns=['node_id', 'date', 'weekday', 'hour', 'minute', 'action'])
                action_plan = pd.concat([action_plan, aux_df], ignore_index=True)

        for index, row in action_plan.iterrows():
            node_id = row['node_id']
            action = row['action']
            date = row['date']
            self.database_manager.insert_node_action(node_id, action, date)
