##########################
# Import required modules
##########################
import csv
import mysql.connector
import os
import requests
from datetime import datetime

##################################
# Define required files & folders
##################################
target_directory = "C:/Users/LRS07/OneDrive - Sky/Documents/Others/SME Water Project/data/"
file_list = os.listdir(target_directory)
configuration = "C:/Users/LRS07/OneDrive - Sky/Documents/Others/SME Water Project/configuration.csv"

###########################
# Set connection to the DB
###########################
mydb = mysql.connector.connect(host='localhost', port=3306, database='dpm-solution', user='root', password='root')

############################
# Delete all existing files
############################
for name in file_list:
    os.remove(target_directory + name)

#####################################
# Download files & load data into DB
#####################################
with open(configuration) as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)

    #####################################################
    # loop to download each csv file to target_directory
    #####################################################
    for row in reader:

        # Get all values into variables
        site_id = row[0]
        type_untrimmed = row[1]
        type = type_untrimmed.strip()
        channel = row[2]
        url = row[3]
        file = target_directory + site_id + '.csv'

        # Download and write the output file
        get_file = requests.get(url)
        open(file, 'wb').write(get_file.content)

        print(site_id + " - File Download Completed!")

        ############################
        # loop to load data into DB
        ############################
        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)

            for row in reader:
                mycursor = mydb.cursor()

                # Convert datetime field from string to datetime type
                datetime_string = row[0]
                datetime_to_load = datetime.strptime(datetime_string, '%d-%m-%Y %H:%M')

                # Get value based on its channel
                if channel == "1":
                    value = row[1]
                elif channel == "2":
                    value = row[2]
                elif channel == "3":
                    value = row[3]
                elif channel == "4":
                    value = row[4]
                elif channel == "5":
                    value = row[5]
                else:
                    value = ""

                # If value is missing (no value), set it to 0
                if value == '':
                    value_to_load = 0
                else:
                    value_to_load = value

                # Define SQL to load the data into destination table based on its type (Flow or Pressure)
                # If the record has existed then update the record, otherwise insert the record
                sql_flow = "INSERT INTO flow (datetime, site_id, value) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE datetime=%s, site_id=%s, value= %s"
                sql_pressure = "INSERT INTO pressure (datetime, site_id, value) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE datetime=%s, site_id=%s, value= %s"
                values = (datetime_to_load, site_id, value_to_load, datetime_to_load, site_id, value_to_load)

                # Execute the SQL to load the data
                # If the type = Flow, data is loaded into flow table
                # If the type = Pressure, data is loaded into pressure table
                # If the type is not Flow or Pressure, error message is printed out no data is inserted to any tables
                if type == "Flow":
                    mycursor.execute(sql, values)
                elif type == "Pressure":
                    mycursor.execute(sql_pressure, values)
                else:
                    print("Invalid Type! Expected type: Flow or Pressure.")

            print(site_id + " - Data Load Completed!")

# Commit & close connection once ALL loading completed
# If encounter any errors, all loaded data will be rolled back
mydb.commit()
mydb.close()

print("All Process Completed!")
