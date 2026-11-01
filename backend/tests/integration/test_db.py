from sqlalchemy import text
from app.db.session import engine


def test_database_connection():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT version()")
        )

        version = result.scalar()

        assert version is not None
        assert "PostgreSQL" in version