## Table of Contents
* [General Info](#General-Info)
* [Technologies](#Technologies)
* [Setup](#Setup)
* [Executing The Pipeline](#Executing-The-Pipeline)
* [Design](#Design)
* [Git Info](#Git-Info)

## General Info
This project is data pipeline which part of SME Water - DPM Solution. The pipeline is broken down into the following processes:
* Pull data from HMW web server into local via HTTP request.
* Load data into local database (MySQL).
* Push data out from local database (MySQL) into a txt file. The output files are used by Tableau for visualization purpose.

## Technologies
* Python: 3.7
* MySQL Workbench 8.0 CE
* MySQL Server
* Tableau Public 2019.4 (Desktop)
* Github
	
## Setup
To run this locally or on a VM please follow the following steps:
* Install Python 3.7
* Install Git
* Clone the project
```
git clone https://github.com/lydiarosalia/sme-water-dpm-solution.git
```

* Install all the python requirements
```
cd import-hmw
pip install -r requirements.txt
```

## Executing The Pipeline
### Runtime Argument
Runtime argument = the name of configuration file that will be used.
The file must be located in /utils directory.

* If no argument is provided, then it will use default configuration file.
* If argument is provided, then it will use provided configuration file.
  
### Running Locally or on a VM
To run the pipeline locally:
* Complete [Setup](#setup).
* Execute `run_locally.py` with argument `--configfile`
Syntax:
```
python run_locally.py --configfile [{filename}.csv]
```
Example: to run BAU data pipeline (using default configuration file)
```
python run_locally.py
```
Example: to run adhoc data pipeline (using adhoc configuration file named adhoc_config.csv)
```
python run_locally.py --configfile adhoc_config.csv
```
## Design
### High Level Design
The high level overview of how the data move within the pipeline.

![alt text](import-hmw/images/high-level-design-v02.jpeg)

### High Level Process Flow
![alt text](import-hmw/images/high-level-process-flow-v01.jpeg)

### Error Handling
|Error Summary|Description|
|----------|-----------|
|Missing configuration file| Error caused by configuration file (CSV file which contain the list of sites) is not found in /utils directory. If encounter this error, then the process will be terminated, error message displayed and logged into log file.|
|Database is not exist| Error caused by the database is not found in local MySQL instance. If encounter this error, then the process will be terminated, error message displayed and logged into log file.|
|Invalid data type| Error caused by incorrect data type. Valid data types are "flow" or "pressure". If encounter this error, it will be logged into log file, the process will still continue.|
|Error during file download| Any error that is encountered when downloading a file will be logged into log file, the process will still continue.|
|Error during adding missin record process| Any error that is encountered when processing missing record will be logged into log file, the process will still continue.|
|Database error during data load| Any DB error that is encountered when loading data will be logged into log file, the process will still continue.|


## Git Info
### Branching
![alt text](import-hmw/images/git-branching-v01.jpeg)
