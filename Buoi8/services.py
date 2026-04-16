from sqlalchemy.orm import sessionmaker

from database import DB_PATH, get_engine
from models import Book, User
from sqlalchemy.exc import IntegrityError


class BookModel:
    def __init__(self, db_path=DB_PATH):
        self.engine = get_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)

    def get_all(self):
        with self.Session() as session:
            return [b.to_dict() for b in session.query(Book).all()]

    def get_by_id(self, book_id):
        with self.Session() as session:
            book = session.query(Book).filter(Book.id == book_id).first()
            return book.to_dict() if book else None

    def add(self, title, author, published_year=None):
        if not title or not author:
            raise ValueError("Title and author are required")
        with self.Session() as session:
            new_book = Book(title=title, author=author, published_year=published_year)
            session.add(new_book)
            session.commit()
            return new_book.to_dict()

    def update(self, book_id, update_data):
        with self.Session() as session:
            book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                return None

            if "title" in update_data:
                book.title = update_data["title"]
            if "author" in update_data:
                book.author = update_data["author"]
            if "published_year" in update_data:
                book.published_year = update_data["published_year"]

            session.commit()
            return book.to_dict()

    def delete(self, book_id):
        with self.Session() as session:
            book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                return False
            session.delete(book)
            session.commit()
            return True


class UserModel:
    def __init__(self, db_path=DB_PATH):
        self.engine = get_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)

    def get_all(self):
        with self.Session() as session:
            return [u.to_dict() for u in session.query(User).all()]

    def get_by_id(self, user_id):
        with self.Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            return user.to_dict() if user else None

    def add(self, name, email):
        if not name or not email:
            raise ValueError("Name and email are required")
        with self.Session() as session:
            new_user = User(name=name, email=email)
            session.add(new_user)
            try:
                session.commit()
                return new_user.to_dict()
            except IntegrityError:
                session.rollback()
                raise ValueError("Email already exists")

    def delete(self, user_id):
        with self.Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            session.delete(user)
            session.commit()
            return True
