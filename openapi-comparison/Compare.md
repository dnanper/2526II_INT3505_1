## 1. Bảng so sánh các định dạng

| Tiêu chí              | OpenAPI (OAS)         | API Blueprint          | RAML                    | TypeSpec               |
| :-------------------- | :-------------------- | :--------------------- | :---------------------- | :--------------------- |
| **Cú pháp**           | YAML / JSON           | Markdown (MSON)        | YAML                    | TypeScript-like DSL    |
| **Độ phổ biến**       | Cao nhất (Tiêu chuẩn) | Trung bình (Đang giảm) | Trung bình (Enterprise) | Đang tăng (Hiện đại)   |
| **Tái sử dụng**       | Khá (`$ref`)          | Thấp                   | Rất cao (Traits)        | Tuyệt vời (Mixins)     |
| **Mức độ trừu tượng** | Thấp (Chi tiết)       | Cao (Dễ đọc)           | Cao                     | Rất cao (Gần với Code) |
| **Hệ sinh thái**      | Khổng lồ              | Hạn chế                | Tốt (MuleSoft)          | Tốt (Microsoft)        |

## 2. Phân tích chi tiết các định dạng

### OpenAPI (OAS)

- **Triết lý:** Định nghĩa mọi khía cạnh của HTTP request/response một cách tường minh.
- **Ưu điểm:** Hệ sinh thái công cụ hỗ trợ (Swagger UI, Redoc, Generator) là tiêu chuẩn vàng ngành phần mềm.
- **Nhược điểm:** File YAML rất nhanh bị phình to (verbose). Với các dự án lớn, việc quản trị hàng ngàn dòng code YAML là một thách thức.
- **Case study:** Phù hợp cho mọi dự án RESTful hiện đại cần sự chuyên nghiệp và ổn định.

### API Blueprint

- **Triết lý:** Thiết kế xoay quanh Markdown, giúp người không chuyên (PM, khách hàng) cũng có thể hiểu logic API.
- **Ưu điểm:** Cực kỳ dễ học, dễ viết. Cú pháp MSON giúp định nghĩa cấu trúc dữ liệu rất tự nhiên.
- **Nhược điểm:** Tooling hiện đại đã ngừng cập nhật. Cần nhiều bước chuyển đổi để sử dụng được với các thư viện sinh code mới.
- **Case study:** Phù hợp cho giai đoạn Brainstorming hoặc các dự án nhỏ cần giao tiếp nhanh.

### RAML

- **Triết lý:** Mang các khái niệm OOP (kế thừa, tái sử dụng) vào thiết kế API thông qua **Traits** và **Resource Types**.
- **Ưu điểm:** Giảm thiểu trùng lặp code (DRY) tốt hơn hẳn OpenAPI. Phù hợp cho quản lý các API phân tầng.
- **Nhược điểm:** Độ dốc về học thuật (learning curve) cao. Phụ thuộc nhiều vào hệ sinh thái MuleSoft.
- **Case study:** Các hệ thống Enterprise lớn, có hàng trăm endpoint tương đồng.

### TypeSpec

- **Triết lý:** Cho phép developer "code" API bằng ngôn ngữ có tính năng kiểm tra kiểu (Type-safe) tương tự TypeScript.
- **Ưu điểm:** Tốc độ viết nhanh, phát hiện lỗi ngay khi gõ (IDE support mạnh). Khả năng trừu tượng hóa tuyệt vời.
- **Nhược điểm:** Cần bước biên dịch (Compilation) để ra kết quả OpenAPI cuối cùng.
- **Case study:** Các dự án hiện đại, team Backend ưu tiên hiệu suất và quản lý Spec như mã nguồn thực thụ.
