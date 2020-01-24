##########################
# Import required modules
##########################
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(host='localhost', port=3306, database='dpm-solution', user='root', password='root')

datetime_to_load = datetime.strptime('01-01-2019 00:00', '%d-%m-%Y %H:%M')
site_id = '9999'
value_to_load = None

mycursor = mydb.cursor()

sql_flow = "INSERT INTO flow (datetime, site_id, value) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE datetime=%s, site_id=%s, value= %s"
values = (datetime_to_load, site_id, value_to_load, datetime_to_load, site_id, value_to_load)

mycursor.execute(sql_flow, values)

# Commit & close connection once ALL loading completed
# If encounter any errors, all loaded data will be rolled back
mydb.commit()
mydb.close()

print("All Process Completed!")
