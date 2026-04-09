from pymongo.errors import DuplicateKeyError

from Buoi7.database import books_collection, loans_collection, members_collection
from Buoi7.exceptions import AppError
from Buoi7.mappers.book_mapper import (
    book_document_to_entity,
    book_entity_to_document,
    book_entity_to_list_item,
    book_entity_to_response,
    book_request_to_entity,
)
from Buoi7.mappers.member_mapper import member_document_to_entity
from Buoi7.schemas.book import (
    BookCreateRequestSchema,
    BookCreateResponseSchema,
    BookDetailEnvelopeSchema,
    BookListEnvelopeSchema,
)
from Buoi7.utils import generate_entity_id


class BookService:
    def list_books(self) -> BookListEnvelopeSchema:
        documents = list(books_collection.find().sort("title", 1))

        data = []
        for document in documents:
            entity = book_document_to_entity(document)
            is_available = not loans_collection.find_one(
                {"book_id": entity.id, "returned_date": None}
            )
            data.append(book_entity_to_list_item(entity, is_available=is_available))

        return BookListEnvelopeSchema(data=data)

    def create_book(
        self,
        payload: BookCreateRequestSchema,
    ) -> BookCreateResponseSchema:
        entity = book_request_to_entity(payload, generate_entity_id("book"))

        try:
            books_collection.insert_one(book_entity_to_document(entity))
        except DuplicateKeyError as exc:
            raise AppError("isbn already exists", 409) from exc

        return BookCreateResponseSchema(
            message="Book created successfully",
            data=book_entity_to_list_item(entity, is_available=True),
        )

    def get_book_detail(self, book_id: str) -> BookDetailEnvelopeSchema:
        document = books_collection.find_one({"_id": book_id})
        if not document:
            raise AppError("Book not found", 404)

        entity = book_document_to_entity(document)
        active_loan = loans_collection.find_one({"book_id": book_id, "returned_date": None})
        borrowed_by = None
        if active_loan:
            member_document = members_collection.find_one({"_id": active_loan["member_id"]})
            if member_document:
                borrowed_by = member_document_to_entity(member_document)

        return BookDetailEnvelopeSchema(
            data=book_entity_to_response(
                entity,
                is_available=active_loan is None,
                borrowed_by=borrowed_by,
            )
        )
