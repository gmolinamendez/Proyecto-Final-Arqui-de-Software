import requests
import os
from flask import Flask, jsonify, redirect, render_template, request, url_for
from sqlalchemy import create_engine, text
from database import engine
from main import app

from Metodos.Usuarios import *
from Metodos.Eventos import *



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