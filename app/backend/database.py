import os
import logging

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

logger = logging.getLogger(__name__)

_RAW_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./benkhawiya.db",
)

# Normalise plain postgresql:// / postgres:// URLs (emitted by Railway /
# docker-compose) to the asyncpg dialect that SQLAlchemy expects.
def _normalise_url(url: str) -> str:
    for prefix in ("postgresql://", "postgres://"):
        if url.startswith(prefix):
            return url.replace(prefix, "postgresql+asyncpg://", 1)
    # Ensure sqlite URLs use the aiosqlite driver.
    if url.startswith("sqlite:///") and "+aiosqlite" not in url:
        return url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    return url


DATABASE_URL = _normalise_url(_RAW_DATABASE_URL)

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db():
    """Yield an async database session and close it when done."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """Create all tables defined by the ORM models."""
    # Import models so that their metadata is registered on Base before
    # create_all is called.
    from app.backend.models import cosmic_principle  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database tables created / verified")
