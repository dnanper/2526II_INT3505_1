# API Blueprint - Library API

Vì các công cụ sinh code hiện đại không còn hỗ trợ API Blueprint, cần convert sang OpenAPI 3.0:

```bash
# Convert sang Swagger 2.0
docker run --rm -v "${PWD}:/app" -w /app node:20 npx apib2swagger -i apiary.apib -o openapi.yaml --yaml

# Nâng cấp lên OpenAPI 3.0
docker run --rm -v "${PWD}:/app" -w /app node:20 npx swagger2openapi openapi.yaml -o openapi3.yaml --yaml
```

Sau đó, chạy các lệnh tương tự openapi
