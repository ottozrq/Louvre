from typing import Dict

from fastapi import Depends
from sqlalchemy import nullslast, or_

from src.routes import algo, app, d, delete_response, m, schema_show_all, sm, TAG
from utils.sql_utils import update_json, db_geo_feature
from utils.utils import VisionDb, VisionSearch


def _artwork_order(order: m.ItemOrder):
    return (
        sm.Artwork.artwork_rate.desc()
        if order == m.ItemOrder.rate_backwards
        else nullslast(sm.Artwork.artwork_rate.desc())
    )


@app.get(
    "/landmarks/{landmark_id}/artworks/",
    response_model=m.ArtworkCollection,
    tags=[TAG.Artworks],
    include_in_schema=schema_show_all,
)
def get_artworks(
    landmark_id: int,
    order: m.ItemOrder = m.ItemOrder.rate,
    pagination: m.Pagination = Depends(d.get_pagination),
    db: VisionDb = Depends(d.get_psql),
):
    return m.ArtworkCollection.paginate(
        pagination,
        m.Artwork.db(db)
        .query.filter_by(landmark_id=landmark_id)
        .filter(or_(sm.Artwork.artwork_rate != 0, sm.Artwork.artwork_rate == None))
        .order_by(
            _artwork_order(order),
            sm.Artwork.artwork_id,
        ),
    )


@app.get(
    "/artworks/{artwork_id}/",
    response_model=m.Artwork,
    tags=[TAG.Artworks],
    include_in_schema=schema_show_all,
)
def get_artworks_artwork_id(
    artwork_id: int,
    db: VisionDb = Depends(d.get_psql),
):
    return m.Artwork.db(db).from_id(artwork_id)


@app.post(
    "/landmarks/{landmark_id}/artworks/",
    response_model=m.Artwork,
    tags=[TAG.Artworks],
    include_in_schema=schema_show_all,
)
def post_artworks(
    landmark_id: int,
    artwork: m.ArtworkCreate,
    db: VisionDb = Depends(d.get_psql),
    user: sm.User = Depends(d.get_logged_in_user),
):
    db_artwork = sm.Artwork(
        artwork_name=artwork.artwork_name,
        landmark_id=landmark_id,
        cover_image=artwork.cover_image,
        description=artwork.description,
        extra=artwork.extra,
        geometry=db_geo_feature(artwork.geometry),
        descriptors=algo.get_image_descriptor(artwork.cover_image),
    )
    db.session.add(db_artwork)
    db.session.commit()
    return m.Artwork.db(db).from_id(db_artwork.artwork_id)


@app.patch(
    "/artworks/{artwork_id}/",
    response_model=m.Artwork,
    tags=[TAG.Artworks],
    include_in_schema=schema_show_all,
)
def patch_artworks_artwork_id(
    artwork: m.ArtworkPatch,
    artwork_id: int,
    db: VisionDb = Depends(d.get_psql),
    user: sm.User = Depends(d.get_logged_in_user),
):
    db_artwork = m.Artwork.db(db).get_or_404(artwork_id)
    artwork_model = m.Artwork.db(db).from_id(artwork_id)
    if artwork.artwork_name:
        db_artwork.artwork_name = update_json(
            artwork_model.artwork_name, artwork.artwork_name
        )
    if artwork.cover_image:
        db_artwork.cover_image = artwork.cover_image
        db_artwork.descriptors = algo.get_image_descriptor(artwork.cover_image)
    if artwork.description:
        db_artwork.description = update_json(
            artwork_model.description, artwork.description
        )
    if artwork.extra:
        db_artwork.extra = update_json(artwork_model.extra, artwork.extra)
    if artwork.geometry:
        db_artwork.geometry = db_geo_feature(artwork.geometry)
    if artwork.artwork_rate is not None:
        db_artwork.artwork_rate = artwork.artwork_rate
    db.session.commit()
    db.session.refresh(db_artwork)
    return m.Artwork.db(db).from_id(artwork_id)


@app.delete(
    "/artworks/{artwork_id}/",
    response_model=Dict,
    tags=[TAG.Artworks],
    include_in_schema=schema_show_all,
)
def delete_artworks_artwork_id(
    artwork_id: int,
    db: VisionDb = Depends(d.get_psql),
    user: sm.User = Depends(d.get_logged_in_user),
):
    db.session.delete(m.Artwork.db(db).get_or_404(artwork_id))
    db.session.commit()
    return delete_response


@app.get("/search/artworks/", response_model=m.ArtworkCollection, tags=[TAG.Artworks])
def search_artworks(
    q: str,
    order: m.ItemOrder = m.ItemOrder.rate,
    pagination: m.Pagination = Depends(d.get_pagination),
    db: VisionDb = Depends(d.get_psql),
    search: VisionSearch = Depends(d.get_search),
):
    result = search.es.search(
        index="artwork",
        body={
            "_source": ["id"],
            "query": {"match": {"_all": f"{q}"}},
            "size": 1000,
        },
    )
    ids = [hit["_id"] for hit in result.get("hits", {}).get("hits", [])]
    return m.ArtworkCollection.paginate(
        pagination,
        m.Artwork.db(db)
        .query.filter(sm.Artwork.artwork_id.in_(ids))
        .order_by(_artwork_order(order), sm.Artwork.artwork_id),
    )
