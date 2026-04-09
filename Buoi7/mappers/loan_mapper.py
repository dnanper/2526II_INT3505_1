from datetime import date

from Buoi7.entities import LoanEntity
from Buoi7.schemas.loan import LoanCreateRequestSchema, LoanResponseSchema


def loan_request_to_entity(
    schema: LoanCreateRequestSchema,
    *,
    loan_id: str,
    member_id: str,
    borrow_date: date,
    due_date: date,
) -> LoanEntity:
    return LoanEntity(
        id=loan_id,
        member_id=member_id,
        book_id=schema.book_id,
        borrow_date=borrow_date,
        due_date=due_date,
        returned_date=None,
    )


def loan_entity_to_document(entity: LoanEntity) -> dict:
    return {
        "_id": entity.id,
        "member_id": entity.member_id,
        "book_id": entity.book_id,
        "borrow_date": entity.borrow_date.isoformat(),
        "due_date": entity.due_date.isoformat(),
        "returned_date": entity.returned_date.isoformat()
        if entity.returned_date
        else None,
    }


def loan_document_to_entity(document: dict) -> LoanEntity:
    returned_date = document.get("returned_date")
    return LoanEntity(
        id=document["_id"],
        member_id=document["member_id"],
        book_id=document["book_id"],
        borrow_date=date.fromisoformat(document["borrow_date"]),
        due_date=date.fromisoformat(document["due_date"]),
        returned_date=date.fromisoformat(returned_date) if returned_date else None,
    )


def loan_entity_to_response(
    entity: LoanEntity,
    *,
    member_name: str | None = None,
    book_title: str | None = None,
) -> LoanResponseSchema:
    return LoanResponseSchema(
        id=entity.id,
        member_id=entity.member_id,
        book_id=entity.book_id,
        member_name=member_name,
        book_title=book_title,
        borrow_date=entity.borrow_date,
        due_date=entity.due_date,
        returned_date=entity.returned_date,
        status="RETURNED" if entity.returned_date else "BORROWED",
    )
