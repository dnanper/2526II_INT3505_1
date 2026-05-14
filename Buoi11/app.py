"""
Flask API Design Patterns Demo

File này chỉ giữ phần route/controller.
Logic xử lý được tách sang services.py.
Dữ liệu mẫu nằm trong data.py của bạn.

Run:
  pip install flask
  python app.py
"""

import json

from flask import Flask, jsonify, request

from services import (
    accept_webhook_event,
    cancel_order_service,
    create_order_service,
    delete_order_service,
    get_order_service,
    graphql_lite_service,
    list_event_queue,
    list_orders_service,
    mark_order_paid_and_build_event,
    sign_payload,
    update_order_service,
)

app = Flask(__name__)


@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"})


# -----------------------------------------------------------------------------
# CRUD + Query Pattern
# -----------------------------------------------------------------------------


@app.get("/api/orders")
def list_orders():
    """
    Query examples:
      /api/orders?status=paid
      /api/orders?sort=-amount
      /api/orders?fields=id,status,amount
      /api/orders?page=1&limit=2
    """
    response = list_orders_service(
        args=request.args,
        full_path=request.full_path.rstrip("?"),
    )
    return jsonify(response)


@app.post("/api/orders")
def create_order():
    """
    Create order with optional Idempotency-Key header.
    Try sending the same request twice with the same Idempotency-Key.
    """
    body = request.get_json(force=True)
    idem_key = request.headers.get("Idempotency-Key")

    response, status_code = create_order_service(body, idem_key)
    return jsonify(response), status_code


@app.get("/api/orders/<int:order_id>")
def get_order(order_id: int):
    response, status_code = get_order_service(order_id)
    return jsonify(response), status_code


@app.patch("/api/orders/<int:order_id>")
def update_order(order_id: int):
    body = request.get_json(force=True)

    response, status_code = update_order_service(order_id, body)
    return jsonify(response), status_code


@app.delete("/api/orders/<int:order_id>")
def delete_order(order_id: int):
    response, status_code = delete_order_service(order_id)
    return jsonify(response), status_code


@app.post("/api/orders/<int:order_id>/cancel")
def cancel_order(order_id: int):
    response, status_code = cancel_order_service(order_id)
    return jsonify(response), status_code


# -----------------------------------------------------------------------------
# Event-driven + Webhook Pattern
# -----------------------------------------------------------------------------


@app.post("/api/orders/<int:order_id>/pay")
def pay_order(order_id: int):
    """
    Simulate Payment service finishing payment, then pushing a webhook
    to Notification service.
    """
    response, status_code = mark_order_paid_and_build_event(order_id)

    if status_code != 200:
        return jsonify(response), status_code

    event = response["event"]
    raw_body = json.dumps(event, separators=(",", ":")).encode()
    signature = sign_payload(raw_body)

    # Internal HTTP call via Flask test client to keep demo dependency-free.
    # In real world, Payment service would HTTP POST to Notification service URL.
    with app.test_client() as client:
        webhook_response = client.post(
            "/notify-webhook",
            data=raw_body,
            content_type="application/json",
            headers={"x-signature": signature},
        )

    return jsonify(
        {
            "order": response["order"],
            "webhook_delivery": {
                "status_code": webhook_response.status_code,
                "response": webhook_response.get_json(),
            },
        }
    )


@app.post("/notify-webhook")
def notify_webhook():
    """
    Notification service endpoint:
    1. Receives HTTP POST
    2. Verifies HMAC signature
    3. Returns 200 quickly
    4. Processes event asynchronously
    """
    raw_body = request.get_data()
    signature = request.headers.get("x-signature")

    response, status_code = accept_webhook_event(raw_body, signature)
    return jsonify(response), status_code


@app.get("/internal/events")
def list_events():
    """Debug endpoint to see events pushed into the fake queue."""
    return jsonify(list_event_queue())


# -----------------------------------------------------------------------------
# GraphQL-like/BFF demo without installing GraphQL libraries
# -----------------------------------------------------------------------------


@app.post("/graphql-lite")
def graphql_lite():
    """
    A tiny GraphQL-like endpoint: client asks for specific fields.

    Request body:
    {
      "order_id": 1,
      "order_fields": ["id", "status", "amount"],
      "user_fields": ["name", "email"]
    }
    """
    body = request.get_json(force=True)

    response, status_code = graphql_lite_service(body)
    return jsonify(response), status_code


if __name__ == "__main__":
    app.run(debug=True, port=5000)
