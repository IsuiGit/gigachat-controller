from pydantic import BaseModel
from typing import (
    Any,
    Dict,
    Tuple,
)

from gigachat import GigaChat
from gigachat.models import (
    Models,
    ChatCompletion,
    ChatCompletionChunk,
)

from gigachat_controller.models import (
    _create_config_instance,
    GigaChatStreamResponse,
)
from gigachat_controller.utils import (
    _create_llm,
    GCC_REPR
)

class _GigaChatController:
    def __init__(
        self,
        llm: Any = None,
        config: Dict[str, Any] = None,
        **kwargs
    ) -> None:

        if llm is None:
            llm = GigaChat

        self._config = _create_config_instance(config)
        self._llm = llm

        super().__init__(**kwargs)

    def _info(self) -> str:
        return GCC_REPR.format(
            config=self._config.model_dump_json(indent=2),
            llm = self._llm
        )

    def _models(self) -> Models:
        try:
            _conn = _create_llm(self._llm, self._config)
            models = _conn.get_models()
            return models
        except Exception as e:
            raise e

    def _chat(self, message: Any) -> ChatCompletion:
        try:
            _conn = _create_llm(self._llm, self._config)
            _str_message = str(message)
            response = _conn.chat(_str_message)
            return response
        except Exception as e:
            raise e

    def _stream(self, message: Any) -> List[ChatCompletionChunk]:
        try:
            _conn = _create_llm(self._llm, self._config)
            _stream = []
            for chunk in _conn.stream(message):
                _stream.append(chunk)
            return GigaChatStreamResponse(chunks=_stream)
        except Exception as e:
            raise e

    async def _astream(self) -> List[str] : pass

    # #TODO: knows type of embeding return
    # def _embedings(self) -> Any: pass
    #
    # #TODO: knows type of fc return
    # def _function_call(self) -> None: pass
    #
    # def _structured(self, model: BaseModel) -> BaseModel: pass

    async def _achat(self, message: Any) -> ChatCompletion:
        try:
            _conn = _create_llm(self._llm, self._config)
            _str_message = str(message)
            response = await _conn.achat(_str_message)
            return response
        except Exception as e:
            raise e
