from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    loans = relationship("Loan", back_populates="member")

    def to_dto(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)

    loans = relationship("Loan", back_populates="book")

    def to_dto(self):
        return {"id": self.id, "title": self.title, "isbn": self.isbn}


class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(Date, default=date.today)
    due_date = Column(Date, nullable=False)
    returned_date = Column(Date, nullable=True)

    member = relationship("Member", back_populates="loans")
    book = relationship("Book", back_populates="loans")

    def to_dto(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "borrow_date": self.borrow_date.isoformat() if self.borrow_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "returned_date": self.returned_date.isoformat()
            if self.returned_date
            else None,
            "status": "RETURNED" if self.returned_date else "BORROWED",
        }
