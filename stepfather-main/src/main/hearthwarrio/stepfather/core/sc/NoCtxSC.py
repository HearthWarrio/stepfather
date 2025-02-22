from typing import Protocol, TypeVar, Generic, Any
from function.ThRunnable import ThRunnable, unchecked as th_unchecked_runnable
from function.ThSupplier import ThSupplier, unchecked as th_unchecked_supplier
from function.ThConsumer import ThConsumer, unchecked as th_unchecked_consumer
from function.ThFunction import ThFunction, unchecked as th_unchecked_function
from core import StepfatherException
from base import BaseNoCtxSC
from sc import CtxSC

R = TypeVar('R')
S = TypeVar('S', bound='NoCtxSC')


class NoCtxSC(BaseNoCtxSC['NoCtxSC'], Protocol):
    def exec(self, action: ThRunnable[Exception]) -> 'NoCtxSC':
        """
        Выполняет заданное действие.
        :raises StepfatherException: если action равен None.
        """
        ...

    def with_(self, action: ThSupplier[R, Exception]) -> CtxSC[R]:
        """
        Выполняет заданное действие и возвращает новый контекст шага.
        :raises StepfatherException: если action равен None.
        """
        ...

    def res(self, action: ThSupplier[R, Exception]) -> R:
        """
        Выполняет заданное действие и возвращает результат.
        :raises StepfatherException: если action равен None.
        """
        ...

    def it(self, action: ThConsumer['NoCtxSC', Exception]) -> 'NoCtxSC':
        """
        Выполняет заданное действие над этим контекстом.
        :raises StepfatherException: если action равен None.
        """
        ...

    def it_res(self, action: ThFunction['NoCtxSC', R, Exception]) -> R:
        """
        Выполняет заданное действие над этим контекстом и возвращает результат.
        :raises StepfatherException: если action равен None.
        """
        ...

    @staticmethod
    def instance() -> 'NoCtxSC':
        """
        Возвращает единственный экземпляр NoCtxSC.
        """
        ...


class NoCtxSCOf(NoCtxSC):
    _instance: 'NoCtxSCOf' = None

    def __new__(cls) -> 'NoCtxSCOf':
        if cls._instance is None:
            cls._instance = super(NoCtxSCOf, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        pass

    def exec(self, action: ThRunnable[Exception]) -> 'NoCtxSCOf':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_runnable(action).run()
        return self

    def with_(self, action: ThSupplier[R, Exception]) -> CtxSC[R]:
        if action is None:
            raise StepfatherException("action arg is null")
        result = th_unchecked_supplier(action).get()
        return CtxSC.CtxSCOf(result)

    def res(self, action: ThSupplier[R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_supplier(action).get()

    def it(self, action: ThConsumer['NoCtxSC', Exception]) -> 'NoCtxSCOf':
        if action is None:
            raise StepfatherException("action arg is null")
        th_unchecked_consumer(action).accept(self)
        return self

    def it_res(self, action: ThFunction['NoCtxSC', R, Exception]) -> R:
        if action is None:
            raise StepfatherException("action arg is null")
        return th_unchecked_function(action).apply(self)

    @staticmethod
    def instance() -> 'NoCtxSC':
        return NoCtxSCOf()