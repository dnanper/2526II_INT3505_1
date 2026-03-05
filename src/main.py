from fastapi import FastAPI, Request, Response, status
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/code-on-demand")
def get_executable_code(request: Request, response: Response):
    # Show Request Headers
    print("--- Request Headers ---")
    for key, value in request.headers.items():
        print(f"{key}: {value}")

    # Set Response Header tùy chỉnh
    response.headers["X-Demo-REST"] = "Code-On-Demand-Active"
    
    # Mã JavaScript trả về cho client (Code on Demand)
    js_code = """
    function showMessage() {
        alert('Đây là mã code được gửi từ server xuống client để thực thi!');
    }
    showMessage();
    """
    
    # Định dạng Content-Type là javascript
    return Response(content=js_code, media_type="application/javascript", status_code=200)

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item():
    # 201 Created: Thường dùng cho POST khi tạo mới resource
    return {"message": "Đã tạo item mới (POST)"}

@app.put("/items/{item_id}", status_code=status.HTTP_200_OK)
def replace_item(item_id: int):
    # Dùng để cập nhật toàn bộ resource
    return {"message": f"Đã ghi đè toàn bộ item {item_id} (PUT)"}

@app.patch("/items/{item_id}", status_code=status.HTTP_200_OK)
def update_item_partially(item_id: int):
    # Dùng để cập nhật một phần resource
    return {"message": f"Đã cập nhật một phần item {item_id} (PATCH)"}

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    # 204 No Content: Xóa thành công nhưng không cần trả về body
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@app.get("/status-1xx")
def status_informational():
    # 102 Processing: Báo client chờ, server đang xử lý
    return Response(status_code=102, content="Đang xử lý...")

@app.get("/status-3xx")
def status_redirection():
    # 307 Temporary Redirect: Chuyển hướng client sang endpoint khác
    return RedirectResponse(url="/code-on-demand", status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@app.get("/status-4xx")
def status_client_error():
    # 400 Bad Request: Lỗi do client gửi request sai
    return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Lỗi Request từ Client!")

@app.get("/status-5xx")
def status_server_error():
    # 501 Not Implemented: Lỗi từ phía Server (chưa implement tính năng này)
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED, content="Server chưa hỗ trợ tính năng này!")