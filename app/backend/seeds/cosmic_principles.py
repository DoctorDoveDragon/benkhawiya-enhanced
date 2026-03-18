import logging
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.models.cosmic_principle import CosmicPrinciple

logger = logging.getLogger(__name__)

# Initial seed data for the Benkhawiya cosmological framework
COSMIC_PRINCIPLES_DATA = [
    {"name": "DÁNÁ",   "meaning": "Truth",       "aspect": "pelu"},
    {"name": "MÁTÁ",   "meaning": "Justice",     "aspect": "sewu"},
    {"name": "HÓTÉ",   "meaning": "Harmony",     "aspect": "ruwa"},
    {"name": "MÉKÁ",   "meaning": "Balance",     "aspect": "temu"},
    {"name": "SÉBÁ",   "meaning": "Order",       "aspect": "sewu"},
    {"name": "KÉPÉ",   "meaning": "Reciprocity", "aspect": "ruwa"},
    {"name": "ÌTỌJÚ", "meaning": "Mystery",      "aspect": "ntu"},
]


async def seed_cosmic_principles(db: AsyncSession) -> None:
    """Populate the cosmic_principles table if it is empty."""
    result = await db.execute(select(func.count()).select_from(CosmicPrinciple))
    existing = result.scalar_one()
    if existing > 0:
        logger.info(
            "🌌 Cosmic principles already seeded (%d rows) – skipping", existing
        )
        return

    for data in COSMIC_PRINCIPLES_DATA:
        db.add(CosmicPrinciple(**data))

    await db.commit()
    logger.info("✅ Seeded %d cosmic principles", len(COSMIC_PRINCIPLES_DATA))
