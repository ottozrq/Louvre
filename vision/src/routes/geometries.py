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
    geometry_type: str = None,
    db: VisionDb = Depends(d.get_psql),
    pagination: m.Pagination = Depends(d.get_pagination),
):
    geometry_items = m.GeometryItem.db(db).query.filter(sm.Geometry.display)
    if geometry_type:
        geometry_items = geometry_items.filter(
            sm.Geometry.geometry_type == geometry_type
        )
    geometry_items = (
        geometry_items.filter(
            func.ST_DWithin(
                func.ST_GeogFromWKB(WKTElement(f"POINT({lon} {lat})", srid=4326)),
                sm.Geometry.geometry,
                range,
            )
        )
    ).order_by(sm.Geometry.geometry_id)
    return m.GeometryItemCollection.paginate(pagination, geometry_items)
