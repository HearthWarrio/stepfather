from typing import Protocol, TypeVar, Generic
from base import StepContext
from sc import MemNoCtxSC

S = TypeVar('S', bound='BaseAnyCtxSC')

class BaseAnyCtxSC(StepContext, Protocol, Generic[S]):
    def noContext(self) -> MemNoCtxSC[S]:
        """
        Возвращает no context step context.
        """
        ...
