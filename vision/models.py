import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generic, List, Literal, TypeVar, Union

import fastapi
import pycountry
import pydantic
import pydantic.generics
import sqlalchemy
from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic.types import (
    NonNegativeInt,
    PositiveInt,
)
from sqlalchemy.orm import session

import sql_models as sm
from pagination import paginate
from utils.auto_enum import AutoEnum, auto
from utils.utils import VisionDb
from utils.visionmodels import AutoLink, Model, Link


class OpenAPITag(AutoEnum):
    Activity = auto()
    Artworks = auto()
    Images = auto()
    Introductions = auto()
    Landmarks = auto()
    Root = auto()
    Series = auto()
    Users = auto()


class Kind(AutoEnum):
    activity = auto()
    artwork = auto()
    collection = auto()
    introduction = auto()
    landmark = auto()
    series = auto()
    user = auto()

    @property
    def plural(self) -> str:
        if self.value == "activity":
            return "activities"
        return f"{self.value}s"


@dataclass
class EntityQuery:
    db: VisionDb
    entity: "Entity"

    @property
    def query(self):
        return self.entity.query(self.session)

    @property
    def session(self):
        return self.db.session

    def get_or_404(self, primary_key):
        return self.entity.get_or_404(self.session, primary_key)

    def from_id(self, id_value):
        return self.entity.from_db(self.get_or_404(id_value))


class PrimaryKey(int):
    pass


class Entity(Model):
    self_link: Link
    kind: Kind

    @classmethod
    def db(cls, db):
        return EntityQuery(db, cls)

    @classmethod
    def query(cls, session: session.Session):
        return session.query(cls.Config.db_model)

    @classmethod
    def _get(cls, session: session.Session, primary_key):
        return cls.query(session).get(cls._to_id(primary_key))

    @classmethod
    def get_or_404(cls, session, primary_key):
        record = cls._get(session, primary_key)
        if not record:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Record not found")
        return record

    @classmethod
    def from_db_list(cls, xs: List[sm.PsqlBase], **forward_args):
        return [cls.from_db(x, **forward_args) for x in xs]

    @classmethod
    def _to_id(cls, x):
        if isinstance(x, uuid.UUID):
            return str(x)
        return x

    @classmethod
    def link(cls, item, field=None):
        if item is None:
            return None
        if isinstance(item, Path):
            return item
        instance_id = (
            item
            if type(item) in {str, int, float, uuid.UUID}
            else getattr(item, field)
            if field is not None
            else cls._extract_id(item)
        )
        value = cls.Config.kind.value
        return Path(f"/{value}{'' if value == 'series' else 's'}") / str(instance_id)

    @classmethod
    def _extract_id(cls, item):
        return next(
            getattr(item, field) for field in cls._id_fields() if hasattr(item, field)
        )

    @classmethod
    def _id_fields(cls):
        return (f"{cls.Config.kind}_id",)

    @classmethod
    def links(
        cls,
        instance: Union[fastapi.Request, sm.PsqlBase],
        *args,
        self_link: str = None,
    ):
        kind = cls.Config.kind
        if not self_link and instance:
            if isinstance(instance, fastapi.Request):
                self_link = instance.url.path.rstrip("/")
            else:
                instance_id = cls._extract_id(instance)
                value = kind.value
                if value != 'series':
                    value = kind.plural
                self_link = f"/{value}/{instance_id}"
        return dict(
            self_link=self_link,
            kind=kind,
            **{
                arg: f"{self_link}/{arg}"
                for arg in {
                    x
                    for y in [
                        args,
                        {k for k, v in cls.__fields__.items() if v.type_ is AutoLink},
                    ]
                    for x in y
                }
            },
        )


@dataclass
class Pagination:
    request: fastapi.Request
    page_size: PositiveInt
    page_token: str


EntityT = TypeVar("EntityT", Entity, Entity)


