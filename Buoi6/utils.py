from functools import wraps

from flask import Flask, jsonify
from flask_jwt_extended import (
    get_jwt,
)

app = Flask(__name__)


def role_required(*required_roles):
    """Kiểm tra xem user có thuộc một trong các Role được phép không"""

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in required_roles:
                return jsonify(
                    msg=f"Forbidden: Access requires one of roles {required_roles}"
                ), 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def scope_required(*required_scopes):
    """Kiểm tra xem Access Token có chứa ít nhất một Scope hợp lệ không"""

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            token_scopes = claims.get("scopes", [])
            if not any(scope in token_scopes for scope in required_scopes):
                return jsonify(
                    msg=f"Forbidden: Access requires one of scopes {required_scopes}"
                ), 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper
