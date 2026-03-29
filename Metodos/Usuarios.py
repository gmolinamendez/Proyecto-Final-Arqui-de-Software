import bcrypt
import re

from sqlalchemy import text

from database import database


EMAIL_REGEX = re.compile(r"^(?P<local>[a-zA-Z0-9._%+-]+)@(?P<provider>[a-zA-Z0-9-]+)\.(?P<tld>[a-zA-Z]{2,63})$")
ALLOWED_EMAIL_PROVIDERS = {
    "gmail",
    "yahoo",
    "outlook",
    "hotmail",
    "protonmail",
    "icloud",
    "aol",
}

class Usuarios:
    def __init__(self):
        self.database = database()

    def _normalize_required(self, value, field_name):
        cleaned = (value or "").strip()
        if not cleaned:
            raise ValueError(f"{field_name} is required")
        return cleaned

    def _validate_email(self, email):
        match = EMAIL_REGEX.match(email)
        if not match:
            raise ValueError("Invalid email format")

        provider = match.group("provider").lower()
        if provider not in ALLOWED_EMAIL_PROVIDERS:
            allowed_values = ", ".join(sorted(ALLOWED_EMAIL_PROVIDERS))
            raise ValueError(
                f"Email provider not allowed. Use one of: {allowed_values}"
            )

    def _validate_password(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

    def create_user(self, name, username, email, password):
        name = self._normalize_required(name, "name")
        username = self._normalize_required(username, "username")
        email = self._normalize_required(email, "email")
        password = self._normalize_required(password, "password")
        email = email.lower()
        self._validate_email(email)
        self._validate_password(password)

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
        updates = {}

        if name is not None:
            updates["name"] = self._normalize_required(name, "name")
        if username is not None:
            updates["username"] = self._normalize_required(username, "username")
        if email is not None:
            cleaned_email = self._normalize_required(email, "email")
            cleaned_email = cleaned_email.lower()
            self._validate_email(cleaned_email)
            existing = self.get_user_by_email(cleaned_email)
            if existing and existing[0] != user_id:
                raise ValueError("Email already registered")
            updates["email"] = cleaned_email
        if password is not None:
            cleaned_password = self._normalize_required(password, "password")
            self._validate_password(cleaned_password)
            updates["password"] = cleaned_password

        if not updates:
            raise ValueError("At least one field is required")

        updated_rows = 0
        with self.database.engine.begin() as connection:
            if "name" in updates:
                result = connection.execute(
                    text("UPDATE Users SET name = :name WHERE id = :user_id"),
                    {"name": updates["name"], "user_id": user_id},
                )
                updated_rows = max(updated_rows, result.rowcount or 0)
            if "username" in updates:
                result = connection.execute(
                    text("UPDATE Users SET username = :username WHERE id = :user_id"),
                    {"username": updates["username"], "user_id": user_id},
                )
                updated_rows = max(updated_rows, result.rowcount or 0)
            if "email" in updates:
                result = connection.execute(
                    text("UPDATE Users SET email = :email WHERE id = :user_id"),
                    {"email": updates["email"], "user_id": user_id},
                )
                updated_rows = max(updated_rows, result.rowcount or 0)
            if "password" in updates:
                hashed_password = bcrypt.hashpw(updates["password"].encode('utf-8'), bcrypt.gensalt())
                result = connection.execute(
                    text("UPDATE Users SET password = :password WHERE id = :user_id"),
                    {"password": hashed_password.decode('utf-8'), "user_id": user_id},
                )
                updated_rows = max(updated_rows, result.rowcount or 0)

        return updated_rows > 0

    def delete_user(self, user_id):
        with self.database.engine.begin() as connection:
            result = connection.execute(
                text("DELETE FROM Users WHERE id = :user_id"),
                {"user_id": user_id},
            )
        return (result.rowcount or 0) > 0
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