import os
from datetime import timedelta

from data import USERS_DB
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from utils import role_required, scope_required

load_dotenv()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_COOKIE_SECURE"] = False  # Đặt True nếu deploy có HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # 1. Xác thực thông tin đăng nhập
    user = USERS_DB.get(username)
    if not user or user["password"] != password:
        return jsonify({"msg": "Sai tài khoản hoặc mật khẩu"}), 401

    # 2. Định nghĩa Custom Claims (chứa thông tin Role và Scopes)
    additional_claims = {"role": user["role"], "scopes": user["default_scopes"]}

    # 3. Tạo Access Token và Refresh Token
    access_token = create_access_token(
        identity=username, additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(identity=username)

    # 4. Thiết lập Response: Access Token ở JSON body, Refresh Token ở HttpOnly Cookie
    resp = jsonify(
        {
            "msg": "Đăng nhập thành công",
            "access_token": access_token,
            "user_info": {"username": username, "role": user["role"]},
        }
    )

    # Hàm này tự động set HttpOnly=True và các cờ bảo mật khác dựa trên config
    set_refresh_cookies(resp, refresh_token)
    return resp, 200


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Dùng Refresh Token để lấy Access Token mới"""
    current_user = get_jwt_identity()
    user = USERS_DB.get(current_user)

    if not user:
        return jsonify({"msg": "User không tồn tại"}), 401

    # Cấp lại Access Token mới (có thể update lại Role/Scope mới nhất từ DB tại bước này)
    additional_claims = {"role": user["role"], "scopes": user["default_scopes"]}
    new_access_token = create_access_token(
        identity=current_user, additional_claims=additional_claims
    )

    return jsonify(
        {"msg": "Refresh token thành công", "access_token": new_access_token}
    ), 200


@app.route("/logout", methods=["POST"])
def logout():
    """Xóa Refresh Token khỏi Cookie"""
    resp = jsonify({"msg": "Đăng xuất thành công"})
    unset_jwt_cookies(resp)
    return resp, 200


@app.route("/api/profile", methods=["GET"])
@jwt_required()
@scope_required("profile.read")  # Phân quyền: Cần scope profile.read
def get_profile():
    current_user = get_jwt_identity()
    claims = get_jwt()
    return jsonify(
        {
            "msg": "Truy cập profile thành công",
            "username": current_user,
            "role": claims.get("role"),
            "active_scopes": claims.get("scopes"),
        }
    ), 200


@app.route("/api/admin/system", methods=["GET"])
@jwt_required()
@role_required("Admin")  # Phân quyền: Cần role Admin
def admin_system_status():
    return jsonify(
        {
            "msg": "Truy cập dashboard Admin thành công",
            "status": "Hệ thống đang hoạt động ổn định",
        }
    ), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
