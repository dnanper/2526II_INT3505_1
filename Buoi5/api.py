from datetime import date, timedelta

from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

try:
    from .main import DB_PATH, SessionLocal, initialize_database, seed_database
    from .models import Book, Loan, Member
except ImportError:
    from main import DB_PATH, SessionLocal, initialize_database, seed_database
    from models import Book, Loan, Member


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


def parse_pagination(default_limit=10, max_limit=100):
    try:
        limit = int(request.args.get("limit", default_limit))
        offset = int(request.args.get("offset", 0))
    except (TypeError, ValueError):
        return None, None, error_response("Invalid pagination parameters", 400)

    if limit < 1 or offset < 0:
        return None, None, error_response("limit must be >= 1 and offset must be >= 0", 400)

    return min(limit, max_limit), offset, None


def create_app():
    app = Flask(__name__)
    initialize_database()
    seed_database()

    @app.get("/")
    def index():
        return jsonify(
            {
                "message": "Library API is running",
                "endpoints": {
                    "health": "/api/v1/health",
                    "books": "/api/v1/books",
                    "members": "/api/v1/members",
                    "member_loans": "/api/v1/members/<member_id>/loans",
                    "loan_return": "/api/v1/loans/<loan_id>/return",
                },
            }
        )

    @app.get("/api/v1/health")
    def health_check():
        return jsonify({"status": "ok", "database": str(DB_PATH)})

    @app.get("/api/v1/books")
    def get_books():
        limit, offset, error = parse_pagination()
        if error:
            return error

        session = SessionLocal()
        try:
            total_books = session.query(Book).count()
            books = session.query(Book).offset(offset).limit(limit).all()

            data = []
            for book in books:
                active_loan = (
                    session.query(Loan)
                    .filter(Loan.book_id == book.id, Loan.returned_date.is_(None))
                    .first()
                )
                book_data = book.to_dto()
                book_data["is_available"] = active_loan is None
                data.append(book_data)

            return jsonify(
                {
                    "metadata": {
                        "total": total_books,
                        "limit": limit,
                        "offset": offset,
                        "has_next": (offset + limit) < total_books,
                    },
                    "data": data,
                }
            )
        finally:
            session.close()

    @app.post("/api/v1/books")
    def create_book():
        payload = request.get_json(silent=True) or {}
        title = (payload.get("title") or "").strip()
        isbn = (payload.get("isbn") or "").strip()

        if not title or not isbn:
            return error_response("title and isbn are required", 400)

        session = SessionLocal()
        try:
            book = Book(title=title, isbn=isbn)
            session.add(book)
            session.commit()
            session.refresh(book)
            return (
                jsonify({"message": "Book created successfully", "data": book.to_dto()}),
                201,
            )
        except IntegrityError:
            session.rollback()
            return error_response("isbn already exists", 409)
        finally:
            session.close()

    @app.get("/api/v1/books/<int:book_id>")
    def get_book_detail(book_id):
        session = SessionLocal()
        try:
            book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                return error_response("Book not found", 404)

            active_loan = (
                session.query(Loan)
                .options(joinedload(Loan.member))
                .filter(Loan.book_id == book.id, Loan.returned_date.is_(None))
                .first()
            )

            data = book.to_dto()
            data["is_available"] = active_loan is None
            data["borrowed_by"] = active_loan.member.to_dto() if active_loan else None
            return jsonify({"data": data})
        finally:
            session.close()

    @app.get("/api/v1/members")
    def get_members():
        limit, offset, error = parse_pagination()
        if error:
            return error

        session = SessionLocal()
        try:
            total_members = session.query(Member).count()
            members = session.query(Member).offset(offset).limit(limit).all()

            data = []
            for member in members:
                member_data = member.to_dto()
                member_data["active_loans"] = (
                    session.query(Loan)
                    .filter(Loan.member_id == member.id, Loan.returned_date.is_(None))
                    .count()
                )
                data.append(member_data)

            return jsonify(
                {
                    "metadata": {
                        "total": total_members,
                        "limit": limit,
                        "offset": offset,
                        "has_next": (offset + limit) < total_members,
                    },
                    "data": data,
                }
            )
        finally:
            session.close()

    @app.get("/api/v1/members/<int:member_id>")
    def get_member_detail(member_id):
        session = SessionLocal()
        try:
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                return error_response("Member not found", 404)

            data = member.to_dto()
            data["active_loans"] = (
                session.query(Loan)
                .filter(Loan.member_id == member.id, Loan.returned_date.is_(None))
                .count()
            )
            return jsonify({"data": data})
        finally:
            session.close()

    @app.get("/api/v1/members/<int:member_id>/loans")
    def get_member_loans(member_id):
        limit, offset, error = parse_pagination(default_limit=5)
        if error:
            return error

        session = SessionLocal()
        try:
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                return error_response("Member not found", 404)

            total_loans = session.query(Loan).filter(Loan.member_id == member_id).count()
            loans = (
                session.query(Loan)
                .options(joinedload(Loan.book), joinedload(Loan.member))
                .filter(Loan.member_id == member_id)
                .offset(offset)
                .limit(limit)
                .all()
            )

            return jsonify(
                {
                    "metadata": {
                        "total": total_loans,
                        "limit": limit,
                        "offset": offset,
                        "has_next": (offset + limit) < total_loans,
                    },
                    "data": [loan.to_dto() for loan in loans],
                }
            )
        finally:
            session.close()

    @app.post("/api/v1/members/<int:member_id>/loans")
    def create_loan(member_id):
        payload = request.get_json(silent=True) or {}
        book_id = payload.get("book_id")

        if not book_id:
            return error_response("book_id is required", 400)

        session = SessionLocal()
        try:
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                return error_response("Member not found", 404)

            book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                return error_response("Book not found", 404)

            active_loan = (
                session.query(Loan)
                .filter(Loan.book_id == book_id, Loan.returned_date.is_(None))
                .first()
            )
            if active_loan:
                return error_response("Book is currently borrowed", 409)

            new_loan = Loan(
                member_id=member_id,
                book_id=book_id,
                borrow_date=date.today(),
                due_date=date.today() + timedelta(days=14),
            )
            session.add(new_loan)
            session.commit()
            session.refresh(new_loan)

            created_loan = (
                session.query(Loan)
                .options(joinedload(Loan.book), joinedload(Loan.member))
                .filter(Loan.id == new_loan.id)
                .first()
            )

            return (
                jsonify(
                    {
                        "message": "Loan created successfully",
                        "data": created_loan.to_dto(),
                    }
                ),
                201,
            )
        finally:
            session.close()

    @app.get("/api/v1/loans/<int:loan_id>")
    def get_loan_detail(loan_id):
        session = SessionLocal()
        try:
            loan = (
                session.query(Loan)
                .options(joinedload(Loan.book), joinedload(Loan.member))
                .filter(Loan.id == loan_id)
                .first()
            )
            if not loan:
                return error_response("Loan not found", 404)

            return jsonify({"data": loan.to_dto()})
        finally:
            session.close()

    @app.post("/api/v1/loans/<int:loan_id>/return")
    def return_loan(loan_id):
        session = SessionLocal()
        try:
            loan = (
                session.query(Loan)
                .options(joinedload(Loan.book), joinedload(Loan.member))
                .filter(Loan.id == loan_id)
                .first()
            )
            if not loan:
                return error_response("Loan not found", 404)
            if loan.returned_date:
                return error_response("Loan already returned", 409)

            loan.returned_date = date.today()
            session.commit()
            session.refresh(loan)

            return jsonify({"message": "Loan returned successfully", "data": loan.to_dto()})
        finally:
            session.close()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
