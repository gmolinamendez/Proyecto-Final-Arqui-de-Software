import os

from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine, text
from database import database
from logic import BusinessLogic
import psycopg2


app = Flask(__name__)
database = database()
blogic = BusinessLogic()

# PostgreSQL connection string
# Format: postgresql+psycopg2://username:password@host:port/database
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:BackEnd@localhost:5432/postgres"
)

# engine
engine = create_engine(DATABASE_URL)


@app.route("/")
def hello():
    return render_template("index.html", message="Hello from Flask with PostgreSQL!")


@app.route("/db-test")
def db_test():
    #Test database connection
    try:
        result = blogic.run_database_test()
        print('Running Tests', result)
        return render_template(
            "db_test.html",
            status="success",
            message="Database connection successful!",
            )
    except Exception as e:
        return render_template("db_test.html", status="error", message=str(e)), 500


@app.route("/persons")
def list_persons():
    # Show everyone
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM Persons"))
            persons = result.fetchall()
            return render_template("persons_list.html", persons=persons)
    except Exception as e:
        return render_template("error.html", message=str(e)), 500


@app.route("/persons/add", methods=["GET", "POST"])
def add_person():
    #Add a new person
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        monthlySalary = request.form.get("monthlySalary")
        try:
            with engine.connect() as connection:
                connection.execute(
                    text(
                        "INSERT INTO Persons (name, age, monthlySalary) VALUES (:name, :age, :monthlySalary)"
                    ),
                    {"name": name, "age": age, "monthlySalary": monthlySalary},
                )
                connection.commit()
            return redirect(url_for("list_persons"))
        except Exception as e:
            return render_template("error.html", message=str(e)), 500
    return render_template("persons_add.html")


@app.route("/products")
def list_products():
    # Show all products
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM Products"))
            products = result.fetchall()
            return render_template("products_list.html", products=products)
    except Exception as e:
        return render_template("error.html", message=str(e)), 500


@app.route("/products/add", methods=["GET"])
def add_product_get():
    return render_template("products_add.html")


@app.route("/products/add", methods=["POST"])
def add_product():
    name = request.form.get("name")
    description = request.form.get("description")
    quantity = request.form.get("quantity")
    cost = request.form.get("cost")
    selldefault = request.form.get("selldefault")

    try:
        database.add_product(name, description, quantity, cost, selldefault)
        return redirect(url_for("list_products"))
    except Exception as e:
        return render_template("error.html", message=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)