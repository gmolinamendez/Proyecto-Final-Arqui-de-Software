from flask import jsonify, request

from app_instance import app
from Metodos.Eventos import Eventos


eventos_service = Eventos()


@app.route("/events/<int:event_id>/attendees", methods=["POST"])
def add_attendee(event_id):
    data = request.get_json() or {}
    if data.get("person_id") is None:
        return jsonify({"error": "person_id required"}), 400
    try:
        eventos_service.add_attendee(event_id, data["person_id"])
        return jsonify({"message": "Attendee added"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/events/<int:event_id>/attendees", methods=["GET"])
def get_attendees(event_id):
    try:
        attendees = eventos_service.get_attendees(event_id)
        return (
            jsonify([{"id": a[0], "name": a[1], "age": a[2]} for a in attendees]),
            200,
        )
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/events/<int:event_id>/attendees/<int:person_id>", methods=["DELETE"])
def remove_attendee(event_id, person_id):
    try:
        removed = eventos_service.remove_attendee(event_id, person_id)
        if not removed:
            return jsonify({"error": "Attendee not found for this event"}), 404
        return jsonify({"message": "Attendee removed"}), 200
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
