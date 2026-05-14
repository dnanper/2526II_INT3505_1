from typing import Any, Dict

orders: Dict[int, Dict[str, Any]] = {
    1: {"id": 1, "user_id": 101, "status": "pending_payment", "amount": 150.0},
    2: {"id": 2, "user_id": 102, "status": "paid", "amount": 230.5},
    3: {"id": 3, "user_id": 101, "status": "cancelled", "amount": 99.0},
}

users: Dict[int, Dict[str, Any]] = {
    101: {"id": 101, "name": "An", "email": "an@example.com"},
    102: {"id": 102, "name": "Binh", "email": "binh@example.com"},
}
