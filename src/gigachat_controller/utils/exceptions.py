from typing import Callable, Any, Dict
import functools

from gigachat_controller.models import (
    GigaChatControllerException,
    GigaChatControllerHttpException,
    GigaChatControllerHttpXException,
)

from gigachat.exceptions import (
    GigaChatException,
    AuthenticationError,
    RateLimitError,
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    RequestEntityTooLargeError,
    UnprocessableEntityError,
    ServerError,
)

from httpx import ConnectError

def _get_callable_info(func: Callable) -> Dict[str, Any]:
    """
    {
        'type': 'method' | 'function' | 'staticmethod' | 'classmethod' | 'unknown',
        'class_name': str | None,
        'func_name': str,
        'module': str,
        'instance': object | None
    }
    """
    info = {
        'func_name': getattr(func, '__name__', str(func)),
        'module': getattr(func, '__module__', ''),
        'class_name': None,
        'instance': None,
        'type': 'unknown'
    }
    raw_func = func
    if isinstance(func, staticmethod):
        info['type'] = 'staticmethod'
        raw_func = func.__func__
    elif isinstance(func, classmethod):
        info['type'] = 'classmethod'
        raw_func = func.__func__
    if hasattr(raw_func, '__self__'):
        instance = raw_func.__self__
        if isinstance(instance, type):
            info['type'] = 'classmethod'
            info['class_name'] = instance.__name__
            info['instance'] = instance
        else:
            info['type'] = 'method'
            info['class_name'] = type(instance).__name__
            info['instance'] = instance
        info['func_name'] = raw_func.__func__.__name__ if hasattr(raw_func, '__func__') else raw_func.__name__
    else:
        qualname = getattr(raw_func, '__qualname__', raw_func.__name__)
        if '.' in qualname:
            class_part, func_part = qualname.rsplit('.', 1)
            info['class_name'] = class_part
            info['func_name'] = func_part
        else:
            info['func_name'] = qualname
        info['type'] = 'function'
    return info

def _get_exception(e: Exception, info: Dict[str, Any]) -> GigaChatControllerException:
    if isinstance(e, ConnectError):
        return GigaChatControllerHttpXException(e, code=42, method=info)
    elif isinstance(e, BadRequestError):
        return GigaChatControllerHttpException(e, code=400, method=info)
    elif isinstance(e, AuthenticationError):
        return GigaChatControllerHttpException(e, code=401, method=info)
    elif isinstance(e, ForbiddenError):
        return GigaChatControllerHttpException(e, code=403, method=info)
    elif isinstance(e, NotFoundError):
        return GigaChatControllerHttpException(e, code=404, method=info)
    elif isinstance(e, RequestEntityTooLargeError):
        return GigaChatControllerHttpException(e, code=413, method=info)
    elif isinstance(e, UnprocessableEntityError):
        return GigaChatControllerHttpException(e, code=422, method=info)
    elif isinstance(e, RateLimitError):
        return GigaChatControllerHttpException(e, code=429, method=info)
    elif isinstance(e, ServerError):
        return GigaChatControllerHttpException(e, code=500, method=info)
    else:
        return GigaChatControllerException(e, code=-1, method=info)
