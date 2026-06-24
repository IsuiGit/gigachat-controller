import logging
import logging.config
from logging.handlers import RotatingFileHandler

from typing import (
    Any,
    Callable,
    Union,
    List,
)

from gigachat.models import (
    ChatCompletion,
)

from gigachat_controller.models import (
    GigaChatControllerContext,
    GigaChatControllerException,
    GigaChatStreamResponse,
)

from gigachat_controller.utils import (
    _get_callable_info,
    _get_exception,
    _get_chat_completion,
    _get_stream,
)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": "app.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
        },
    },

    "loggers": {
        "gigachat_controller": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)


class _GigaChatControllerMeta:
    def __init__(
        self,
        logger: Any = None,
        max_ctx: int = 10,
        **kwargs
    ):
        self._logger = logger
        self._ctx = GigaChatControllerContext()
        self._max_ctx = max_ctx

        if self._logger is None:
            self._logger = logging.getLogger("gigachat_controller")

        super().__init__(**kwargs)

    #TODO: add max_context eraser & available tokens + released tokens functions

    def _commit(self, function: Callable, *args, **kwargs) -> Union[Any, None]:
        try:
            #TODO: add max_ctx controll function
            _info = _get_callable_info(function)
            result = function(*args, **kwargs)
            if isinstance(result, ChatCompletion):
                text, meta = _get_chat_completion(result)
                self._ctx.agent_responses.append(text)
                self._ctx.agent_responses_meta.append(meta)
                self._logger.info(f"Execute func {function.__name__}.")
                self._logger.info(f"Response from agent: {self._ctx.agent_responses[-1]}")
                self._logger.info(f"Result metadata: {self._ctx.agent_responses_meta[-1].model_dump_json(indent=2)}")
                return self._ctx.agent_responses[-1]
            elif isinstance(result, GigaChatStreamResponse):
                text, meta = _get_stream(result)
                self._ctx.agent_responses.append(text)
                self._ctx.agent_responses_meta.append(meta)
                self._logger.info(f"Execute func {function.__name__}.")
                self._logger.info(f"Response from agent: {self._ctx.agent_responses[-1]}")
                self._logger.info(f"Result metadata: {self._ctx.agent_responses_meta[-1].model_dump_json(indent=2)}")
                return self._ctx.agent_responses[-1]
            else:
                self._ctx.last_response = result
                self._logger.info(f"Execute func {function.__name__}.")
                return self._ctx.last_response
        except Exception as e:
            self._ctx.last_error = _get_exception(e, _info)
            self._logger.error(f"Exception at func {function.__name__}.\nException: {self._ctx.last_error}")
            return None

    async def _acommit(self, function: Callable, *args, **kwargs) -> Union[Any, None]:
        try:
            _info = _get_callable_info(function)
            result = await function(*args, **kwargs)
            if isinstance(result, ChatCompletion):
                text, meta = _get_chat_completion(result)
                self._ctx.agent_responses.append(text)
                self._ctx.agent_responses_meta.append(meta)
                self._logger.info(f"Execute func {function.__name__}.")
                self._logger.info(f"Response from agent: {self._ctx.agent_responses[-1]}")
                self._logger.info(f"Result metadata: {self._ctx.agent_responses_meta[-1].model_dump_json(indent=2)}")
                return self._ctx.agent_responses[-1]
            elif isinstance(result, GigaChatStreamResponse):
                text, meta = _get_stream(result)
                self._ctx.agent_responses.append(text)
                self._ctx.agent_responses_meta.append(meta)
                self._logger.info(f"Execute func {function.__name__}.")
                self._logger.info(f"Response from agent: {self._ctx.agent_responses[-1]}")
                self._logger.info(f"Result metadata: {self._ctx.agent_responses_meta[-1].model_dump_json(indent=2)}")
                return self._ctx.agent_responses[-1]
            else:
                self._ctx.last_response = result
                self._logger.info(f"Execute func {function.__name__}.")
                return self._ctx.last_response
        except Exception as e:
            self._ctx.last_error = _get_exception(e, _info)
            self._logger.error(f"Exception at func {function.__name__}.\nException: {self._ctx.last_error}")
            return None
