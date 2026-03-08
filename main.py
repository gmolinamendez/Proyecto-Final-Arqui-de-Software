import os
from flask import Flask, jsonify, redirect, render_template, request, url_for
from sqlalchemy import create_engine, text
from database import engine

from APIs.Users import *
from APIs.Events import *
from APIs.Persons import *
from APIs.Attendees import *

from Metodos.Usuarios import Usuarios
from Metodos.Eventos import Eventos


app = Flask(__name__)
usuarios_service = Usuarios()
eventos_service = Eventos()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:BackEnd@localhost:5432/postgres"
)



@app.route("/")
def hello():
    return render_template("index.html", message="Hello from Flask with PostgreSQL!")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)