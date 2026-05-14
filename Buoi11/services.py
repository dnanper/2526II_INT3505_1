"""
Service layer for Flask API Design Patterns Demo.

File này chứa logic xử lý chính:
- CRUD service
- Query Pattern: filtering, sorting, pagination, field selection
- HATEOAS links
- HMAC signature
- Webhook async processing
- GraphQL-like/BFF logic
"""

import hashlib
import hmac
import threading
import time
from copy import deepcopy
from math import ceil
from typing import Any, Dict, List, Mapping

from data import orders, users
from flask import url_for

# Demo secret shared between Payment service and Notification service.
# In real systems, put this in environment variables / secret manager.
WEBHOOK_SECRET = "demo-secret-key"

# Simple idempotency cache like Stripe's Idempotency-Key idea.
idempotency_cache: Dict[str, Dict[str, Any]] = {}

# Pretend queue for webhook events waiting for background processing.
event_queue: List[Dict[str, Any]] = []


# -----------------------------------------------------------------------------
# Common helpers
# -----------------------------------------------------------------------------


def next_order_id() -> int:
    return max(orders.keys(), default=0) + 1


def add_hateoas_links(order: Dict[str, Any]) -> Dict[str, Any]:
    """Add possible next actions, so client does not need to hardcode URLs."""
    result = deepcopy(order)
    order_id = order["id"]

    links = {
        "self": {"href": url_for("get_order", order_id=order_id, _external=False)},
        "collection": {"href": url_for("list_orders", _external=False)},
    }

    if order["status"] == "pending_payment":
        links["pay"] = {
            "href": url_for("pay_order", order_id=order_id, _external=False)
        }
        links["cancel"] = {
            "href": url_for("cancel_order", order_id=order_id, _external=False)
        }

    result["_links"] = links
    return result


def select_fields(item: Dict[str, Any], fields_param: str | None) -> Dict[str, Any]:
    """Return only requested fields, e.g. ?fields=id,status,amount"""
    if not fields_param:
        return item

    selected = {}
    fields = {field.strip() for field in fields_param.split(",") if field.strip()}

    for field in fields:
        if field in item:
            selected[field] = item[field]

    return selected


def parse_positive_int(value: str | None, default: int) -> int:
    """Parse query param int safely, always >= 1."""
    try:
        return max(int(value or default), 1)
    except ValueError:
        return default


# -----------------------------------------------------------------------------
# CRUD + Query services
# -----------------------------------------------------------------------------


def list_orders_service(args: Mapping[str, str], full_path: str) -> Dict[str, Any]:
    status = args.get("status")
    sort = args.get("sort", "id")
    fields = args.get("fields")
    page = parse_positive_int(args.get("page"), 1)
    limit = parse_positive_int(args.get("limit"), 10)

    result = list(orders.values())

    # Filtering
    if status:
        result = [order for order in result if order["status"] == status]

    # Sorting: sort=amount ASC, sort=-amount DESC
    reverse = sort.startswith("-")
    sort_key = sort[1:] if reverse else sort

    if result and sort_key in result[0]:
        result = sorted(result, key=lambda item: item[sort_key], reverse=reverse)

    # Pagination
    total = len(result)
    start = (page - 1) * limit
    end = start + limit
    paged = result[start:end]

    # Field selection + HATEOAS per item
    items = [select_fields(add_hateoas_links(order), fields) for order in paged]

    return {
        "data": items,
        "meta": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": ceil(total / limit) if total else 0,
        },
        "_links": {
            "self": {"href": full_path},
            "create": {"href": url_for("create_order", _external=False)},
        },
    }


def create_order_service(
    body: Dict[str, Any],
    idem_key: str | None = None,
) -> tuple[Dict[str, Any], int]:
    if idem_key and idem_key in idempotency_cache:
        cached = deepcopy(idempotency_cache[idem_key])
        cached["idempotent_replay"] = True
        return cached, 200

    required_fields = ["user_id", "amount"]
    missing_fields = [field for field in required_fields if field not in body]

    if missing_fields:
        return {"error": "Missing required fields", "fields": missing_fields}, 400

    order = {
        "id": next_order_id(),
        "user_id": int(body["user_id"]),
        "status": body.get("status", "pending_payment"),
        "amount": float(body["amount"]),
    }
    orders[order["id"]] = order

    response = add_hateoas_links(order)

    if idem_key:
        idempotency_cache[idem_key] = deepcopy(response)

    return response, 201