class EntityCollection(pydantic.generics.GenericModel, Entity, Generic[EntityT]):
    page_token: str
    next_page_token: str
    page_size: PositiveInt
    total_size: NonNegativeInt
    total_pages: NonNegativeInt
    contents: List[EntityT]

    class Config:
        kind = Kind.collection

    @classmethod
    def from_list(cls, values: List[sm.PsqlBase], request_: fastapi.Request):
        class FakePagination:
            request = request_

        return cls.paginate(FakePagination, values)

    @classmethod
    def collection_model(cls) -> Model:
        return cls.__fields__["contents"].type_

    @classmethod
    def paginate(
        cls,
        pagination: Pagination,
        query: Union[List[sm.PsqlBase], sqlalchemy.orm.Query],
        **from_db_list_kwargs,
    ):
        if isinstance(query, list):
            return cls(
                contents=cls.collection_model().from_db_list(
                    query, **from_db_list_kwargs
                ),
                page_token=str(1),
                next_page_token="",
                page_size=max(1, len(query)),
                total_size=len(query),
                total_pages=1,
                **cls.links(pagination.request),
            )
        p = paginate(
            query,
            max_per_page=pagination.page_size,
            per_page=pagination.page_size,
            page=(pagination.page_token and int(pagination.page_token)) or 1,
        )
        return cls(
            contents=cls.collection_model().from_db_list(
                p.items, **from_db_list_kwargs
            ),
            page_token=str(p.page),
            next_page_token=str(p.next_num),
            page_size=max(1, p.per_page),
            total_size=p.total,
            total_pages=p.pages,
            **cls.links(pagination.request),
        )


class GeometryType(AutoEnum):
    Point = auto()
    LineString = auto()
    Polygon = auto()
    MultiPolygon = auto()
    GeometryCollection = auto()


class GeometryElement(Model):
    coordinates: List
    type: GeometryType


class GeometryCollection(Model):
    type: GeometryType
    geometries: List[GeometryElement]


Geometry = Union[GeometryElement, GeometryCollection]


class GeoJSONFeature(Model):
    type: Literal["Feature"] = "Feature"
    properties: Dict[str, Any]
    geometry: Geometry


class Root(Model):
    users: Link
    landmarks: Link
    artworks: Link
    series: Link
    introductions: Link


Country = AutoEnum("Country", [country.name for country in pycountry.countries])


class UserPatch(Model):
    first_name: str = None
    last_name: str = None
    language: sm.Language = None
    role: sm.UserRole = None
    extras: Dict[str, Any] = {}


class UserBase(UserPatch):
    user_email: str
    first_name: str = ""
    last_name: str = ""
    language: sm.Language = sm.Language.en
    role: sm.UserRole = sm.UserRole.visitor
    extras: Dict[str, Any] = {}


class UserCreate(UserBase):
    password: str


class User(Entity, UserBase):
    user_id: uuid.UUID
    date_joined: datetime = None

    class Config:
        db_model = sm.User
        kind = Kind.user

    @classmethod
    def from_db(cls, user: sm.User):
        return cls(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            user_email=user.user_email,
            language=user.language,
            date_joined=user.date_joined,
            extra=user.extras,
            role=user.role,
            **cls.links(user),
        )


class LoginResponse(Model):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


class ItemOrder(AutoEnum):
    rate = auto()
    rate_backwards = auto()


class ItemPatchBase(Model):
    cover_image: str = None
    description: Dict[str, Any] = None
    extra: Dict[str, Any] = None
    geometry: Geometry = None


class LandmarkPatch(ItemPatchBase):
    landmark_name: Dict[str, Any] = None


class LandmarkCreate(LandmarkPatch):
    landmark_name: Dict[str, Any]
    country: Country
    city: str


