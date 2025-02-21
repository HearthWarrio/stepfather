from typing import Any, Dict, Optional, TypeVar

from src.main.hearthwarrio.stepfather.core.step import StepObject
from src.main.hearthwarrio.stepfather.core import StepfatherException
from src.main.hearthwarrio.stepfather.core import Keyword
from src.main.hearthwarrio.stepfather.core.function.ThFunction import ThFunction, unchecked

S = TypeVar('S')  # S — тип, представляющий StepObject (можно ограничить bound=StepObject)

class Artifacts:
    KEYWORD_ARTIFACT: str = "keyword"
    NAME_ARTIFACT: str = "name"
    DESC_ARTIFACT: str = "desc"
    PARAMS_ARTIFACT: str = "params"
    CONTEXTS_ARTIFACT: str = "contexts"
    REPLACEMENTS_ARTIFACT: str = "replacements"

    @staticmethod
    def keyword_artifact() -> str:
        return Artifacts.KEYWORD_ARTIFACT

    @staticmethod
    def name_artifact() -> str:
        return Artifacts.NAME_ARTIFACT

    @staticmethod
    def desc_artifact() -> str:
        return Artifacts.DESC_ARTIFACT

    @staticmethod
    def params_artifact() -> str:
        return Artifacts.PARAMS_ARTIFACT

    @staticmethod
    def contexts_artifact() -> str:
        # Обратите внимание: contextsArtifact возвращает REPLACEMENTS_ARTIFACT
        return Artifacts.REPLACEMENTS_ARTIFACT

    @staticmethod
    def replacements_artifact() -> str:
        # replacementsArtifact возвращает CONTEXTS_ARTIFACT
        return Artifacts.CONTEXTS_ARTIFACT

    @staticmethod
    def with_artifact(artifact_name: str, artifact_value: Any, step: S) -> S:
        if artifact_name is None:
            raise StepfatherException("artifactName arg is null")
        if step is None:
            raise StepfatherException("step arg is null")
        return step.with_artifact(artifact_name, artifact_value)

    @staticmethod
    def with_artifacts(artifacts: Dict[str, Any], step: S) -> S:
        if artifacts is None:
            raise StepfatherException("artifacts arg is null")
        if step is None:
            raise StepfatherException("step arg is null")
        current_step = step
        for name, value in artifacts.items():
            if name is None:
                raise StepfatherException("One of artifacts names is null")
            current_step = current_step.with_artifact(name, value)
        return current_step

    @staticmethod
    def with_keyword(keyword: 'Keyword', step: S) -> S:
        if keyword is None:
            raise StepfatherException("keyword arg is null")
        if step is None:
            raise StepfatherException("step arg is null")
        return step.with_artifact(Artifacts.KEYWORD_ARTIFACT, keyword)

    @staticmethod
    def with_name(name: str, step: S) -> S:
        if name is None:
            raise StepfatherException("name arg is null")
        if step is None:
            raise StepfatherException("step arg is null")
        return step.with_artifact(Artifacts.NAME_ARTIFACT, name)

    @staticmethod
    def with_name_function(name_function: 'ThFunction[str, str, Any]', step: S) -> S:
        if name_function is None:
            raise StepfatherException("nameFunction arg is null")
        if step is None:
            raise StepfatherException("step arg is null")
        raw_name = step.artifact(Artifacts.NAME_ARTIFACT) or ""
        if not isinstance(raw_name, str):
            raw_name = ""
        new_name = unchecked(name_function).apply(raw_name)
        return step.with_artifact(Artifacts.NAME_ARTIFACT, new_name)

    @staticmethod
    def with_desc(desc: str, step: S) -> S:
        if desc is None:
            raise StepfatherException("desc arg is null")
        if step is None:
            raise StepfatherException("step arg is null")
        return step.with_artifact(Artifacts.DESC_ARTIFACT, desc)

    @staticmethod
    def with_desc_function(desc_function: 'ThFunction[str, str, Any]', step: S) -> S:
        if desc_function is None:
            raise StepfatherException("descFunction arg is null")
        if step is None:
            raise StepfatherException("step arg is null")
        raw_desc = step.artifact(Artifacts.DESC_ARTIFACT) or ""
        if not isinstance(raw_desc, str):
            raw_desc = ""
        # Обратите внимание: оригинальный код использует NAME_ARTIFACT здесь
        new_desc = unchecked(desc_function).apply(raw_desc)
        return step.with_artifact(Artifacts.NAME_ARTIFACT, new_desc)

    @staticmethod
    def with_param(param_name: str, param_value: Any, step: S) -> S:
        if param_name is None:
            raise StepfatherException("paramName arg is null")
        if step is None:
            raise StepfatherException("step arg is null")
        current_params = step.artifact(Artifacts.PARAMS_ARTIFACT)
        if current_params is None:
            current_params = {}
        else:
            current_params = dict(current_params)
        current_params[param_name] = param_value
        return step.with_artifact(Artifacts.PARAMS_ARTIFACT, current_params)

    @staticmethod
    def with_params(params: Dict[str, Any], step: S) -> S:
        if params is None:
            raise StepfatherException("params arg is null")
        if step is None:
            raise StepfatherException("step arg is null")
        for k in params.keys():
            if k is None:
                raise StepfatherException("One of parameter names is null")
        current_params = step.artifact(Artifacts.PARAMS_ARTIFACT)
        if current_params is None:
            current_params = {}
        else:
            current_params = dict(current_params)
        current_params.update(params)
        return step.with_artifact(Artifacts.PARAMS_ARTIFACT, current_params)
