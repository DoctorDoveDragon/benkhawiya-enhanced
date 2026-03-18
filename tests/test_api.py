"""Tests for the FastAPI endpoints, including the DB-backed cosmic-principles route."""
import os
import pytest
import pytest_asyncio

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.backend.database import Base, get_db
from app.backend.models import cosmic_principle  # noqa: F401 – register model
from app.backend.seeds.cosmic_principles import seed_cosmic_principles, COSMIC_PRINCIPLES_DATA


# ---------------------------------------------------------------------------
# Shared async app fixture that overrides the DB dependency with a test DB
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture
async def client():
    """
    Yield an httpx AsyncClient pointed at the FastAPI app with the DB
    dependency overridden to use an isolated in-memory SQLite database.
    """
    # Build an isolated engine + session factory for this test.
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # Seed the test DB.
    async with session_factory() as seed_session:
        await seed_cosmic_principles(seed_session)

    # Override the get_db dependency so the app uses our test session.
    async def override_get_db():
        async with session_factory() as session:
            yield session

    # Import app here (after env var is set) to avoid module-level side-effects.
    from app.backend.main import app

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


# ---------------------------------------------------------------------------
# /api/cosmic-principles
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_cosmic_principles_returns_200(client):
    response = await client.get("/api/cosmic-principles")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_cosmic_principles_returns_all_seven(client):
    response = await client.get("/api/cosmic-principles")
    data = response.json()
    assert "principles" in data
    assert len(data["principles"]) == len(COSMIC_PRINCIPLES_DATA)


@pytest.mark.asyncio
async def test_cosmic_principles_schema(client):
    """Each principle object must have name, meaning and aspect keys."""
    response = await client.get("/api/cosmic-principles")
    for p in response.json()["principles"]:
        assert "name" in p
        assert "meaning" in p
        assert "aspect" in p


@pytest.mark.asyncio
async def test_cosmic_principles_first_entry(client):
    """The first principle seeded must be DÁNÁ / Truth."""
    response = await client.get("/api/cosmic-principles")
    first = response.json()["principles"][0]
    assert first["name"] == "DÁNÁ"
    assert first["meaning"] == "Truth"
    assert first["aspect"] == "pelu"


# ---------------------------------------------------------------------------
# /health
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_health_reports_db_connected(client):
    response = await client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["services"]["database"] == "connected"


@pytest.mark.asyncio
async def test_health_status_healthy_when_db_connected(client):
    response = await client.get("/health")
    assert response.json()["status"] == "healthy"


# ---------------------------------------------------------------------------
# /api/status
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_api_status(client):
    response = await client.get("/api/status")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"
