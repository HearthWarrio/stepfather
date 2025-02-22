from abc import abstractmethod
from typing import Generic, Protocol, TypeVar
from hearthwarrio.stepfather.core.function.ThConsumer import ThConsumer
from hearthwarrio.stepfather.core.function.ThFunction import ThFunction

S = TypeVar('S', bound='StepContext')
R = TypeVar('R')

class StepContext(Protocol, Generic[S]):
    @abstractmethod
    def it(self, action: 'ThConsumer[S, Exception]') -> S:
        """
        Выполняет заданное действие на этом step context.
        Может выбрасывать StepfatherException, если action равен None.
        """
        pass

    @abstractmethod
    def it_res(self, action: 'ThFunction[S, R, Exception]') -> 'R':
        """
        Выполняет заданное действие на этом step context и возвращает результат.
        Может выбрасывать StepfatherException, если action равен None.
        """
        pass
