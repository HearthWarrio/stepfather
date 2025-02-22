from typing import Protocol, TypeVar, Generic, Any
from function.ThBiConsumer import ThBiConsumer, unchecked as th_unchecked_biconsumer
from function.ThBiFunction import ThBiFunction, unchecked as th_unchecked_bifunction
from function.ThConsumer import ThConsumer, unchecked as th_unchecked_consumer
from function.ThFunction import ThFunction, unchecked as th_unchecked_function
from core import StepfatherException
from base import BaseBiCtxSC
from sc import MemNoCtxSC
from sc import MemTriCtxSC
from sc import MemBiCtxSC

C1 = TypeVar('C1')
C2 = TypeVar('C2')
R = TypeVar('R')
R1 = TypeVar('R1')
R2 = TypeVar('R2')


class BiCtxSC(BaseBiCtxSC[C1, C2, 'BiCtxSC[C1, C2]'], Protocol, Generic[C1, C2]):
    def with_(self, action: ThBiFunction[C1, C2, R, Exception]) -> MemTriCtxSC[R, C1, C2, 'BiCtxSC[C1, C2]']:
        """
        Выполняет заданное действие и возвращает новый триконтекстный step context.
        :raises StepfatherException: если action равен None.
        """
        ...

    def map(self,
            action1: ThBiFunction[C1, C2, R1, Exception],
            action2: ThBiFunction[C1, C2, R2, Exception]) -> MemBiCtxSC[R1, R2, 'BiCtxSC[C1, C2]']:
        """
        Выполняет два действия и возвращает новый запоминающий би-контекстный step context.
        :raises StepfatherException: если любой из action равен None.
        """
        ...

    def exec(self, action: ThBiConsumer[C1, C2, Exception]) -> 'BiCtxSC[C1, C2]':
        ...

    def res(self, action: ThBiFunction[C1, C2, R, Exception]) -> R:
        ...

    def it(self, action: ThConsumer['BiCtxSC[C1, C2]', Exception]) -> 'BiCtxSC[C1, C2]':
        ...

    def it_res(self, action: ThFunction['BiCtxSC[C1, C2]', R, Exception]) -> R:
        ...

    def context1(self) -> C1:
        ...

    def context2(self) -> C2:
        ...

    def noContext(self) -> MemNoCtxSC['BiCtxSC[C1, C2]']:
        ...


class BiCtxSCOf(Generic[C1, C2], BiCtxSC[C1, C2]):
    def __init__(self, context1: C1, context2: C2) -> None:
        self._context1 = context1
        self._context2 = context2

    def exec(self, action: ThBiConsumer[C1, C2, Exception]) -> 'BiCtxSCOf[C1, C2]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_biconsumer(action).accept(self._context1, self._context2)
        return self

    def with_(self, action: ThBiFunction[C1, C2, R, Exception]) -> MemTriCtxSC[R, C1, C2, 'BiCtxSCOf[C1, C2]']:
        if action is None:
            raise StepfatherException("action arg is null")
        result = th_unchecked_bifunction(action).apply(self._context1, self._context2)
        return MemTriCtxSC.MemTriCtxSCOf(result, self._context1, self._context2, self)

    def res(self, action: ThBiFunction[C1, C2, R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_bifunction(action).apply(self._context1, self._context2)

    def it(self, action: ThConsumer['BiCtxSCOf[C1, C2]', Exception]) -> 'BiCtxSCOf[C1, C2]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_consumer(action).accept(self)
        return self

    def it_res(self, action: ThFunction['BiCtxSCOf[C1, C2]', R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_function(action).apply(self)

    def map(self,
            action1: ThBiFunction[C1, C2, R1, Exception],
            action2: ThBiFunction[C1, C2, R2, Exception]) -> MemBiCtxSC[R1, R2, 'BiCtxSCOf[C1, C2]']:
        if action1 is None:
            raise StepfatherException("action1 arg is null")
        if action2 is None:
            raise StepfatherException("action2 arg is null")
        new_c1 = th_unchecked_bifunction(action1).apply(self._context1, self._context2)
        new_c2 = th_unchecked_bifunction(action2).apply(self._context1, self._context2)
        return MemBiCtxSC.MemBiCtxSCOf(new_c1, new_c2, self)

    def context1(self) -> C1:
        return self._context1

    def context2(self) -> C2:
        return self._context2

    def noContext(self) -> MemNoCtxSC['BiCtxSCOf[C1, C2]']:
        from sc.MemNoCtxSC import MemNoCtxSCOf
        return MemNoCtxSCOf(self)
