"""Tests for the database seed layer."""
import pytest
from sqlalchemy import select

from app.backend.models.cosmic_principle import CosmicPrinciple
from app.backend.seeds.cosmic_principles import (
    COSMIC_PRINCIPLES_DATA,
    seed_cosmic_principles,
)


@pytest.mark.asyncio
async def test_seed_populates_empty_table(db_session):
    """Running the seed on an empty table inserts every principle."""
    await seed_cosmic_principles(db_session)

    result = await db_session.execute(select(CosmicPrinciple))
    rows = result.scalars().all()

    assert len(rows) == len(COSMIC_PRINCIPLES_DATA)


@pytest.mark.asyncio
async def test_seed_data_matches_expected_values(db_session):
    """Verify the names, meanings and aspects stored match the seed definitions."""
    await seed_cosmic_principles(db_session)

    result = await db_session.execute(select(CosmicPrinciple).order_by(CosmicPrinciple.id))
    rows = result.scalars().all()

    for row, expected in zip(rows, COSMIC_PRINCIPLES_DATA):
        assert row.name == expected["name"]
        assert row.meaning == expected["meaning"]
        assert row.aspect == expected["aspect"]


@pytest.mark.asyncio
async def test_seed_is_idempotent(db_session):
    """Calling the seed function twice must not insert duplicates."""
    await seed_cosmic_principles(db_session)
    await seed_cosmic_principles(db_session)

    result = await db_session.execute(select(CosmicPrinciple))
    rows = result.scalars().all()

    assert len(rows) == len(COSMIC_PRINCIPLES_DATA)


@pytest.mark.asyncio
async def test_seed_contains_all_seven_principles(db_session):
    """There must be exactly 7 cosmic principles."""
    await seed_cosmic_principles(db_session)

    result = await db_session.execute(select(CosmicPrinciple))
    rows = result.scalars().all()

    assert len(rows) == 7
    names = {r.name for r in rows}
    assert "DÁNÁ" in names
    assert "MÁTÁ" in names
    assert "HÓTÉ" in names
    assert "MÉKÁ" in names
    assert "SÉBÁ" in names
    assert "KÉPÉ" in names
    assert "ÌTỌJÚ" in names


@pytest.mark.asyncio
async def test_principle_names_are_unique(db_session):
    """Each principle name must be unique in the table."""
    await seed_cosmic_principles(db_session)

    result = await db_session.execute(select(CosmicPrinciple))
    rows = result.scalars().all()

    names = [r.name for r in rows]
    assert len(names) == len(set(names))
