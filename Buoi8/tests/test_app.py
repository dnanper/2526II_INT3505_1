import sys
from pathlib import Path

import pytest

# Ensure imports work whether pytest is run from repo root or Buoi8 folder.
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = CURRENT_DIR.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import app as app_module
from database import init_db
from services import BookModel, UserModel


@pytest.fixture()
def client(tmp_path: Path):
    db_file = tmp_path / "test_library.db"
    db_url = f"sqlite:///{db_file.as_posix()}"

    init_db(db_url)
    app_module.book_model = BookModel(db_url)
    app_module.user_model = UserModel(db_url)
    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as test_client:
        yield test_client

    app_module.book_model.engine.dispose()
    app_module.user_model.engine.dispose()
    if db_file.exists():
        db_file.unlink()


def test_get_books_returns_list(client):
    response = client.get("/books")
    assert response.status_code == 200
    data = response.get_json()
    assert "books" in data
    assert isinstance(data["books"], list)


def test_create_and_get_book(client):
    create_response = client.post(
        "/books",
        json={"title": "Clean Code", "author": "Robert Martin", "published_year": 2008},
    )
    assert create_response.status_code == 201
    created = create_response.get_json()
    assert "id" in created

    get_response = client.get(f"/books/{created['id']}")
    assert get_response.status_code == 200
    detail = get_response.get_json()
    assert detail["title"] == "Clean Code"


def test_create_duplicate_user_email_returns_400(client):
    first = client.post("/users", json={"name": "A", "email": "a@example.com"})
    assert first.status_code == 201

    duplicate = client.post("/users", json={"name": "B", "email": "a@example.com"})
    assert duplicate.status_code == 400
    assert "error" in duplicate.get_json()
