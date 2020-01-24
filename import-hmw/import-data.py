############################################################################################################################################################
# Import required modules
############################################################################################################################################################
import csv
import mysql.connector
from mysql.connector import errorcode
import os
import requests
from datetime import datetime
import datetime as dt

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " All Process Started!")

############################################################################################################################################################
# Define path for files & folders
############################################################################################################################################################
target_directory = "C:/Users/LRS07/OneDrive - Sky/Documents/Others/SME Water Project/data/"
file_list = os.listdir(target_directory)
configuration = "C:/Users/LRS07/OneDrive - Sky/Documents/Others/SME Water Project/code/sme-water-dpm-solution/import-hmw/configuration.csv"

############################################################################################################################################################
# Set connection to the DB
############################################################################################################################################################

try:
    mydb = mysql.connector.connect(host='localhost', port=3306, database='dpm-solution', user='root', password='root')
    mycursor = mydb.cursor()
except mysql.connector.Error as errordb:
    print("Error code:" + errordb.errno)        # error number
    print("SQLSTATE value:" + errordb.sqlstate) # SQLSTATE value
    print("Error message:" + errordb.msg)       # error message
    print("Error:"+ errordb)                    # errno, sqlstate, msg values

############################################################################################################################################################
# Delete all existing files in target directory
############################################################################################################################################################
for name in file_list:

    os.remove(target_directory + name)

############################################################################################################################################################
# Define constant variables
############################################################################################################################################################
# Define urls
url1 = "https://st.hwmonline.com/hwmonline/hwmcarcgi.cgi?user=viewer01&pass=viewer01&logger="
url2 = "&startdate="
url3 = "+00:00&enddate="
url4 = "+23:45&flowunits=2&pressureunits=1&flowinterval=2&interval=5&export=csv"

# Define dates for required data - set up as data for last 90 days
startdate = dt.datetime.strftime(dt.datetime.today() - dt.timedelta(days=90), '%Y-%m-%d')
enddate = dt.datetime.strftime(dt.datetime.today(), '%Y-%m-%d')

############################################################################################################################################################
# Download files & load data into DB
############################################################################################################################################################
with open(configuration) as csvfile:

    reader = csv.reader(csvfile)
    header = next(reader)

############################################################################################################################################################
# loop to download each csv file to target_directory
############################################################################################################################################################
    for row in reader:

        # Get all values into variables
        site_id = row[0]
        type = row[1].strip().lower()
        channel = int(row[2])
        url = url1 + row[3] + url2 + startdate + url3 + enddate + url4
        file = target_directory + site_id + '.csv'

        # Download and write the output file
        get_file = requests.get(url)
        open(file, 'wb').write(get_file.content)

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Site " + site_id + " - File Download Completed!")

############################################################################################################################################################
# loop to load data into DB
############################################################################################################################################################
        with open(file) as csvfile:

            reader = csv.reader(csvfile)
            header = next(reader)

            try:
                for row in reader:

                    datetime_to_load = datetime.strptime(row[0], '%d-%m-%Y %H:%M')
                    value = row[channel]

                    # If value is missing (no value), set it to None (equivalent as null)
                    if value == '':
                        value_to_load = None
                    else:
                        value_to_load = value

                    # Define SQL to load the data into destination table based on its type (Flow or Pressure)
                    # If the record has existed then update the record, otherwise insert the record
                    sql_flow = "INSERT INTO flow (datetime, site_id, value) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE datetime=%s, site_id=%s, value= %s"
                    sql_pressure = "INSERT INTO pressure (datetime, site_id, value) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE datetime=%s, site_id=%s, value= %s"
                    values = (datetime_to_load, site_id, value_to_load, datetime_to_load, site_id, value_to_load)

                    # It's case insensitive
                    # If the type = Flow, data is loaded into flow table; If the type = Pressure, data is loaded into pressure table
                    # If the type is not Flow or Pressure, error message is printed out no data is inserted to any tables
                    if type == "flow":
                        mycursor.execute(sql_flow, values)
                    elif type == "pressure":
                        mycursor.execute(sql_pressure, values)
                    else:
                        print("Invalid Type! Expected type: Flow or Pressure.")

                # Commit after load each file
                # If encounter any errors, all loaded data successful files will be remained while the failed file will be rolled back
                mydb.commit()

                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Site " + site_id + " - Data Load Completed!")

            except mysql.connector.Error as error:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Site " + site_id + " - Data Load Failed!")
                print("Error: {}".format(error))

                # reverting changes because of exception
                mydb.rollback()
                print("Process is rolled back!")

        # Delete file which has successfully loaded
        os.remove(file)

############################################################################################################################################################
# Close DB Connection, All Process Completed
############################################################################################################################################################
mydb.close()

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " All Process Completed!")