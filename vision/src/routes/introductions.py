from typing import Dict

from fastapi import Depends

from src.routes import app, d, delete_response, m, schema_show_all, sm, TAG
from utils.utils import VisionDb


@app.get(
    "/series/{series_id}/introductions",
    response_model=m.IntroductionCollection,
    tags=[TAG.Introductions],
    include_in_schema=schema_show_all,
)
def get_series_series_id_introductions(
    series_id: int,
    pagination: m.Pagination = Depends(d.get_pagination),
    db: VisionDb = Depends(d.get_psql),
):
    return m.IntroductionCollection.paginate(
        pagination,
        m.Introduction.db(db)
        .query.filter_by(series_id=series_id)
        .order_by(sm.Introduction.series_id),
    )


@app.get(
    "/introductions/{introduction_id}",
    response_model=m.Introduction,
    tags=[TAG.Introductions],
    include_in_schema=schema_show_all,
)
def get_introductions_introduction_id(
    introduction_id: int,
    db: VisionDb = Depends(d.get_psql),
):
    return m.Introduction.db(db).from_id(introduction_id)


@app.post(
    "/series/{series_id}/introductions",
    response_model=m.Introduction,
    tags=[TAG.Introductions],
    include_in_schema=schema_show_all,
)
def post_series_series_id_introduction(
    series_id: int,
    introduction: m.IntroductionCreate,
    db: VisionDb = Depends(d.get_psql),
    user: sm.User = Depends(d.get_logged_in_user),
):
    db_introduction = sm.Introduction(
        introduction_name=introduction.introduction_name,
        series_id=series_id,
        language=introduction.language,
        artwork_id=introduction.artwork_id,
        introduction=introduction.introduction,
    )
    db.session.add(db_introduction)
    db.session.commit()
    return m.Introduction.db(db).from_id(db_introduction.introduction_id)


@app.patch(
    "/introductions/{introduction_id}",
    response_model=m.Introduction,
    tags=[TAG.Introductions],
    include_in_schema=schema_show_all,
)
def patch_introduction_introduction_id(
    introduction: m.IntroductionPatch,
    introduction_id: int,
    db: VisionDb = Depends(d.get_psql),
    user: sm.User = Depends(d.get_logged_in_user),
):
    db_introduction = m.Introduction.db(db).get_or_404(introduction_id)
    if introduction.introduction_name:
        db_introduction.introduction_name = introduction.introduction_name
    if introduction.introduction:
        db_introduction.introduction = introduction.introduction
    db.session.commit()
    db.session.refresh(db_introduction)
    return m.Introduction.db(db).from_id(introduction_id)


@app.delete(
    "/introductions/{introduction_id}",
    response_model=Dict,
    tags=[TAG.Introductions],
    include_in_schema=schema_show_all,
)
def delete_series_series_id(
    introduction_id: int,
    db: VisionDb = Depends(d.get_psql),
    user: sm.User = Depends(d.get_logged_in_user),
):
    db.session.delete(m.Series.db(db).get_or_404(introduction_id))
    db.session.commit()
    return delete_response
