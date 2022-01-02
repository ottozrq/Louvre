from typing import Dict

from fastapi import Depends

from src.routes import app, d, delete_response, m, schema_show_all, sm, TAG
from utils.utils import VisionDb


@app.get(
    "/landmarks/{landmark_id}/series",
    response_model=m.SeriesCollection,
    tags=[TAG.Series],
    include_in_schema=schema_show_all,
)
def get_landmarks_landmark_id_series(
    landmark_id: int,
    pagination: m.Pagination = Depends(d.get_pagination),
    db: VisionDb = Depends(d.get_psql),
):
    return m.SeriesCollection.paginate(
        pagination,
        m.Series.db(db)
        .query.filter_by(landmark_id=landmark_id)
        .order_by(sm.Series.series_id),
    )


@app.get(
    "/series/{series_id}",
    response_model=m.Series,
    tags=[TAG.Series],
    include_in_schema=schema_show_all,
)
def get_series_series_id(
    series_id: int,
    db: VisionDb = Depends(d.get_psql),
):
    return m.Series.db(db).from_id(series_id)


@app.post(
    "/landmarks/{landmark_id}/series",
    response_model=m.Series,
    tags=[TAG.Series],
    include_in_schema=schema_show_all,
)
def post_landmarks_landmark_id_series(
    landmark_id: int,
    series: m.SeriesCreate,
    db: VisionDb = Depends(d.get_psql),
):
    db_series = sm.Series(
        series_name=series.series_name,
        cover_image=series.cover_image,
        landmark_id=landmark_id,
        description=series.description,
        price=series.price,
    )
    db.session.add(db_series)
    db.session.commit()
    return m.Series.db(db).from_id(db_series.series_id)


@app.patch(
    "/series/{series_id}",
    response_model=m.Series,
    tags=[TAG.Series],
    include_in_schema=schema_show_all,
)
def patch_series_series_id(
    series: m.SeriesPatch,
    series_id: int,
    db: VisionDb = Depends(d.get_psql),
):
    db_series = m.Series.db(db).get_or_404(series_id)
    if series.series_name:
        db_series.series_name = series.series_name
    if series.cover_image:
        db_series.cover_image = series.cover_image
    if series.description:
        db_series.description = series.description
    if series.price:
        db_series.price = series.price
    db.session.commit()
    db.session.refresh(db_series)
    return m.Series.db(db).from_id(series_id)


@app.delete(
    "/series/{series_id}",
    response_model=Dict,
    tags=[TAG.Series],
    include_in_schema=schema_show_all,
)
def delete_series_series_id(
    series_id: int,
    db: VisionDb = Depends(d.get_psql),
):
    db.session.delete(m.Series.db(db).get_or_404(series_id))
    db.session.commit()
    return delete_response
