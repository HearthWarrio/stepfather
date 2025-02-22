from typing import Protocol, TypeVar, Generic, Any
from sc.base import StepContext
from sc.base import BaseAnyCtxSC
from sc.base import BaseBiCtxSC
from function.ThConsumer import ThConsumer
from function.ThFunction import ThFunction
from core import StepfatherException

C = TypeVar('C')
S = TypeVar('S', bound='BaseCtxSC')
R = TypeVar('R')


class BaseCtxSC(StepContext[S], BaseAnyCtxSC[S], Protocol, Generic[C, S]):
    def exec(self, action: ThConsumer[C, Exception]) -> S:
        """
        Executes given action.

        :param action: действие, принимающее контекст типа C.
        :return: этот step context.
        :raises StepfatherException: если action равен None.
        """
        ...

    def with_(self, action: ThFunction[C, R, Exception]) -> BaseBiCtxSC[R, C, Any]:
        """
        Executes given action and returns new context step context.

        :param action: функция, принимающая контекст типа C и возвращающая новый контекст типа R.
        :return: новый BaseBiCtxSC с контекстом R.
        :raises StepfatherException: если action равен None.
        """
        ...

    def res(self, action: ThFunction[C, R, Exception]) -> R:
        """
        Executes given action and returns action result.

        :param action: функция, принимающая контекст типа C и возвращающая результат типа R.
        :return: результат выполнения action.
        :raises StepfatherException: если action равен None.
        """
        ...

    def map(self, action: ThFunction[C, R, Exception]) -> 'BaseCtxSC[R, Any]':
        """
        Executes given action and returns new context step context.

        :param action: функция, принимающая контекст типа C и возвращающая новый контекст типа R.
        :return: новый BaseCtxSC с контекстом R.
        :raises StepfatherException: если action равен None.
        """
        ...

    def context(self) -> C:
        """
        Returns the context.

        :return: контекст типа C.
        """
        ...
