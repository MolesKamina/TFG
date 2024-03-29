from consumer import Consumer
from nodo import Nodo
from actuador import Actuador
from fileReader import FileReader
import os
import pandas as pd
from multiprocessing import Process

# Function to create an Actuator object
def create_actuator(message):
    actuator_id, node_id, description = message
    actuator = Actuador(actuator_id, description, Nodo(node_id))
    return actuator

# Function to assign actions to actuators based on received messages
def assign_actions(node_id, act_df, actions_df):
    actuators = act_df[act_df['node_id'] == node_id]
    for index, row in actuators.iterrows():
        actuator_id = row['actuator_id']
        description = row['description']
        for j, action_row in actions_df.iterrows():
            action = action_row['action']
            date_action = action_row['date']
            actuator = Actuador(actuator_id, description, Nodo(node_id))
            actuator.execute_action(action, date_action)

if __name__ == "__main__":
    actuators_file = "actuators.txt"
    file_reader = FileReader()
    actuators = []
    processes = []
    consumer = Consumer(['Topic5'], 'bmoles.ddns.net:9092', enable_auto_commit=True)

    # Check if the actuators file exists
    if not os.path.exists(actuators_file):
        print(f"The actuators file '{actuators_file}' does not exist.")
    else:
        # Process actuators
        actuators_data = file_reader.read_actuators_file(actuators_file)
        for a in actuators_data:
            actuator = create_actuator(a)
            actuators.append(a)

        actuator_list = pd.DataFrame(actuators, columns=['actuator_id', 'node_id', 'description'])
        actions_df = pd.DataFrame(columns=['node_id', 'action', 'date'])
        node_count = actuator_list['node_id'].nunique()
        end_count = 0
        while end_count != node_count:
            msg = consumer.receive_message('Topic5')
            node_id, action, date_str = msg.split(',')
            if node_id in actuator_list['node_id'].values:
                if action == 'FIN':
                    end_count += 1
                else:
                    date = pd.to_datetime(date_str)
                    df = pd.DataFrame([[node_id, action, date]], columns=['node_id', 'action', 'date'])
                    actions_df = pd.concat([actions_df, df], ignore_index=True)

        actions_df = actions_df.sort_values(by='date')
        group_by_node = actions_df.groupby('node_id')
        
        for node_id, group_node in group_by_node:
            p = Process(target=assign_actions, args=(node_id, actuator_list, group_node))
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()
