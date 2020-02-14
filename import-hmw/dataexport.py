import csv
import mysql.connector
import configparser
from utils.singleton import SingletonType
from utils.logger import MyLogger

logger = MyLogger.__call__().get_logger()

class ExportData(object, metaclass=SingletonType):
    """This class implements the data export from MySQL DB into text file located in the /data/output/"""

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

        try:
            if data_type.lower() == config['DEFAULT']['data_type_flow']:
                sql_get_output_data = "SELECT CONVERT(site_id USING utf8), CONVERT(all_datetime USING utf8), CONVERT(value USING utf8) FROM flow_view"
                output_filename = config['path']['path_output_flow_file']
            elif data_type.lower() == config['DEFAULT']['data_type_pressure']:
                sql_get_output_data = "SELECT CONVERT(site_id USING utf8), CONVERT(all_datetime USING utf8), CONVERT(value USING utf8) FROM pressure_view"
                output_filename = config['path']['path_output_pressure_file']

            mycursor.execute(sql_get_output_data)
            result = mycursor.fetchall()
            output_file_header = config['dataexportdetails']['output_file_header'] + "\n"
            open(output_filename, 'w').write(output_file_header)

            with open(output_filename, 'a', newline='') as content:
                write_output = csv.writer(content)
                write_output.writerows(result)

            logger.info("Data ({}) is exported".format(data_type))

        except Exception:
            logger.error("Unable export data ({}). Check log".format(data_type))
            pass

        finally:
            mydb.close()
            logger.info("Disconnect from mysql db succeed")