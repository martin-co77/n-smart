class InvalidClassException(Exception):

    errors = None

    def __init__(self, message, errors=None):
        """
        :param message:
        :param errors:
        """
        super().__init__(message)
        self.errors = errors

