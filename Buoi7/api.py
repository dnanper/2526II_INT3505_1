from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from flask import Flask, jsonify, request
from pydantic import ValidationError

from Buoi7.database import DATABASE_NAME, seed_database
from Buoi7.exceptions import AppError
from Buoi7.schemas.book import BookCreateRequestSchema
from Buoi7.schemas.common import (
    ErrorResponseSchema,
    HealthResponseSchema,
    IndexResponseSchema,
)
from Buoi7.schemas.loan import LoanCreateRequestSchema
from Buoi7.services import BookService, LoanService, MemberService


def error_response(message: str, status_code: int):
    payload = ErrorResponseSchema(error=message)
    return jsonify(payload.model_dump(mode="json")), status_code


def parse_request(schema_class):
    payload = request.get_json(silent=True) or {}
    try:
        return schema_class.model_validate(payload)
    except ValidationError as exc:
        first_error = exc.errors()[0]
        message = first_error.get("msg", "Invalid request body")
        location = ".".join(str(item) for item in first_error.get("loc", []))
        if location:
            message = f"{location}: {message}"
        raise AppError(message, 400) from exc


def success_response(schema, status_code: int = 200):
    return jsonify(schema.model_dump(mode="json")), status_code


def create_app() -> Flask:
    app = Flask(__name__)
    seed_database()

    book_service = BookService()
    member_service = MemberService()
    loan_service = LoanService()

    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        return error_response(error.message, error.status_code)

    @app.get("/")
    def index():
        payload = IndexResponseSchema(
            message="Library API is running",
            endpoints={
                "health": "/api/v1/health",
                "books": "/api/v1/books",
                "members": "/api/v1/members",
                "member_loans": "/api/v1/members/<member_id>/loans",
                "loan_return": "/api/v1/loans/<loan_id>/return",
            },
        )
        return success_response(payload)

    @app.get("/api/v1/health")
    def health_check():
        payload = HealthResponseSchema(status="ok", database=DATABASE_NAME)
        return success_response(payload)

    @app.get("/api/v1/books")
    def get_books():
        return success_response(book_service.list_books())

    @app.post("/api/v1/books")
    def create_book():
        payload = parse_request(BookCreateRequestSchema)
        return success_response(book_service.create_book(payload), 201)

    @app.get("/api/v1/books/<string:book_id>")
    def get_book_detail(book_id: str):
        return success_response(book_service.get_book_detail(book_id))

    @app.get("/api/v1/members")
    def get_members():
        return success_response(member_service.list_members())

    @app.get("/api/v1/members/<string:member_id>")
    def get_member_detail(member_id: str):
        return success_response(member_service.get_member_detail(member_id))

    @app.get("/api/v1/members/<string:member_id>/loans")
    def get_member_loans(member_id: str):
        return success_response(loan_service.list_member_loans(member_id=member_id))

    @app.post("/api/v1/members/<string:member_id>/loans")
    def create_loan(member_id: str):
        payload = parse_request(LoanCreateRequestSchema)
        return success_response(
            loan_service.create_loan(member_id=member_id, payload=payload),
            201,
        )

    @app.get("/api/v1/loans/<string:loan_id>")
    def get_loan_detail(loan_id: str):
        return success_response(loan_service.get_loan_detail(loan_id))

    @app.post("/api/v1/loans/<string:loan_id>/return")
    def return_loan(loan_id: str):
        return success_response(loan_service.return_loan(loan_id))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
