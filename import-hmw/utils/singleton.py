class SingletonType(type):
    """A Base class for Singleton implementation"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Instantiate the class. Only one instance allowed. Return existing instance in all other cases
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
