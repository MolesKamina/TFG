import sys
from planner_creator import Planificador
from databaseManager import DatabaseManager

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <date>")
    sys.exit(1)

# Extract the date from the command-line argument
date = sys.argv[1]

# Create an instance of DatabaseManager
db_manager = DatabaseManager(host="bmoles.ddns.net", username="kafka", 
                             password="26Kafka97*", database="proyecto_db")

# Create an instance of Planificador
planificador = Planificador(db_manager)

# Set the date
planificador.set_date(date)

# Generate and execute the plan
planificador.set_plan()