def get_order_service(order_id: int) -> tuple[Dict[str, Any], int]:
    order = orders.get(order_id)

    if not order:
        return {"error": "Order not found"}, 404

    return add_hateoas_links(order), 200


def update_order_service(
    order_id: int,
    body: Dict[str, Any],
) -> tuple[Dict[str, Any], int]:
    order = orders.get(order_id)

    if not order:
        return {"error": "Order not found"}, 404

    for field in ["status", "amount", "user_id"]:
        if field in body:
            order[field] = body[field]

    return add_hateoas_links(order), 200


def delete_order_service(order_id: int) -> tuple[Dict[str, Any], int]:
    if order_id not in orders:
        return {"error": "Order not found"}, 404

    deleted = orders.pop(order_id)

    return {
        "deleted": deleted,
        "_links": {"collection": {"href": url_for("list_orders", _external=False)}},
    }, 200


def cancel_order_service(order_id: int) -> tuple[Dict[str, Any], int]:
    order = orders.get(order_id)

    if not order:
        return {"error": "Order not found"}, 404

    if order["status"] != "pending_payment":
        return {"error": "Only pending_payment orders can be cancelled"}, 409

    order["status"] = "cancelled"
    return add_hateoas_links(order), 200


# -----------------------------------------------------------------------------
# Event-driven + Webhook services
# -----------------------------------------------------------------------------


def sign_payload(raw_body: bytes) -> str:
    return hmac.new(WEBHOOK_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()


def verify_signature(raw_body: bytes, signature: str | None) -> bool:
    if not signature:
        return False

    expected = sign_payload(raw_body)
    return hmac.compare_digest(expected, signature)


def mark_order_paid_and_build_event(order_id: int) -> tuple[Dict[str, Any], int]:
    order = orders.get(order_id)

    if not order:
        return {"error": "Order not found"}, 404

    order["status"] = "paid"

    event = {
        "type": "payment.succeeded",
        "data": {
            "order_id": order["id"],
            "user_id": order["user_id"],
            "amount": order["amount"],
        },
    }

    return {
        "order": add_hateoas_links(order),
        "event": event,
    }, 200


def accept_webhook_event(
    raw_body: bytes,
    signature: str | None,
) -> tuple[Dict[str, Any], int]:
    if not verify_signature(raw_body, signature):
        return {"error": "Invalid webhook signature"}, 400

    import json

    event = json.loads(raw_body.decode())
    event_queue.append(event)

    if event.get("type") == "payment.succeeded":
        thread = threading.Thread(
            target=send_email_async,
            args=(event,),
            daemon=True,
        )
        thread.start()

    return {
        "status": "ok",
        "message": "Event accepted for async processing",
    }, 200


def send_email_async(event: Dict[str, Any]) -> None:
    """Simulate slow email sending without blocking webhook response."""
    time.sleep(2)

    data = event.get("data", {})
    user_id = data.get("user_id")
    user = users.get(user_id, {})

    print(
        "[ASYNC EMAIL] Sent payment success email "
        f"to {user.get('email')} for order {data.get('order_id')}"
    )


def list_event_queue() -> Dict[str, Any]:
    return {
        "queue_size": len(event_queue),
        "events": event_queue,
    }


# -----------------------------------------------------------------------------
# GraphQL-like/BFF service
# -----------------------------------------------------------------------------


def graphql_lite_service(body: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
    if "order_id" not in body:
        return {"error": "Missing order_id"}, 400

    order_id = int(body["order_id"])
    order = orders.get(order_id)

    if not order:
        return {"error": "Order not found"}, 404

    user = users.get(order["user_id"], {})
    order_fields = body.get("order_fields", ["id", "status", "amount"])
    user_fields = body.get("user_fields", ["id", "name", "email"])

    return {
        "data": {
            "order": {field: order.get(field) for field in order_fields},
            "user": {field: user.get(field) for field in user_fields},
        }
    }, 200
