from typing import Protocol, TypeVar, Optional

R = TypeVar('R')

class ThSupplier(Protocol[R]):
    def get(self) -> R:
        """
        Gets the result.
        May raise an exception.
        """
        ...

def unchecked(supplier: Optional[ThSupplier[R]]) -> Optional[ThSupplier[R]]:
    """
    Returns the given ThSupplier as unchecked, or None if supplier is None.
    """
    return supplier
