from sqlalchemy import text
from database import database
import bcrypt

class Usuarios:
    def __init__(self):
        self.database = database()
    
    def create_user(self, name, username, email, password):
        existing = self.get_user_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with self.database.engine.begin() as connection:
            result = connection.execute(
                text(
                    "INSERT INTO Users (name, username, email, password) VALUES (:name, :username, :email, :password) RETURNING id"
                ),
                {"name": name, "username": username, "email": email, "password": hashed_password.decode('utf-8')},
            )
            user_id = result.fetchone()[0]
        return user_id
    
    def get_user_by_email(self, email):
        with self.database.engine.connect() as connection:
            result = connection.execute(
                text("SELECT id, name, username, email FROM Users WHERE email = :email"),
                {"email": email},
            )
            user = result.fetchone()
        return user
    
    def get_user_by_id(self, user_id):
        with self.database.engine.connect() as connection:
            result = connection.execute(
                text("SELECT id, name, username, email FROM Users WHERE id = :user_id"),
                {"user_id": user_id},
            )
            user = result.fetchone()
        return user
    
    def get_users(self):
        with self.database.engine.connect() as connection:
            result = connection.execute(
                text("SELECT id, name, username, email FROM Users")
            )
            users = result.fetchall()
        return users
    
    def update_user(self, user_id, name=None, username=None, email=None, password=None):
        with self.database.engine.begin() as connection:
            if name:
                connection.execute(
                    text("UPDATE Users SET name = :name WHERE id = :user_id"),
                    {"name": name, "user_id": user_id},
                )
            if username:
                connection.execute(
                    text("UPDATE Users SET username = :username WHERE id = :user_id"),
                    {"username": username, "user_id": user_id},
                )
            if email:
                connection.execute(
                    text("UPDATE Users SET email = :email WHERE id = :user_id"),
                    {"email": email, "user_id": user_id},
                )
            if password:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                connection.execute(
                    text("UPDATE Users SET password = :password WHERE id = :user_id"),
                    {"password": hashed_password.decode('utf-8'), "user_id": user_id},
                )

    def delete_user(self, user_id):
        with self.database.engine.begin() as connection:
            connection.execute(
                text("DELETE FROM Users WHERE id = :user_id"),
                {"user_id": user_id},
            )
#######################################################Log In#######################################################
    
    def verify_user(self, email, password):
        with self.database.engine.connect() as connection:
            result = connection.execute(
                text("SELECT password FROM Users WHERE email = :email"),
                {"email": email}
            )
            row = result.fetchone()
        if not row:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), row[0].encode('utf-8')) 