from flask import Flask, jsonify, request
from data import users_db

app = Flask(__name__)

# 1. GET /api/v1/users (List all)
# Hỗ trợ Query Parameters: ?role=... & limit=...
@app.route('/api/v1/users', methods=['GET'])
def get_users():
    # Lấy query parameters từ URL
    role_filter = request.args.get('role')
    limit = request.args.get('limit', type=int)

    result = users_db

    if role_filter:
        result = [u for u in result if u.get('role') == role_filter]
    if limit:
        result = result[:limit]

    return jsonify({
        "status": "success",
        "total": len(result),
        "data": result
    }), 200

# 2. GET /api/v1/users/{id} (Get one)
# Sử dụng Path Parameter: <int:id>
@app.route('/api/v1/users/<int:id>', methods=['GET'])
def get_user(id):
    user = next((u for u in users_db if u['id'] == id), None)
    if user:
        return jsonify({"status": "success", "data": user}), 200
    
    return jsonify({"status": "error", "message": "User not found"}), 404

# 3. POST /api/v1/users (Create)
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Validate cơ bản
    if not data or not data.get('name'):
        return jsonify({"status": "error", "message": "Name is required"}), 400

    new_id = users_db[-1]['id'] + 1 if users_db else 1
    new_user = {
        "id": new_id,
        "name": data.get('name'),
        "role": data.get('role', 'user') # Mặc định là 'user' nếu không truyền
    }
    
    users_db.append(new_user)
    return jsonify({"status": "success", "data": new_user}), 201

# 4. PUT /api/v1/users/{id} (Update)
# Sử dụng Path Parameter: <int:id>
@app.route('/api/v1/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = next((u for u in users_db if u['id'] == id), None)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    data = request.get_json()
    
    # Cập nhật các trường nếu có truyền lên
    if data.get('name'):
        user['name'] = data['name']
    if data.get('role'):
        user['role'] = data['role']

    return jsonify({"status": "success", "data": user}), 200

# 5. DELETE /api/v1/users/{id} (Delete)
# Sử dụng Path Parameter: <int:id>
@app.route('/api/v1/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    global users_db
    user = next((u for u in users_db if u['id'] == id), None)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    # Giữ lại các user không trùng ID với ID cần xóa
    users_db = [u for u in users_db if u['id'] != id]
    return jsonify({"status": "success", "message": f"User {id} deleted successfully"}), 200

if __name__ == '__main__':
    # Chạy server ở chế độ debug
    app.run(debug=True, port=5000)