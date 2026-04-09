from pydantic import Field, field_validator

from Buoi7.schemas.common import BaseSchema


class MemberSummarySchema(BaseSchema):
    id: str
    name: str
    email: str


class MemberListItemSchema(MemberSummarySchema):
    active_loans: int = Field(ge=0)


class MemberDetailResponseSchema(MemberListItemSchema):
    pass


class MemberListEnvelopeSchema(BaseSchema):
    data: list[MemberListItemSchema]


class MemberDetailEnvelopeSchema(BaseSchema):
    data: MemberDetailResponseSchema


class MemberCreateRequestSchema(BaseSchema):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=100)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("email must be a valid email address")
        return value.lower()
