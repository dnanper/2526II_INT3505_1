"""
API Versioning and Lifecycle Management Demo
Main Flask Application

Demonstrates URL-based versioning with v1 (deprecated) and v2 (current) payment APIs
"""

from flask import Flask
from v1_endpoints import v1_bp
from test.v2_endpoints import v2_bp
from test.docs_endpoints import docs_bp


def create_app():
    """
    Application factory - creates and configures the Flask app
    """
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(v1_bp)
    app.register_blueprint(v2_bp)
    app.register_blueprint(docs_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {
            "error": "Not Found",
            "message": "The requested endpoint does not exist",
            "version": "unknown",
        }, 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return {
            "error": "Method Not Allowed",
            "message": "The HTTP method is not supported for this endpoint",
            "version": "unknown",
        }, 405

    @app.errorhandler(500)
    def internal_error(error):
        return {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "version": "unknown",
        }, 500

    return app


def print_startup_info():
    """
    Print helpful information when the app starts
    """
    print("\n" + "=" * 70)
    print("API Versioning Demo - Payment Service")
    print("=" * 70)
    print("\n📋 Endpoints:")
    print("\n  v1 (Deprecated - will sunset in 90 days):")
    print("    POST   /api/v1/payments       - Create payment (VND only)")
    print("    GET    /api/v1/payments/<id> - Get payment details")
    print("    GET    /api/v1/health         - Health check")
    print("\n  v2 (Current - recommended):")
    print("    POST   /api/v2/payments       - Create payment (multi-currency)")
    print("    GET    /api/v2/payments/<id> - Get payment details")
    print("    GET    /api/v2/health         - Health check with features")
    print("    GET    /api/v2/currencies     - List supported currencies")
    print("\n  Documentation:")
    print("    GET    /docs/migration/v1-to-v2 - Migration guide")
    print("    GET    /docs/changelog          - Version history")
    print("\n" + "=" * 70)
    print("\n⚠️  Note:")
    print("  - v1 endpoints include deprecation headers")
    print("  - Sunset date: 90 days from now")
    print("  - v1 requires no currency field (defaults to VND)")
    print("  - v2 REQUIRES currency field (breaking change)")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    app = create_app()
    print_startup_info()
    app.run(debug=True, port=5000)
