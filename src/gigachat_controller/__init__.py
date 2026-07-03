from .core import _GigaChatController
from .meta import _GigaChatControllerMeta
from .models import (
    GigaChatControllerContext,
    FunctionCall,
    FunctionCallNode
)

from typing import (
    Type,
    Dict,
    Any,
)

class GigaChatController(_GigaChatController, _GigaChatControllerMeta):
    @property
    def context(self) -> GigaChatControllerContext:
        return self._ctx

    @property
    def logger(self):
        return self._logger

    def info(self):
        return self._commit(self._info)

    def models(self):
        return self._commit(self._models)

    def invoke(self, message: Any) -> str:
        return self._commit(self._chat, message)

    async def ainvoke(self, message: Any) -> str:
        return await self._acommit(self._achat, message)

    def stream(self, message: Any) -> str:
        return self._commit(self._stream, message)

    async def astream(self, message: Any) -> str:
        return await self._acommit(self._astream, message)

    def function_call_factory(self, function_call: FunctionCall) -> List[str]:
        _nodes = sorted(function_call.nodes, key=lambda node: node.order)
        for _node in _nodes:
            self._logger.info(f"Attempting to execute node {_node.name} by order {_node.order}")
            function_call_node = self._commit(self._function_call, _node)
            if function_call_node:
                function_call.responses.append(function_call_node)
        return function_call

__all__ = [
    "GigaChatController",
    "FunctionCall",
    "FunctionCallNode",
]
