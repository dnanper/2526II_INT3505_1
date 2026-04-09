from dataclasses import dataclass


@dataclass(slots=True)
class BookEntity:
    id: str
    title: str
    isbn: str
