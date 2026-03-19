from flask import Flask, jsonify, request

app = Flask(__name__)

users = []
tickets = []

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_id = len(users) + 1
    new_user = {"id": user_id, "username": data['username'], "email": data['email']}
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/tickets', methods=['POST'])
def create_ticket():
    user_id = request.args.get('user_id')
    data = request.json
    
    # Kiểm tra user tồn tại (logic đơn giản)
    if not any(u['id'] == int(user_id) for u in users):
        return jsonify({"error": "User not found"}), 400
        
    new_ticket = {
        "id": len(tickets) + 1,
        "user_id": user_id,
        "title": data['title'],
        "description": data['description'],
        "priority": data.get('priority', 'medium')
    }
    tickets.append(new_ticket)
    return jsonify(new_ticket), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)