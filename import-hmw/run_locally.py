import argparse
import os
import datetime as dt
import configparser
from utils.logger import MyLogger
from utils.exceptions import MissingConfigFile
from dataimport import ImportData
from dataexport import ExportData

loggin_obj = MyLogger()


def main():
    """This is a function that will run when the import-hmw is deployed locally.

    :return: None"""

    loggin_obj.add_logger_file_handler()
    logger = loggin_obj.get_logger()
    parser = argparse.ArgumentParser(description='Run import-hmw from VM or Local Python')
    parser.add_argument('--configfile', help='format: [filename].csv For example file name is "abc" then argument will be "abc.csv"')
    args = parser.parse_args()
    adhoc_config_file = args.configfile
    config = configparser.ConfigParser()
    config.read('projectconfig.ini')

    logger.info("Pipeline start")

    # ----- Define config file to be used
    if adhoc_config_file is None:
        configuration_file_used = config['path']['path_utils'] + config['path']['configuration_file_name']
    else:
        configuration_file_used = config['path']['path_utils'] + adhoc_config_file

    logger.info("Using this configuration file = {}".format(configuration_file_used))

    # ----- Validates configuration files
    if not os.path.exists(configuration_file_used):
        logger.error("{} not found".format(configuration_file_used))
        raise MissingConfigFile("{} not found. Check log".format(configuration_file_used))

    # ----- Define period start date & end date
    download_period_length = int(config['DEFAULT']['delta_days'])
    download_start_date = dt.datetime.strftime(dt.datetime.today() - dt.timedelta(days=download_period_length), '%Y-%m-%d')
    download_end_date = dt.datetime.strftime(dt.datetime.today(), '%Y-%m-%d')

    # ----- Download data into local machine, load data into mysql, export data into text file
    ImportData.download_data(configuration_file_used, download_start_date, download_end_date)
    ImportData.load_data(configuration_file_used)
    ExportData.generate_output(config['DEFAULT']['data_type_flow'])
    ExportData.generate_output(config['DEFAULT']['data_type_pressure'])

    logger.info("Pipeline end")

if __name__== "__main__":
  main()