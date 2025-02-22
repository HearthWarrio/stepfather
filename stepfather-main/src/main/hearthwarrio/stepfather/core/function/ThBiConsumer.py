from typing import Protocol, TypeVar, Optional, cast

T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E', bound=BaseException)

class ThBiConsumer(Protocol[T, U, E]):
    def accept(self, t: T, u: U) -> None:
        """
        Выполняет операцию над двумя аргументами.
        Может выбрасывать исключение типа E.
        """
        ...

def unchecked(consumer: Optional[ThBiConsumer[T, U, E]]) -> Optional[ThBiConsumer[T, U, Exception]]:
    """
    Возвращает переданный ThBiConsumer, приведённый к варианту с исключениями типа Exception,
    либо None, если consumer равен None.
    """
    return cast(Optional[ThBiConsumer[T, U, Exception]], consumer)