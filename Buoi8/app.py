from database import init_db
from flask import Flask, jsonify, request
from services import BookModel, UserModel

app = Flask(__name__)

# Initialize database and populate examples when app starts
init_db()

book_model = BookModel()
user_model = UserModel()

# =================
# BOOKS ENDPOINTS
# =================


@app.route("/books", methods=["GET"])
def get_books():
    books = book_model.get_all()
    return jsonify({"books": books}), 200


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = book_model.get_by_id(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200


@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    if not data or "title" not in data or "author" not in data:
        return jsonify({"error": "Missing title or author"}), 400

    try:
        new_book = book_model.add(
            title=data["title"],
            author=data["author"],
            published_year=data.get("published_year"),
        )
        return jsonify(new_book), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    book = book_model.update(book_id, data)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(book), 200


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    success = book_model.delete(book_id)
    if not success:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({"message": "Book deleted successfully"}), 200


# =================
# USERS ENDPOINTS
# =================


@app.route("/users", methods=["GET"])
def get_users():
    users = user_model.get_all()
    return jsonify({"users": users}), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = user_model.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Missing name or email"}), 400

    try:
        new_user = user_model.add(name=data["name"], email=data["email"])
        return jsonify(new_user), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    success = user_model.delete(user_id)
    if not success:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
