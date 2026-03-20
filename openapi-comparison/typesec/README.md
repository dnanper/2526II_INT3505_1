# TypeSpec - Library API

TypeSpec không sinh code trực tiếp mà đóng vai trò như mã nguồn (source code) để biên dịch (compile) ra chuẩn OpenAPI 3.0:

```bash
# Cài đặt compiler và biên dịch file main.tsp
docker run --rm -v "${PWD}:/app" -w /app node:20 bash -c "npm install -g @typespec/compiler @typespec/openapi3 && tsp compile main.tsp --emit @typespec/openapi3"
```

Sau đó, chạy các lệnh tương tự openapi.
