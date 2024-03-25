#!/bin/bash

# Ejecutar creación de tablas
python3 tables_creation.py

# Ejecutar los programas del servidor
python3 server_main_nodes.py &

python3 server_main_sensors.py &

# Ejecutar el otro programa del servidor
python3 server_receiver.py &
