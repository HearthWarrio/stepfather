class StepfatherException(Exception):
    """
    Xteps exception.
    """

    def __init__(self, message: str = None, cause: Exception = None):
        """
        Инициализирует StepfatherException.

        :param message: Сообщение исключения.
        :param cause: Причина исключения.
        """
        if message is None and cause is not None:
            message = str(cause)
        super().__init__(message)
        self.cause = cause
