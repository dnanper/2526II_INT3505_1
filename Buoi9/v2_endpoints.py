"""
API v2 Endpoints (Current)

v2 supports multiple currencies (breaking change from v1)
currency field is now REQUIRED
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from test.config import (
    API_VERSION_V2,
    SUPPORTED_CURRENCIES,
    CURRENCY_SYMBOLS,
    CURRENCY_NAMES,
    EXCHANGE_RATES,
)

v2_bp = Blueprint("v2", __name__, url_prefix="/api/v2")


@v2_bp.route("/payments", methods=["POST"])
def create_payment():
    """
    v2: Create payment with multi-currency support

    Breaking change from v1: currency field is now REQUIRED

    Request body:
        {
            "amount": 100000,
            "currency": "USD"  # ← Required in v2
        }

    Response:
        {
            "success": true,
            "data": {
                "id": "pay_20250423103045",
                "amount": 100000,
                "currency": "USD",
                "status": "completed",
                "exchange_rate_applied": true,
                "created_at": "2025-01-15T10:30:00Z",
                "version": "2.0"
            },
            "message": "Payment created successfully in USD",
            "version": "2.0"
        }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON", "version": API_VERSION_V2}), 400

    amount = data.get("amount")
    currency = data.get("currency")  # NEW: Required in v2

    # Validation
    if not amount:
        return jsonify(
            {
                "error": "Missing required field: amount",
                "version": API_VERSION_V2,
                "required_fields": ["amount", "currency"],
            }
        ), 400

    if not currency:
        return jsonify(
            {
                "error": "Missing required field: currency",
                "version": API_VERSION_V2,
                "message": "v2 breaking change: currency is now required",
                "supported_currencies": SUPPORTED_CURRENCIES,
            }
        ), 400

    if currency not in SUPPORTED_CURRENCIES:
        return jsonify(
            {
                "error": f"Unsupported currency: {currency}",
                "version": API_VERSION_V2,
                "supported_currencies": SUPPORTED_CURRENCIES,
            }
        ), 400

    # Simulate payment processing with currency conversion logic
    payment = {
        "id": f"pay_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "amount": amount,
        "currency": currency,
        "status": "completed",
        "exchange_rate_applied": currency != "VND",
        "amount_vnd": amount * EXCHANGE_RATES.get(currency, 1)
        if currency != "VND"
        else amount,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "version": API_VERSION_V2,
    }

    return jsonify(
        {
            "success": True,
            "data": payment,
            "message": f"Payment created successfully in {currency}",
            "version": API_VERSION_V2,
        }
    ), 201


@v2_bp.route("/payments/<payment_id>", methods=["GET"])
def get_payment(payment_id):
    """
    v2: Get payment details with currency information
    """
    # Mock data with currency support
    payment = {
        "id": payment_id,
        "amount": 100000,
        "currency": "USD",
        "status": "completed",
        "exchange_rate": EXCHANGE_RATES["USD"],
        "amount_vnd": 2450000000,
        "created_at": "2025-01-15T10:30:00Z",
        "version": API_VERSION_V2,
    }

    return jsonify({"success": True, "data": payment, "version": API_VERSION_V2}), 200


@v2_bp.route("/health", methods=["GET"])
def health_check():
    """
    v2: Health check endpoint

    Shows supported features
    """
    return jsonify(
        {
            "status": "healthy",
            "version": API_VERSION_V2,
            "features": ["multi-currency", "exchange-rate", "international-payments"],
        }
    ), 200


@v2_bp.route("/currencies", methods=["GET"])
def list_currencies():
    """
    v2: List all supported currencies

    New endpoint not available in v1
    """
    currencies = [
        {
            "code": code,
            "name": CURRENCY_NAMES[code],
            "symbol": CURRENCY_SYMBOLS[code],
            "exchange_rate_to_vnd": EXCHANGE_RATES[code],
        }
        for code in SUPPORTED_CURRENCIES
    ]

    return jsonify(
        {"success": True, "data": currencies, "version": API_VERSION_V2}
    ), 200
