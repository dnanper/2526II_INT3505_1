from flask import Flask, jsonify, request
from data import orders_db

# 1. GET /api/v1/orders (List all)
# Thêm Query Parameter để lọc theo status: ?status=pending
@app.route('/api/v1/orders', methods=['GET'])
def get_orders():
    status_filter = request.args.get('status')
    result = orders_db
    
    if status_filter:
        result = [o for o in result if o['status'] == status_filter]
        
    return jsonify({"status": "success", "data": result}), 200

# 2. GET /api/v1/orders/{id} (Get one)
@app.route('/api/v1/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = next((o for o in orders_db if o['id'] == id), None)
    if order:
        return jsonify({"status": "success", "data": order}), 200
    return jsonify({"status": "error", "message": "Order not found"}), 404

# 3. POST /api/v1/orders (Create)
@app.route('/api/v1/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or 'product' not in data:
        return jsonify({"status": "error", "message": "Product is required"}), 400

    new_id = orders_db[-1]['id'] + 1 if orders_db else 1
    new_order = {
        "id": new_id,
        "user_id": data.get('user_id'),
        "product": data.get('product'),
        "amount": data.get('amount', 0),
        "status": "pending"
    }
    orders_db.append(new_order)
    return jsonify({"status": "success", "data": new_order}), 201

# 4. PUT /api/v1/orders/{id} (Update)
@app.route('/api/v1/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = next((o for o in orders_db if o['id'] == id), None)
    if not order:
        return jsonify({"status": "error", "message": "Order not found"}), 404

    data = request.get_json()
    order.update({
        "product": data.get('product', order['product']),
        "amount": data.get('amount', order['amount']),
        "status": data.get('status', order['status'])
    })
    return jsonify({"status": "success", "data": order}), 200

# 5. DELETE /api/v1/orders/{id} (Delete)
@app.route('/api/v1/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    global orders_db
    orders_db = [o for o in orders_db if o['id'] != id]
    return jsonify({"status": "success", "message": f"Order {id} deleted"}), 200