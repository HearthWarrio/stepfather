from typing import Protocol, TypeVar, Generic, Any
from function.ThTriConsumer import ThTriConsumer
from function.ThTriFunction import ThTriFunction
from base import StepContext
from base import BaseAnyCtxSC
from core import StepfatherException

C1 = TypeVar('C1')
C2 = TypeVar('C2')
C3 = TypeVar('C3')
S = TypeVar('S', bound='BaseTriCtxSC[C1, C2, C3, S]')
R = TypeVar('R')
R1 = TypeVar('R1')
R2 = TypeVar('R2')
R3 = TypeVar('R3')


class BaseTriCtxSC(StepContext[S], BaseAnyCtxSC[S], Protocol, Generic[C1, C2, C3, S]):
    def exec(self, action: ThTriConsumer[C1, C2, C3, Exception]) -> S:
        """
        Выполняет заданное действие.

        :param action: действие типа ThTriConsumer, которое принимает три контекста.
        :return: этот step context.
        :raises StepfatherException: если action равен None.
        """
        ...

    def with_(self, action: ThTriFunction[C1, C2, C3, R, Exception]) -> 'BaseTriCtxSC[R, C1, C2, Any]':
        """
        Выполняет заданное действие и возвращает новый step context.

        :param action: функция типа ThTriFunction, которая принимает три контекста и возвращает результат типа R.
        :return: новый BaseTriCtxSC с первым контекстом типа R и вторыми и третьими контекстами оставшимися.
        :raises StepfatherException: если action равен None.
        """
        ...

    def res(self, action: ThTriFunction[C1, C2, C3, R, Exception]) -> R:
        """
        Выполняет заданное действие и возвращает его результат.

        :param action: функция типа ThTriFunction, которая принимает три контекста и возвращает результат типа R.
        :return: результат выполнения action.
        :raises StepfatherException: если action равен None.
        """
        ...

    def map(self,
            action1: ThTriFunction[C1, C2, C3, R1, Exception],
            action2: ThTriFunction[C1, C2, C3, R2, Exception],
            action3: ThTriFunction[C1, C2, C3, R3, Exception]
            ) -> 'BaseTriCtxSC[R1, R2, R3, Any]':
        """
        Выполняет три действия и возвращает новый step context с обновлёнными контекстами.

        :param action1: функция для первого нового контекста.
        :param action2: функция для второго нового контекста.
        :param action3: функция для третьего нового контекста.
        :return: новый BaseTriCtxSC с контекстами типов R1, R2, R3.
        :raises StepfatherException: если хотя бы один из action равен None.
        """
        ...

    def context1(self) -> C1:
        """
        Возвращает первый контекст.
        """
        ...

    def context2(self) -> C2:
        """
        Возвращает второй контекст.
        """
        ...

    def context3(self) -> C3:
        """
        Возвращает третий контекст.
        """
        ...
