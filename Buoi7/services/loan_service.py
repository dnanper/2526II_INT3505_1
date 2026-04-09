from datetime import date, timedelta

from pymongo.errors import DuplicateKeyError

from Buoi7.database import books_collection, loans_collection, members_collection
from Buoi7.exceptions import AppError
from Buoi7.mappers.book_mapper import book_document_to_entity
from Buoi7.mappers.loan_mapper import (
    loan_document_to_entity,
    loan_entity_to_document,
    loan_entity_to_response,
    loan_request_to_entity,
)
from Buoi7.mappers.member_mapper import member_document_to_entity
from Buoi7.schemas.loan import (
    LoanCreateRequestSchema,
    LoanDetailEnvelopeSchema,
    LoanListEnvelopeSchema,
    LoanWriteEnvelopeSchema,
)
from Buoi7.utils import generate_entity_id


class LoanService:
    def list_member_loans(
        self,
        *,
        member_id: str,
    ) -> LoanListEnvelopeSchema:
        member_document = members_collection.find_one({"_id": member_id})
        if not member_document:
            raise AppError("Member not found", 404)

        documents = list(
            loans_collection.find({"member_id": member_id})
            .sort("borrow_date", -1)
        )

        member_entity = member_document_to_entity(member_document)
        data = []
        for document in documents:
            loan_entity = loan_document_to_entity(document)
            book_document = books_collection.find_one({"_id": loan_entity.book_id})
            book_title = book_document["title"] if book_document else None
            data.append(
                loan_entity_to_response(
                    loan_entity,
                    member_name=member_entity.name,
                    book_title=book_title,
                )
            )

        return LoanListEnvelopeSchema(data=data)

    def create_loan(
        self,
        *,
        member_id: str,
        payload: LoanCreateRequestSchema,
    ) -> LoanWriteEnvelopeSchema:
        member_document = members_collection.find_one({"_id": member_id})
        if not member_document:
            raise AppError("Member not found", 404)

        book_document = books_collection.find_one({"_id": payload.book_id})
        if not book_document:
            raise AppError("Book not found", 404)

        today = date.today()
        entity = loan_request_to_entity(
            payload,
            loan_id=generate_entity_id("loan"),
            member_id=member_id,
            borrow_date=today,
            due_date=today + timedelta(days=14),
        )

        try:
            loans_collection.insert_one(loan_entity_to_document(entity))
        except DuplicateKeyError as exc:
            raise AppError("Book is currently borrowed", 409) from exc

        member_entity = member_document_to_entity(member_document)
        book_entity = book_document_to_entity(book_document)
        return LoanWriteEnvelopeSchema(
            message="Loan created successfully",
            data=loan_entity_to_response(
                entity,
                member_name=member_entity.name,
                book_title=book_entity.title,
            ),
        )

    def get_loan_detail(self, loan_id: str) -> LoanDetailEnvelopeSchema:
        document = loans_collection.find_one({"_id": loan_id})
        if not document:
            raise AppError("Loan not found", 404)

        loan_entity = loan_document_to_entity(document)
        member_document = members_collection.find_one({"_id": loan_entity.member_id})
        book_document = books_collection.find_one({"_id": loan_entity.book_id})

        member_name = member_document["name"] if member_document else None
        book_title = book_document["title"] if book_document else None
        return LoanDetailEnvelopeSchema(
            data=loan_entity_to_response(
                loan_entity,
                member_name=member_name,
                book_title=book_title,
            )
        )

    def return_loan(self, loan_id: str) -> LoanWriteEnvelopeSchema:
        document = loans_collection.find_one({"_id": loan_id})
        if not document:
            raise AppError("Loan not found", 404)

        loan_entity = loan_document_to_entity(document)
        if loan_entity.returned_date:
            raise AppError("Loan already returned", 409)

        returned_date = date.today()
        loans_collection.update_one(
            {"_id": loan_id},
            {"$set": {"returned_date": returned_date.isoformat()}},
        )

        updated_entity = loan_document_to_entity(
            {**document, "returned_date": returned_date.isoformat()}
        )
        member_document = members_collection.find_one({"_id": updated_entity.member_id})
        book_document = books_collection.find_one({"_id": updated_entity.book_id})

        member_name = member_document["name"] if member_document else None
        book_title = book_document["title"] if book_document else None
        return LoanWriteEnvelopeSchema(
            message="Loan returned successfully",
            data=loan_entity_to_response(
                updated_entity,
                member_name=member_name,
                book_title=book_title,
            ),
        )
