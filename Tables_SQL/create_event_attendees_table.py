import sys
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database import engine


CREATE_EVENT_ATTENDEES_SQL = """
CREATE TABLE IF NOT EXISTS public.eventattendees (
    event_id BIGINT NOT NULL,
    person_id BIGINT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (event_id, person_id),
    CONSTRAINT fk_eventattendees_event
        FOREIGN KEY (event_id)
        REFERENCES public.events(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_eventattendees_person
        FOREIGN KEY (person_id)
        REFERENCES public.persons(id)
        ON DELETE CASCADE
);
"""


ALTER_EVENT_ATTENDEES_SQL = [
    """
    ALTER TABLE public.eventattendees
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    """,
    """
    CREATE INDEX IF NOT EXISTS eventattendees_person_id_idx
    ON public.eventattendees (person_id)
    """,
]


def main() -> None:
    try:
        with engine.begin() as connection:
            connection.execute(text(CREATE_EVENT_ATTENDEES_SQL))
            for statement in ALTER_EVENT_ATTENDEES_SQL:
                connection.execute(text(statement))
    except SQLAlchemyError as exc:
        print("EventAttendees table setup failed.")
        print(exc)
        raise SystemExit(1)

    print("EventAttendees table is ready.")


if __name__ == "__main__":
    main()
