from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Book, User

DB_PATH = "sqlite:///library.db"


def get_engine(db_path=DB_PATH):
    # check_same_thread=False cần thiết cho SQLite trong web framework để tránh lỗi Thread
    return create_engine(db_path, connect_args={"check_same_thread": False})


def init_db(db_path=DB_PATH):
    engine = get_engine(db_path)
    # Sinh các bảng trong CSDL
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Thêm dữ liệu mẫu nếu bảng books rỗng
    if session.query(Book).count() == 0:
        session.add_all(
            [
                Book(
                    title="To Kill a Mockingbird",
                    author="Harper Lee",
                    published_year=1960,
                ),
                Book(title="1984", author="George Orwell", published_year=1949),
                Book(
                    title="The Great Gatsby",
                    author="F. Scott Fitzgerald",
                    published_year=1925,
                ),
            ]
        )

    # Thêm dữ liệu mẫu nếu bảng users rỗng
    if session.query(User).count() == 0:
        session.add_all(
            [
                User(name="Alice", email="alice@example.com"),
                User(name="Bob", email="bob@example.com"),
            ]
        )

    session.commit()
    session.close()
