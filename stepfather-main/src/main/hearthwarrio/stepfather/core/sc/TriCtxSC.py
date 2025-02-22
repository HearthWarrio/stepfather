from typing import Protocol, TypeVar, Generic, Any
from function.ThTriConsumer import ThTriConsumer, unchecked as th_unchecked_triconsumer
from function.ThTriFunction import ThTriFunction, unchecked as th_unchecked_trifunction
from function.ThConsumer import ThConsumer, unchecked as th_unchecked_consumer
from function.ThFunction import ThFunction, unchecked as th_unchecked_function
from core import StepfatherException
from base import StepContext
from base import BaseTriCtxSC
from sc import MemNoCtxSC
from sc import MemTriCtxSC

C1 = TypeVar('C1')
C2 = TypeVar('C2')
C3 = TypeVar('C3')
R = TypeVar('R')
R1 = TypeVar('R1')
R2 = TypeVar('R2')
R3 = TypeVar('R3')
S = TypeVar('S', bound='TriCtxSC[C1, C2, C3]')

class TriCtxSC(BaseTriCtxSC[C1, C2, C3, 'TriCtxSC[C1, C2, C3]'], Protocol, Generic[C1, C2, C3]):
    def exec(self, action: ThTriConsumer[C1, C2, C3, Exception]) -> 'TriCtxSC[C1, C2, C3]':
        """
        Выполняет заданное действие.
        :raises StepfatherException: если action равен None.
        """
        ...

    def with_(self, action: ThTriFunction[C1, C2, C3, R, Exception]) -> MemTriCtxSC[R, C1, C2, 'TriCtxSC[C1, C2, C3]']:
        """
        Выполняет заданное действие и возвращает новый step context.
        :raises StepfatherException: если action равен None.
        """
        ...

    def res(self, action: ThTriFunction[C1, C2, C3, R, Exception]) -> R:
        """
        Выполняет заданное действие и возвращает его результат.
        :raises StepfatherException: если action равен None.
        """
        ...

    def it(self, action: ThConsumer['TriCtxSC[C1, C2, C3]', Exception]) -> 'TriCtxSC[C1, C2, C3]':
        """
        Выполняет заданное действие на этом step context.
        :raises StepfatherException: если action равен None.
        """
        ...

    def it_res(self, action: ThFunction['TriCtxSC[C1, C2, C3]', R, Exception]) -> R:
        """
        Выполняет заданное действие на этом step context и возвращает результат.
        :raises StepfatherException: если action равен None.
        """
        ...

    def map(self,
            action1: ThTriFunction[C1, C2, C3, R1, Exception],
            action2: ThTriFunction[C1, C2, C3, R2, Exception],
            action3: ThTriFunction[C1, C2, C3, R3, Exception]
            ) -> MemTriCtxSC[R1, R2, R3, 'TriCtxSC[C1, C2, C3]']:
        """
        Выполняет три действия и возвращает новый step context с обновлёнными контекстами.
        :raises StepfatherException: если любой из action равен None.
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

    def noContext(self) -> MemNoCtxSC['TriCtxSC[C1, C2, C3]']:
        """
        Возвращает no context step context.
        """
        ...

class TriCtxSCOf(Generic[C1, C2, C3], TriCtxSC[C1, C2, C3]):
    def __init__(self, context1: C1, context2: C2, context3: C3) -> None:
        self._context1 = context1
        self._context2 = context2
        self._context3 = context3

    def exec(self, action: ThTriConsumer[C1, C2, C3, Exception]) -> 'TriCtxSCOf[C1, C2, C3]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_triconsumer(action).accept(self._context1, self._context2, self._context3)
        return self

    def with_(self, action: ThTriFunction[C1, C2, C3, R, Exception]) -> MemTriCtxSC[R, C1, C2, 'TriCtxSCOf[C1, C2, C3]']:
        if action is None:
            raise StepfatherException("action arg is null")
        result = th_unchecked_trifunction(action).apply(self._context1, self._context2, self._context3)
        return MemTriCtxSC.MemTriCtxSCOf(result, self._context1, self._context2, self._context3, self)

    def res(self, action: ThTriFunction[C1, C2, C3, R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_trifunction(action).apply(self._context1, self._context2, self._context3)

    def it(self, action: ThConsumer['TriCtxSCOf[C1, C2, C3]', Exception]) -> 'TriCtxSCOf[C1, C2, C3]':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_consumer(action).accept(self)
        return self

    def it_res(self, action: ThFunction['TriCtxSCOf[C1, C2, C3]', R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_function(action).apply(self)

    def map(self,
            action1: ThTriFunction[C1, C2, C3, R1, Exception],
            action2: ThTriFunction[C1, C2, C3, R2, Exception],
            action3: ThTriFunction[C1, C2, C3, R3, Exception]
            ) -> MemTriCtxSC[R1, R2, R3, 'TriCtxSCOf[C1, C2, C3]']:
        if action1 is None:
            raise StepfatherException("action1 arg is null")
        if action2 is None:
            raise StepfatherException("action2 arg is null")
        if action3 is None:
            raise StepfatherException("action3 arg is null")
        new_c1 = th_unchecked_trifunction(action1).apply(self._context1, self._context2, self._context3)
        new_c2 = th_unchecked_trifunction(action2).apply(self._context1, self._context2, self._context3)
        new_c3 = th_unchecked_trifunction(action3).apply(self._context1, self._context2, self._context3)
        return MemTriCtxSC.MemTriCtxSCOf(new_c1, new_c2, new_c3, self)

    def context1(self) -> C1:
        return self._context1

    def context2(self) -> C2:
        return self._context2

    def context3(self) -> C3:
        return self._context3

    def noContext(self) -> MemNoCtxSC['TriCtxSCOf[C1, C2, C3]']:
        return MemNoCtxSC.MemNoCtxSCOf(self)
