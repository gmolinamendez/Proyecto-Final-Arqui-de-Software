from main import app
import os
from flask import Flask, jsonify, redirect, render_template, request, url_for
from sqlalchemy import create_engine, text
from database import engine

from Metodos.Usuarios import *
from Metodos.Eventos import *


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