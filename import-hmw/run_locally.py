import argparse
import os
import datetime as dt
import configparser
from utils.logger import MyLogger
from utils.exceptions import InvalidArgumentRunMode,NoArgumentRunMode,MissingConfigFile
from dataimport import ImportData
from dataexport import ExportData
import mysql.connector

loggin_obj = MyLogger()

def main():
    """This is a function that will run when the import-hmw is deployed locally.

    :Arguments:
    --runmode: "run_bau" or "run_fail"

    :return: None"""

    loggin_obj.add_logger_file_handler()
    logger = loggin_obj.get_logger()
    parser = argparse.ArgumentParser(description='Run import-hmw from VM or Local Python')
    parser.add_argument('--runmode', help='Option: run_bau (to run as usual) or run_fail (to run only those failing files')
    args = parser.parse_args()
    run_mode = args.runmode
    config = configparser.ConfigParser()
    config.read('projectconfig.ini')

    logger.info("Pipeline start")

    # ----- Validates argument - runmode
    if run_mode is None:
        logger.error("No run mode provided")
        raise NoArgumentRunMode("The run mode is required. Currently no run mode provided. Check log")

    elif run_mode.lower() == config['DEFAULT']['run_mode_bau']:
        logger.info("The run mode is:{}".format(run_mode))
        configuration_file_used = config['path']['path_configuration_file']

    elif run_mode.lower()== config['DEFAULT']['run_mode_fail']:
        logger.info("The run mode is:{}".format(run_mode))
        configuration_file_used = config['path']['path_configuration_failed_file']

    else:
        logger.error("The run mode '{}' is not a valid value".format(run_mode))
        raise InvalidArgumentRunMode("The run mode is required. Run mode provided:'{}'. Check log".format(run_mode))

    # ----- Validates configuration files
    if not os.path.exists(configuration_file_used):
        logger.error("{} not found".format(configuration_file_used))
        raise MissingConfigFile("{} not found. Check log".format(configuration_file_used))

    # ----- Define period start date & end date
    download_period_length = int(config['DEFAULT']['delta_days'])
    download_start_date = dt.datetime.strftime(dt.datetime.today() - dt.timedelta(days=download_period_length), '%Y-%m-%d')
    download_end_date = dt.datetime.strftime(dt.datetime.today(), '%Y-%m-%d')

    # ----- Download data into local machine, load data into mysql, export data into text file
    ImportData.download_data(configuration_file_used, config['path']['path_configuration_failed_file'], download_start_date, download_end_date)
    ImportData.load_data(configuration_file_used, config['path']['path_configuration_failed_file'])
    ExportData.generate_output(config['DEFAULT']['data_type_flow'])
    ExportData.generate_output(config['DEFAULT']['data_type_pressure'])

    logger.info("Pipeline end")

if __name__== "__main__":
  main()