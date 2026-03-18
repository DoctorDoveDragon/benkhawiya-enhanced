from sqlalchemy import Column, Integer, String
from app.backend.database import Base


class CosmicPrinciple(Base):
    """A single cosmic principle in the Benkhawiya cosmological framework."""

    __tablename__ = "cosmic_principles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    meaning = Column(String, nullable=False)
    aspect = Column(String, nullable=False)
