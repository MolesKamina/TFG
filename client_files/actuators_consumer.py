from consumer import Consumer
from nodo import Nodo
from actuador import Actuador
from fileReader import FileReader
import os
import pandas as pd
from multiprocessing import Process

def createActuator(message):
    actuator_id, node_id, description = message
    actuador = Actuador(actuator_id, description, Nodo(node_id))
    return actuador

def assign_actuator(var_node_id, act_df, actions_df):
    actuators = act_df[act_df['node_id'] == node_id]
    #filtro = act_df['node_id'] == var_node_id
    #print(filtro)
    for index, row in actuators.iterrows():
        a_id = row['actuator_id']
        n_id = row['node_id']
        d_id = row['description']
        #print(actions_df)
        for j, action_row in actions_df.iterrows():
            action = action_row['action']
            date_action = action_row['date']
            a = Actuador(a_id, d_id, Nodo(n_id))
            a.ejecutar_accion(action, date_action)
    

    #print(actuators)

if __name__ == "__main__":
    actuators_file = "actuators.txt"
    fr = FileReader()
    actuators = []
    processes = []
    consumer = Consumer(['Topic5'], 'bmoles.ddns.net:9092', enable_auto_commit=True)
    # Verificar si el archivo de actuadores existe
    if not os.path.exists(actuators_file):
        print(f"El archivo de actuadores '{actuators_file}' no existe.")
    else:
        # Procesar los actuadores
        actuators_data = fr.read_actuators_file(actuators_file)
        for a in actuators_data:
            act = createActuator(a)
            actuators.append(a)
        #print(actuators)
        actuator_list = pd.DataFrame(actuators, columns=['actuator_id', 'node_id', 'description'])
        actions_df = pd.DataFrame(columns=['node_id', 'action', 'date'])
        #print(actions_df)
        node_count = actuator_list['node_id'].nunique()
        end_count = 0

        while end_count != node_count:
            msg = consumer.receive_message('Topic5')
            #actions_df = actions_df.append(msg, ignore_index=True)
            #actions_df += pd.DataFrame(msg)
            node_id, action, date_str = msg.split(',')
            if action == 'FIN':
                end_count += 1
                #print(node_count)
                #print(end_count)
            else:
                date = pd.to_datetime(date_str)
                df = pd.DataFrame([[node_id, action, date]], columns=['node_id', 'action', 'date'])
                actions_df = pd.concat([actions_df, df], ignore_index=True)
                #print(msg)
                #print(actions_df)
        #print(actions_df) 

        group_by_node = actions_df.groupby('node_id')
        for node_id, group_node in group_by_node:
            #print(node_id)
            #assign_actuator(node_id, actuator_list, group_node)
            p = Process(target=assign_actuator, args=(node_id, actuator_list, group_node))
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()

