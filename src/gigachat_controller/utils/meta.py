from typing import Tuple

from gigachat.models import (
    ChatCompletion,
)

from gigachat_controller.models import (
    GigaChatResponseMeta,
    GigaChatResponseMetaHeaders,
    GigaChatResponseMetaUsage,
    GigaChatStreamResponse,
)

def _get_chat_completion(chat_completion: ChatCompletion) -> Tuple[str, GigaChatResponseMeta]:
    _text = chat_completion.choices[0].message.content
    _meta = GigaChatResponseMeta(
        headers=GigaChatResponseMetaHeaders(**chat_completion.x_headers),
        created=chat_completion.created,
        model=chat_completion.model,
        usage=GigaChatResponseMetaUsage(
            prompt_tokens = chat_completion.usage.prompt_tokens,
            completion_tokens = chat_completion.usage.completion_tokens,
            total_tokens = chat_completion.usage.total_tokens,
            precached_prompt_tokens = chat_completion.usage.precached_prompt_tokens,
        ),
        finish_reason=chat_completion.choices[0].finish_reason
    )
    return _text, _meta

def _get_stream(stream: GigaChatStreamResponse) -> Tuple[str, GigaChatResponseMeta]:
    _text = "".join([chunk.choices[0].delta.content for chunk in stream.chunks])
    _meta = GigaChatResponseMeta(
        headers=GigaChatResponseMetaHeaders(**stream.chunks[-1].x_headers),
        created=stream.chunks[-1].created,
        model=stream.chunks[-1].model,
        usage=GigaChatResponseMetaUsage(
            prompt_tokens = stream.chunks[-1].usage.prompt_tokens,
            completion_tokens = stream.chunks[-1].usage.completion_tokens,
            total_tokens = stream.chunks[-1].usage.total_tokens,
            precached_prompt_tokens = stream.chunks[-1].usage.precached_prompt_tokens,
        ),
        finish_reason=stream.chunks[-1].choices[0].finish_reason
    )
    return _text, _meta
