import sys
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database import engine


CREATE_EVENTS_SQL = """
CREATE TABLE IF NOT EXISTS public.events (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""


ALTER_EVENTS_SQL = [
    """
    ALTER TABLE public.events
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    """,
    """
    ALTER TABLE public.events
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    """,
    """
    ALTER TABLE public.events
    ALTER COLUMN name SET NOT NULL
    """,
    """
    ALTER TABLE public.events
    ALTER COLUMN date SET NOT NULL
    """,
    """
    ALTER TABLE public.events
    ALTER COLUMN location SET NOT NULL
    """,
    """
    CREATE INDEX IF NOT EXISTS events_date_idx
    ON public.events (date)
    """,
]


def main() -> None:
    try:
        with engine.begin() as connection:
            connection.execute(text(CREATE_EVENTS_SQL))
            for statement in ALTER_EVENTS_SQL:
                connection.execute(text(statement))
    except SQLAlchemyError as exc:
        print("Events table setup failed.")
        print(exc)
        raise SystemExit(1)

    print("Events table is ready.")


if __name__ == "__main__":
    main()
