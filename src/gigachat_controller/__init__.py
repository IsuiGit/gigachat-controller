from .core import _GigaChatController
from .meta import _GigaChatControllerMeta

from typing import (
    Type,
    Dict,
    Any,
)

class GigaChatController(_GigaChatController, _GigaChatControllerMeta):

    def info(self):
        return self._commit(self._info)

    def models(self):
        return self._commit(self._models)

    def invoke(self, message: Any):
        return self._commit(self._chat, message)

    async def ainvoke(self, message: Any):
        return await self._acommit(self._achat, message)

__all__ = [
    "GigaChatController"
]
