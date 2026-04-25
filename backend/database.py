"""
database.py - Cau hinh ket noi SQLAlchemy voi PostgreSQL.
Doc DATABASE_URL tu file .env bang thu vien python-dotenv.
"""

import os
import sys
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Doc bien moi truong tu file .env cung thu muc
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")

# URL-encode ky tu dac biet trong password (vi du: @ -> %40)
# De tranh psycopg2 parse sai khi password chua @
if DATABASE_URL and "@" in DATABASE_URL:
    # Tach cac phan: scheme://user:password@host:port/db
    prefix, rest = DATABASE_URL.split("://", 1)      # 'postgresql', 'user:pass@host/db'
    credentials, location = rest.rsplit("@", 1)       # 'user:pass', 'host/db'
    if ":" in credentials:
        user, password = credentials.split(":", 1)
        DATABASE_URL = f"{prefix}://{user}:{quote_plus(password)}@{location}"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL chưa được cấu hình trong file .env")

# Tạo engine kết nối tới PostgreSQL
engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)

# Factory để tạo session làm việc với database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class dùng cho tất cả các ORM model
Base = declarative_base()


def get_db():
    """Dependency dùng trong FastAPI để cấp và đóng session tự động."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    """Test ket noi database khi chay truc tiep: python database.py"""
    # Dung UTF-8 de hien thi dung tren moi terminal Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        with engine.connect() as connection:
            print("=" * 55)
            print("[OK] Ket noi PostgreSQL thanh cong!")
            print(f"     DATABASE_URL (da encode): {DATABASE_URL}")
            print("=" * 55)
    except Exception as e:
        print("=" * 55)
        print(f"[FAIL] Ket noi that bai: {e}")
        print("=" * 55)
