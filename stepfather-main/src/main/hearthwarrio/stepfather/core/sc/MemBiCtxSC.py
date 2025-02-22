from typing import Protocol, TypeVar, Generic, Any
from function.ThBiConsumer import ThBiConsumer, unchecked as th_unchecked_biconsumer
from function.ThBiFunction import ThBiFunction, unchecked as th_unchecked_bifunction
from function.ThConsumer import ThConsumer, unchecked as th_unchecked_consumer
from function.ThFunction import ThFunction, unchecked as th_unchecked_function
from core import StepfatherException
from base import StepContext
from base import BaseBiCtxSC
from base import MemSC

from sc import MemTriCtxSC
from sc import BiCtxSC
from sc import MemNoCtxSC

C1 = TypeVar('C1')
C2 = TypeVar('C2')
P = TypeVar('P', bound=StepContext[Any])
R = TypeVar('R')
R1 = TypeVar('R1')
R2 = TypeVar('R2')
S = TypeVar('S', bound='MemBiCtxSC[C1, C2, P]')

class MemBiCtxSC(BaseBiCtxSC[C1, C2, 'MemBiCtxSC[C1, C2, P]'], MemSC[P, BiCtxSC[C1, C2]], Protocol, Generic[C1, C2, P]):
    def exec(self, action: ThBiConsumer[C1, C2, Exception]) -> 'MemBiCtxSC[C1, C2, P]':
        """
        Выполняет заданное действие на context1 и context2.
        """
        ...

    def with_(self, action: ThBiFunction[C1, C2, R, Exception]) -> MemTriCtxSC[R, C1, C2, 'MemBiCtxSC[C1, C2, P]']:
        """
        Выполняет заданное действие и возвращает новый step context с тремя контекстами.
        """
        ...

    def res(self, action: ThBiFunction[C1, C2, R, Exception]) -> R:
        """
        Выполняет заданное действие и возвращает результат.
        """
        ...

    def it(self, action: ThConsumer['MemBiCtxSC[C1, C2, P]', Exception]) -> 'MemBiCtxSC[C1, C2, P]':
        """
        Выполняет заданное действие на этом step context.
        """
        ...

    def it_res(self, action: ThFunction['MemBiCtxSC[C1, C2, P]', R, Exception]) -> R:
        """
        Выполняет заданное действие на этом step context и возвращает результат.
        """
        ...

    def map(self,
            action1: ThBiFunction[C1, C2, R1, Exception],
            action2: ThBiFunction[C1, C2, R2, Exception]
            ) -> 'MemBiCtxSC[R1, R2, MemBiCtxSC[C1, C2, P]]':
        """
        Выполняет два действия и возвращает новый step context с обновлёнными контекстами.
        """
        ...

    def context1(self) -> C1:
        """
        Возвращает первый context.
        """
        ...

    def context2(self) -> C2:
        """
        Возвращает второй context.
        """
        ...

    def noContext(self) -> MemNoCtxSC['MemBiCtxSC[C1, C2, P]']:
        """
        Возвращает no context step context.
        """
        ...

    def previous(self) -> P:
        """
        Возвращает предыдущий step context.
        """
        ...

    def forget(self) -> BiCtxSC[C1, C2]:
        """
        Возвращает новый bi-context step context, забывая текущий.
        """
        ...

class MemBiCtxSCOf(MemBiCtxSC[C1, C2, P], Generic[C1, C2, P]):
    def __init__(self, context1: C1, context2: C2, previous: P) -> None:
        self._context1 = context1
        self._context2 = context2
        self._previous = previous

    def exec(self, action: ThBiConsumer[C1, C2, Exception]) -> 'MemBiCtxSCOf[C1, C2, P]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_biconsumer(action).accept(self._context1, self._context2)
        return self

    def with_(self, action: ThBiFunction[C1, C2, R, Exception]) -> MemTriCtxSC[R, C1, C2, 'MemBiCtxSCOf[C1, C2, P]']:
        if action is None:
            raise StepfatherException("action arg is null")
        result = th_unchecked_bifunction(action).apply(self._context1, self._context2)
        return MemTriCtxSC.MemTriCtxSCOf(result, self._context1, self._context2, self)

    def res(self, action: ThBiFunction[C1, C2, R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_bifunction(action).apply(self._context1, self._context2)

    def it(self, action: ThConsumer['MemBiCtxSCOf[C1, C2, P]', Exception]) -> 'MemBiCtxSCOf[C1, C2, P]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_consumer(action).accept(self)
        return self

    def it_res(self, action: ThFunction['MemBiCtxSCOf[C1, C2, P]', R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_function(action).apply(self)

    def map(self,
            action1: ThBiFunction[C1, C2, R1, Exception],
            action2: ThBiFunction[C1, C2, R2, Exception]
            ) -> 'MemBiCtxSCOf[R1, R2, MemBiCtxSCOf[C1, C2, P]]':
        if action1 is None:
            raise StepfatherException("action1 arg is null")
        if action2 is None:
            raise StepfatherException("action2 arg is null")
        new_c1 = th_unchecked_bifunction(action1).apply(self._context1, self._context2)
        new_c2 = th_unchecked_bifunction(action2).apply(self._context1, self._context2)
        return MemBiCtxSCOf(new_c1, new_c2, self)

    def context1(self) -> C1:
        return self._context1

    def context2(self) -> C2:
        return self._context2

    def noContext(self) -> MemNoCtxSC['MemBiCtxSCOf[C1, C2, P]']:
        return MemNoCtxSC.MemNoCtxSCOf(self)

    def previous(self) -> P:
        return self._previous

    def forget(self) -> BiCtxSC[C1, C2]:
        from sc import BiCtxSC
        return BiCtxSC.BiCtxSCOf(self._context1, self._context2)
