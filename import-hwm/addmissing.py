import csv
import configparser
import datetime as dt
from utils.singleton import SingletonType
from utils.logger import MyLogger

logger = MyLogger.__call__().get_logger()

class MissingAdding(object, metaclass=SingletonType):
    """This class implements the data import to Mysql db"""


    def add_missing_records(configuration_file_used):
        """Add missing (15 mins.) records

        :param configuration_file_used: configuration file that will be used

        :return: None"""

        config = configparser.ConfigParser()
        config.read('projectconfig.ini')

        with open(configuration_file_used) as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)

            for row in reader:
                data_type = row[1].strip().lower()
                channel_no = int(row[2])
                site_id = row[0]
                path_input_file = config['path']['path_input'] + site_id + '_' + str(channel_no) + '_' + data_type + '.csv'

                try:
                    list1 = []

                    with open(path_input_file) as csvfile:
                        reader = csv.reader(csvfile)
                        next(reader)

                        for row in reader:
                            list1.append([dt.datetime.strptime(row[0],'%d-%m-%Y %H:%M'),row[channel_no]])

                    list2 = []

                    for i in range(len(list1)-1):
                        list2.append([list1[i][0],(list1[i + 1][0] - list1[i][0])/dt.timedelta(minutes=15)])

                    list3 = []

                    for x in range(len(list2)):
                        if (list2[x][1]) > 1.0:
                            list3.append([list2[x][0],list2[x+1][0],list2[x][1]])

                    for y in list3:
                        start = y[0]
                        end = y[1]- dt.timedelta(minutes=15)
                        current = start
                        while current != end:
                            current = current + dt.timedelta(minutes=15)
                            list1.append([current, None])

                    list1.sort()

                    with open(path_input_file, 'w', newline = "") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['Datetime','Value'])
                        writer.writerows(list1)

                except Exception:
                    pass

    def add_missing_records2(channel_no, path_input_file):
        """Add missing (15 mins.) records

        :param channel_no: channel number in a logger
        :param path_input_file: path of the input file

        :return: None"""

        config = configparser.ConfigParser()
        config.read('projectconfig.ini')

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

        open(path_input_file, 'w').write(config['dataimportdetails']['file_header'] + "\n")

        with open(path_input_file, 'a', newline="") as content:
            write_content = csv.writer(content)
            write_content.writerows(list1)