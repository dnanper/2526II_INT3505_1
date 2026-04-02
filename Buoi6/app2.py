import os
from datetime import timedelta

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request
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

load_dotenv()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv(
    "FLASK_SECRET_KEY", "fallback_secret_neu_thieu_env"
)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_COOKIE_SECURE"] = False  # Đặt True nếu có HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)

# ==========================================
# CẤU HÌNH GOOGLE OAUTH 2.0
# ==========================================
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/oauth/callback"

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


# ==========================================
# LUỒNG OAUTH 2.0 & AUTHENTICATION
# ==========================================
@app.route("/oauth/login", methods=["GET"])
def oauth_login():
    """BƯỚC 1: ĐIỀU HƯỚNG YÊU CẦU QUYỀN"""
    auth_url = (
        f"{GOOGLE_AUTH_URL}"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
        f"&access_type=offline"
    )
    return redirect(auth_url)


@app.route("/oauth/callback", methods=["GET"])
def oauth_callback():
    """BƯỚC 2 & 3: LẤY CODE, ĐỔI TOKEN VÀ CẤP PHÁT JWT NỘI BỘ"""
    auth_code = request.args.get("code")
    if not auth_code:
        return jsonify(
            {"msg": "Lỗi: Không nhận được Authorization Code từ Google"}
        ), 400

    # Gửi Code + Secret lên server Google để đổi lấy Access Token
    token_payload = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_response = requests.post(GOOGLE_TOKEN_URL, data=token_payload).json()
    google_access_token = token_response.get("access_token")

    if not google_access_token:
        return jsonify(
            {"msg": "Lỗi: Không thể đổi code lấy token", "details": token_response}
        ), 401

    # Dùng Token của Google để lấy Profile
    headers = {"Authorization": f"Bearer {google_access_token}"}
    userinfo_response = requests.get(GOOGLE_USERINFO_URL, headers=headers).json()

    user_email = userinfo_response.get("email")
    user_name = userinfo_response.get("name")

    # Bridge: Sinh JWT nội bộ (Giả lập logic check DB)
    role = "Admin" if user_email == "admin@gmail.com" else "User"
    additional_claims = {"role": role, "scopes": ["profile.read"]}

    local_access_token = create_access_token(
        identity=user_email, additional_claims=additional_claims
    )
    local_refresh_token = create_refresh_token(identity=user_email)

    resp = jsonify(
        {
            "msg": f"Chào mừng {user_name}!",
            "email": user_email,
            "access_token": local_access_token,
        }
    )

    set_refresh_cookies(resp, local_refresh_token)
    return resp, 200


# ==========================================
# ENDPOINTS QUẢN LÝ TOKEN & NGHIỆP VỤ
# ==========================================
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Xin lại Access Token mới bằng Refresh Token lưu ngầm trong Cookie"""
    current_user = get_jwt_identity()
    # Thực tế bạn query lại DB ở đây để update role/scopes mới nhất nếu cần
    additional_claims = {"role": "User", "scopes": ["profile.read"]}
    new_access_token = create_access_token(
        identity=current_user, additional_claims=additional_claims
    )

    return jsonify({"access_token": new_access_token}), 200


@app.route("/logout", methods=["POST"])
def logout():
    """Xóa Refresh Token ở Cookie"""
    resp = jsonify({"msg": "Đăng xuất thành công"})
    unset_jwt_cookies(resp)
    return resp, 200


@app.route("/api/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """Test truy cập bằng Access Token"""
    current_user = get_jwt_identity()
    claims = get_jwt()
    return jsonify(email=current_user, role=claims.get("role")), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
