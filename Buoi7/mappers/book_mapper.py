from Buoi7.entities import BookEntity, MemberEntity
from Buoi7.schemas.book import (
    BookCreateRequestSchema,
    BookDetailResponseSchema,
    BookListItemSchema,
)
from Buoi7.schemas.member import MemberSummarySchema


def book_request_to_entity(schema: BookCreateRequestSchema, book_id: str) -> BookEntity:
    return BookEntity(id=book_id, title=schema.title, isbn=schema.isbn)


def book_entity_to_document(entity: BookEntity) -> dict:
    return {"_id": entity.id, "title": entity.title, "isbn": entity.isbn}


def book_document_to_entity(document: dict) -> BookEntity:
    return BookEntity(
        id=document["_id"],
        title=document["title"],
        isbn=document["isbn"],
    )


def book_entity_to_list_item(
    entity: BookEntity,
    *,
    is_available: bool,
) -> BookListItemSchema:
    return BookListItemSchema(
        id=entity.id,
        title=entity.title,
        isbn=entity.isbn,
        is_available=is_available,
    )


def book_entity_to_response(
    entity: BookEntity,
    *,
    is_available: bool,
    borrowed_by: MemberEntity | None = None,
) -> BookDetailResponseSchema:
    borrowed_by_schema = None
    if borrowed_by:
        borrowed_by_schema = MemberSummarySchema(
            id=borrowed_by.id,
            name=borrowed_by.name,
            email=borrowed_by.email,
        )

    return BookDetailResponseSchema(
        id=entity.id,
        title=entity.title,
        isbn=entity.isbn,
        is_available=is_available,
        borrowed_by=borrowed_by_schema,
    )
