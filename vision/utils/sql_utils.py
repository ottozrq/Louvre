import json
import numbers

import geojson
from shapely.geometry import shape

from src.routes import HTTPException, logger, m, status


def db_geo_feature(geo_feature: m.Geometry):
    try:
        geometry = json.dumps(
            {
                "type": "Feature",
                "geometry": json.loads(geo_feature.json()),
                "properties": {},
            }
        )
        parsed = geojson.loads(geometry)
        if errors := parsed.errors():
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Invalid geometry: {errors}. Geometry: {parsed}",
            )

        def _walk(current_item):
            if not isinstance(current_item, list):
                _walk(
                    next(
                        getattr(current_item, k)
                        for k in {
                            "coordinates",
                            "features",
                            "geometries",
                            "geometry",
                        }
                        if hasattr(current_item, k)
                    )
                )
                return
            if not current_item:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    f"Invalid geometry: Empty list. Geometry: {parsed}",
                )
            if not isinstance(current_item[0], numbers.Number):
                for xx in current_item:
                    _walk(xx)
                return
            if len(current_item) != 2:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    f"Invalid geometry: Encountered coordinates with length != 2 ({current_item}) Geometry: {parsed}",  # noqa
                )
            if not -180 <= current_item[0] <= 180:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    f"Invalid geometry: Longitude not between -180 and 180 ({current_item}). Geometry: {parsed}",  # noqa
                )
            if not -90 <= current_item[1] <= 90:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    f"Invalid geometry: Latitude not between -90 and 90 ({current_item}). Geometry: {parsed}",  # noqa
                )

        _walk(parsed)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Failed to parse geometry", exc_info=e)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Invalid geometry: {parsed}")

    return shape(geo_feature.dict()).wkt
