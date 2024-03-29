from planner_creator import Planificador
from databaseManager import DatabaseManager




# Crear una instancia de DatabaseManager
db_manager = DatabaseManager(host="bmoles.ddns.net", username="kafka", 
                             password="26Kafka97*", database="proyecto_db")

# Crear una instancia de Planificador
planificador = Planificador(db_manager)

# Establecer la fecha
planificador.set_date('2024-03-25')

# Generar y ejecutar el plan
planificador.set_plan()
