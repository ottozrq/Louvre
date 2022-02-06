from typing import Dict

from fastapi import Depends

from src.routes import algo, app, d, delete_response, m, schema_show_all, sm, TAG
from utils.sql_utils import db_geo_feature, update_json
from utils.utils import VisionDb


@app.get(
    "/landmarks/",
    response_model=m.LandmarkCollection,
    tags=[TAG.Landmarks],
    include_in_schema=schema_show_all,
)
def get_landmarks(
    pagination: m.Pagination = Depends(d.get_pagination),
    db: VisionDb = Depends(d.get_psql),
):
    return m.LandmarkCollection.paginate(
        pagination, m.Landmark.db(db).query.order_by(sm.Landmark.landmark_id)
    )


@app.get(
    "/landmarks/{landmark_id}/",
    response_model=m.Landmark,
    tags=[TAG.Landmarks],
    include_in_schema=schema_show_all,
)
def get_landmarks_landmark_id(
    landmark_id: int,
    db: VisionDb = Depends(d.get_psql),
):
    return m.Landmark.db(db).from_id(landmark_id)


@app.post(
    "/landmarks/",
    response_model=m.Landmark,
    tags=[TAG.Landmarks],
    include_in_schema=schema_show_all,
)
def post_landmarks(
    landmark: m.LandmarkCreate,
    db: VisionDb = Depends(d.get_psql),
    user: sm.User = Depends(d.get_logged_in_user),
):
    db_landmark = sm.Landmark(
        landmark_name=landmark.landmark_name,
        country=landmark.country,
        city=landmark.city,
        cover_image=landmark.cover_image,
        description=landmark.description,
        extra=landmark.extra,
        geometry=db_geo_feature(landmark.geometry),
        descriptors=algo.get_image_descriptor(landmark.cover_image),
    )
    db.session.add(db_landmark)
    db.session.commit()
    return m.Landmark.db(db).from_id(db_landmark.landmark_id)


@app.patch(
    "/landmarks/{landmark_id}/",
    response_model=m.Landmark,
    tags=[TAG.Landmarks],
    include_in_schema=schema_show_all,
)
def patch_landmarks_landmark_id(
    landmark: m.LandmarkPatch,
    landmark_id: int,
    db: VisionDb = Depends(d.get_psql),
    user: sm.User = Depends(d.get_logged_in_user),
):
    db_landmark = m.Landmark.db(db).get_or_404(landmark_id)
    landmark_model = m.Landmark.db(db).from_id(landmark_id)
    if landmark.landmark_name:
        db_landmark.landmark_name = update_json(
            landmark_model.landmark_name, landmark.landmark_name
        )
    if landmark.cover_image:
        db_landmark.cover_image = landmark.cover_image
        db_landmark.descriptors = algo.get_image_descriptor(landmark.cover_image)
    if landmark.description:
        db_landmark.description = update_json(
            landmark_model.description, landmark.description
        )
    if landmark.extra:
        db_landmark.extra = update_json(landmark_model.extra, landmark.extra)
    if landmark.geometry:
        db_landmark.geometry = db_geo_feature(landmark.geometry)
    db.session.commit()
    db.session.refresh(db_landmark)
    return m.Landmark.db(db).from_id(landmark_id)


@app.delete(
    "/landmarks/{landmark_id}/",
    response_model=Dict,
    tags=[TAG.Landmarks],
    include_in_schema=schema_show_all,
)
def delete_landmarks_landmark_id(
    landmark_id: int,
    db: VisionDb = Depends(d.get_psql),
    user: sm.User = Depends(d.get_logged_in_user),
):
    db.session.delete(m.Landmark.db(db).get_or_404(landmark_id))
    db.session.commit()
    return delete_response
