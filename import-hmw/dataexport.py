import csv
import mysql.connector
import configparser
from utils.singleton import SingletonType
from utils.logger import MyLogger
from utils.exceptions import Error

logger = MyLogger.__call__().get_logger()


class ExportData(object, metaclass=SingletonType):
    """This class implements the data export from MySQL DB into 2 text files (non-denormalized & denormalized)
    located in the /data/output/ """

    def __init__(self):
        """Initialize  Python Client"""

    def generate_output(data_type):
        """Export data from local db (mysql) into a text file which located in data/ouput folder

        :param data_type: type of data, whether it's a "flow" or "pressure" data

        :return: None"""

        config = configparser.ConfigParser()
        config.read('projectconfig.ini')

        mydb = mysql.connector.connect(host=config['dbdetails']['db_host'], port=int(config['dbdetails']['db_port']),
                                       database=config['dbdetails']['db_database'], user=config['dbdetails']['db_user'],
                                       password=config['dbdetails']['db_password'])
        logger.info("Connect to mysql db succeed")
        mycursor = mydb.cursor()

        if data_type.lower() == config['DEFAULT']['data_type_flow']:
            output_filename = config['path']['path_output_flow_file']
            output_header = config['dataexportdetails']['output_fields'] + "\n"
            sql_get_output_data = config['dataexportdetails']['sql_output_flow']
            output_filename_denormalized = config['path']['path_output_flow_denorm_file']
            output_header_denormalized = config['dataexportdetails']['output_fields_flow_denormalized']+ "\n"
            sql_get_output_data_denormalized = config['dataexportdetails']['sql_output_flow_denormalized']

        elif data_type.lower() == config['DEFAULT']['data_type_pressure']:
            output_filename = config['path']['path_output_pressure_file']
            output_header = config['dataexportdetails']['output_fields'] + "\n"
            sql_get_output_data = config['dataexportdetails']['sql_output_pressure']
            output_filename_denormalized = config['path']['path_output_pressure_denorm_file']
            output_header_denormalized = config['dataexportdetails']['output_fields_pressure_denormalized']+ "\n"
            sql_get_output_data_denormalized = config['dataexportdetails']['sql_output_pressure_denormalized']

        # ----- Export non-denormalized data
        try:
            open(output_filename, 'w').write(output_header)

            mycursor.execute(sql_get_output_data)
            output_data= mycursor.fetchall()

            with open(output_filename, 'a', newline='') as content:
                write_output = csv.writer(content)
                write_output.writerows(output_data)

            logger.info("Non-denormalized data ({}) is exported".format(data_type))

        except mysql.connector.errors.DatabaseError as error_db:
            error_db_message = str(error_db.errno) + " - " + error_db.sqlstate + " - " + error_db.msg
            logger.error("datatype={} | {}. Check log".format(data_type, error_db_message))
            logger.error("Unable export non-denormalized data ({}). Check log".format(data_type))
            pass

        except Error:
            logger.error("Unable export denormalized data ({}). Check log".format(data_type))
            pass

        # ----- Export denormalized data
        try:
            open(output_filename_denormalized, 'w').write(output_header_denormalized)

            mycursor.execute(sql_get_output_data_denormalized)
            output_data_denormalized = mycursor.fetchall()

            with open(output_filename_denormalized, 'a', newline='') as content:
                write_output = csv.writer(content)
                write_output.writerows(output_data_denormalized)

            logger.info("Denormalized data ({}) is exported".format(data_type))

        except mysql.connector.errors.DatabaseError as error_db:
            error_db_message = str(error_db.errno) + " - " + error_db.sqlstate + " - " + error_db.msg
            logger.error("datatype={} | {}. Check log".format(data_type, error_db_message))
            logger.error("Unable export denormalized data ({}). Check log".format(data_type))
            pass

        except Error:
            logger.error("Unable export denormalized data ({}). Check log".format(data_type))
            pass

        mydb.close()
        logger.info("Disconnect from mysql db succeed")
