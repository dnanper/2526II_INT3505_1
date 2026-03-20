# OpenAPI - Library API

## 1. Xem tài liệu (Render UI)

Để hiển thị giao diện Swagger UI trên trình duyệt web, chạy lệnh Docker sau:

```bash
docker run --rm -p 8080:8080 -v "${PWD}:/app" -e SWAGGER_JSON=/app/openapi.yaml swaggerapi/swagger-ui
```

## 2. Sinh code tự động

Code tự động sinh nằm trong folder library-api-client

```bash
uvx openapi-python-client generate --path openapi.yaml
```
