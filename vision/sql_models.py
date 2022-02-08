# import pathlib
import re
import uuid

from typing import List
import sqlalchemy
from geoalchemy2 import Geography, Geometry
from geoalchemy2.functions import ST_IsValid
from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    String,
    func,
    select,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSON, UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import column_property, relationship

from utils.auto_enum import AutoEnum, auto


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


class Language(AutoEnum):
    cn = auto()
    en = auto()
    fr = auto()


def _language_column():
    return enum_field(
        Language, server_default=Language.en, default=Language.en, nullable=False
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


class GeoJsonBase:
    geometry = Column(
        Geography(spatial_index=False),
        CheckConstraint(
            ST_IsValid(sqlalchemy.literal_column("geometry").cast(Geometry))
        ),
        nullable=True,
    )

    @declared_attr
    def _geojson(self):
        return column_property(
            select(
                (
                    text(
                        """
        CASE WHEN :include_geometries THEN
        ST_ASGEOJSON(
            ST_SIMPLIFY(
                geometry::GEOMETRY,
                :geometry_resolution_meters / 111320.0
            )
        )::JSON
        END
        """
                    ).bindparams(geometry_resolution_meters=1, include_geometries=True),
                )
            )
        )

    @property
    def geojson(self):
        return self._geojson or {"geometry": {"type": "Polygon", "coordinates": []}}


class UserRole(AutoEnum):
    admin = auto()
    editor = auto()
    visitor = auto()


class User(PsqlBase):
    user_id = uuid_field(primary_key=True)
    user_email = Column(
        String,
        unique=True,
        nullable=False,
    )
    password = Column(String, nullable=False)
    first_name = name_field()
    last_name = name_field()
    language = _language_column()
    date_joined = Column(DateTime(True), nullable=False, server_default=func.now())
    is_superuser = Column(Boolean, server_default="FALSE", nullable=False)
    role = enum_field(UserRole, server_default=UserRole.visitor, nullable=False)
    extras = Column(JSON, nullable=True)

    # relations
    series: List["Series"]
    introductions: List["Introduction"]

    def own_series(self, series_id: int) -> bool:
        if not series_id:
            return self.is_superuser
        return series_id in {series.series_id for series in self.series}

    def own_introduction(self, introduction_id: int) -> bool:
        if not introduction_id:
            return self.is_superuser
        return introduction_id in {
            introduction.introduction_id
            for introduction in {series.introductions for series in self.series}
        }


class Landmark(GeoJsonBase, PsqlBase):
    landmark_id = seq("landmark_id")
    landmark_name = Column(JSON, nullable=False)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    cover_image = Column(String, nullable=True)
    description = Column(JSON, nullable=True)
    extra = Column(JSON, nullable=True)
    descriptors = Column(
        "descriptors",
        ARRAY(Float),
        default=[],
        nullable=True,
    )


class Artwork(GeoJsonBase, PsqlBase):
    artwork_id = seq("artwork_id")
    artwork_name = Column(JSON, nullable=False)
    landmark_id = fk(Landmark.landmark_id)
    landmark = rel(Landmark)
    cover_image = Column(String, nullable=True)
    description = Column(JSON, nullable=True)
    extra = Column(JSON, nullable=True)
    descriptors = Column(
        "descriptors",
        ARRAY(Float),
        default=[],
        nullable=True,
    )


class Series(PsqlBase):
    series_id = seq("series_id")
    series_name = name_field()
    landmark_id = fk(Landmark.landmark_id)
    landmark = rel(Landmark)
    author_id = fk(User.user_id, nullable=False)
    author = rel(User, back_populates="series")
    language = _language_column()
    cover_image = Column(String, nullable=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=True)

    # relations
    introductions: List["Introduction"]


class Introduction(PsqlBase):
    introduction_id = seq("introduction_id")
    introduction_name = name_field()
    series_id = fk(Series.series_id)
    series = rel(Series, back_populates="introductions")
    artwork_id = fk(Artwork.artwork_id)
    artwork = rel(Artwork)
    language = _language_column()
    introduction = Column(JSON, nullable=True)


User.series = rel(Series, back_populates="author")

Series.introductions = rel(Introduction, back_populates="series")
