from typing import Any, Dict, TypeVar, Protocol, Optional
from function.ThSupplier import ThSupplier, unchecked as th_unchecked_supplier
from core import StepfatherException
from core import StepListener

R = TypeVar('R')

class StepReporter(Protocol):
    def start_step(self, artifacts: Dict[str, Any]) -> None:
        ...

    def pass_step(self) -> None:
        ...

    def fail_step(self, exception: BaseException) -> None:
        ...

    def execute_step(self, artifacts: Dict[str, Any], action: ThSupplier[R, Exception]) -> R:
        ...

class DefaultStepReporter(StepReporter):
    def __init__(self, exception_handler: Any, listeners: list[StepListener]) -> None:
        if exception_handler is None:
            raise StepfatherException("exceptionHandler arg is null")
        if listeners is None:
            raise StepfatherException("listeners arg is null")
        self.exception_handler = exception_handler
        self.listeners = listeners

    def start_step(self, artifacts: Dict[str, Any]) -> None:
        if artifacts is None:
            raise StepfatherException("artifacts arg is null")
        for listener in self.listeners:
            listener.step_started(artifacts)

    def pass_step(self) -> None:
        for listener in self.listeners:
            listener.step_passed()

    def fail_step(self, exception: BaseException) -> None:
        if exception is None:
            raise StepfatherException("exception arg is null")
        for listener in self.listeners:
            listener.step_failed(exception)

    def execute_step(self, artifacts: Dict[str, Any], action: ThSupplier[R, Exception]) -> R:
        if artifacts is None:
            raise StepfatherException("artifacts arg is null")
        if action is None:
            raise StepfatherException("action arg is null")
        self.start_step(artifacts)
        step_exception: Optional[BaseException] = None
        step_result: Optional[R] = None
        try:
            step_result = action.get()
        except Exception as ex:
            step_exception = ex
        if step_exception is None:
            self.pass_step()
            return step_result  # type: ignore
        else:
            self.exception_handler.handle(step_exception)
            self.fail_step(step_exception)
            raise step_exception

class FakeStepReporter(StepReporter):
    def __init__(self, exception_handler: Any) -> None:
        if exception_handler is None:
            raise StepfatherException("exceptionHandler arg is null")
        self.exception_handler = exception_handler

    def start_step(self, artifacts: Dict[str, Any]) -> None:
        if artifacts is None:
            raise StepfatherException("artifacts arg is null")

    def pass_step(self) -> None:
        pass

    def fail_step(self, exception: BaseException) -> None:
        if exception is None:
            raise StepfatherException("exception arg is null")
        self.exception_handler.handle(exception)

    def execute_step(self, artifacts: Dict[str, Any], action: ThSupplier[R, Exception]) -> R:
        if artifacts is None:
            raise StepfatherException("artifacts arg is null")
        if action is None:
            raise StepfatherException("action arg is null")
        try:
            return th_unchecked_supplier(action).get()
        except Exception as step_ex:
            self.exception_handler.handle(step_ex)
            raise step_ex
