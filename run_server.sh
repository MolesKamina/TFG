#!/bin/bash

# Ejecutar creación de tablas
python3 tables_creation.py &

# Ejecutar los programas del servidor
# Carga de nodos (siempre está a la espera de recibir nuevos mensajes y actualizar la base de datos)
python3 server_main_nodes.py  &

# Carga de sensores (siempre está a la espera de recibir nuevos mensajes y actualizar la base de datos)
python3 server_main_sensors.py &

# Carga de actuadores (siempre está a la espera de recibir nuevos mensajes y actualizar la base de datos)
python3 server_main_actuators.py &

# Ejecutar el otro programa del servidor
python3 server_receiver.py &
