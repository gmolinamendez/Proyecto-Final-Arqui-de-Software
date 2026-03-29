from sqlalchemy import text
from database import engine


class Eventos:
    def __init__(self):
        pass

    def create_person(self, name, age):
        with engine.begin() as connection:
            result = connection.execute(
                text(
                    "INSERT INTO Persons (name, age) VALUES (:name, :age) RETURNING id"
                ),
                {"name": name, "age": age},
            )
            person_id = result.fetchone()[0]
        return person_id

    def create_event(self, name, date, location):
        with engine.begin() as connection:
            result = connection.execute(
                text(
                    "INSERT INTO Events (name, date, location) VALUES (:name, :date, :location) RETURNING id"
                ),
                {"name": name, "date": date, "location": location},
            )
            event_id = result.fetchone()[0]
        return event_id

    def add_attendee(self, event_id, person_id):
        with engine.begin() as connection:
            existing = connection.execute(
                text(
                    "SELECT 1 FROM EventAttendees WHERE event_id = :event_id AND person_id = :person_id"
                ),
                {"event_id": event_id, "person_id": person_id},
            ).fetchone()
            if existing:
                raise ValueError("Attendee already registered for this event")

            connection.execute(
                text(
                    "INSERT INTO EventAttendees (event_id, person_id) VALUES (:event_id, :person_id)"
                ),
                {"event_id": event_id, "person_id": person_id},
            )

    def update_event(self, event_id, name=None, date=None, location=None):
        if name is None and date is None and location is None:
            raise ValueError("At least one field is required")

        updated_rows = 0
        with engine.begin() as connection:
            if name is not None:
                result = connection.execute(
                    text("UPDATE Events SET name = :name WHERE id = :event_id"),
                    {"name": name, "event_id": event_id},
                )
                updated_rows = max(updated_rows, result.rowcount or 0)
            if date is not None:
                result = connection.execute(
                    text("UPDATE Events SET date = :date WHERE id = :event_id"),
                    {"date": date, "event_id": event_id},
                )
                updated_rows = max(updated_rows, result.rowcount or 0)
            if location is not None:
                result = connection.execute(
                    text("UPDATE Events SET location = :location WHERE id = :event_id"),
                    {"location": location, "event_id": event_id},
                )
                updated_rows = max(updated_rows, result.rowcount or 0)

        return updated_rows > 0

    def get_attendees(self, event_id):
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    "SELECT p.id, p.name, p.age FROM Persons p JOIN EventAttendees ea ON p.id = ea.person_id WHERE ea.event_id = :event_id"
                ),
                {"event_id": event_id},
            )
            attendees = result.fetchall()
        return attendees

    def get_events(self):
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM Events"))
            events = result.fetchall()
        return events

    def get_events_by_id(self, event_id):
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT * FROM Events WHERE id = :event_id"),
                {"event_id": event_id},
            )
            event = result.fetchone()
        return event

    def get_persons(self):
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM Persons"))
            persons = result.fetchall()
        return persons

    def delete_event(self, event_id):
        with engine.begin() as connection:
            connection.execute(
                text("DELETE FROM EventAttendees WHERE event_id = :event_id"),
                {"event_id": event_id},
            )
            result = connection.execute(
                text("DELETE FROM Events WHERE id = :event_id"),
                {"event_id": event_id},
            )
        return (result.rowcount or 0) > 0

    def remove_attendee(self, event_id, person_id):
        with engine.begin() as connection:
            result = connection.execute(
                text(
                    "DELETE FROM EventAttendees WHERE event_id = :event_id AND person_id = :person_id"
                ),
                {"event_id": event_id, "person_id": person_id},
            )
        return (result.rowcount or 0) > 0

    def delete_person(self, person_id):
        with engine.begin() as connection:
            connection.execute(
                text("DELETE FROM EventAttendees WHERE person_id = :person_id"),
                {"person_id": person_id},
            )
            result = connection.execute(
                text("DELETE FROM Persons WHERE id = :person_id"),
                {"person_id": person_id},
            )
        return (result.rowcount or 0) > 0
