## Table of contents
* [General Info](#General-Info)
* [Technologies](#Technologies)
* [Setup](#Setup)
* [Runtime arguments](#Runtime-Arguments)
* [Running locally or on a VM](Running-Locally-or-on-a-VM)

* [Data Classification Input File specification](#data-classification-input-file-specification)
* [Tagging Obfuscation Process Flow](#tagging-obfuscation-process-flow)
* [Data Governance Tag Templates](#data-governance-tag-templates)
* [Validations performed in the API](#validations-performed-in-the-api)
* [Processing Logic Flow](#processing-logic-flow)
* [Dependencies and assumptions](#dependencies-and-assumptions)
* [Logging](#logging)
* [Rainbow deployment notes](#rainbow-deployment-notes)
* [Documentation and help](#documentation-and-help)

## General Info
This project is data pipeline which part of SME Water - DPM Solution. The pipeline is broken down into the following processes:
* Pull data from HMW web server into local via HTTP request.
* Load data into local database (MySQL).
* Push data out from local database (MySQL) into a txt file. The output files are used by Tableau for visualization purpose.

how the code works??
	
## Technologies
* Python: 3.7
* MySQL Workbench 8.0 CE
* MySQL Server
	
## Setup
To run this project locally or on a VM please follow the following steps:
* Install Python 3.7
* Install Git
* Install gcloud sdk
* Create / Use service account that has:
   * Access to Data Catalog. Role: "Data Catalogue Tag Template User"
   * Big Query Read and write access to the project that is deploying Obfuscation
   * Access to bigquery.datasets.update permission for all datasets in the project 
   * Access to deploy and run cloud functions
   * Access to stack driver
* Clone the project
```
git clone org-1391938@github.com:sky-uk/tagging-obfuscation.git
```

* Install all the python requirements
```
cd tagging-obfuscation
pip install -r requirements.txt
```

* Assume a service account that has access to the Source and Target project. Code snippets below are for GCP project 'skyuk-uk-viewing-proc-dev'
```
gcloud iam service-accounts keys create viewing-proc-dev.json --iam-account viewing-proc-dev@skyuk-uk-viewing-proc-dev.iam.gserviceaccount.com
gcloud auth activate-service-account --key-file=viewing-proc-dev.json
```

* Setup GOOGLE_APPLICATION_CREDENTIALS environment variable to the fully qualified key file downloaded in previous step
```
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]" # For Linux
set GOOGLE_APPLICATION_CREDENTIALS=[PATH] REM Windows
```

* Ways to run the function:
  * Run the python code locally. 
  * Deploy the Python code as cloud function

## Deploying http cloud function
* Deploy the cloud function as an http cloud function using gcloud

```
gcloud functions deploy run_obfuscation_tagging_http --region europe-west1 --runtime python37  --service-account viewing-proc-dev@skyuk-uk-viewing-proc-dev.iam.gserviceaccount.com --trigger-http
```

## Runtime arguments for script
There are 2 deployment ways:
* Script running on VM
* Cloud Function

Both the script API and cloud function require 2 input arguments:

![alt text](images/Runtime.JPG)

* Run Type: This is whether the API does Tagging, Obfuscation or Both
* File Type: Data Classification input file

Specifying run time arguments for script: The script needs to be called with 2 input paramaters:
* --filename: This is the fully qualified file path of the data classification file
* --type: This is the run type. Based on this argument the script will do either Tagging, Obfuscation or Both. Valid 
argument values are:
  * tagging: API will do only tagging
  * obfuscation-all: API will create all views specified in the data classification. (Tables in Clear + Tables with PII)
  * obfuscation-PIIOnly: API will create views only for Tables with PII
  * tagging-obfuscation-all: API will do Tagging first and then Obfuscation for all views (Tables in Clear + Tables with PII)
  * tagging-obfuscation-PIIOnly: API will do Tagging first and then Obfuscation for Tables with PII
  
Specifying run time argument to http cloud function: The cloud function will be called using a http curl request 
using curl -X POST. The call has a header argument and a binary data argument. 
  * Header: The Content-Type tag of the http request header will be used to specify the file type and the run type. 
  This Has to be specified as -H "Content-Type:run_type/file_format". Where run_type and file_format are:
    *  run_type: Valid values are: {tagging/obfuscation-all/obfuscation-PIIOnly/tagging-obfuscation-all/tagging-obfuscation-PIIOnly}
    *  file_format: Valid values are: {csv/json}
  * binary data: Has to be sepcified by the --data-binary @file_path/filename. The content of the /file_path/file_name 
  are passed as a binary data with the request.
  
## Running locally or on a VM
To run the tagging and obfuscation function locally:
* Complete [Setup](#setup)
* Run `run_locally.py` with argument `--filename` <fully qualified file with data classification> and `--type` 
```
python run_locally.py --filename ./test/data_classification_tag_entries.json --type obfuscation-PIIOnly
```

## Running cloud Function

* Run the cloud function as a curl command with the contents of the .json or .csv file (on local) passed on as request content
  * -H "Content-Type:run_type/file_type" parameter of the curl specifies the run_type and the file_type.
    * run_type:{tagging: Runs only tagging
    , obfuscation-all: Runs only obfuscation for all tables in Data Classification
    , obfuscation-PIIOnly: Runs obfuscation for Tables with PII
    , tagging-obfuscation-all: Runs Tagging and then obfuscation for all Tables in input
    , tagging-obfuscation-PIIOnly: Runs Tagging and then obfuscation for Tables with PII Only}
    * file_type:{csv:when the data classification file is csv, json: when the data classification file is json}


Examples of the curl command:
    
To run tagging with a local json file:
```
curl -X POST https://europe-west1-skyuk-uk-viewing-proc-dev.cloudfunctions.net/run_obfuscation_tagging_http -H "Content-Type:tagging/json"  --data-binary @./test/data_classification_tag_entries.json
```

To run obfuscation with a local csv file:
```
curl -X POST https://europe-west1-skyuk-uk-viewing-proc-dev.cloudfunctions.net/run_obfuscation_tagging_http -H "Content-Type:obfuscation-PIIOnly/csv"  --data-binary @./test/data_classification_tag_entries.csv
```

To run both tagging and obfuscation with a local json file:
```
curl -X POST https://europe-west1-skyuk-uk-viewing-proc-dev.cloudfunctions.net/run_obfuscation_tagging_http -H "Content-Type:tagging-obfuscation-PIIOnly/json"  --data-binary @./test/data_classification_tag_entries.json
```

## Data Classification Input File specification
The Tagging and Obfuscation requires an input file with the data classification information. This file can either be a csv (*.csv) or json (*.json)
* CSV file format: The csv file should have the following column headers:
  * source_project
  * source_dataset
  * source_table
  * includes_pii
  * source_column
  * pii_element: Type enum. Valid values are: ['AccessibilityInfo','AccountID','AccountNumber','ActivationDate','BBUsageAddress','BBUsageMeasure','BIC','BankAccountNumer','BillingDate','BillingItem','BillingValue','BirthPlace','CDRDuration','CDRNumber','CallRouting','CardExpiryDate','CardName','CardNumber','CommsAV','CommsTranscripts','CompEntrantDetails','ContentOrderItem','Cookie','CoordinatesCoarse','CoordinatesFine','CreditCheckScore','CustomerModelValue','DDRequestDate','DOB','DebtIndicator','DeviceID','DrivingLicenceNumber','Ethnicity','FraudIndicator','Gender','IBAN','ICCID','IMEI','IMSI','IPAddress','InternationalIdentifier','JourneyTag','LetterTypePref','LoyaltyID','LoyaltyStatus','MACAddress','MACCode','MedicalIdentifier','MoneyLaunderingResult','NDSNumber','NationalIdentifier','Nationality','OrderAction','OrderDate','OrdinaryOrderItem','PEPStatus','PassportNumber','PaymentDate','PaymentMethod','PersonAV','PersonAddressCoarse','PersonAddressFine','PersonAge','PersonAgeBand','PersonConsents','PersonEmail','PersonHandle','PersonID','PersonName','PersonNotes','PersonPassword','PersonPhone','PersonPhoneAreaCode','PersonPrefs','PersonSecurityQ','PersonSurveyResponse','Religion','RollNumber','SerialNumber','ServiceID','ServicePrefs','SexualOrientation','SortCode','SurveyResponse','TaxIdentifier','TrackingID','UserID','Username','VIPIndicator','ViewingCardNumber','ViewingDLDateTime','ViewingDLTime','ViewingDate','ViewingDuration','ViewingFavourites','ViewingItem','ViewingProvider','ViewingTime','VisitDateTime'],
  * target_project
  * target_dataset
  * target_obfuscated_viewname

Please see the sample at this link: [sample input classification in csv](test/data_classification_tag_entries.csv)

* JSON File format: The JSON file should be a JSON array with each array element having the following:
  * source_project
  * source_dataset
  * source_table
  * includes_pii
  * Columns: [ {source_column:column_name, pii_element:pii_element_type Type enum. Valid values are: ['AccessibilityInfo','AccountID','AccountNumber','ActivationDate','BBUsageAddress','BBUsageMeasure','BIC','BankAccountNumer','BillingDate','BillingItem','BillingValue','BirthPlace','CDRDuration','CDRNumber','CallRouting','CardExpiryDate','CardName','CardNumber','CommsAV','CommsTranscripts','CompEntrantDetails','ContentOrderItem','Cookie','CoordinatesCoarse','CoordinatesFine','CreditCheckScore','CustomerModelValue','DDRequestDate','DOB','DebtIndicator','DeviceID','DrivingLicenceNumber','Ethnicity','FraudIndicator','Gender','IBAN','ICCID','IMEI','IMSI','IPAddress','InternationalIdentifier','JourneyTag','LetterTypePref','LoyaltyID','LoyaltyStatus','MACAddress','MACCode','MedicalIdentifier','MoneyLaunderingResult','NDSNumber','NationalIdentifier','Nationality','OrderAction','OrderDate','OrdinaryOrderItem','PEPStatus','PassportNumber','PaymentDate','PaymentMethod','PersonAV','PersonAddressCoarse','PersonAddressFine','PersonAge','PersonAgeBand','PersonConsents','PersonEmail','PersonHandle','PersonID','PersonName','PersonNotes','PersonPassword','PersonPhone','PersonPhoneAreaCode','PersonPrefs','PersonSecurityQ','PersonSurveyResponse','Religion','RollNumber','SerialNumber','ServiceID','ServicePrefs','SexualOrientation','SortCode','SurveyResponse','TaxIdentifier','TrackingID','UserID','Username','VIPIndicator','ViewingCardNumber','ViewingDLDateTime','ViewingDLTime','ViewingDate','ViewingDuration','ViewingFavourites','ViewingItem','ViewingProvider','ViewingTime','VisitDateTime'],} ]
  * target_project
  * target_dataset
  * target_obfuscated_viewname
  
Please see the sample at this link: [sample input classification in json](test/data_classification_tag_entries.json)

## Tagging Obfuscation Process Flow
![alt text](images/Obfuscation.jpg)

## Data Governance Tag Templates
The following Tag Templates provided by the Data Governance Team would be used to Tag entries with PII information:
* Asset Governance Template: { Project: skyuk-uk-ds-catalogue-prod, Tag_Template_ID: asset_governance, Tag: includes_pii }
The Big query Table resources will be tagged with the tag mentioned. Tables which have PII will have the includes_pii set to True. 
Tables which do not have PII will either have no attached value for this Tag or the includes_pii Tag set to False. 
The second scenario may happen when once a Table has been tagged as True but later on changed to False.
* Column Governance Template: { Project: skyuk-uk-ds-catalogue-prod, Tag_Template_ID: column_governance, Tag: pii_element } 
If the Table has PII, then every column which has PII has to be tagged with the corresponding pii element type.

## Validations performed in the API
* Tagging API: The following validations are performed in the tagging api:
  * Validate that the user / service account running the code has access to both the Tag Templates
  * Validate that the input Data Classification file has all the required columns / JSON keys
  * Validate that the Tables specified in the input Data classification document are valid tables 
  and the user / service account running the API has access to the resource in the GCP Data Catalog
  * Validate that the includes_pii value specified in the input Data classification document is only True or False
  * Validate that the pii_element specified in the input Data classification document are valid enumerated values in 
  the { Project: skyuk-uk-ds-catalogue-prod, Tag_Template_ID: column_governance, Tag: pii_element } enumerations

* Obfuscation api: The following validations are performed in the Obfuscation api
  * The resource (Big Query Table) specified in the request has a corresponding Tag entries
  * If a Target view is specified, whether the user running the API has create privileges on the Project and the data set specified
  * Tables with PII has a Target view reference provided in the input Data classification
  * If create all views (obfuscate-all) option is specified then whether all the Tables have a Target view specified
  
## Processing Logic Flow

* Tagging API: The tagging API implements the following logic in sequence:
  1. Read the Data Classification input file
  2. Validate the Data classification input file
  3. Log errors and exit if there are any errors
  4. For each resource specified in the Data classification input file create / update the Tags
  5. Validate that all that tags have been created
  6. Log status
  
* Obfuscation API: The obfuscation API implements the following logic in sequence:
  1. Read the source & target inputs from Data Classification input file
  2. Check whether to Obfuscate all tables or only tables with PII by reading the runtime arguments
  3. Check if the Big Query UDF functions are present and compiled in the Target Dataset
  4. Compile the functions if they are not there
  5. Create the sql for the views which need to be created
  6. Compile / Run the view sql to create the target views
  7. Authorize to views
  
## Dependencies and assumptions
* All Tables for which views need to be created will have to be specified in the data classification document
* All Tables in the Data classification document will have to have the Target View name specified
* Rainbow will run the Obfuscation API with the specific run_type argument (the type which will create all views)
* The API will not check whether all the Tables in a Dataset are included in the Data classification document.
* Other Tables (in Datasets) which are not included in the data classification will neither be tagged nor would they be obfuscated.

## Logging
The logging behaviour depends on whether the API is deployed on Cloud Function or is deployed locally

* Logging on cloud function: If the api is deployed as a cloud function all the logs will be available in stackdriver. 
The stackdriver logs are available under: project -> Cloud Function -> run_obfuscation_tagging_http. The status of the 
function is also returned as a response object with http status code of 200 for a successful run and non 200 codes for
failures.

* Logging on local / VM deployment: When the code is run as ascript on local or on VM, the log file is created 
in the logs directory with the name log_YYYY-MM-DD-HH-MI-SS.log using standard date mask. The logs are also available
in Stackdriver under the group Global


## Rainbow deployment notes
* On the VM make sure that the following are installed:
   * Python 3.7
   * GCloud SDK
   * Git 
```bash
sudo apt-get install python3.7
sudo apt-get install google-cloud-sdk
sudo apt-get install git
```

* Check installation. Run the following to check the installation:
```bash
python --version
gcloud --version
git --version
```

* Clone the project
```
git clone org-1391938@github.com:sky-uk/tagging-obfuscation.git
```

* Install all the python requirements
```
cd tagging-obfuscation
pip install -r requirements.txt
```

* Service account that has the following:
   * Access to Data Catalog. Role: "Data Catalogue Tag Template User"
   * Access to "bigquery.datasets.update" permission for all datasets in the project
   * Big Query Read and write access to the project that is deploying Obfuscation
   * Access to deploy and run cloud functions
   * Access to stack driver
   
* Download the service account keyfile and assume a service account that has access to the Source and Target project. 
Code snippets below are for GCP project 'skyuk-uk-viewing-proc-dev' and service account viewing-proc-dev@skyuk-uk-viewing-proc-dev.iam.gserviceaccount.com
```
gcloud iam service-accounts keys create viewing-proc-dev.json --iam-account viewing-proc-dev@skyuk-uk-viewing-proc-dev.iam.gserviceaccount.com
gcloud auth activate-service-account --key-file=viewing-proc-dev.json
```

* Setup GOOGLE_APPLICATION_CREDENTIALS environment variable to the fully qualified key file downloaded in previous step
```
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]" # For Linux
```
  
* Create the dataclassification file. Important things to remember are:
   * File structure. All the columns / json key value pairs should be present
   * includes_pii identifies whether the table has PII or not. It is a boolean with True / False as only valid values
   * If includes_pii is True, then specify all columns that have PII. Also specify the PII_Element type. The valid PII 
   elements types are:
   ['AccessibilityInfo', 'AccountID', 'AccountNumber', 'ActivationDate', 'BBUsageAddress', 'BBUsageMeasure', 'BIC'
   ,'BankAccountNumer','BillingDate','BillingItem','BillingValue','BirthPlace','CDRDuration','CDRNumber','CallRouting'
   ,'CardExpiryDate','CardName','CardNumber','CommsAV','CommsTranscripts','CompEntrantDetails','ContentOrderItem'
   ,'Cookie','CoordinatesCoarse','CoordinatesFine','CreditCheckScore','CustomerModelValue','DDRequestDate','DOB'
   ,'DebtIndicator','DeviceID','DrivingLicenceNumber','Ethnicity','FraudIndicator','Gender','IBAN','ICCID','IMEI','IMSI'
   ,'IPAddress','InternationalIdentifier','JourneyTag','LetterTypePref','LoyaltyID','LoyaltyStatus','MACAddress'
   ,'MACCode','MedicalIdentifier','MoneyLaunderingResult','NDSNumber','NationalIdentifier','Nationality'
   ,'OrderAction','OrderDate','OrdinaryOrderItem','PEPStatus','PassportNumber','PaymentDate','PaymentMethod'
   ,'PersonAV','PersonAddressCoarse','PersonAddressFine','PersonAge','PersonAgeBand','PersonConsents','PersonEmail'
   ,'PersonHandle','PersonID','PersonName','PersonNotes','PersonPassword','PersonPhone','PersonPhoneAreaCode'
   ,'PersonPrefs','PersonSecurityQ','PersonSurveyResponse','Religion','RollNumber','SerialNumber','ServiceID'
   ,'ServicePrefs','SexualOrientation','SortCode','SurveyResponse','TaxIdentifier','TrackingID','UserID'
   ,'Username','VIPIndicator','ViewingCardNumber','ViewingDLDateTime','ViewingDLTime','ViewingDate','ViewingDuration'
   ,'ViewingFavourites','ViewingItem','ViewingProvider','ViewingTime','VisitDateTime']
   * Specify Target Project, Dataset and Viewname
   
* Run `run_locally.py` with argument `--filename` <fully qualified file with data classification> and `--type` 'tagging-obfuscation-all'

```
python run_locally.py --filename ./test/data_classification_tag_entries.json --type tagging-obfuscation-all
```
   
## Documentation and help

   * [Full technical Documentation](docs/Tagging-Obfuscation-API-V1.pdf)
   
   * [Demo video using cloud Function and json format - Click and then download to view](docs/demo_Cloud_Function_JSON_create-all-views.mp4)
   
   * [Demo video using script run on VM - Click and then download to watch](docs/demo_locallyOnVM_CSV_create-PII-only.mp4)

