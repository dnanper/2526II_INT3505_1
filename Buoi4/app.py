from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from data import users, tickets
from schema import template

app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

swagger = Swagger(app, 
                  config=swagger_config, 
                  template=template)

@app.route('/users', methods=['POST'])
@swag_from('swagger_users.yml')
def create_user():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    user_id = len(users) + 1
    new_user = {
        "id": user_id, 
        "username": data['username'], 
        "email": data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/tickets', methods=['POST'])
@swag_from('swagger_tickets.yml')
def create_ticket():
    user_id = request.args.get('user_id')
    data = request.get_json()
    if not user_id:
        return jsonify({"error": "Missing user_id in query parameters"}), 400
    if not data or 'title' not in data or 'description' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    if not any(u['id'] == int(user_id) for u in users):
        return jsonify({"error": "User not found"}), 400
        
    ticket_id = len(tickets) + 1
    new_ticket = {
        "id": ticket_id,
        "user_id": user_id,
        "title": data['title'],
        "description": data['description'],
        "priority": data.get('priority', 'medium')
    }
    tickets.append(new_ticket)
    return jsonify(new_ticket), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)