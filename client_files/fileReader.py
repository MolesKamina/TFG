import re

class FileReader:
    def __init__(self):
        pass
    
    def read_node_file(self, filename):
        node_data = []
        with open(filename, 'r') as file:
            for line in file:
                node_id, neighbors = re.split(r'\s+', line.strip(), maxsplit=1)
                neighbors = neighbors.split(',')
                node_data.append((node_id, neighbors))
        return node_data

    def read_sensor_file(self, filename):
        sensor_data = []
        with open(filename, 'r') as file:
            for line in file:
                sensor_id, node_id, description = line.strip().split(',')
                sensor_data.append((sensor_id, node_id, description))
        return sensor_data
    
    def read_actuators_file(self, filename):
        actuator_data = []
        with open(filename, 'r') as file:
            for line in file:
                actuator_id, node_id, description = line.strip().split(',')
                actuator_data.append((actuator_id, node_id, description))
        return actuator_data