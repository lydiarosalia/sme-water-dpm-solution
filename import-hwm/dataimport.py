import csv
import os
import mysql.connector
import configparser
import datetime as dt
import requests
from utils.singleton import SingletonType
from utils.logger import MyLogger

logger = MyLogger.__call__().get_logger()


class ImportData(object, metaclass=SingletonType):
    """This class implements the data import to Mysql db"""


    def __init__(self):
        """Initialize  Python Client"""


    def download_data(data_type, site_id, channel_no, logger_id, path_input_file, download_start_date, download_end_date):
        """Function to download data from HWM web server into local machine (via HTTPS request) as CSV file

        :param data_type: (must be derived from the configuration) "flow" or "pressure"
        :param site_id: (must be derived from the configuration) site ID
        :param channel_no: (must be derived from the configuration) channel number
        :param logger_id: (must be derived from the configuration) logger ID
        :param path_input_file: (must be derived from the configuration) file path of downloaded file
        :param download_start_date: start time of download period
        :param download_end_date: end time of download period

        :return: None"""

        config = configparser.ConfigParser()
        confpath = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
        config.read(os.path.join(confpath, 'projectconfig.ini'))
        # config.read('projectconfig.ini')

        url = config['dataimportdetails']['url1']  + str(logger_id) + config['dataimportdetails']['url2']  + download_start_date + config['dataimportdetails']['url3']  + download_end_date + config['dataimportdetails']['url4']

        try:
            # ----- Download file and write it as csv
            open(path_input_file, 'wb').write(requests.get(url).content)

            if os.path.exists(path_input_file):
                logger.info("logger={} site={} channelno={} datatype={} | Data is downloaded".format(logger_id,site_id,str(channel_no),data_type))
            else:
                logger.warning("logger={} site={} channelno={} datatype={} | No data is downloaded".format(logger_id,site_id,str(channel_no),data_type))

        except Exception:
            if os.path.exists(path_input_file):
                os.remove(path_input_file)

            logger.error("logger={} site={} channelno={} datatype={} | Unable download data. Check log".format(logger_id,site_id,str(channel_no),data_type))
            pass

    def add_missing_records(data_type, site_id, channel_no, logger_id, path_input_file):
        """Function to add missing datetime records

        :param data_type: (must be derived from the configuration) "flow" or "pressure"
        :param site_id: (must be derived from the configuration) site ID
        :param channel_no: (must be derived from the configuration) channel number
        :param logger_id: (must be derived from the configuration) logger ID
        :param path_input_file: (must be derived from the configuration) file path of downloaded file

        :return: None"""

        config = configparser.ConfigParser()
        confpath = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
        config.read(os.path.join(confpath, 'projectconfig.ini'))
        # config.read('projectconfig.ini')

        try:
            # ----- Add missing rows
            list1 = []

            with open(path_input_file) as csvfile_input:
                reader_input = csv.reader(csvfile_input)
                next(reader_input)

                for row in reader_input:
                    list1.append([dt.datetime.strptime(row[0], '%d-%m-%Y %H:%M'), row[channel_no]])

            list2 = []

            for i in range(len(list1) - 1):
                list2.append([list1[i][0], (list1[i + 1][0] - list1[i][0]) / dt.timedelta(minutes=int(config['dataimportdetails']['delta_time']))])

            list3 = []

            for x in range(len(list2)):
                if (list2[x][1]) > 1.0:
                    list3.append([list2[x][0], list2[x + 1][0], list2[x][1]])

            for y in list3:
                start = y[0]
                end = y[1] - dt.timedelta(minutes=15)
                current = start

                while current != end:
                    current = current + dt.timedelta(minutes=int(config['dataimportdetails']['delta_time']))
                    list1.append([current, None])

            list1.sort()

            # ----- Overwrite files with the complete data
            open(path_input_file, 'w').write(config['dataimportdetails']['file_header'] + "\n")

            with open(path_input_file, 'a', newline="") as content:
                write_content = csv.writer(content)
                write_content.writerows(list1)

            logger.info("logger={} site={} channelno={} datatype={} | Missing records is added".format(logger_id,site_id,str(channel_no),data_type))

        except Exception:
            if os.path.exists(path_input_file):
                os.remove(path_input_file)

            logger.error("logger={} site={} channelno={} datatype={} | Unable add missing records. Check log".format(logger_id,site_id,str(channel_no),data_type))
            pass


    def load_data(data_type, site_id, channel_no, logger_id, path_input_file, db_database):
        """Function to load data from local machine into local db (MySQL)

        :param data_type: (must be derived from the configuration) "flow" or "pressure"
        :param site_id: (must be derived from the configuration) site ID
        :param channel_no: (must be derived from the configuration) channel number
        :param logger_id: (must be derived from the configuration) logger ID
        :param path_input_file: (must be derived from the configuration) file path of downloaded file

        :return: None"""

        config = configparser.ConfigParser()
        confpath = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
        config.read(os.path.join(confpath, 'projectconfig.ini'))
        # config.read('projectconfig.ini')

        # ----- Open db connection
        mydb = mysql.connector.connect(host=config['dbdetails']['db_host'], port=int(config['dbdetails']['db_port']),
                                       database=db_database, user=config['dbdetails']['db_user'],
                                       password=config['dbdetails']['db_password'])

        logger.info("logger={} site={} channelno={} datatype={} | Connect to mysql db succeed".format(logger_id, site_id,str(channel_no),data_type))

        mycursor = mydb.cursor()

        # ----- Loop and load all files
        with open(path_input_file) as csvfile_load:

            reader_load = csv.reader(csvfile_load)
            header_load = next(reader_load)

            try:
                for row in reader_load:
                    datetime_to_load = dt.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')

                    if row[1] == '':
                        value = 'NULL'
                    else:
                        value = row[1]

                    if data_type == config['DEFAULT']['data_type_flow']:
                        sql_insert = "INSERT INTO flow (datetime, site_id, channel_no, value) VALUES ('{}', '{}', {}, {}) ON DUPLICATE KEY UPDATE datetime='{}', site_id='{}', channel_no={}, value= {}".format(datetime_to_load, site_id, channel_no, value, datetime_to_load, site_id, channel_no, value)
                    elif data_type == config['DEFAULT']['data_type_pressure']:
                        sql_insert = "INSERT INTO pressure (datetime, site_id, channel_no, value) VALUES ('{}', '{}', {}, {}) ON DUPLICATE KEY UPDATE datetime='{}', site_id='{}', channel_no={}, value= {}".format(datetime_to_load, site_id, channel_no, value, datetime_to_load, site_id, channel_no, value)

                    mycursor.execute(sql_insert)

                mydb.commit()

                logger.info("logger={} site={} channelno={} datatype={} | Data is loaded".format(logger_id,site_id,str(channel_no),data_type))

            except mysql.connector.errors.DatabaseError as error_db:
                mydb.rollback()
                error_db_message = str(error_db.errno) + " - " + error_db.sqlstate + " - " + error_db.msg

                if os.path.exists(path_input_file):
                    os.remove(path_input_file)

                logger.error("logger={} site={} channelno={} datatype={} | {}. Check log".format(logger_id, site_id, str(channel_no), data_type, error_db_message))
                pass

        # ----- Close db connection
        mydb.close()

        logger.info("logger={} site={} channelno={} datatype={} | Disconnect from mysql db succeed".format(logger_id, site_id, str(channel_no), data_type))