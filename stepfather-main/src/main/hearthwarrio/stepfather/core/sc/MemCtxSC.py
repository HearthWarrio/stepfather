from typing import Protocol, TypeVar, Generic, Any

from function.ThConsumer import ThConsumer, unchecked as th_unchecked_consumer
from function.ThFunction import ThFunction, unchecked as th_unchecked_function
from function.ThRunnable import ThRunnable, unchecked as th_unchecked_runnable
from function.ThSupplier import ThSupplier, unchecked as th_unchecked_supplier
from core import StepfatherException
from sc.base import StepContext
from sc.base import BaseCtxSC
from base import MemSC
from sc import MemBiCtxSC
from sc import CtxSC
from sc import MemNoCtxSC

C = TypeVar('C')
P = TypeVar('P', bound=StepContext[Any])
S = TypeVar('S', bound='MemCtxSC[C, P]')
R = TypeVar('R')

class MemCtxSC(BaseCtxSC[C, 'MemCtxSC[C, P]'], MemSC[P, CtxSC[C]], Protocol, Generic[C, P]):
    """
    Memorizing single context step context.
    """
    def with_(self, action: ThFunction[C, R, Exception]) -> MemBiCtxSC[R, C, 'MemCtxSC[C, P]']:
        """
        Выполняет заданное действие и возвращает новый context с двумя контекстами.
        :raises StepfatherException: если action равен None.
        """
        ...

    def map(self, action: ThFunction[C, R, Exception]) -> 'MemCtxSC[C, P]':
        """
        Выполняет заданное действие и возвращает новый context (отображённый).
        :raises StepfatherException: если action равен None.
        """
        ...

class MemCtxSCOf(MemCtxSC[C, P], Generic[C, P]):
    def __init__(self, context: C, previous: P) -> None:
        self._context = context
        self._previous = previous

    def exec(self, action: ThConsumer[C, Exception]) -> 'MemCtxSCOf[C, P]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_consumer(action).accept(self._context)
        return self

    def with_(self, action: ThFunction[C, R, Exception]) -> 'MemBiCtxSCOf[R, C, MemCtxSCOf[C, P]]':
        if action is None:
            raise StepfatherException("action arg is null")
        result = th_unchecked_function(action).apply(self._context)
        return MemBiCtxSC.MemBiCtxSCOf(result, self._context, self)

    def res(self, action: ThFunction[C, R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_function(action).apply(self._context)

    def it(self, action: ThConsumer['MemCtxSCOf[C, P]', Exception]) -> 'MemCtxSCOf[C, P]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_consumer(action).accept(self)
        return self

    def it_res(self, action: ThFunction['MemCtxSCOf[C, P]', R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_function(action).apply(self)

    def map(self, action: ThFunction[C, R, Exception]) -> 'MemCtxSCOf[R, MemCtxSCOf[C, P]]':
        if action is None:
            raise StepfatherException("action arg is null")
        new_context = th_unchecked_function(action).apply(self._context)
        return MemCtxSCOf(new_context, self)

    def context(self) -> C:
        return self._context

    def noContext(self) -> 'MemNoCtxSC[MemCtxSCOf[C, P]]':
        return MemNoCtxSC.MemNoCtxSCOf(self)

    def previous(self) -> P:
        return self._previous

    def forget(self) -> CtxSC[C]:
        return CtxSC.Of(self._context)

