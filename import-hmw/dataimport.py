import csv
import os
import requests
import mysql.connector
import configparser
from datetime import datetime
from utils.singleton import SingletonType
from utils.logger import MyLogger

logger = MyLogger.__call__().get_logger()

class ImportData(object, metaclass=SingletonType):
    """This class implements the data import to Mysql db"""

    def __init__(self):
        """Initialize  Python Client"""

    def generate_config_failed_files(filename, site_id, data_type, channel_no, logger_no):
        """Create utils/configuration_failed_files.csv if any fail encountered

        :param filename: file that will be created
        :param data_type: type of data, whether it's a "flow" or "pressure" data
        :param channel_no: channel number
        :param logger_no: logger number

        :return: None"""

        config = configparser.ConfigParser()
        config.read('projectconfig.ini')

        if not os.path.exists(filename):
            output_file_header = config['dataimportdetails']['config_failed_file_header'] + "\n"
            open(filename, 'w').write(output_file_header)

        open(filename, 'a').write(site_id + "," + data_type + "," + str(channel_no) + "," + logger_no)

        logger.info("site={} | {} is generated".format(site_id, filename))

    def download_data(configuration_file_used, configuration_failed_file, download_start_date, download_end_date):
        """Download data from HMW server into local machine

        :param configuration_file_used: configuration file that will be used
        :param configuration_failed_file: configuration file that contain failing logger
        :param download_start_date: start time of download period
        :param download_end_date: end time of download period

        :return: None"""

        config = configparser.ConfigParser()
        config.read('projectconfig.ini')

        with open(configuration_file_used) as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)

            for row in reader:
                data_type = row[1].strip().lower()
                channel_no = int(row[2])
                logger_no = row[3]
                site_id = row[0]
                url = config['dataimportdetails']['url1']  + row[3] + config['dataimportdetails']['url2']  + download_start_date + config['dataimportdetails']['url3']  + download_end_date + config['dataimportdetails']['url4']
                path_input_file = config['path']['path_input'] + site_id + '.csv'

                try:
                    open(path_input_file, 'wb').write(requests.get(url).content)

                except Exception:
                    logger.error("site={} | Unable download data. Check log".format(site_id))
                    ImportData.generate_config_failed_files(configuration_failed_file, site_id, data_type, channel_no, logger_no)
                    pass

                finally:
                    if os.path.exists(path_input_file):
                        logger.info("site={} | Data is downloaded".format(site_id))
                    else:
                        logger.warning("site={} | No data is downloaded".format(site_id))

    def load_data(configuration_file_used, configuration_failed_file):
        """Load data from local machine into local db (mysql)

        :param configuration_file_used: configuration file that will be used
        :param configuration_failed_file: configuration file that contain failing logger

        :return: None"""

        config = configparser.ConfigParser()
        config.read('projectconfig.ini')

        mydb = mysql.connector.connect(host=config['dbdetails']['db_host'], port=int(config['dbdetails']['db_port']),
                                       database=config['dbdetails']['db_database'], user=config['dbdetails']['db_user'],
                                       password=config['dbdetails']['db_password'])
        logger.info("Connect to mysql db succeed")
        mycursor = mydb.cursor()

        with open(configuration_file_used) as csvfile_config:
            reader_config = csv.reader(csvfile_config)
            header_config = next(csvfile_config)

            for row in reader_config:
                site_id = row[0]
                path_input_file = config['path']['path_input'] + site_id + '.csv'
                data_type = row[1].strip().lower()
                channel_no = int(row[2])
                logger_no = row[3]

                if data_type == config['DEFAULT']['data_type_flow'] or data_type == config['DEFAULT']['data_type_pressure']:
                    if os.path.exists(path_input_file):

                        with open(path_input_file) as csvfile_load:

                            reader_load = csv.reader(csvfile_load)
                            header_load = next(reader_load)

                            try:
                                for row in reader_load:
                                    datetime_to_load = datetime.strptime(row[0], '%d-%m-%Y %H:%M')

                                    if row[channel_no] == '':
                                        value = None
                                    else:
                                          value = row[channel_no]

                                    if data_type == config['DEFAULT']['data_type_flow']:
                                        sql_insert = "INSERT INTO flow (datetime, site_id, value) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE datetime=%s, site_id=%s, value= %s"
                                        values_to_load = (datetime_to_load, site_id, value, datetime_to_load, site_id, value)
                                    elif data_type == config['DEFAULT']['data_type_pressure']:
                                        sql_insert = "INSERT INTO pressure (datetime, site_id, value) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE datetime=%s, site_id=%s, value= %s"
                                        values_to_load = (datetime_to_load, site_id, value, datetime_to_load, site_id, value)

                                    mycursor.execute(sql_insert, values_to_load)

                                mydb.commit()
                                logger.info("site={} | Data ({}) is loaded".format(site_id,data_type))

                            except mysql.connector.errors.DatabaseError as error_db:
                                mydb.rollback()
                                error_db_message = str(error_db.errno) + " - " + error_db.sqlstate + " - " + error_db.msg
                                logger.error("site={} | {}. Check log".format(site_id, error_db_message))
                                ImportData.generate_config_failed_files(configuration_failed_file, site_id, data_type, channel_no, logger_no)

                                pass

                        os.remove(path_input_file)

                    else:
                        logger.warning("site={} | No data is loaded because file not found".format(site_id))

                else:
                    logger.error("site={} | No data is loaded because {} is not a valid logger type, expected value is flow or pressure".format( site_id, data_type))

        mydb.close()
        logger.info("Disconnect from mysql db succeed")
