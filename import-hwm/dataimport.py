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

    def download_data(configuration_file_used, download_start_date, download_end_date):
        """Download data from HMW server into local machine

        :param configuration_file_used: configuration file that will be used
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
                path_input_file = config['path']['path_input'] + site_id + '_' + str(channel_no) + '_' + data_type + '.csv'

                try:
                    open(path_input_file, 'wb').write(requests.get(url).content)

                except Exception:
                    logger.error("site={} channelno={} datatype={} | Unable download data. Check log".format(site_id,str(channel_no),data_type))
                    os.remove(path_input_file)
                    pass

                finally:
                    if os.path.exists(path_input_file):
                        logger.info("site={} channelno={} datatype={}  | Data is downloaded".format(site_id,str(channel_no),data_type))
                    else:
                        logger.warning("site={} channelno={} datatype={}  | No data is downloaded".format(site_id,str(channel_no),data_type))

    def load_data(configuration_file_used):
        """Load data from local machine into local db (mysql), then the file will be deleted from the local machine after its loaded

        :param configuration_file_used: configuration file that will be used

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
                data_type = row[1].strip().lower()
                channel_no = int(row[2])
                logger_no = row[3]
                path_input_file = config['path']['path_input'] + site_id + '_' + str(channel_no) + '_' + data_type + '.csv'

                if data_type == config['DEFAULT']['data_type_flow'] or data_type == config['DEFAULT']['data_type_pressure']:
                    if os.path.exists(path_input_file):

                        with open(path_input_file) as csvfile_load:

                            reader_load = csv.reader(csvfile_load)
                            header_load = next(reader_load)

                            try:
                                for row in reader_load:
                                    datetime_to_load = datetime.strptime(row[0], '%d-%m-%Y %H:%M')

                                    if row[channel_no] == '':
                                        value = 'NULL'
                                    else:
                                        value = row[channel_no]

                                    field_name = site_id + "_" + str(channel_no)

                                    if data_type == config['DEFAULT']['data_type_flow']:
                                        sql_insert = "INSERT INTO flow (datetime, site_id, channel_no, value) VALUES ('{}', '{}', {}, {}) ON DUPLICATE KEY UPDATE datetime='{}', site_id='{}', channel_no={}, value= {}".format(datetime_to_load, site_id, channel_no, value, datetime_to_load, site_id, channel_no, value)
                                        sql_insert_denormalized = "INSERT INTO flow_denormalized (datetime," + field_name + ") VALUES ('{}', {}) ON DUPLICATE KEY UPDATE datetime='{}', ".format(datetime_to_load, value, datetime_to_load) + field_name + "= {}".format(value)
                                    elif data_type == config['DEFAULT']['data_type_pressure']:
                                        sql_insert = "INSERT INTO pressure (datetime, site_id, channel_no, value) VALUES ('{}', '{}', {}, {}) ON DUPLICATE KEY UPDATE datetime='{}', site_id='{}', channel_no={}, value= {}".format(datetime_to_load, site_id, channel_no, value, datetime_to_load, site_id, channel_no, value)
                                        sql_insert_denormalized = "INSERT INTO pressure_denormalized (datetime," + field_name + ") VALUES ('{}', {}) ON DUPLICATE KEY UPDATE datetime='{}', ".format(datetime_to_load, value, datetime_to_load) + field_name + "= {}".format(value)

                                    mycursor.execute(sql_insert)
                                    mycursor.execute(sql_insert_denormalized)

                                mydb.commit()
                                logger.info("site={} channelno={} datatype={} | Data is loaded".format(site_id,str(channel_no),data_type))

                            except mysql.connector.errors.DatabaseError as error_db:
                                mydb.rollback()
                                error_db_message = str(error_db.errno) + " - " + error_db.sqlstate + " - " + error_db.msg
                                logger.error("site={} channelno={} datatype={} | {}. Check log".format(site_id,str(channel_no),data_type,error_db_message))
                                pass

                        os.remove(path_input_file)

                    else:
                        logger.warning("site={} channelno={} datatype={} | No data is loaded because file not found".format(site_id,str(channel_no),data_type))

                else:
                    logger.error("site={} channelno={} datatype={} | No data is loaded because {} is not a valid logger type, expected value is flow or pressure".format( site_id,str(channel_no),data_type))

        mydb.close()
        logger.info("Disconnect from mysql db succeed")
