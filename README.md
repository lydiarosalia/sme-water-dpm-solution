## Table of Contents
* [General Info](#General-Info)
* [Technologies](#Technologies)
* [Setup](#Setup)
* [Runtime arguments](#Runtime-Arguments)
* [Running locally or on a VM](Running-Locally-or-on-a-VM)
* [High Level Design](#High-Level-Design)
* [Lower Level Design](#Lower-Level-Design)
* [Error Handling](#Error-Handling)

## General Info
This project is data pipeline which part of SME Water - DPM Solution. The pipeline is broken down into the following processes:
* Pull data from HMW web server into local via HTTP request.
* Load data into local database (MySQL).
* Push data out from local database (MySQL) into a txt file. The output files are used by Tableau for visualization purpose.

## Technologies
* Python: 3.7
* MySQL Workbench 8.0 CE
* MySQL Server
	
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

## Runtime Arguments
* run_bau : execute Business-As-Usual data pipeline, means that it will process the sites that is in utils/configuration_file.csv.
* run_fail : execute data pipeline for particular sites(s) that are failed in the earlier execution, means that it will process the sites that is in utils/configuration_failed_file.csv.
  
## Running Locally or on a VM
To run the pipeline locally:
* Complete [Setup](#setup).
* Execute `run_locally.py` with argument `--runmode`
Syntax:
```
python run_locally.py --runmode [run_bau or run_fail]
```
Example: to run BAU data pipeline.
```
python run_locally.py --runmode run_bau
```

## High Level Design
The high level overview of how the data move within the pipeline.

![alt text](import-hmw/images/high-level-design-v01.jpeg)

## Lower Level Design
The detail overview of how the data move within the pipeline, include the business logics.

## Error Handling
???
