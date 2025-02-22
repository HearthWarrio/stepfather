from typing import Protocol, TypeVar, runtime_checkable, Any
from hearthwarrio.stepfather.core.sc.base import StepContext
from hearthwarrio.stepfather.core.sc.base import BaseAnyCtxSC
from hearthwarrio.stepfather.core.sc.base import BaseTriCtxSC
from hearthwarrio.stepfather.core.function.ThBiConsumer import ThBiConsumer
from hearthwarrio.stepfather.core.function.ThBiFunction import ThBiFunction
from hearthwarrio.stepfather.core import StepfatherException

C1 = TypeVar('C1')
C2 = TypeVar('C2')
S = TypeVar('S', bound='BaseBiCtxSC[C1, C2, S]')
R = TypeVar('R')
R1 = TypeVar('R1')
R2 = TypeVar('R2')

@runtime_checkable
class BaseBiCtxSC(StepContext[S], BaseAnyCtxSC[S], Protocol[C1, C2, S]):
    def exec(self, action: ThBiConsumer[C1, C2, Exception]) -> S:
        """
        Выполняет заданное действие.
        :raises StepfatherException: если action равен None.
        """
        ...

    def with_(self, action: ThBiFunction[C1, C2, R, Exception]) -> BaseTriCtxSC[R, C1, C2, Exception]:
        """
        Выполняет заданное действие и возвращает новый контекст шага.
        :raises StepfatherException: если action равен None.
        """
        ...

    def res(self, action: ThBiFunction[C1, C2, R, Exception]) -> R:
        """
        Выполняет заданное действие и возвращает его результат.
        :raises StepfatherException: если action равен None.
        """
        ...

    def map(self,
            action1: ThBiFunction[C1, C2, R1, Exception],
            action2: ThBiFunction[C1, C2, R2, Exception]
            ) -> 'BaseBiCtxSC[R1, R2, Any]':
        """
        Выполняет два действия и возвращает новый контекст шага.
        :raises StepfatherException: если action1 или action2 равны None.
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
