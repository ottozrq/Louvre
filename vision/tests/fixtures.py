from datetime import datetime

from passlib.context import CryptContext

# import models as m
import sql_models as sm

from .sqlalchemy_fixture_factory.sqla_fix_fact import (
    BaseFix,
    subFactoryGet,
    # subFactoryModel,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseFix):
    MODEL = sm.User
    user_email = "otto@example.com"
    password = pwd_context.hash("666666")
    first_name = "Otto"
    last_name = "Zhang"
    language = sm.Language.en
    date_joined = datetime(1970, 1, 1)
    extra = {}


class Landmark(BaseFix):
    MODEL = sm.Landmark
    landmark_name = {"en": "Louvre"}
    country = "France"
    city = "Paris"
    cover_image = "louvre.jpg"
    geometry = "POINT(1 1)"
    description = {"en": "This is Louvre"}
    extra = {}
    descriptors = []


class Artwork(BaseFix):
    MODEL = sm.Artwork
    artwork_name = {"en": "Art"}
    landmark = subFactoryGet(Landmark)
    cover_image = "art.jpg"
    geometry = "POINT(1 1)"
    description = {"en": "This is Art"}
    extra = {}
    descriptors = []


class Series(BaseFix):
    MODEL = sm.Series
    series_name = "Louvre"
    landmark = subFactoryGet(Landmark)
    author = subFactoryGet(User)
    language = sm.Language.en
    cover_image = "louvre.jpg"
    description = "This is Louvre introductions"
    price = 1.0


class Introduction(BaseFix):
    MODEL = sm.Introduction
    introduction_name = "Louvre"
    artwork = subFactoryGet(Artwork)
    series = subFactoryGet(Series)
    language = sm.Language.en
    introduction = {"content": "This is Louvre introductions"}
