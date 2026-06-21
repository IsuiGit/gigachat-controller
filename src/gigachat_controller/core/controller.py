from typing import (
    Any,
    Dict,
    Tuple,
)

from gigachat import GigaChat
from gigachat.models import (
    Models,
)

from gigachat_controller.models import _create_config_instance
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
        self._llm = _create_llm(llm, self._config)

        super().__init__(**kwargs)

    def _info(self) -> str:
        return GCC_REPR.format(
            config=self._config.model_dump_json(indent=2),
            llm = self._llm
        )

    def _models(self) -> Models:
        try:
            models = self._llm.get_models()
            return models
        except Exception as e:
            raise e

    def _chat(self, message: Any) -> Any:
        try:
            if isinstance(message, str):
                response = self._llm.chat(message)
            else:
                _str_message = str(message)
                response = self._llm.chat(_str_message)
            return response
        except Exception as e:
            raise e

    async def _achat(self, message: Any) -> Any:
        try:
            if isinstance(message, str):
                response = await self._llm.achat(message)
            else:
                _str_message = str(message)
                response = await self._llm.achat(_str_message)
            return response
        except Exception as e:
            raise e


    def _close(self):
        if self._llm:
            self._llm.close()
            self._llm = None

    def __del__(self):
        self._close()
