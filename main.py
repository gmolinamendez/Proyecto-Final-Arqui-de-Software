import os

from flask import Flask, jsonify, redirect, render_template, request, url_for
from sqlalchemy import create_engine, text
from database import engine
from Metodos.Usuarios import Usuarios
from Metodos.eventos import Eventos


app = Flask(__name__)
usuarios_service = Usuarios()
eventos_service = Eventos()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:BackEnd@localhost:5432/postgres"
)



@app.route("/")
def hello():
    return render_template("index.html", message="Hello from Flask with PostgreSQL!")


############################################## USUARIOS ####################################################

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    if not all(data.get(k) for k in ["name", "username", "email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        user_id = usuarios_service.create_user(data["name"], data["username"], data["email"], data["password"])
        return jsonify({"message": "User created", "id": user_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = usuarios_service.get_users()
        return jsonify([{"id": u[0], "name": u[1], "username": u[2], "email": u[3]} for u in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user = usuarios_service.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"id": user[0], "name": user[1], "username": user[2], "email": user[3]}), 200
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
        return jsonify({"id": user[0], "name": user[1], "username": user[2], "email": user[3]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    data = request.get_json() or {}
    try:
        usuarios_service.update_user(user_id, name=data.get("name"), username=data.get("username"), email=data.get("email"), password=data.get("password"))
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


############################################## EVENTOS ####################################################

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json() or {}
    if not all(data.get(k) for k in ["name", "date", "location"]):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        event_id = eventos_service.create_event(data["name"], data["date"], data["location"])
        return jsonify({"message": "Event created", "id": event_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/events", methods=["GET"])
def get_events():
    try:
        events = eventos_service.get_events()
        return jsonify([{"id": e[0], "name": e[1], "date": str(e[2]), "location": e[3]} for e in events]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/events/<int:event_id>", methods=["GET"])
def get_event_by_id(event_id):
    try:
        event = eventos_service.get_events_by_id(event_id)            
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return jsonify({"id": event[0], "name": event[1], "date": str(event[2]), "location": event[3]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json() or {}
    try:
        eventos_service.update_event(event_id, name=data.get("name"), date=data.get("date"), location=data.get("location"))
        return jsonify({"message": "Event updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    try:
        eventos_service.delete_event(event_id)
        return jsonify({"message": "Event deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


############################################## PERSONS ####################################################

@app.route("/persons", methods=["POST"])
def create_person():
    data = request.get_json() or {}
    if not data.get("name") or data.get("age") is None:
        return jsonify({"error": "name and age required"}), 400
    try:
        person_id = eventos_service.create_person(data["name"], data["age"])
        return jsonify({"message": "Person created", "id": person_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/persons", methods=["GET"])
def get_persons():
    try:
        persons = eventos_service.get_persons()
        return jsonify([{"id": p[0], "name": p[1], "age": p[2]} for p in persons]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/persons/<int:person_id>", methods=["DELETE"])
def delete_person(person_id):
    try:
        eventos_service.delete_person(person_id)
        return jsonify({"message": "Person deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


############################################## ATTENDEES ####################################################

@app.route("/events/<int:event_id>/attendees", methods=["POST"])
def add_attendee(event_id):
    data = request.get_json() or {}
    if data.get("person_id") is None:
        return jsonify({"error": "person_id required"}), 400
    try:
        eventos_service.add_attendee(event_id, data["person_id"])
        return jsonify({"message": "Attendee added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/events/<int:event_id>/attendees", methods=["GET"])
def get_attendees(event_id):
    try:
        attendees = eventos_service.get_attendees(event_id)
        return jsonify([{"id": a[0], "name": a[1], "age": a[2]} for a in attendees]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/events/<int:event_id>/attendees/<int:person_id>", methods=["DELETE"])
def remove_attendee(event_id, person_id):
    try:
        eventos_service.remove_attendee(event_id, person_id)
        return jsonify({"message": "Attendee removed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)