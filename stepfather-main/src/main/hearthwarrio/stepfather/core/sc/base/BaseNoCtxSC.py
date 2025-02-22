from typing import Protocol, TypeVar, Generic, Any
from function.ThRunnable import ThRunnable
from function.ThSupplier import ThSupplier
from core import StepfatherException
from sc.base import StepContext
from sc.base import BaseCtxSC

S = TypeVar('S', bound='BaseNoCtxSC')
R = TypeVar('R')

class BaseNoCtxSC(StepContext[S], Protocol):
    def exec(self, action: ThRunnable[Exception]) -> S:
        """
        Выполняет заданное действие.

        :param action: Действие (ThRunnable), которое может выбросить исключение.
        :return: Этот step context.
        :raises StepfatherException: если action равен None.
        """
        ...

    def with_(self, action: ThSupplier[R, Exception]) -> BaseCtxSC[R, Any]:
        """
        Выполняет заданное действие и возвращает новый контекст шага.

        :param action: Действие (ThSupplier), которое может выбросить исключение.
        :return: Новый контекст шага с типом результата R и неуточнённым вторым параметром.
        :raises StepfatherException: если action равен None.
        """
        ...

    def res(self, action: ThSupplier[R, Exception]) -> R:
        """
        Выполняет заданное действие и возвращает результат.

        :param action: Действие (ThSupplier), которое может выбросить исключение.
        :return: Результат действия.
        :raises StepfatherException: если action равен None.
        """
        ...
