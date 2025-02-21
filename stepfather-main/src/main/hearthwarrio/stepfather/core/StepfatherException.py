class StepfatherException(Exception):
    """
    Stepfather exception.
    """
    def __init__(self, message: str = None, cause: Exception = None):
        if message is None and cause is not None:
            message = str(cause)
        super().__init__(message)
        self.cause = cause