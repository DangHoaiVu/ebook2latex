from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router
from app.core.config import FRONTEND_ORIGIN
from app.core.database import Base, engine
from app import models  # noqa: F401 - import de SQLAlchemy nhan dien model


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Tao bang khi ung dung khoi dong de co the chay local ngay.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Ebook2LateX API",
    version="0.3.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
