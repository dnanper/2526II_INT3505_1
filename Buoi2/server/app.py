from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "service is running"
    }), 200

if __name__ == "__main__":
    app.run(port=5000)