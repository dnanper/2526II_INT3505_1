from dotenv import load_dotenv
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def analyze_openweather_api():
    # 1. Khai báo thông tin API
    # LƯU Ý: Thay 'YOUR_API_KEY_HERE' bằng API Key thật của bạn
    API_KEY = os.getenv("OPEN_WEATHER_API")
    # print(API_KEY)
    CITY = "Hanoi"
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    # 2. Xây dựng Query Parameters
    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "metric" # Sử dụng độ C thay vì độ K
    }
    
    print(f"Đang gửi GET request đến: {BASE_URL}...\n")
    
    # 3. Thực hiện gọi API
    try:
        response = requests.get(BASE_URL, params=params)
        
        # --- PHÂN TÍCH KẾT QUẢ TRẢ VỀ ---
        
        # A. Status Code (Kiểm tra thành công hay thất bại)
        print("=== 1. STATUS CODE ===")
        print(f"Code: {response.status_code}")
        if response.status_code == 200:
            print("Trạng thái: THÀNH CÔNG (OK)\n")
        elif response.status_code == 401:
            print("Trạng thái: LỖI XÁC THỰC (Sai API Key)\n")
        elif response.status_code == 404:
            print("Trạng thái: KHÔNG TÌM THẤY (Sai tên thành phố)\n")
        
        # B. Headers (Xem server trả về metadata gì)
        print("=== 2. RESPONSE HEADERS (Một số trường quan trọng) ===")
        headers_to_check = ['Content-Type', 'Server', 'Date']
        for key in headers_to_check:
            # Dùng .get() để tránh lỗi nếu header không tồn tại
            print(f"{key}: {response.headers.get(key)}")
        print()
        
        # C. Body (Dữ liệu thực tế)
        print("=== 3. DATA BODY (JSON) ===")
        if response.status_code == 200:
            data = response.json() # Chuyển chuỗi JSON thành Dictionary của Python
            
            # In ra toàn bộ JSON cho đẹp
            print("Toàn bộ phản hồi:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Trích xuất dữ liệu cụ thể
            print("\n--- Trích xuất thông tin nhanh ---")
            print(f"Thành phố: {data['name']}")
            print(f"Nhiệt độ hiện tại: {data['main']['temp']} °C")
            print(f"Độ ẩm: {data['main']['humidity']}%")
            print(f"Mô tả thời tiết: {data['weather'][0]['description']}")
            
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")

if __name__ == "__main__":
    analyze_openweather_api()