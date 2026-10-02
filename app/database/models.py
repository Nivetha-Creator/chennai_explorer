from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from app.database.session import Base


class Area(Base):

    __tablename__ = "areas"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(100),
        nullable=False,
        unique=True,
    )

    name_ta = Column(
        String(100),
        nullable=True,
    )

    lat = Column(
        Float,
        nullable=True,
    )

    lng = Column(
        Float,
        nullable=True,
    )


class Place(Base):

    __tablename__ = "places"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(200),
        nullable=False,
    )

    name_ta = Column(
        String(200),
        nullable=True,
    )

    category = Column(
        String(100),
        nullable=False,
    )

    area_id = Column(
        Integer,
        ForeignKey("areas.id"),
        nullable=True,
    )

    lat = Column(
        Float,
        nullable=True,
    )

    lng = Column(
        Float,
        nullable=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    visit_duration_min = Column(
        Integer,
        nullable=True,
    )

    entry_fee_inr = Column(
        Float,
        nullable=True,
    )

    hours_note = Column(
        String(300),
        nullable=True,
    )

    indoor_outdoor = Column(
        String(50),
        nullable=True,
    )

    best_time = Column(
        String(100),
        nullable=True,
    )

    source = Column(
        String(200),
        nullable=True,
    )

    source_url = Column(
        String(500),
        nullable=True,
    )

    last_verified_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


class Eatery(Base):

    __tablename__ = "eateries"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(200),
        nullable=False,
    )

    area_id = Column(
        Integer,
        ForeignKey("areas.id"),
        nullable=True,
    )

    lat = Column(
        Float,
        nullable=True,
    )

    lng = Column(
        Float,
        nullable=True,
    )

    diet = Column(
        String(100),
        nullable=True,
    )

    cuisine = Column(
        String(100),
        nullable=True,
    )

    price_band = Column(
        String(50),
        nullable=True,
    )

    notes = Column(
        Text,
        nullable=True,
    )

    source = Column(
        String(200),
        nullable=True,
    )

    last_verified_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


class Dish(Base):

    __tablename__ = "dishes"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(150),
        nullable=False,
    )

    name_ta = Column(
        String(150),
        nullable=True,
    )

    diet = Column(
        String(100),
        nullable=True,
    )

    description = Column(
        Text,
        nullable=True,
    )


class TransportNode(Base):

    __tablename__ = "transport_nodes"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(150),
        nullable=False,
    )

    mode = Column(
        String(50),
        nullable=False,
    )

    line = Column(
        String(100),
        nullable=True,
    )

    area_id = Column(
        Integer,
        ForeignKey("areas.id"),
        nullable=True,
    )

    lat = Column(
        Float,
        nullable=True,
    )

    lng = Column(
        Float,
        nullable=True,
    )


class TransportHint(Base):

    __tablename__ = "transport_hints"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    from_area = Column(
        String(100),
        nullable=False,
    )

    to_area = Column(
        String(100),
        nullable=False,
    )

    mode = Column(
        String(50),
        nullable=False,
    )

    typical_minutes = Column(
        Integer,
        nullable=True,
    )

    approx_fare_inr = Column(
        Float,
        nullable=True,
    )

    notes = Column(
        Text,
        nullable=True,
    )

    last_verified_at = Column(
        DateTime,
        default=datetime.utcnow,
    )