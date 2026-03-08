from flask import jsonify, request

from main import app
from Metodos.Usuarios import Usuarios


usuarios_service = Usuarios()


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    if not all(data.get(k) for k in ["name", "username", "email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        user_id = usuarios_service.create_user(
            data["name"], data["username"], data["email"], data["password"]
        )
        return jsonify({"message": "User created", "id": user_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = usuarios_service.get_users()
        return (
            jsonify(
                [{"id": u[0], "name": u[1], "username": u[2], "email": u[3]} for u in users]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user = usuarios_service.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return (
            jsonify(
                {
                    "id": user[0],
                    "name": user[1],
                    "username": user[2],
                    "email": user[3],
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/users/by-email", methods=["GET"])
def get_user_by_email():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "email query param required"}), 400
    try:
        user = usuarios_service.get_user_by_email(email)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return (
            jsonify(
                {
                    "id": user[0],
                    "name": user[1],
                    "username": user[2],
                    "email": user[3],
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/users/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    data = request.get_json() or {}
    try:
        usuarios_service.update_user(
            user_id,
            name=data.get("name"),
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
        )
        return jsonify({"message": "User updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        usuarios_service.delete_user(user_id)
        return jsonify({"message": "User deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
