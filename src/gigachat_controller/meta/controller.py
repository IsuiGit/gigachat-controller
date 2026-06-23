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
    GigaChatResponseMeta,
    GigaChatResponseMetaHeaders,
    GigaChatResponseMetaUsage,
    GigaChatControllerException,
    GigaChatStreamResponse,
)

from gigachat_controller.utils import _get_callable_info, _get_exception

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
                self._ctx.agent_responses.append(result.choices[0].message.content)
                self._ctx.agent_responses_meta.append(
                    GigaChatResponseMeta(
                        headers=GigaChatResponseMetaHeaders(**result.x_headers),
                        created=result.created,
                        model=result.model,
                        usage=GigaChatResponseMetaUsage(
                            prompt_tokens = result.usage.prompt_tokens,
                            completion_tokens = result.usage.completion_tokens,
                            total_tokens = result.usage.total_tokens,
                            precached_prompt_tokens = result.usage.precached_prompt_tokens,
                        ),
                        finish_reason=result.choices[0].finish_reason
                    )
                )
                self._logger.info(f"Execute func {function.__name__}.")
                self._logger.info(f"Response from agent: {self._ctx.agent_responses[-1]}")
                self._logger.info(f"Result metadata: {self._ctx.agent_responses_meta[-1].model_dump_json(indent=2)}")
                return self._ctx.agent_responses[-1]
            elif isinstance(result, GigaChatStreamResponse):
                self._ctx.agent_responses.append(
                    "".join([chunk.choices[0].delta.content for chunk in result.chunks])
                )
                self._ctx.agent_responses_meta.append(
                    GigaChatResponseMeta(
                        headers=GigaChatResponseMetaHeaders(**result.chunks[-1].x_headers),
                        created=result.chunks[-1].created,
                        model=result.chunks[-1].model,
                        usage=GigaChatResponseMetaUsage(
                            prompt_tokens = result.chunks[-1].usage.prompt_tokens,
                            completion_tokens = result.chunks[-1].usage.completion_tokens,
                            total_tokens = result.chunks[-1].usage.total_tokens,
                            precached_prompt_tokens = result.chunks[-1].usage.precached_prompt_tokens,
                        ),
                        finish_reason=result.chunks[-1].choices[0].finish_reason
                    )
                )
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
                self._ctx.agent_responses.append(result.choices[0].message.content)
                self._ctx.agent_responses_meta.append(
                    GigaChatResponseMeta(
                        headers=GigaChatResponseMetaHeaders(**result.x_headers),
                        created=result.created,
                        model=result.model,
                        usage=GigaChatResponseMetaUsage(
                            prompt_tokens = result.usage.prompt_tokens,
                            completion_tokens = result.usage.completion_tokens,
                            total_tokens = result.usage.total_tokens,
                            precached_prompt_tokens = result.usage.precached_prompt_tokens,
                        ),
                        finish_reason=result.choices[0].finish_reason
                    )
                )
                self._logger.info(f"Execute func {function.__name__}.")
                self._logger.info(f"Response from agent: {self._ctx.agent_responses[-1]}")
                self._logger.info(f"Result metadata: {self._ctx.agent_responses_meta[-1].model_dump_json(indent=2)}")
                return self._ctx.agent_responses[-1]
            elif isinstance(result, GigaChatStreamResponse):
                self._ctx.agent_responses.append(
                    "".join([chunk.choices[0].delta.content for chunk in result.chunks])
                )
                self._ctx.agent_responses_meta.append(
                    GigaChatResponseMeta(
                        headers=GigaChatResponseMetaHeaders(**result.chunks[-1].x_headers),
                        created=result.chunks[-1].created,
                        model=result.chunks[-1].model,
                        usage=GigaChatResponseMetaUsage(
                            prompt_tokens = result.chunks[-1].usage.prompt_tokens,
                            completion_tokens = result.chunks[-1].usage.completion_tokens,
                            total_tokens = result.chunks[-1].usage.total_tokens,
                            precached_prompt_tokens = result.chunks[-1].usage.precached_prompt_tokens,
                        ),
                        finish_reason=result.chunks[-1].choices[0].finish_reason
                    )
                )
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
