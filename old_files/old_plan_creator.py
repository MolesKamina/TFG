import mysql.connector

cnx = mysql.connector.connect(user='kafka', password='kafka',
                              host= 'localhost', database='ls_database')

mycursor= cnx.cursor()

mycursor.execute('SELECT GROUP_VALUES / COUNT_VALUES AS FINAL_VALUE, DATE_VALUE FROM ' +
                    '(SELECT SUM(sensor_value) AS GROUP_VALUES, input_dt AS DATE_VALUE, COUNT(1) AS COUNT_VALUES ' +
                    'FROM sensor_data GROUP BY input_dt) T1; ')

myresult = mycursor.fetchall()
for x in myresult:
  print(x) 