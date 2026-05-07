import os

import pybreaker
import requests
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# 1. Khởi tạo Prometheus Metrics
# Tự động tạo endpoint /metrics và đo lường latency, request rate cho mọi routes
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Application info", version="1.0.0")

# Lấy Redis URI từ biến môi trường
REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379/0")

# 2. Thiết lập Rate Limiter
limiter = Limiter(get_remote_address, app=app, storage_uri=REDIS_URI)

# 3. Thiết lập Circuit Breaker
# chặn request nếu thất bại 5 lần liên tiếp. Thử lại sau 60 giây.
circuit = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)


@circuit
def call_external_api():
    # Giả lập gọi một API bên ngoài. Dùng httpstat.us để test lỗi 503
    response = requests.get("https://httpstat.us/503", timeout=3)
    response.raise_for_status()
    return response.json()


@app.route("/v1/items")
@limiter.limit("10/minute")  # Giới hạn 10 request/phút trên mỗi IP
def get_items():
    return jsonify({"data": ["item_A", "item_B"], "status": "success"})


@app.route("/v1/external")
def get_external_data():
    try:
        data = call_external_api()
        return jsonify(data)
    except pybreaker.CircuitBreakerError:
        # Bắt lỗi khi mạch đang MỞ (Open) -> Trả về lỗi ngay lập tức, không tốn time chờ request
        return jsonify(
            {"error": "Circuit breaker is OPEN. External service is down."}
        ), 503
    except requests.exceptions.RequestException as e:
        # Bắt lỗi khi request thất bại (Timeout, 5xx)
        return jsonify({"error": f"External API call failed: {str(e)}"}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
