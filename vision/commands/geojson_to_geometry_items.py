import typer
import geojson
from shapely.geometry import shape

import sql_models as sm
from utils.utils import postgres_session

FILE_PATH = "/Users/otto/PycharmProjects/Louvre/data/wifi.geojson"
NAME_FIELD = "nom_site"
GEOMETRY_TYPE = "wifi"


def add_geometry_item(feature):
    property = feature.properties
    with postgres_session() as db:
        geometry_item = sm.Geometry(
            geometry_name={"fr": property.get(NAME_FIELD)}
            if property.get(NAME_FIELD)
            else None,
            geometry_type=GEOMETRY_TYPE,
            description={},
            extra=property,
            display=True,
            geometry=shape(feature.geometry).wkt,
        )
        db.session.add(geometry_item)
        db.session.commit()


def main():
    with open(FILE_PATH) as f:
        feature_collection = geojson.loads(f.read())
    for feature in feature_collection.features:
        print(feature.properties.get(NAME_FIELD))
        add_geometry_item(feature)


if __name__ == "__main__":
    typer.run(main)
