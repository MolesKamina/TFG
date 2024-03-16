import json
from kafka import KafkaConsumer
#from kafka import KafkaProducer
from json import loads
import mysql.connector
import time

print("Connecting to database...")
cnx = mysql.connector.connect(user='kafka', password='kafka',
                              host= 'localhost', database='ls_database')
print("Connected to database...")

mycursor= cnx.cursor()

sql= "INSERT INTO sensor_data (sensor_code, sensor_value, input_dt) VALUES (%s, %s, %s)"

consumer = KafkaConsumer('sensor_input',
                          bootstrap_servers=['192.168.10.181:9092'],
                          enable_auto_commit=True,
                          value_deserializer=lambda x: loads(x.decode('utf-8')))
for msg in consumer:
  msg = msg.value
  val = (msg['sensor_code'], msg['sensor_value'], msg['input_dt'])
  mycursor.execute(sql, val)
  cnx.commit()
  print(mycursor.rowcount, "record inserted")



