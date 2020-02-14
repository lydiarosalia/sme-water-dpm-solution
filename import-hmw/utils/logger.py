import logging
from utils.singleton import SingletonType
import datetime

# python 3 style
class MyLogger(object, metaclass=SingletonType):
    """Creates the Logger object. The Class is a singleton implementation"""
    _logger = None

    def __init__(self):
        """Instantiates an instance of logger. Only one instance can be created.

        """
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s : line %(lineno)s] >> %(message)s')
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(self.formatter)
        self._logger.addHandler(streamHandler)

    def add_logger_file_handler(self):
        """This adds a filehandler to the logger class and also configures StackDriver Logging.

        The logs will be created in the logs directory under the base project.
        The Stackdriver logs can be found under Global logs.

        :return: None
        """
        now = datetime.datetime.now()
        fileHandler = logging.FileHandler("logs/" + "import-data-"+ now.strftime("%Y%m%d%H%M%S%f")+".log")
        fileHandler.setFormatter(self.formatter)
        self._logger.addHandler(fileHandler)

    def get_logger(self):
        """Returns the Instance of the logger created

        :return: logger object
        """
        return self._logger