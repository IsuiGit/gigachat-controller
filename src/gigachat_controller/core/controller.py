import json

from pydantic import BaseModel
from typing import (
    Any,
    Dict,
    Tuple,
    Callable,
)

from gigachat import GigaChat
from gigachat.models import (
    Models,
    ChatCompletion,
    ChatCompletionChunk,
    Chat,
)

from gigachat_controller.models import (
    _create_config_instance,
    GigaChatStreamResponse,
    FunctionCallNode,
    GigaChatControllerFunctionCallException,
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
        _conn = _create_llm(self._llm, self._config)
        models = _conn.get_models()
        return models

    def _chat(self, message: Any) -> ChatCompletion:
        _conn = _create_llm(self._llm, self._config)
        _str_message = str(message)
        response = _conn.chat(_str_message)
        return response

    async def _achat(self, message: Any) -> ChatCompletion:
        _conn = _create_llm(self._llm, self._config)
        _str_message = str(message)
        response = await _conn.achat(_str_message)
        return response

    def _stream(self, message: Any) -> List[ChatCompletionChunk]:
        _conn = _create_llm(self._llm, self._config)
        _stream = []
        _str_message = str(message)
        for chunk in _conn.stream(_str_message):
            _stream.append(chunk)
        return GigaChatStreamResponse(chunks=_stream)

    async def _astream(self, message: Any) -> List[ChatCompletionChunk]:
        _conn = _create_llm(self._llm, self._config)
        _stream = []
        _str_message = str(message)
        async for chunk in _conn.astream(_str_message):
            _stream.append(chunk)
        return GigaChatStreamResponse(chunks=_stream)

    def _function_call(self, function_call_node: FunctionCallNode) -> FunctionCallNode:
        _conn = _create_llm(self._llm, self._config)
        _messages = [{"role": "user", "content": function_call_node.message}]
        _chat = Chat(messages=_messages, functions=[function_call_node.map])
        _function_call_response = _conn.chat(_chat)
        _function_call_message = _function_call_response.choices[0].message
        if _function_call_message.function_call:
            _messages.append(_function_call_message.dict())
            _name = _function_call_message.function_call.name
            _args = _function_call_message.function_call.arguments
            if _name != function_call_node.function.__name__:
                raise GigaChatControllerFunctionCallException(
                    f"Name of function_call {_name} not equal function name {function_call_node.function.__name__}",
                    code=201,
                    tool=function_call_node.function.__name__,
                )
            _function_response = function_call_node.function(**_args)
            _messages.append({"role": "function", "name": _name, "content": json.dumps(_function_response, ensure_ascii=False)})
            _final_chat = Chat(messages=_messages)
            _function_call_final_response = _conn.chat(_final_chat)
            function_call_node.response = _function_call_final_response
            return function_call_node
        else:
            function_call_node.response = _function_call_response
            return function_call_node
