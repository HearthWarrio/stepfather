from abc import ABC, abstractmethod

"""
Exception as StepfatherException.
Исключение, аналогичное StepfatherException.
"""
class StepfatherException(Exception):

    pass

"""
Keyword abstract base class.
Абстрактный базовый класс для ключевого слова.
"""
class Keyword(ABC):

    """
    Returns string of keyword.
    Возвращает строковое представление ключевого слова.
    """
    @abstractmethod
    def __str__(self) -> str:

        pass


class Of(Keyword):
    """
    Реализация Keyword.
    Keyword implementation
    При инициализации проверяет, что аргумент name не равен None.
    Asserts that arg not null.
    """

    def __init__(self, name: str) -> None:
        if name is None:
            raise StepfatherException("name arg is null")
        self.name = name

    def __str__(self) -> str:
        return self.name
