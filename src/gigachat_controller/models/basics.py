from enum import StrEnum, auto
from pydantic import BaseModel, create_model, Field, ConfigDict
from typing import Optional, Any, Annotated

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
    x_request_id: Annotated[
        str | None,
        Field(description="GigaChat response x-request-id", alias="x-request-id")
    ] = None
    x_session_id: Annotated[
        str | None,
        Field(description="GigaChat response x-session-id", alias="x-session-id")
    ] = None
    x_client_id: Annotated[
        str | None,
        Field(description="GigaChat response x-client-id", alias="x-client-id")
    ] = None

class GigaChatResponseMetaUsage(BaseModel):
    prompt_tokens: Annotated[
        int | None,
        Field(description="GigaChat usage prompt_tokens")
    ] = None
    completion_tokens: Annotated[
        int | None,
        Field(description="GigaChat usage completion_tokens")
    ] = None
    total_tokens: Annotated[
        int | None,
        Field(description="GigaChat usage total_tokens")
    ] = None
    precached_prompt_tokens: Annotated[
        int | None,
        Field(description="GigaChat usage precached_prompt_tokens")
    ] = None

class GigaChatResponseMeta(BaseModel):
    headers: GigaChatResponseMetaHeaders = Field(default=GigaChatResponseMetaHeaders())
    created: int = Field(default=0)
    model: str = Field(default=str())
    usage: GigaChatResponseMetaUsage = Field(default=GigaChatResponseMetaUsage())
    finish_reason: str = Field(default=str())

class GigaChatControllerContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    last_error: Annotated[
        GigaChatControllerException | None,
        Field(description="Last GCC exception/error.")
    ] = None
    last_response: Annotated[
        Any | None,
        Field(description="Response model")
    ] = None
    last_agent_response: Annotated[
        str | None,
        Field(description="GigaChat response model")
    ] = None
    last_agent_response_meta: Annotated[
        GigaChatResponseMeta | None,
        Field(description="GigaChat response meta model")
    ] = None
