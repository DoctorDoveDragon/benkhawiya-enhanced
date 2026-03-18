"""
Shared pytest fixtures.

An in-memory SQLite database is used for all tests so that the suite can run
without a real PostgreSQL instance.
"""
import os
import pytest
import pytest_asyncio

# Point the app at an in-memory SQLite database before any app module is
# imported so that the engine is created with the right URL.
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.backend.database import Base
from app.backend.models import cosmic_principle  # noqa: F401 – registers model


@pytest_asyncio.fixture
async def db_session():
    """Yield a fresh async session backed by an in-memory SQLite database."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
