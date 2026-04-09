from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class LoanEntity:
    id: str
    member_id: str
    book_id: str
    borrow_date: date
    due_date: date
    returned_date: date | None = None
