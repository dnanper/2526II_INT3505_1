"""
Documentation Endpoints

Provides migration guides, changelog, and API documentation
"""

from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from test.config import (
    API_VERSION_V1,
    API_VERSION_V2,
    SUPPORTED_CURRENCIES,
    DEPRECATION_DAYS_NOTICE,
)

docs_bp = Blueprint("docs", __name__, url_prefix="/docs")


@docs_bp.route("/migration/v1-to-v2", methods=["GET"])
def migration_guide():
    """
    Migration guide from v1 to v2

    Provides:
    - Breaking changes summary
    - Migration steps
    - Code examples (before/after)
    - Timeline information
    """
    return jsonify(
        {
            "title": "Migration Guide: v1 → v2",
            "version": API_VERSION_V2,
            "breaking_changes": [
                {
                    "field": "currency",
                    "change": "Now required in all payment requests",
                    "impact": "HIGH",
                    "description": 'In v1, currency was implicitly set to "VND". In v2, clients must explicitly specify the currency.',
                    "migration": "Add currency field to all POST /payments requests",
                }
            ],
            "migration_steps": [
                "1. Update endpoint URL from /api/v1/payments to /api/v2/payments",
                '2. Add "currency" field to payment request body',
                "3. Handle currency conversion in your application logic",
                f"4. Test with supported currencies: {', '.join(SUPPORTED_CURRENCIES)}",
                "5. Update error handling for currency validation",
                "6. Update any hardcoded assumptions about VND-only payments",
            ],
            "code_examples": {
                "v1_deprecated": {
                    "description": "Old v1 approach (will stop working)",
                    "request": """POST /api/v1/payments
Content-Type: application/json

{
  "amount": 100000
}""",
                    "response": """{
  "success": true,
  "data": {
    "id": "pay_001",
    "amount": 100000,
    "currency": "VND",
    "status": "completed"
  },
  "version": "1.0",
  "deprecated": true
}""",
                },
                "v2_recommended": {
                    "description": "New v2 approach (required)",
                    "request": """POST /api/v2/payments
Content-Type: application/json

{
  "amount": 100000,
  "currency": "USD"
}""",
                    "response": """{
  "success": true,
  "data": {
    "id": "pay_20250423103045",
    "amount": 100000,
    "currency": "USD",
    "status": "completed",
    "exchange_rate_applied": true,
    "amount_vnd": 2450000000
  },
  "message": "Payment created successfully in USD",
  "version": "2.0"
}""",
                },
            },
            "timeline": {
                "v2_release_date": "2025-01-15",
                "deprecated_since": "2025-01-15",
                "sunset_date": (
                    datetime.utcnow() + timedelta(days=DEPRECATION_DAYS_NOTICE)
                ).strftime("%Y-%m-%d"),
                "end_of_life": (
                    datetime.utcnow() + timedelta(days=DEPRECATION_DAYS_NOTICE)
                ).strftime("%Y-%m-%d"),
                "grace_period_days": DEPRECATION_DAYS_NOTICE,
            },
            "support_contact": "api-support@example.com",
            "additional_resources": [
                {"title": "Full Changelog", "url": "/changelog"},
                {"title": "API Health Status", "url": "/api/v2/health"},
                {"title": "Supported Currencies", "url": "/api/v2/currencies"},
            ],
        }
    ), 200


@docs_bp.route("/changelog", methods=["GET"])
def changelog():
    """
    API Changelog - Version history and changes
    """
    return jsonify(
        {
            "current_version": API_VERSION_V2,
            "versions": {
                API_VERSION_V2: {
                    "release_date": "2025-01-15",
                    "status": "current",
                    "changes": [
                        "Added multi-currency support (USD, EUR, JPY, CNY)",
                        "Breaking: currency field now required in payment requests",
                        "Added exchange rate calculation (auto-convert to VND)",
                        "New endpoint: GET /api/v2/currencies",
                        "Improved error messages with validation details",
                    ],
                    "breaking_changes": [
                        'POST /api/v2/payments now requires "currency" field'
                    ],
                },
                API_VERSION_V1: {
                    "release_date": "2024-10-01",
                    "status": "deprecated",
                    "sunset_date": (
                        datetime.utcnow() + timedelta(days=DEPRECATION_DAYS_NOTICE)
                    ).strftime("%Y-%m-%d"),
                    "changes": [
                        "Initial release",
                        "VND currency only (implicit)",
                        "Basic payment creation and retrieval",
                        "Health check endpoint",
                    ],
                    "deprecated": True,
                    "deprecated_since": "2025-01-15",
                    "end_of_life": (
                        datetime.utcnow() + timedelta(days=DEPRECATION_DAYS_NOTICE)
                    ).strftime("%Y-%m-%d"),
                },
            },
            "migration_guide_url": "/docs/migration/v1-to-v2",
        }
    ), 200
