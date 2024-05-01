import sys
from action_plan_generator import ActionPlanGenerator
from databaseManager import DatabaseManager
import pandas as pd

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 2:
    print("Usage: python3 server_main_planner.py <date>")
    sys.exit(1)

# Extract the date from the command-line argument
date = sys.argv[1]

# Create an instance of DatabaseManager
db_manager = DatabaseManager(host="bmoles.ddns.net", username="kafka", 
                             password="26Kafka97*", database="proyecto_db")

# Create an instance of ActionPlanGenerator
plan_generator = ActionPlanGenerator(db_manager, date)
print("Generando plan de gestión de iluminación...")
plan_generator.extract_values_motion()
plan_generator.train_model()
action_plan = plan_generator.generate_action_plan()
print("Plan de acción de iluminación generado")

print("Generando plan de gestión de temperatura...")
plan_generator.extract_values_temperature()
plan_generator.train_model()
action_plan = plan_generator.generate_action_plan()
print("Plan de acción de temperatura generado")
