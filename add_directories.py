import os

# Directorio que quieres añadir
directorio = '/home/kafka/.local/bin'

# Obtener el valor actual de la variable de entorno PATH
path_actual = os.environ.get('PATH', '')

# Concatenar el directorio al PATH si aún no está presente
if directorio not in path_actual.split(':'):
    nuevo_path = f"{path_actual}:{directorio}"

    # Establecer la variable de entorno PATH con el nuevo valor
    os.environ['PATH'] = nuevo_path

    print("Directorio añadido correctamente al PATH.")
else:
    print("El directorio ya está presente en el PATH.")
