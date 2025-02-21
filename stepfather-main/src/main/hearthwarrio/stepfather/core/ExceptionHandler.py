import threading
import traceback
from abc import abstractmethod, ABC
from collections import deque
from typing import Set, Deque, Any, TypeVar
import StepfatherException

class ExceptionHandler(ABC):
    @abstractmethod
    def handle(self, exception: BaseException) -> None:
        """
        Handles given exception.
        Raises StepfatherException if exception arg is null.
        """
        pass

T = TypeVar('T')

class FixedMaxSizeUniqueQueue:
    """
    Очередь фиксированного размера с уникальными элементами.
    Если очередь достигает max_size, самый старый элемент удаляется.
    """
    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.queue = deque()
        self.set = set()

    def offer(self, element: Any) -> bool:
        if element not in self.set:
            self.queue.append(element)
            self.set.add(element)
            if len(self.set) == self.max_size:
                oldest = self.queue.popleft()
                self.set.remove(oldest)
            return True
        return False

class CleanStackTrace(ExceptionHandler):
    """
    Реализация ExceptionHandler, которая рекурсивно обходит все связанные исключения,
    очищает их стек вызовов (удаляет строки, начинающиеся с заданного префикса) и сохраняет
    результат в атрибуте cleaned_traceback.
    """
    def __init__(self):
        # Префикс для фильтрации строк стека вызовов
        stepfather_class_prefix = "hearthwarrio"
        self.cached_exceptions = threading.local()  # thread-local для хранения очереди
        self.clean_stack_trace_element_filter = lambda frame: not frame.filename.startswith(stepfather_class_prefix)

    def handle(self, exception: BaseException) -> None:
        if exception is None:
            raise StepfatherException("exception arg is null")
        all_related_exceptions: Set[BaseException] = set()
        self.recursively_add_all_related_exceptions(all_related_exceptions, exception)
        for current_ex in all_related_exceptions:
            # Если исключение не является StepfatherException и добавляется в кэш
            if not isinstance(current_ex, StepfatherException) and self.offer_cached_exception(current_ex):
                if current_ex.__traceback__ is not None:
                    tb_list = traceback.extract_tb(current_ex.__traceback__)
                    clean_tb_list = [frame for frame in tb_list if self.clean_stack_trace_element_filter(frame)]
                    if len(clean_tb_list) != len(tb_list):
                        current_ex.cleaned_traceback = clean_tb_list

    def recursively_add_all_related_exceptions(self, exceptions: Set[BaseException], main_ex: BaseException) -> None:
        if main_ex in exceptions:
            return
        exceptions.add(main_ex)
        if main_ex.__cause__:
            self.recursively_add_all_related_exceptions(exceptions, main_ex.__cause__)
        if main_ex.__context__:
            self.recursively_add_all_related_exceptions(exceptions, main_ex.__context__)

    def offer_cached_exception(self, exception: BaseException) -> bool:
        if not hasattr(self.cached_exceptions, 'queue'):
            self.cached_exceptions.queue = FixedMaxSizeUniqueQueue()
        return self.cached_exceptions.queue.offer(exception)

class FakeExceptionHandler(ExceptionHandler):
    """
    Фиктивная реализация ExceptionHandler – просто проверяет, что аргумент не null.
    """
    def __init__(self):
        pass

    def handle(self, exception: BaseException) -> None:
        if exception is None:
            raise StepfatherException("exception arg is null")