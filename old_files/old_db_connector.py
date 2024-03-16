import mysql.connector
import time

cnx = mysql.connector.connect(user='kafka', password='kafka',
                              host= 'localhost', database='ls_database')

mycursor= cnx.cursor()

sql= "INSERT INTO sensor_data (sensor_code, sensor_value, input_dt) VALUES (%s, %s, %s)"
val = (1, 1, time.strftime('%Y-%m-%d %H:%M:%S'))
mycursor.execute(sql, val)

cnx.commit()

print(mycursor.rowcount, "record inserted")
