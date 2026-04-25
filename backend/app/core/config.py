import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH if ENV_PATH.exists() else None)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:123456@localhost:5432/ebook2latex_db",
)
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
UPLOAD_DIR = BASE_DIR / "uploads"
FORMULA_IMAGE_DIR = BASE_DIR / "formula_images"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
FORMULA_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
