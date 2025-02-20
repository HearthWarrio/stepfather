import threading
import traceback
from collections import deque
from typing import Set, Deque, Any

class StepfatherException(Exception):

    pass
"""
Exception handler.
"""
class ExceptionHandler:

    def handle(self, exception: BaseException) -> None:
        raise NotImplementedError("Method handle should be implemented")

class FixedMaxSizeUniqueQueue:

    def __init__(self, max_size: int = 10):
        self.max_size: int = max_size
        self.queue: Deque[Any] = deque()
        self.set: Set[Any] = set()

    def offer(self, element: Any) -> bool:
        if element not in self.set:
            self.queue.append(element)
            self.set.add(element)
            if len(self.set) == self.max_size:
                oldest = self.queue.popleft()
                self.set.remove(oldest)
            return True
        return False
"""
Default ExceptionHandler implementation
Обработчик исключений, который рекурсивно обходит все связанные исключения
и "очищает" их стек вызовов, удаляя элементы, начинающиеся с определенного префикса.
"""
class CleanStackTrace(ExceptionHandler):

    def __init__(self):

        self.stepfather_class_prefix = "com.hearthwarrio.stepfather"
        self._thread_local = threading.local()

    @property
    def cached_exceptions(self) -> FixedMaxSizeUniqueQueue:
        if not hasattr(self._thread_local, 'queue'):
            self._thread_local.queue = FixedMaxSizeUniqueQueue()
        return self._thread_local.queue

    def handle(self, exception: BaseException) -> None:
        if exception is None:
            raise StepfatherException("exception arg is null")
        all_related_exceptions: Set[BaseException] = set()
        self.recursively_add_all_related_exceptions(all_related_exceptions, exception)
        for current_ex in all_related_exceptions:
            if not isinstance(current_ex, StepfatherException) and self.cached_exceptions.offer(current_ex):
                if current_ex.__traceback__ is not None:
                    tb_list = traceback.extract_tb(current_ex.__traceback__)
                    clean_tb_list = [
                        frame for frame in tb_list
                        if not frame.filename.startswith(self.Stepfather_class_prefix)
                    ]
                    if len(clean_tb_list) != len(tb_list):
                        current_ex.cleaned_traceback = clean_tb_list

    @staticmethod
    def recursively_add_all_related_exceptions(exceptions: Set[BaseException], main_ex: BaseException) -> None:
        if main_ex in exceptions:
            return
        exceptions.add(main_ex)
        if main_ex.__cause__:
            CleanStackTrace.recursively_add_all_related_exceptions(exceptions, main_ex.__cause__)
        if main_ex.__context__:
            CleanStackTrace.recursively_add_all_related_exceptions(exceptions, main_ex.__context__)
"""
Fake handler. Just checks that arg not null.
Фиктивный обработчик исключений – просто проверяет, что аргумент не None.
"""
class Fake(ExceptionHandler):

    def __init__(self):
        pass

    def handle(self, exception: BaseException) -> None:
        if exception is None:
            raise StepfatherException("exception arg is null")
