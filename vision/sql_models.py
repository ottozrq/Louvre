# import pathlib
import re
import uuid
# from typing import Any, Dict, List

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship


class _tablemixin:
    @declared_attr
    def __tablename__(cls):
        def _join(match):
            word = match.group()

            if len(word) > 1:
                return f"_{word[:-1]}_{word[-1]}".lower()

            return f"_{word.lower()}"

        return re.compile(r"([A-Z]+)(?=[a-z0-9])").sub(_join, cls.__name__).lstrip("_")


class _postgresql_tablemixin(_tablemixin):
    inserted_at = Column(DateTime(True), server_default=func.now(), nullable=False)


PsqlBase = declarative_base(cls=_postgresql_tablemixin)
PsqlBase.__table_args__ = {"schema": "vision_sources"}

rel = relationship


def seq(name):
    return Column(name, BigInteger, primary_key=True, autoincrement=True, unique=True)


def enum_field(klass, nullable=False, **kwargs):
    return Column(Enum(klass), nullable=nullable, **kwargs)


def uuid_field(name=None, primary_key=False, default=False):
    return Column(
        *([name] if name else []),
        UUID(as_uuid=False),
        primary_key=primary_key,
        server_default=func.uuid_generate_v4(),
        default=uuid.uuid4 if default else None,
        unique=True,
        nullable=False,
    )


def fk(foreign_field, nullable=False, index=True, ondelete="CASCADE", **kwargs):
    return Column(
        None,
        ForeignKey(
            foreign_field,
            ondelete=ondelete,
            onupdate="CASCADE",
        ),
        nullable=nullable,
        index=index,
        **kwargs,
    )


def name_field(nullable=False):
    return Column(
        String,
        nullable=nullable,
    )


class Landmark(PsqlBase):
    landmark_id = seq("landmark_id")
    landmark_name = name_field()
    country = Column(String, nullable=True)


class Artwork(PsqlBase):
    artwork_id = seq("artwork_id")
    artwork_name = name_field()
    landmark_id = fk(Landmark.landmark_id)
    landmark = rel(Landmark, back_populates="artworks")
