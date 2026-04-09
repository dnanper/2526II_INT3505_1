from datetime import date
from typing import Literal

from pydantic import Field

from Buoi7.schemas.common import BaseSchema


class LoanCreateRequestSchema(BaseSchema):
    book_id: str = Field(min_length=1)


class LoanResponseSchema(BaseSchema):
    id: str
    member_id: str
    book_id: str
    member_name: str | None = None
    book_title: str | None = None
    borrow_date: date
    due_date: date
    returned_date: date | None = None
    status: Literal["BORROWED", "RETURNED"]


class LoanListEnvelopeSchema(BaseSchema):
    data: list[LoanResponseSchema]


class LoanDetailEnvelopeSchema(BaseSchema):
    data: LoanResponseSchema


class LoanWriteEnvelopeSchema(BaseSchema):
    message: str
    data: LoanResponseSchema
