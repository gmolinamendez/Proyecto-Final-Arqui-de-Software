import sys
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database import engine


CREATE_USERS_SQL = """
CREATE TABLE IF NOT EXISTS public.users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""


ALTER_USERS_SQL = [
    """
    ALTER TABLE public.users
    ADD COLUMN IF NOT EXISTS username VARCHAR(50)
    """,
    """
    ALTER TABLE public.users
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    """,
    """
    ALTER TABLE public.users
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    """,
    """
    ALTER TABLE public.users
    ALTER COLUMN name SET NOT NULL
    """,
    """
    ALTER TABLE public.users
    ALTER COLUMN email SET NOT NULL
    """,
    """
    ALTER TABLE public.users
    ALTER COLUMN password SET NOT NULL
    """,
    """
    ALTER TABLE public.users
    ALTER COLUMN username SET NOT NULL
    """,
    """
    CREATE UNIQUE INDEX IF NOT EXISTS users_email_key
    ON public.users (email)
    """,
    """
    CREATE UNIQUE INDEX IF NOT EXISTS users_username_key
    ON public.users (username)
    """,
]


def main() -> None:
    try:
        with engine.begin() as connection:
            connection.execute(text(CREATE_USERS_SQL))
            for statement in ALTER_USERS_SQL:
                connection.execute(text(statement))
    except SQLAlchemyError as exc:
        print("Users table setup failed.")
        print(exc)
        raise SystemExit(1)

    print("Users table is ready.")


if __name__ == "__main__":
    main()
