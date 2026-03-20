from flask import Flask, jsonify, request
from flasgger import Swagger

from data import tickets, users
from schema import template

app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs",
    "uiversion": 3
}

swagger = Swagger(app, config=swagger_config, template=template)

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    """
    Lay thong tin user theo id
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Thong tin user
        schema:
          $ref: '#/definitions/User'
      404:
        description: Khong tim thay user
        schema:
          $ref: '#/definitions/Error'
    """
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404


@app.route("/tickets", methods=["POST"])
def create_ticket():
    """
    Tao ticket moi
    ---
    tags:
      - Tickets
    parameters:
      - name: user_id
        in: query
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - title
            - description
          properties:
            title:
              type: string
              example: Loi phan mem
            description:
              type: string
              example: He thong bao loi 500
            priority:
              type: string
              enum:
                - low
                - medium
                - high
              example: medium
    responses:
      201:
        description: Tao ticket thanh cong
        schema:
          $ref: '#/definitions/Ticket'
      400:
        description: Du lieu khong hop le
        schema:
          $ref: '#/definitions/Error'
    """
    user_id = request.args.get("user_id", type=int)
    data = request.get_json()

    if user_id is None:
        return jsonify({"error": "Missing user_id in query parameters"}), 400
    if not data or "title" not in data or "description" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    if not any(u["id"] == user_id for u in users):
        return jsonify({"error": "User not found"}), 400

    ticket_id = len(tickets) + 1
    new_ticket = {
        "id": ticket_id,
        "user_id": user_id,
        "title": data["title"],
        "description": data["description"],
        "priority": data.get("priority", "medium"),
    }
    tickets.append(new_ticket)
    return jsonify(new_ticket), 201


@app.route("/tickets", methods=["GET"])
def get_tickets():
    """
    Lay danh sach ticket
    ---
    tags:
      - Tickets
    responses:
      200:
        description: Danh sach ticket
        schema:
          type: array
          items:
            $ref: '#/definitions/Ticket'
    """
    return jsonify(tickets), 200


@app.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket_by_id(ticket_id):
    """
    Lay thong tin ticket theo id
    ---
    tags:
      - Tickets
    parameters:
      - name: ticket_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Thong tin ticket
        schema:
          $ref: '#/definitions/Ticket'
      404:
        description: Khong tim thay ticket
        schema:
          $ref: '#/definitions/Error'
    """
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if ticket:
        return jsonify(ticket), 200
    return jsonify({"error": "Ticket not found"}), 404

@app.after_request
def cleanup_swagger_spec(response):
    # Kiểm tra nếu request là để lấy file đặc tả JSON của Swagger
    if request.endpoint == 'apispec_1':
        import json
        # Load dữ liệu JSON mà Flasgger vừa tạo ra
        data = json.loads(response.data)
        
        # Nếu tồn tại cả hai version, ta xóa cái 'swagger' (2.0) đi
        if 'openapi' in data and 'swagger' in data:
            del data['swagger']
            
        # Trả lại dữ liệu đã được làm sạch
        response.data = json.dumps(data)
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)
