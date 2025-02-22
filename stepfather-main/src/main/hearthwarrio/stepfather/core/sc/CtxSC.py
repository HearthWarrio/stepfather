from typing import Protocol, TypeVar, Generic, Any
from function.ThConsumer import ThConsumer, unchecked as th_unchecked_consumer
from function.ThFunction import ThFunction, unchecked as th_unchecked_function
from core import StepfatherException
from base import BaseCtxSC
from sc import MemBiCtxSC
from sc import MemCtxSC
from sc import MemNoCtxSC

C = TypeVar('C')
R = TypeVar('R')
S = TypeVar('S', bound='CtxSC')

class CtxSC(BaseCtxSC[C, 'CtxSC[C]'], Protocol, Generic[C]):
    """
    Single context step context.
    """

    def with_(self, action: ThFunction[C, R, Exception]) -> MemBiCtxSC[R, C, 'CtxSC[C]']:
        """
        Выполняет заданное действие и возвращает новый контекст шага с двумя контекстами.
        :raises StepfatherException: если action равен None.
        """
        ...

    def map(self, action: ThFunction[C, R, Exception]) -> MemCtxSC[R, 'CtxSC[C]']:
        """
        Выполняет заданное действие и возвращает новый контекст шага.
        :raises StepfatherException: если action равен None.
        """
        ...

class CtxSCOf(Generic[C], CtxSC[C]):
    """
    Стандартная реализация CtxSC.
    """

    def __init__(self, context: C) -> None:
        self._context = context

    def exec(self, action: ThConsumer[C, Exception]) -> 'CtxSCOf[C]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_consumer(action).accept(self._context)
        return self

    def with_(self, action: ThFunction[C, R, Exception]) -> MemBiCtxSC[R, C, 'CtxSCOf[C]']:
        if action is None:
            raise StepfatherException("action arg is null")
        result = th_unchecked_function(action).apply(self._context)
        return MemBiCtxSC.MemBiCtxSCOf(result, self._context, self)

    def res(self, action: ThFunction[C, R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_function(action).apply(self._context)

    def it(self, action: ThConsumer['CtxSC[C]', Exception]) -> 'CtxSCOf[C]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_consumer(action).accept(self)
        return self

    def it_res(self, action: ThFunction['CtxSC[C]', R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_function(action).apply(self)

    def map(self, action: ThFunction[C, R, Exception]) -> MemCtxSC[R, 'CtxSCOf[C]']:
        if action is None:
            raise StepfatherException("action arg is null")
        new_context = th_unchecked_function(action).apply(self._context)
        return MemCtxSC.MemCtxSCOf(new_context, self)

    def context(self) -> C:
        return self._context

    def noContext(self) -> 'MemNoCtxSC[CtxSCOf[C]]':
        return MemNoCtxSC.MemNoCtxSCOf(self)