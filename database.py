import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:BackEnd@localhost:5432/postgres"
)

engine = create_engine(DATABASE_URL)