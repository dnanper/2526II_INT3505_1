from pydantic import Field

from Buoi7.schemas.common import BaseSchema
from Buoi7.schemas.member import MemberSummarySchema


class BookCreateRequestSchema(BaseSchema):
    title: str = Field(min_length=1, max_length=200)
    isbn: str = Field(min_length=1, max_length=20)


class BookListItemSchema(BaseSchema):
    id: str
    title: str
    isbn: str
    is_available: bool


class BookDetailResponseSchema(BookListItemSchema):
    borrowed_by: MemberSummarySchema | None = None


class BookListEnvelopeSchema(BaseSchema):
    data: list[BookListItemSchema]


class BookDetailEnvelopeSchema(BaseSchema):
    data: BookDetailResponseSchema


class BookCreateResponseSchema(BaseSchema):
    message: str
    data: BookListItemSchema
