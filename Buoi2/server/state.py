from flask import Flask, jsonify, request, session

app = Flask(__name__)

app.secret_key = "super-secret"

# stateful
@app.route("/set-user", methods=["POST"])
def set_user():
    data = request.json
    name = data.get("name")
    session["user_name"] = name
    return jsonify({"message": f"Ok, save you name: {name}"}), 200

@app.route("/get-user", methods=["GET"])
def get_user():
    name = session.get("user_name")
    if name:
        return jsonify({"message": f"You are {name}"}), 200
    return jsonify({"message": "I don't remember you"}), 404 

# stateless
@app.route("/greet", methods=["POST"])
def greet():
    data = request.json
    name = data.get("name")
    
    if not name:
        return jsonify({"message": "I don't know you"}), 400
        
    return jsonify({
        "message": f"Hi {name}, I don't remember you!",
    }), 200

if __name__ == "__main__":
    app.run(port=5000)