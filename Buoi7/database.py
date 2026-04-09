import os
from datetime import date, timedelta

from pymongo import ASCENDING, MongoClient
from pymongo.errors import DuplicateKeyError

from Buoi7.exceptions import AppError


MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("MONGODB_DATABASE", "library_buoi7")

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
database = client[DATABASE_NAME]

books_collection = database["books"]
members_collection = database["members"]
loans_collection = database["loans"]


def initialize_database() -> None:
    try:
        client.admin.command("ping")
        books_collection.create_index([("isbn", ASCENDING)], unique=True)
        members_collection.create_index([("email", ASCENDING)], unique=True)
        loans_collection.create_index([("member_id", ASCENDING)])
        loans_collection.create_index([("book_id", ASCENDING)])
        loans_collection.create_index(
            [("book_id", ASCENDING)],
            unique=True,
            partialFilterExpression={"returned_date": None},
            name="unique_active_book_loan",
        )
    except Exception as exc:
        raise AppError(f"MongoDB connection failed: {exc}", 500) from exc


def seed_database() -> None:
    initialize_database()
    if books_collection.count_documents({}, limit=1):
        print(
            f"MongoDB database already initialized: {DATABASE_NAME} ({MONGODB_URI})"
        )
        return

    books = [
        {"_id": f"book_{index}", "title": f"Python Architecture Book {index}", "isbn": f"ISBN-100{index}"}
        for index in range(1, 21)
    ]
    members = [
        {"_id": "member_1", "name": "Alice Nguyen", "email": "alice@example.com"},
        {"_id": "member_2", "name": "Bob Tran", "email": "bob@example.com"},
    ]

    today = date.today()
    loans = [
        {
            "_id": f"loan_{index}",
            "member_id": "member_1",
            "book_id": f"book_{index}",
            "borrow_date": today.isoformat(),
            "due_date": (today + timedelta(days=14)).isoformat(),
            "returned_date": None,
        }
        for index in range(1, 8)
    ]

    try:
        books_collection.insert_many(books)
        members_collection.insert_many(members)
        loans_collection.insert_many(loans)
    except DuplicateKeyError:
        pass

    print(f"MongoDB database seeded: {DATABASE_NAME} ({MONGODB_URI})")


def show_summary() -> None:
    initialize_database()
    print(f"MongoDB URI: {MONGODB_URI}")
    print(f"Database: {DATABASE_NAME}")
    print(f"Books: {books_collection.count_documents({})}")
    print(f"Members: {members_collection.count_documents({})}")
    print(f"Loans: {loans_collection.count_documents({})}")
