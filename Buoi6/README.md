Access Token được gửi đi qua Header của API.
Authorization: Bearer <chuỗi_access_token>.
Refresh Token tự động lưu/gửi trong cookies

Khi nào thì dùng Refresh Token?

User đăng nhập thành công. Frontend nhận Access Token (lưu vào biến/RAM). Trình duyệt tự lưu Refresh Token vào Cookie.

Frontend gọi các API nghiệp vụ (ví dụ: lấy Profile) kèm Access Token trong Header.

Sau 15 phút, Access Token hết hạn. Frontend gọi API Profile và bị server trả về lỗi 401 Unauthorized (Token Expired).

Lúc này Refresh Token vào việc: Ngay khi nhận lỗi 401, Frontend ngầm gọi một API đến endpoint POST /refresh. Frontend không cần gửi thêm gì cả, trình duyệt sẽ tự động gửi cái Cookie chứa Refresh Token đi.

Server kiểm tra Refresh Token trong Cookie. Nếu hợp lệ, server trả về một Access Token mới tinh.

Frontend lấy Access Token mới này, lưu lại vào RAM, và tự động gọi lại cái API Profile bị tạch ở bước 3. Tất cả quá trình này diễn ra ngầm (thường dùng Interceptors của Axios), user không hề hay biết và không phải đăng nhập lại.

Nếu logout, refresh token bị xóa, phải đăng nhập lại. Tuy nhiên access token nếu còn thời gian thì vẫn hoạt động được.
