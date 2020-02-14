from utils.configuration import GetConfig
from utils.logger import MyLogger
logger = MyLogger.__call__().get_logger()

class ReadInput:
    """Class to read inputs"""

    def __init__(self):
        """Initialize the input reader object. Read configuration values.

        This method does the following:
        - Retrieves the configuration values

        :param: None
        :return: None

        """
        self.config_vals = GetConfig().get_config_values()

