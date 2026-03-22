from flask import jsonify, request

from app_instance import app
from Metodos.eventos import Eventos


eventos_service = Eventos()


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json() or {}
    if not all(data.get(k) for k in ["name", "date", "location"]):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        event_id = eventos_service.create_event(
            data["name"], data["date"], data["location"]
        )
        return jsonify({"message": "Event created", "id": event_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/events", methods=["GET"])
def get_events():
    try:
        events = eventos_service.get_events()
        return (
            jsonify(
                [
                    {
                        "id": e[0],
                        "name": e[1],
                        "date": str(e[2]),
                        "location": e[3],
                    }
                    for e in events
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/events/<int:event_id>", methods=["GET"])
def get_event_by_id(event_id):
    try:
        event = eventos_service.get_events_by_id(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return (
            jsonify(
                {
                    "id": event[0],
                    "name": event[1],
                    "date": str(event[2]),
                    "location": event[3],
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json() or {}
    try:
        eventos_service.update_event(
            event_id,
            name=data.get("name"),
            date=data.get("date"),
            location=data.get("location"),
        )
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
