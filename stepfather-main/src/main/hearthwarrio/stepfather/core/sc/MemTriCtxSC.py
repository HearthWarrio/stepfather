from typing import Protocol, TypeVar, Generic, Any
from function.ThTriConsumer import ThTriConsumer, unchecked as th_unchecked_triconsumer
from function.ThTriFunction import ThTriFunction, unchecked as th_unchecked_trifunction
from function.ThConsumer import ThConsumer, unchecked as th_unchecked_consumer
from function.ThFunction import ThFunction, unchecked as th_unchecked_function
from core import StepfatherException
from base import StepContext
from base import BaseTriCtxSC
from base import MemSC

from sc import TriCtxSC
from sc import MemNoCtxSC

C1 = TypeVar('C1')
C2 = TypeVar('C2')
C3 = TypeVar('C3')
P = TypeVar('P', bound=StepContext[Any])
R = TypeVar('R')
R1 = TypeVar('R1')
R2 = TypeVar('R2')
R3 = TypeVar('R3')
S = TypeVar('S', bound='MemTriCtxSC[C1, C2, C3, P]')

class MemTriCtxSC(BaseTriCtxSC[C1, C2, C3, 'MemTriCtxSC[C1, C2, C3, P]'], MemSC[P, TriCtxSC[C1, C2, C3]], Protocol, Generic[C1, C2, C3, P]):
    def exec(self, action: ThTriConsumer[C1, C2, C3, Exception]) -> 'MemTriCtxSC[C1, C2, C3, P]':
        """
        Выполняет заданное действие на трёх контекстах.
        """
        ...

    def with_(self, action: ThTriFunction[C1, C2, C3, R, Exception]) -> 'MemTriCtxSC[R, C1, C2, MemTriCtxSC[C1, C2, C3, P]]':
        """
        Выполняет заданное действие и возвращает новый триконтекстный step context.
        """
        ...

    def res(self, action: ThTriFunction[C1, C2, C3, R, Exception]) -> R:
        """
        Выполняет заданное действие и возвращает результат.
        """
        ...

    def it(self, action: ThConsumer['MemTriCtxSC[C1, C2, C3, P]', Exception]) -> 'MemTriCtxSC[C1, C2, C3, P]':
        """
        Выполняет заданное действие на этом step context.
        """
        ...

    def it_res(self, action: ThFunction['MemTriCtxSC[C1, C2, C3, P]', R, Exception]) -> R:
        """
        Выполняет заданное действие на этом step context и возвращает результат.
        """
        ...

    def map(self,
            action1: ThTriFunction[C1, C2, C3, R1, Exception],
            action2: ThTriFunction[C1, C2, C3, R2, Exception],
            action3: ThTriFunction[C1, C2, C3, R3, Exception]
            ) -> 'MemTriCtxSC[R1, R2, R3, MemTriCtxSC[C1, C2, C3, P]]':
        """
        Выполняет три действия и возвращает новый триконтекстный step context с обновлёнными контекстами.
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

    def noContext(self) -> MemNoCtxSC['MemTriCtxSC[C1, C2, C3, P]']:
        """
        Возвращает no context step context.
        """
        ...

    def previous(self) -> P:
        """
        Возвращает предыдущий step context.
        """
        ...

    def forget(self) -> TriCtxSC[C1, C2, C3]:
        """
        Возвращает новый tri-context step context, забывая текущий.
        """
        ...

class MemTriCtxSCOf(MemTriCtxSC[C1, C2, C3, P], Generic[C1, C2, C3, P]):
    def __init__(self, context1: C1, context2: C2, context3: C3, previous: P) -> None:
        self._context1 = context1
        self._context2 = context2
        self._context3 = context3
        self._previous = previous

    def exec(self, action: ThTriConsumer[C1, C2, C3, Exception]) -> 'MemTriCtxSCOf[C1, C2, C3, P]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_triconsumer(action).accept(self._context1, self._context2, self._context3)
        return self

    def with_(self, action: ThTriFunction[C1, C2, C3, R, Exception]) -> 'MemTriCtxSCOf[R, C2, C3, MemTriCtxSCOf[C1, C2, C3, P]]':
        if action is None:
            raise StepfatherException("action arg is null")
        result = th_unchecked_trifunction(action).apply(self._context1, self._context2, self._context3)
        return MemTriCtxSCOf(result, self._context1, self._context2, self)

    def res(self, action: ThTriFunction[C1, C2, C3, R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_trifunction(action).apply(self._context1, self._context2, self._context3)

    def it(self, action: ThConsumer['MemTriCtxSCOf[C1, C2, C3, P]', Exception]) -> 'MemTriCtxSCOf[C1, C2, C3, P]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_consumer(action).accept(self)
        return self

    def it_res(self, action: ThFunction['MemTriCtxSCOf[C1, C2, C3, P]', R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_function(action).apply(self)

    def map(self,
            action1: ThTriFunction[C1, C2, C3, R1, Exception],
            action2: ThTriFunction[C1, C2, C3, R2, Exception],
            action3: ThTriFunction[C1, C2, C3, R3, Exception]
           ) -> 'MemTriCtxSCOf[R1, R2, R3, MemTriCtxSCOf[C1, C2, C3, P]]':
        if action1 is None:
            raise StepfatherException("action1 arg is null")
        if action2 is None:
            raise StepfatherException("action2 arg is null")
        if action3 is None:
            raise StepfatherException("action3 arg is null")
        new_c1 = th_unchecked_trifunction(action1).apply(self._context1, self._context2, self._context3)
        new_c2 = th_unchecked_trifunction(action2).apply(self._context1, self._context2, self._context3)
        new_c3 = th_unchecked_trifunction(action3).apply(self._context1, self._context2, self._context3)
        return MemTriCtxSCOf(new_c1, new_c2, new_c3, self)

    def context1(self) -> C1:
        return self._context1

    def context2(self) -> C2:
        return self._context2

    def context3(self) -> C3:
        return self._context3

    def noContext(self) -> 'MemNoCtxSC[MemTriCtxSCOf[C1, C2, C3, P]]':
        return MemNoCtxSC.MemNoCtxSCOf(self)

    def previous(self) -> P:
        return self._previous

    def forget(self) -> 'TriCtxSC[C1, C2, C3]':
        from sc import TriCtxSC
        return TriCtxSC.TriCtxSCOf(self._context1, self._context2, self._context3)
