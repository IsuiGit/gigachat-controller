from .core import _GigaChatController
from .meta import _GigaChatControllerMeta
from .models import GigaChatControllerContext

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

    def invoke(self, message: Any):
        return self._commit(self._chat, message)

    async def ainvoke(self, message: Any):
        return await self._acommit(self._achat, message)

    def stream(self, message: Any):
        return self._commit(self._stream, message)

    async def astream(self, message: Any):
        return await self._acommit(self._astream, message)

__all__ = [
    "GigaChatController"
]
