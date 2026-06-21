from typing import Any, Dict, Type
from pydantic import BaseModel
from gigachat import GigaChat

def _create_llm(llm_class: Type[GigaChat], config: BaseModel) -> Any:
    if not issubclass(llm_class, GigaChat):
        raise ValueError(f"GigaChat controller support only GigaChat instances, not {llm_class=}")
    _llm = llm_class(**config.model_dump())
    return _llm
