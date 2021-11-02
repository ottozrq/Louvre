# from datetime import datetime

# import models as m
import sql_models as sm

from .sqlalchemy_fixture_factory.sqla_fix_fact import (
    BaseFix,
    subFactoryGet,
    # subFactoryModel,
)


class Landmark(BaseFix):
    MODEL = sm.Landmark
    landmark_name = "Louvre"
    country = "France"
    city = "Paris"
    cover_image = "louvre.jpg"
    geometry = "POINT(1 1)"
    description = "This is Louvre"
    extra = {}
    descriptors = []


class Artwork(BaseFix):
    MODEL = sm.Artwork
    artwork_name = "Art"
    landmark = subFactoryGet(Landmark)
    cover_image = "art.jpg"
    geometry = "POINT(1 1)"
    description = "This is Art"
    extra = {}
    descriptors = []
