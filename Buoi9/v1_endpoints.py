"""
API v1 Endpoints (Deprecated/Legacy)

v1 only supports VND currency (implicit)
These endpoints are deprecated and will be sunset on the scheduled date.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from test.config import API_VERSION_V1, DEPRECATION_DAYS_NOTICE


def create_error_response(error_message, status_code, version="unknown", **extra):
    """Helper to create standardized error responses"""
    response = jsonify({"error": error_message, "version": version, **extra})
    response.status_code = status_code
    return response


v1_bp = Blueprint("v1", __name__, url_prefix="/api/v1")

v1_bp = Blueprint("v1", __name__, url_prefix="/api/v1")


@v1_bp.route("/payments", methods=["POST"])
def create_payment():
    """
    v1: Create payment - Only supports VND currency (implicit)

    Breaking change in v2: currency field becomes required

    Request body (v1):
        {
            "amount": 100000
        }

    Response:
        {
            "success": true,
            "data": {
                "id": "pay_001",
                "amount": 100000,
                "currency": "VND",  # ← Implicit, not in request
                "status": "completed",
                "created_at": "2025-01-15T10:30:00Z",
                "version": "1.0"
            },
            "version": "1.0",
            "deprecated": true
        }
    """
    data = request.get_json()

    if not data:
        return create_error_response("Invalid JSON", 400, version=API_VERSION_V1), 400

    amount = data.get("amount")
    if not amount:
        return create_error_response(
            "Missing required field: amount", 400, version=API_VERSION_V1
        ), 400

    # v1 assumes VND only (implicit currency)
    payment = {
        "id": "pay_001",
        "amount": amount,
        "currency": "VND",
        "status": "completed",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "version": API_VERSION_V1,
    }

    response = (
        jsonify(
            {
                "success": True,
                "data": payment,
                "message": "Payment created (v1 - deprecated)",
                "version": API_VERSION_V1,
                "deprecated": True,
            }
        ),
        201,
    )

    # Add deprecation headers
    response[0].headers["X-API-Version"] = API_VERSION_V1
    response[0].headers["Deprecation"] = "true"
    response[0].headers["Sunset"] = (datetime.utcnow() + timedelta(days=90)).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    response[0].headers["Link"] = '</api/v2/payments>; rel="successor-version"'
    response[0].headers["X-Migration-Guide"] = "/docs/migration/v1-to-v2"

    return response


@v1_bp.route("/payments/<payment_id>", methods=["GET"])
def get_payment(payment_id):
    """
    v1: Get payment details

    Response includes deprecated warning
    """
    payment = {
        "id": payment_id,
        "amount": 100000,
        "currency": "VND",
        "status": "completed",
        "created_at": "2025-01-15T10:30:00Z",
        "version": API_VERSION_V1,
    }

    response = (
        jsonify(
            {
                "success": True,
                "data": payment,
                "version": API_VERSION_V1,
                "deprecated": True,
            }
        ),
        200,
    )

    # Add deprecation headers
    response[0].headers["X-API-Version"] = API_VERSION_V1
    response[0].headers["Deprecation"] = "true"
    response[0].headers["Sunset"] = (datetime.utcnow() + timedelta(days=90)).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    response[0].headers["Link"] = '</api/v2/payments>; rel="successor-version"'
    response[0].headers["X-Migration-Guide"] = "/docs/migration/v1-to-v2"

    return response


@v1_bp.route("/health", methods=["GET"])
def health_check():
    """
    v1: Health check endpoint

    Returns deprecation warning in response body
    """
    response = (
        jsonify(
            {
                "status": "healthy",
                "version": API_VERSION_V1,
                "deprecated": True,
                "message": "This endpoint is deprecated. Use /api/v2/health instead.",
            }
        ),
        200,
    )

    # Add deprecation headers
    response[0].headers["X-API-Version"] = API_VERSION_V1
    response[0].headers["Deprecation"] = "true"
    response[0].headers["Sunset"] = (datetime.utcnow() + timedelta(days=90)).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    response[0].headers["Link"] = '</api/v2/health>; rel="successor-version"'
    response[0].headers["X-Migration-Guide"] = "/docs/migration/v1-to-v2"

    return response
