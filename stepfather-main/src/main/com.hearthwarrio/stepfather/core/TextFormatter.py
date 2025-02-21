import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Pattern, Iterable
import StepfatherException
import TextFormatException
import ExceptionHandler

class TextFormatter(ABC):
    @abstractmethod
    def format(self, obj: Any) -> str:
        """
        Возвращает строковое представление объекта.
        Может выбрасывать TextFormatException, если преобразование невозможно.
        """
        pass

    @abstractmethod
    def format_with_replacements(self, text: str, replacements: Dict[str, Any]) -> str:
        """
        Форматирует текст с учётом замен.
        Может выбрасывать TextFormatException, если форматирование невозможно.
        """
        pass

class DefaultTextFormatter(TextFormatter):
    def __init__(self,
                 exception_handler: ExceptionHandler,
                 replacement_pattern: Pattern,
                 field_force_access: bool,
                 method_force_access: bool):
        if exception_handler is None:
            raise StepfatherException.StepfatherException("exceptionHandler arg is null")
        if replacement_pattern is None:
            raise StepfatherException.StepfatherException("replacementPattern arg is null")
        self.check_that_pattern_contains_capturing_groups(replacement_pattern)
        self.exception_handler = exception_handler
        self.replacement_pattern = replacement_pattern
        self.field_force_access = field_force_access
        self.method_force_access = method_force_access

    @staticmethod
    def check_that_pattern_contains_capturing_groups(pattern: Pattern) -> None:
        if pattern.groups < 1:
            raise StepfatherException.StepfatherException(f"replacementPattern arg {pattern} doesn't contain groups, pattern must contain at least one group")

    def format(self, obj: Any) -> str:
        if obj is None:
            return "null"
        cls = type(obj)
        try:
            if isinstance(obj, (list, tuple)):
                return str(obj)
            return str(obj)
        except Exception as ex:
            raise self.handled_ex(TextFormatException.TextFormatException(f"{self.method_desc(cls, 'toString()')} threw {ex}", ex))

    def format_with_replacements(self, text: str, replacements: Dict[str, Any]) -> str:
        if text is None:
            raise StepfatherException.StepfatherException("text arg is null")
        if replacements is None:
            raise StepfatherException.StepfatherException("replacements arg is null")
        if text == "" or not replacements:
            return text
        result = []
        last_index = 0
        for match in self.replacement_pattern.finditer(text):
            result.append(text[last_index:match.start()])
            path = match.group(1).split(".")
            replacement_pointer = path[0]
            if replacement_pointer in replacements:
                replacement_value = replacements[replacement_pointer]
                if len(path) == 1:
                    formatted_replacement = self.format(replacement_value)
                else:
                    formatted_replacement = self.format(
                        self.extract_value(path, replacement_value, self.field_force_access, self.method_force_access)
                    )
                result.append(re.escape(formatted_replacement))
            last_index = match.end()
        result.append(text[last_index:])
        return "".join(result)

    def extract_value(self,
                      path: List[str],
                      first_part_value: Any,
                      field_force_access: bool,
                      method_force_access: bool) -> Any:
        last_value = first_part_value
        for idx in range(1, len(path)):
            path_part = path[idx]
            if '(' in path_part and ')' in path_part:
                last_value = self.method_value(last_value, path_part, method_force_access)
            elif '[' in path_part and ']' in path_part:
                last_value = self.container_value(last_value, path_part)
            else:
                last_value = self.field_value(last_value, path_part, field_force_access)
        return last_value

    def container_value(self, obj: Any, path_part: str) -> Any:
        path_part_length = len(path_part)
        if path_part_length < 3 or not (path_part.startswith('[') and path_part.endswith(']')):
            raise self.handled_ex(TextFormatException.TextFormatException("Incorrect element index " + path_part))
        try:
            index = int(path_part[1:path_part_length - 1])
        except Exception as ex:
            raise self.handled_ex(TextFormatException.TextFormatException("Incorrect element index " + path_part, ex))
        if obj is None:
            raise self.handled_ex(TextFormatException.TextFormatException("Cannot get element of null"))
        if isinstance(obj, (list, tuple)):
            try:
                return obj[index]
            except Exception as ex:
                raise self.handled_ex(TextFormatException.TextFormatException("Cannot get array element by index " + str(index), ex))
        elif isinstance(obj, Iterable):
            for idx, item in enumerate(obj):
                if idx == index:
                    return item
            raise self.handled_ex(TextFormatException.TextFormatException("Cannot get Iterable element by index " + str(index)))
        else:
            raise self.handled_ex(TextFormatException.TextFormatException("Cannot get element of " + str(type(obj))))

    def method_value(self, obj: Any, path_part: str, force_access: bool) -> Any:
        if len(path_part) < 3 or not path_part.endswith("()"):
            raise self.handled_ex(TextFormatException.TextFormatException("Incorrect method " + path_part))
        if obj is None:
            raise self.handled_ex(TextFormatException.TextFormatException(f"Cannot invoke {path_part} method on null"))
        cls = type(obj)
        method_name = path_part[:-2]
        try:
            method = self.find_method(cls, method_name, force_access)
        except Exception as ex:
            raise self.handled_ex(TextFormatException.TextFormatException(f"Cannot get {self.method_desc(cls, path_part)} {self.force_access_desc(force_access)} cause {ex}", ex))
        if method is None:
            raise self.handled_ex(TextFormatException.TextFormatException(f"Cannot find {self.method_desc(cls, path_part)} {self.force_access_desc(force_access)}"))
        try:
            return self.invoke_method(obj, method, force_access)
        except Exception as ex:
            raise self.handled_ex(TextFormatException.TextFormatException(f"Cannot invoke {self.method_desc(cls, path_part)} {self.force_access_desc(force_access)} cause {ex}", ex))

    @staticmethod
    def find_method(cls: type, method_name: str, force_access: bool):
        try:
            method = getattr(cls, method_name)
            if callable(method):
                return method
        except AttributeError:
            pass
        if force_access:
            # TODO: Реализовать доступ к "приватным" методам.
            for current_cls in cls.__mro__:
                if method_name in current_cls.__dict__:
                    candidate = current_cls.__dict__[method_name]
                    if callable(candidate):
                        return candidate
        return None

    @classmethod
    def invoke_method(self, obj: Any, method, force_access: bool) -> Any:
        bound = getattr(method, '__self__', None)
        if bound is not None:
            return method()
        else:
            return method(obj)

    def field_value(self, obj: Any, path_part: str, force_access: bool) -> Any:
        if obj is None:
            raise self.handled_ex(TextFormatException.TextFormatException(f"Cannot get {path_part} field value of null"))
        cls = type(obj)
        try:
            field = self.find_field(cls, path_part, force_access)
        except Exception as ex:
            raise self.handled_ex(TextFormatException.TextFormatException(f"Cannot get {self.field_desc(cls, path_part)} cause {ex}", ex))
        if field is None:
            raise self.handled_ex(TextFormatException.TextFormatException(f"Cannot find {self.field_desc(cls, path_part)} {self.force_access_desc(force_access)}"))
        try:
            return self.get_field_value(obj, field, force_access)
        except Exception as ex:
            raise self.handled_ex(TextFormatException.TextFormatException(f"Cannot get {self.field_desc(cls, path_part)} value {self.force_access_desc(force_access)} cause {ex}", ex))

    @staticmethod
    def find_field(cls: type, field_name: str, force_access: bool):
        if hasattr(cls, field_name):
            return field_name
        if force_access:
            # TODO: Реализовать доступ к "приватным" методам.
            for current_cls in cls.__mro__:
                if field_name in current_cls.__dict__:
                    return field_name
        return None

    @staticmethod
    def get_field_value(obj: Any, field: str, force_access: bool) -> Any:
        return getattr(obj, field)

    def handled_ex(self, exception: TextFormatException) -> TextFormatException:
        self.exception_handler.handle(exception)
        return exception

    @staticmethod
    def method_desc(cls: type, method: str) -> str:
        return f"{cls.__name__} object {method} method"

    @staticmethod
    def field_desc(cls: type, field: str) -> str:
        return f"{cls.__name__} object {field} field"

    @staticmethod
    def force_access_desc(force_access: bool) -> str:
        return "with force access" if force_access else "without force access"

class FakeTextFormatter(TextFormatter):
    def __init__(self):
        pass

    def format(self, obj: Any) -> str:
        return str(obj) if obj is not None else "null"

    def format_with_replacements(self, text: str, replacements: Dict[str, Any]) -> str:
        if text is None:
            raise StepfatherException.StepfatherException("text arg is null")
        if replacements is None:
            raise StepfatherException.StepfatherException("replacements arg is null")
        return text