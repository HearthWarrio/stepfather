from typing import Protocol, TypeVar, Generic, Any
from base import StepContext
from base import BaseNoCtxSC
from base import MemSC
from sc import NoCtxSC
from sc import MemCtxSC
from function.ThRunnable import ThRunnable, unchecked as th_unchecked_runnable
from function.ThSupplier import ThSupplier, unchecked as th_unchecked_supplier
from function.ThConsumer import ThConsumer, unchecked as th_unchecked_consumer
from function.ThFunction import ThFunction, unchecked as th_unchecked_function
from core import StepfatherException

P = TypeVar('P', bound=StepContext[Any])
S = TypeVar('S', bound='MemNoCtxSC[P]')
R = TypeVar('R')
R1 = TypeVar('R1')
R2 = TypeVar('R2')


class MemNoCtxSC(BaseNoCtxSC['MemNoCtxSC[P]'], MemSC[P, NoCtxSC], Protocol, Generic[P]):
    """
    Memorizing no context step context.

    :param P: тип предыдущего шага (StepContext)
    """

    def with_(self, action: ThSupplier[R, Exception]) -> MemCtxSC[R, P]:
        """
        Выполняет заданное действие и возвращает новый context с запоминающимся контекстом.

        :param action: ThSupplier, который может выбрасывать исключение.
        :return: новый MemCtxSC с результатом типа R и предыдущим контекстом типа P.
        :raises StepfatherException: если action равен None.
        """
        ...

    def instance(previous: P) -> 'MemNoCtxSC[P]':
        return MemNoCtxSCOf(previous)


class MemNoCtxSCOf(MemNoCtxSC[P], Generic[P]):
    """
    Стандартная реализация MemNoCtxSC.
    """
    def __init__(self, previous: P) -> None:
        self._previous = previous

    def exec(self, action: ThRunnable[Exception]) -> 'MemNoCtxSC[P]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_runnable(action).run()
        return self

    def with_(self, action: ThSupplier[R, Exception]) -> MemCtxSC[R, P]:
        if action is None:
            raise StepfatherException("action arg is null")
        result = th_unchecked_supplier(action).get()
        return MemCtxSC.MemCtxSCOf(result, self._previous)

    def res(self, action: ThSupplier[R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_supplier(action).get()

    def it(self, action: ThConsumer['MemNoCtxSC[P]', Exception]) -> 'MemNoCtxSC[P]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_consumer(action).accept(self)
        return self

    def it_res(self, action: ThFunction['MemNoCtxSC[P]', R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_function(action).apply(self)

    def previous(self) -> P:
        return self._previous

    def forget(self) -> NoCtxSC:
        return NoCtxSC.NoCtxSCOf.instance()
