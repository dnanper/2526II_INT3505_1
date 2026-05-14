# Flask API Patterns Demo - Split App + Service

Bản này giả định bạn đã có `data.py`.

Cấu trúc đề xuất:

```txt
project/
├── app.py          # Route/controller
├── services.py     # Business logic + helpers
├── data.py         # Dữ liệu mẫu orders, users
└── requirements.txt
```

## Chạy

```bash
pip install -r requirements.txt
python app.py
```

## Test nhanh

```bash
curl "http://127.0.0.1:5000/api/orders?status=paid&sort=-amount&fields=id,status,amount&page=1&limit=5"
```

```bash
curl -X POST "http://127.0.0.1:5000/api/orders/1/pay"
```

## data.py mẫu

Nếu cần, `data.py` nên có dạng:

```python
orders = {
    1: {"id": 1, "user_id": 101, "status": "pending_payment", "amount": 150.0},
    2: {"id": 2, "user_id": 102, "status": "paid", "amount": 230.5},
}

users = {
    101: {"id": 101, "name": "An", "email": "an@example.com"},
    102: {"id": 102, "name": "Binh", "email": "binh@example.com"},
}
```
