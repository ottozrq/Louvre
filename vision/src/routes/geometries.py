from fastapi import Depends
from geoalchemy2.elements import WKTElement
from sqlalchemy.sql import func

from src.routes import app, d, m, schema_show_all, sm, TAG, VisionDb


@app.get(
    "/geometries/",
    response_model=m.GeometryItemCollection,
    tags=[TAG.Geometry],
    include_in_schema=schema_show_all,
)
def get_geometries(
    lat: float = 48.8566,
    lon: float = 2.3522,
    range: int = 3000,
    db: VisionDb = Depends(d.get_psql),
    pagination: m.Pagination = Depends(d.get_pagination),
):
    return m.GeometryItemCollection.paginate(
        pagination,
        m.GeometryItem.db(db)
        .query.filter(
            sm.Geometry.display
        ).filter(
            func.ST_DWithin(
                func.ST_GeogFromWKB(WKTElement(f"POINT({lon} {lat})", srid=4326)),
                sm.Geometry.geometry,
                range
            )
        ),
    )
