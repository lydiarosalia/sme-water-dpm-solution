class Error(Exception):
    """Base class for other exceptions"""
    pass

class InvalidArgumentRunMode(Error):
    """Raised when the run mode argument is invalid"""
    pass

class NoArgumentRunMode(Error):
    """Raised when the run mode argument is invalid"""
    pass

class MissingConfigFile(Error):
    """Raised when the config file is missing"""
    pass
