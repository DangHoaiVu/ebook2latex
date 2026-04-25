from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import DATABASE_URL

# Tao engine ket noi PostgreSQL cho moi truong local.
engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)

# Factory de tao session lam viec voi database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base dung cho cac model ORM ke thua.
Base = declarative_base()


def get_db():
    """Dependency dung trong FastAPI de cap va dong session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
