from flask import Flask, jsonify, request

app = Flask(__name__)

students = {
    "1": {"name": "An", "major": "IT"},
    "2": {"name": "Bình", "major": "Design"}
}

classrooms = {
    "A": {"room": 404},
    "B": {"room": 306}
}

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "service is running"
    }), 200

@app.route("/students", methods=["GET"])
def get_all_students():
    return jsonify(students), 200

@app.route("/classrooms", methods=["GET"])
def get_all_classrooms():
    return jsonify(classrooms), 200

if __name__ == "__main__":
    app.run(port=5000)