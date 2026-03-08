import sys
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database import engine


CREATE_PERSONS_SQL = """
CREATE TABLE IF NOT EXISTS public.persons (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT persons_age_check CHECK (age >= 0)
);
"""


ALTER_PERSONS_SQL = [
    """
    ALTER TABLE public.persons
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    """,
    """
    ALTER TABLE public.persons
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    """,
    """
    ALTER TABLE public.persons
    ALTER COLUMN name SET NOT NULL
    """,
    """
    ALTER TABLE public.persons
    ALTER COLUMN age SET NOT NULL
    """,
]


def main() -> None:
    try:
        with engine.begin() as connection:
            connection.execute(text(CREATE_PERSONS_SQL))
            for statement in ALTER_PERSONS_SQL:
                connection.execute(text(statement))
    except SQLAlchemyError as exc:
        print("Persons table setup failed.")
        print(exc)
        raise SystemExit(1)

    print("Persons table is ready.")


if __name__ == "__main__":
    main()
