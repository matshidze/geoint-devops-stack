import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def database_uri() -> str:
    # Prefer DATABASE_URL (12-factor), fallback to parts.
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    user = os.getenv("POSTGRES_USER", "geoinuser")
    password = os.getenv("POSTGRES_PASSWORD", "geointpass")
    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    name = os.getenv("POSTGRES_DB", "appdb")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"
