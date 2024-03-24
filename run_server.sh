#!/bin/bash

# Ejecutar creación de tablas
python3 tables_creation.py

# Ejecutar el programa del servidor
python3 server_main.py &

# Ejecutar el otro programa del servidor
python3 server_receiver.py &
