from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class ErrorResponseSchema(BaseSchema):
    error: str


class HealthResponseSchema(BaseSchema):
    status: str
    database: str


class IndexResponseSchema(BaseSchema):
    message: str
    endpoints: dict[str, str]
