from enum import StrEnum, auto
from pydantic import BaseModel, create_model, Field, ConfigDict
from typing import Optional, Any, Annotated, List, Optional

from gigachat.models import (
    ChatCompletionChunk,
)

from .exceptions import GigaChatControllerException

class BasicConfigField(StrEnum):
    base_url = auto()
    auth_url = auto()
    credentials = auto()
    scope = auto()
    access_token = auto()
    model = auto()
    profanity_check = auto()
    user = auto()
    password = auto()
    timeout = auto()
    verify_ssl_certs = auto()
    ca_bundle_file = auto()
    cert_file = auto()
    key_file = auto()
    key_file_password = auto()
    ssl_context = auto()
    flags = auto()
    max_connections = auto()
    max_retries = auto()
    retry_backoff_factor = auto()
    retry_on_status_codes = auto()

def _create_config_instance(data: Dict[str, Any] = None) -> BaseModel:
    if data is None: data = {}
    BasicConfig = create_model('BasicConfig', __config__=dict(extra='ignore'), **{field.value: (Optional[Any], None) for field in BasicConfigField})
    return BasicConfig(**data)

class GigaChatResponseMetaHeaders(BaseModel):
    x_request_id: Optional[str] = Field(
        description="GigaChat response x-request-id",
        alias="x-request-id",
        default_factory=str
    )
    x_session_id: Optional[str] = Field(
        description="GigaChat response x-session-id",
        alias="x-session-id",
        default_factory=str
    )
    x_client_id: Optional[str] = Field(
        description="GigaChat response x-client-id",
        alias="x-client-id",
        default_factory=str
    )

class GigaChatResponseMetaUsage(BaseModel):
    prompt_tokens: Optional[int] = Field(
        description="GigaChat usage prompt_tokens",
        default=0
    )
    completion_tokens: Optional[int] = Field(
        description="GigaChat usage completion_tokens",
        default=0
    )
    total_tokens: Optional[int] = Field(
        description="GigaChat usage total_tokens",
        default=0
    )
    precached_prompt_tokens: Optional[int] = Field(
        description="GigaChat usage precached_prompt_tokens",
        default=0
    )

class GigaChatResponseMeta(BaseModel):
    headers: GigaChatResponseMetaHeaders = Field(default=GigaChatResponseMetaHeaders())
    created: int = Field(default=0)
    model: str = Field(default=str())
    usage: GigaChatResponseMetaUsage = Field(default=GigaChatResponseMetaUsage())
    finish_reason: str = Field(default=str())

class GigaChatStreamResponse(BaseModel):
    chunks: List[ChatCompletionChunk] = Field(default=list())

class GigaChatControllerContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    last_error: GigaChatControllerException = Field(
        description="Last GCC exception/error.",
        default=None,
    )
    last_response: Any = Field(
        description="Response model",
        default=None
    )
    agent_responses: Optional[List[str]] = Field(
        description="GigaChat response model",
        default_factory=list
    )
    agent_responses_meta: Optional[List[GigaChatResponseMeta]] = Field(
        description="GigaChat response meta model",
        default_factory=list
    )
