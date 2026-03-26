from datetime import date, timedelta
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    from .models import Base, Book, Loan, Member
except ImportError:
    from models import Base, Book, Loan, Member


DB_PATH = Path(__file__).with_name("library.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def initialize_database():
    Base.metadata.create_all(bind=engine)


def seed_database():
    initialize_database()
    session = SessionLocal()

    try:
        if session.query(Book).first():
            print(f"Database already initialized at: {DB_PATH}")
            return

        for i in range(1, 21):
            session.add(Book(title=f"Python Architecture Book {i}", isbn=f"ISBN-100{i}"))

        session.add(Member(name="Alice Nguyen", email="alice@example.com"))
        session.add(Member(name="Bob Tran", email="bob@example.com"))
        session.commit()

        for i in range(1, 8):
            session.add(
                Loan(
                    member_id=1,
                    book_id=i,
                    due_date=date.today() + timedelta(days=14),
                )
            )
        session.commit()

        print(f"Database seeded with mock data at: {DB_PATH}")
    finally:
        session.close()


def show_summary():
    session = SessionLocal()

    try:
        print(f"SQLite database: {DB_PATH}")
        print(f"Books: {session.query(Book).count()}")
        print(f"Members: {session.query(Member).count()}")
        print(f"Loans: {session.query(Loan).count()}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
    show_summary()
