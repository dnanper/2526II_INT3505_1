# RAML - Library API

Vì các công cụ sinh code hiện đại ưu tiên hệ sinh thái OpenAPI, cần convert từ RAML sang OpenAPI 3.0:

```bash
# Convert trực tiếp từ RAML sang chuẩn OAS 3.0
docker run --rm -v "${PWD}:/app" -w /app node:20 bash -c "npx oas-raml-converter --from RAML --to OAS30 api.raml > openapi.yaml"
```

Sau đó, chạy các lệnh tương tự openapi
