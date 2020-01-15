#----- Import required modules
import os
import csv
import requests

#----- Define required files & folders
filepath = 'C:/Users/LRS07/OneDrive - Sky/Documents/Others/SME Water Project/data'
configfile = 'C:/Users/LRS07/OneDrive - Sky/Documents/Others/SME Water Project/code/sme-water-dpm-solution/import-hmw/configuration.csv'

#----- Delete all existing files
filenames = os.listdir(filepath)
for name in filenames:
    os.remove(filepath +'/'+ name)

#----- loop to download each csv file to folder
with open(configfile) as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    rowcount = 0
    for row in reader:
        rowcount = rowcount + 1
        url = row[3]
        myfile = requests.get(url)
        open('C:/Users/LRS07/OneDrive - Sky/Documents/Others/SME Water Project/data/'+row[0]+'.csv', 'wb').write(myfile.content)

#----- Message after download complete
print("Process Complete")