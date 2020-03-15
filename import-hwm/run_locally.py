import argparse
import csv
import os
import mysql.connector
import configparser
import datetime as dt
from utils.logger import MyLogger
from utils.exceptions import MissingConfigFile,DatabaseNotExist
from dataimport import ImportData

loggin_obj = MyLogger()


def main():
    """This is a function that will run when the import-hmw is deployed locally.

    :return: None"""
    loggin_obj.add_logger_file_handler()
    logger = loggin_obj.get_logger()

    config = configparser.ConfigParser()
    confpath = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
    config.read(os.path.join(confpath, 'projectconfig.ini'))

    parser = argparse.ArgumentParser(description='Run import-hwm from VM or Local Python')
    parser.add_argument('--configfile', help='format: [filename].csv For example file name is "abc" then argument will be "abc.csv"')
    parser.add_argument('--dbname', help='format: [dbname] For example db name is "dpm-solution-dma1" then argument will be "dpm-solution-dma1"')
    args = parser.parse_args()

    logger.info("Pipeline start")

    # ----- Define configuration file whether the default file or not
    adhoc_config_file = args.configfile

    if adhoc_config_file is None:
        configuration_file_used = config['path']['path_utils'] + config['path']['configuration_file_name']
    else:
        configuration_file_used = config['path']['path_utils'] + adhoc_config_file

    # ----- Validate whether the configuration file exists in utils/ directory or not
    if not os.path.exists(configuration_file_used):
        logger.error("{} not found".format(configuration_file_used))
        raise MissingConfigFile("{} not found in /utils directory. Check log".format(configuration_file_used))
    else:
        logger.info("Using this configuration file = {}".format(configuration_file_used))


    # ----- Define db whether the default db or not
    db_name = args.dbname

    if db_name is None:
        db_database = config['dbdetails']['default_db_name']
    else:
        db_database = db_name

    # ----- Validate whether the the db exists or not
    try:
        conn = mysql.connector.connect(host=config['dbdetails']['db_host'], port=int(config['dbdetails']['db_port']),
                                       database=db_database, user=config['dbdetails']['db_user'],
                                       password=config['dbdetails']['db_password'])

        logger.info("Using this database = {}".format(db_database))

    except mysql.connector.Error:
        logger.error("Database {} not found".format(db_database))
        raise DatabaseNotExist("{} not found. Check log".format(db_database))


    # ----- Set the download period (start date & end date)
    download_period_length = int(config['dataimportdetails']['delta_days'])
    download_start_date = dt.datetime.strftime(dt.datetime.today() - dt.timedelta(days=download_period_length), '%Y-%m-%d')
    download_end_date = dt.datetime.strftime(dt.datetime.today(), '%Y-%m-%d')


    # ----- Based on configuration file, (loop) start download and load data from HWM web-server into local MySQL
    with open(configuration_file_used) as csvfile_config:
        read_config = csv.reader(csvfile_config)
        header_config = next(read_config)

        for row in read_config:
            data_type = row[1].strip().lower()
            channel_no = int(row[2])
            site_id = row[0]
            logger_id = int(row[3])
            path_input_file = config['path']['path_input'] + site_id + '_' + str(channel_no) + '_' + data_type + '.csv'

            # ----- Validate data type: only site with a valid data type (pressure, flow) will be processed
            if data_type == config['DEFAULT']['data_type_flow'] or data_type == config['DEFAULT']['data_type_pressure']:

                # ----- Main process: donwload data - add missing records - load data
                ImportData.download_data(data_type, site_id, channel_no, logger_id, path_input_file, download_start_date, download_end_date)

                if os.path.exists(path_input_file):
                    ImportData.add_missing_records(data_type, site_id, channel_no, logger_id, path_input_file)

                if os.path.exists(path_input_file):
                    ImportData.load_data(data_type, site_id, channel_no, logger_id, path_input_file, db_database)

                # ----- Remove file from data/input/ once process is completed
                if os.path.exists(path_input_file):
                    os.remove(path_input_file)

                    logger.info("logger={} site={} channelno={} datatype={} | File is removed".format(logger_id, site_id,str(channel_no), data_type))

            else:
                logger.error("logger={} site={} channelno={} datatype={} | Invalid data type, no data is imported. Check log".format(logger_id, site_id, str(channel_no), data_type))

    logger.info("Pipeline end")

if __name__== "__main__":
  main()