import configparser
from utils.logger import MyLogger
from utils.singleton import SingletonType

logger = MyLogger.__call__().get_logger()

class GetConfig(object, metaclass=SingletonType):
    """ Configuration class to load Config. This is a Singleton implementation """

    def __init__(self):
        """Constructor for the GetConfig Class"""
        # Get the project config from ini file
        self.projconfig = configparser.ConfigParser()
        config_file_path = self._get_proj_configpath()
        self.projconfig.read(config_file_path)


    def get_config_values(self):
        """Return the configuration entries

        :return: Configuration
        :rtype: python config object
        """
        return self.projconfig


    @staticmethod
    def _get_proj_configpath():
        """Returns the configuration file path

        :return: config file path
        :rtype: string
        """
        configfilepath = 'projectconfig.ini'
        return configfilepath
