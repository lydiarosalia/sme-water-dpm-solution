class Error(Exception):
    """Base class for other exceptions"""
    pass

class MissingConfigFile(Error):
    """Raised when the config file is missing"""
    pass
