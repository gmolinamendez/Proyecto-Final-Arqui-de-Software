import os

from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine, text
import psycopg2

app = Flask(__name__)

# PostgreSQL connection string
# Format: postgresql+psycopg2://username:password@host:port/database
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:BackEnd@localhost:5432/postgres"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

class database():
    def __init__(self):
        self.engine = engine
    def db_test(self):
        result = None
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
        return result
    
    def get_all_table(self, table_name):
        with self.engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {table_name}"))
            records = result.fetchall()
        return records

    def get_all_persons(self):
        return self.get_all_table("Persons")
        persons = result.fetchall()
        return persons
    
    def add_persons(self, name, age, monthlySalary):
        with self.engine.connect() as connection:
            connection.execute(
                text(
                    "INSERT INTO Persons (name, age, monthlySalary) VALUES (:name, :age, :monthlySalary)"
                ),
                {"name": name, "age": age, "monthlySalary": monthlySalary},
            )
            connection.commit()
    
    def get_all_products(self):
        return self.get_all_table("Products")
        products = result.fetchall()
        return products
    
    def add_product(self, name, description, quantity, cost, selldefault):
        with self.engine.connect() as connection:
            connection.execute(
                text(
                    "INSERT INTO Products (name, description, quantity, cost, sellDefault) VALUES (:name, :description, :quantity, :cost, :selldefault)"
                ),
                {
                    "name": name,
                    "description": description,
                    "quantity": quantity,
                    "cost": cost,
                    "selldefault": selldefault,
                },
            )
            connection.commit()

    def close(self):
        self.engine.close()
        