from typing import Dict

from fastapi import Depends

from src.routes import app, d, delete_response, m, schema_show_all, sm, TAG
from utils.sql_utils import db_geo_feature, update_json
from utils.utils import VisionDb


@app.get(
    "/activities/",
    response_model=m.ActivityCollection,
    tags=[TAG.Activity],
    include_in_schema=schema_show_all,
)
def get_activities(
    pagination: m.Pagination = Depends(d.get_pagination),
    db: VisionDb = Depends(d.get_psql),
):
    return m.ActivityCollection.paginate(
        pagination, m.Activity.db(db).query.order_by(sm.Activity.activity_id)
    )


@app.get(
    "/activities/{activity_id}/",
    response_model=m.Activity,
    tags=[TAG.Activity],
    include_in_schema=schema_show_all,
)
def get_activities_activity_id(
    activity_id: int,
    db: VisionDb = Depends(d.get_psql),
):
    return m.Activity.db(db).from_id(activity_id)


@app.post(
    "/activities/",
    response_model=m.Activity,
    tags=[TAG.Activity],
    include_in_schema=schema_show_all,
)
def post_activities(
    activity: m.ActivityCreate,
    db: VisionDb = Depends(d.get_psql),
    user: sm.User = Depends(d.get_logged_in_user),
):
    db_activity = sm.Activity(
        activity_name=activity.activity_name,
        activity_unique_id=activity.activity_unique_id,
        cover_image=activity.cover_image,
        description=activity.description,
        extra=activity.extra,
        geometry=db_geo_feature(activity.geometry),
    )
    db.session.add(db_activity)
    db.session.commit()
    return m.Activity.db(db).from_id(db_activity.activity_id)


@app.patch(
    "/activities/{activity_id}/",
    response_model=m.Activity,
    tags=[TAG.Activity],
    include_in_schema=schema_show_all,
)
def patch_activities_activity_id(
    activity: m.ActivityPatch,
    activity_id: int,
    db: VisionDb = Depends(d.get_psql),
    user: sm.User = Depends(d.get_logged_in_user),
):
    db_activity = m.Activity.db(db).get_or_404(activity_id)
    activity_model = m.Activity.db(db).from_id(activity_id)
    if activity.activity_name:
        db_activity.activity_name = update_json(
            activity_model.activity_name, activity.activity_name
        )
    if activity.cover_image:
        db_activity.cover_image = activity.cover_image
    if activity.description:
        db_activity.description = update_json(
            activity_model.description, activity.description
        )
    if activity.extra:
        db_activity.extra = update_json(activity_model.extra, activity.extra)
    if activity.geometry:
        db_activity.geometry = db_geo_feature(activity.geometry)
    db.session.commit()
    db.session.refresh(db_activity)
    return m.Activity.db(db).from_id(activity_id)


@app.delete(
    "/activities/{activity_id}/",
    response_model=Dict,
    tags=[TAG.Activity],
    include_in_schema=schema_show_all,
)
def delete_activities_activity_id(
    activity_id: int,
    db: VisionDb = Depends(d.get_psql),
    user: sm.User = Depends(d.get_logged_in_user),
):
    db.session.delete(m.Activity.db(db).get_or_404(activity_id))
    db.session.commit()
    return delete_response
