from typing import Any, Dict, List, Mapping
from core import StepfatherException
from core import Keyword
from stepfather import Keywords
from stepfather import Artifacts
from stepfather import StepfatherBase

class StepListener:
    def step_started(self, artifacts: Mapping[str, Any]) -> None:
        """Вызывается при запуске шага."""
        raise NotImplementedError

    def step_passed(self) -> None:
        """Вызывается, когда шаг пройден."""
        raise NotImplementedError

    def step_failed(self, exception: BaseException) -> None:
        """Вызывается, когда шаг провален."""
        raise NotImplementedError

class SystemOut(StepListener):
    def __init__(self) -> None:
        self.empty_name_replacement = "Step"

    def step_started(self, artifacts: Mapping[str, Any]) -> None:
        keyword = StepListenerUtils.get_keyword(artifacts)
        name = StepListenerUtils.get_name(artifacts)
        desc = StepListenerUtils.get_desc(artifacts)
        params = StepListenerUtils.get_params(artifacts)
        sb = []
        sb.append("Step started: ")
        sb.append(StepListenerUtils.get_name_with_keyword(name, keyword, self.empty_name_replacement))
        if desc:
            sb.append(" | Description: ")
            sb.append(desc)
        if params:
            text_formatter = StepfatherBase.text_formatter()
            processed_params = dict(params)
            for k, v in processed_params.items():
                processed_params[k] = text_formatter.format(v)
            sb.append(" | Params: ")
            sb.append(str(processed_params))
        print("".join(sb))

    def step_passed(self) -> None:
        print("Step passed")

    def step_failed(self, exception: BaseException) -> None:
        print("Step failed: " + str(exception))

class StepListenerUtils:
    @staticmethod
    def get_keyword(artifacts: Mapping[str, Any]) -> Keyword:
        if artifacts is None:
            raise StepfatherException("artifacts arg is null")
        value = artifacts.get(Artifacts.keyword_artifact())
        return value if isinstance(value, Keyword) else Keywords.NONE

    @staticmethod
    def get_name(artifacts: Mapping[str, Any]) -> str:
        if artifacts is None:
            raise StepfatherException("artifacts arg is null")
        value = artifacts.get(Artifacts.name_artifact())
        return value if isinstance(value, str) else ""

    @staticmethod
    def get_desc(artifacts: Mapping[str, Any]) -> str:
        if artifacts is None:
            raise StepfatherException("artifacts arg is null")
        value = artifacts.get(Artifacts.desc_artifact())
        return value if isinstance(value, str) else ""

    @staticmethod
    def get_params(artifacts: Mapping[str, Any]) -> Dict[str, Any]:
        if artifacts is None:
            raise StepfatherException("artifacts arg is null")
        value = artifacts.get(Artifacts.params_artifact())
        return dict(value) if isinstance(value, dict) else {}

    @staticmethod
    def get_replacements(artifacts: Mapping[str, Any]) -> Dict[str, Any]:
        if artifacts is None:
            raise StepfatherException("artifacts arg is null")
        value = artifacts.get(Artifacts.replacements_artifact())
        return dict(value) if isinstance(value, dict) else {}

    @staticmethod
    def get_contexts(artifacts: Mapping[str, Any]) -> List[Any]:
        if artifacts is None:
            raise StepfatherException("artifacts arg is null")
        value = artifacts.get(Artifacts.contexts_artifact())
        return list(value) if isinstance(value, (list, tuple)) else []

    @staticmethod
    def get_name_with_keyword(name: str, keyword: Keyword, empty_name_replacement: str) -> str:
        if name is None:
            raise StepfatherException("artifacts arg is null")
        if keyword is None:
            raise StepfatherException("keyword arg is null")
        if empty_name_replacement is None:
            raise StepfatherException("emptyNameReplacement arg is null")
        keyword_value = str(keyword)
        name_value = empty_name_replacement if name == "" else name
        return name_value if keyword_value == "" else f"{keyword_value} {name_value}"