class Landmark(Entity, LandmarkCreate):
    landmark_id: PrimaryKey

    class Config:
        db_model = sm.Landmark
        kind = Kind.landmark

    @classmethod
    def from_db(cls, landmark: sm.Landmark):
        return cls(
            landmark_id=landmark.landmark_id,
            landmark_name=landmark.landmark_name,
            country=landmark.country,
            city=landmark.city,
            cover_image=landmark.cover_image,
            description=landmark.description,
            extra=landmark.extra,
            geometry=landmark.geojson,
            **cls.links(landmark),
        )


class LandmarkCollection(EntityCollection[Landmark]):
    pass


class ArtworkPatch(ItemPatchBase):
    artwork_name: Dict[str, Any] = None
    artwork_rate: int = None


class ArtworkCreate(ArtworkPatch):
    artwork_name: Dict[str, Any]


class Artwork(Entity, ArtworkCreate):
    artwork_id: PrimaryKey
    landmark: Link

    class Config:
        db_model = sm.Artwork
        kind = Kind.artwork

    @classmethod
    def from_db(cls, artwork: sm.Artwork):
        return cls(
            artwork_id=artwork.artwork_id,
            landmark=Landmark.link(artwork.landmark),
            artwork_name=artwork.artwork_name,
            artwork_rate=artwork.artwork_rate,
            cover_image=artwork.cover_image,
            description=artwork.description,
            extra=artwork.extra,
            geometry=artwork.geojson,
            **cls.links(artwork),
        )


class ArtworkCollection(EntityCollection[Artwork]):
    pass


class SeriesPatch(Model):
    language: sm.Language = sm.Language.en
    series_name: str = None
    cover_image: str = None
    description: str = None
    price: float = None


class SeriesCreate(SeriesPatch):
    series_name: str
    cover_image: str
    description: str
    price: float = 0


class Series(Entity, SeriesCreate):
    series_id: PrimaryKey
    landmark: Link
    author: Link

    class Config:
        db_model = sm.Series
        kind = Kind.series

    @classmethod
    def from_db(cls, series: sm.Series):
        return cls(
            series_id=series.series_id,
            series_name=series.series_name,
            landmark=Landmark.link(series.landmark),
            author=User.link(series.author_id),
            language=series.language,
            cover_image=series.cover_image,
            description=series.description,
            price=series.price,
            **cls.links(series),
        )


class SeriesCollection(EntityCollection[Series]):
    pass


class IntroductionPatch(Model):
    introduction_name: str = None
    introduction: Dict[str, Any] = None
    language: sm.Language = sm.Language.en


class IntroductionCreate(IntroductionPatch):
    artwork_id: int


class Introduction(Entity, IntroductionCreate):
    introduction_id: PrimaryKey
    series: Link
    artwork: Link

    class Config:
        db_model = sm.Introduction
        kind = Kind.introduction

    @classmethod
    def from_db(cls, introduction: sm.Introduction):
        return cls(
            introduction_id=introduction.introduction_id,
            series=Series.link(introduction.series),
            artwork=Artwork.link(introduction.artwork),
            artwork_id=introduction.artwork.artwork_id,
            language=introduction.language,
            introduction_name=introduction.introduction_name,
            introduction=introduction.introduction,
            **cls.links(introduction),
        )


class IntroductionCollection(EntityCollection[Introduction]):
    pass


class ActivityPatch(ItemPatchBase):
    activity_name: Dict[str, Any] = None


class ActivityCreate(ActivityPatch):
    activity_name: Dict[str, Any]
    activity_unique_id: str = None


class Activity(Entity, ActivityCreate):
    activity_id: PrimaryKey

    class Config:
        db_model = sm.Activity
        kind = Kind.activity

    @classmethod
    def from_db(cls, activity: sm.Activity):
        return cls(
            activity_id=activity.activity_id,
            activity_name=activity.activity_name,
            cover_image=activity.cover_image,
            description=activity.description,
            extra=activity.extra,
            geometry=activity.geojson,
            **cls.links(activity),
        )


class ActivityCollection(EntityCollection[Activity]):
    pass


class ActivityKeywords(Model):
    keywords: List[str]
