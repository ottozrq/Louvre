from models import Landmark
from tests import ApiClient, m, f, status


def test_get_introduction_introduction_id(cl: ApiClient):
    introduction_id = cl.create(f.Introduction).introduction_id
    assert (
        introduction_id
        == m.Introduction.from_response(
            cl(f"/introductions/{introduction_id}")
        ).introduction_id
    )


def test_get_introduction(cl: ApiClient):
    landmark = cl.create(f.Landmark)
    series = cl.create(f.Series, landmark=landmark)
    artwork = cl.create(f.Artwork, landmark=landmark)
    introduction_id = cl.create(
        f.Introduction, series=series, artwork=artwork
    ).introduction_id
    assert m.IntroductionCollection.from_response(
        cl(f"/series/{series.series_id}/introductions")
    ).contents == [
        m.Introduction(
            introduction_name="Louvre",
            introduction={"content": "This is Louvre introductions"},
            series=f"/series/{series.series_id}",
            artwork=f"/artworks/{artwork.artwork_id}",
            artwork_id=artwork.artwork_id,
            self_link=f"/introductions/{introduction_id}",
            kind=m.Kind.introduction,
            introduction_id=introduction_id,
        )
    ]


def test_post_introduction(cl: ApiClient):
    series_id = cl.create(f.Series).series_id
    artwork_id = cl.create(f.Artwork).artwork_id
    introduction = m.Introduction.from_response(
        cl(
            f"/series/{series_id}/introductions",
            method="POST",
            data=m.IntroductionCreate(
                introduction_name="Art",
                introduction={"content": "This is Art"},
                artwork_id=artwork_id,
            ),
        )
    )
    assert introduction == m.Introduction(
        introduction_id=introduction.introduction_id,
        introduction={"content": "This is Art"},
        series=f"/series/{series_id}",
        introduction_name="Art",
        self_link=f"/introductions/{introduction.introduction_id}",
        kind=m.Kind.introduction,
        artwork=f"/artworks/{artwork_id}",
        artwork_id=artwork_id,
    )


def test_patch_introduction_introduction_id(cl: ApiClient):
    artwork = cl.create(f.Artwork)
    series = cl.create(f.Series)
    introduction_id = cl.create(
        f.Introduction, artwork=artwork, series=series
    ).introduction_id
    introduction = m.Introduction.from_response(
        cl(
            f"/introductions/{introduction_id}",
            method="PATCH",
            data=m.IntroductionPatch(
                introduction_name="Art Edit",
                introduction={"content": "This is Art Edit"},
            ),
        )
    )
    assert introduction == m.Introduction(
        introduction={"content": "This is Art Edit"},
        artwork=f"/artworks/{artwork.artwork_id}",
        artwork_id=artwork.artwork_id,
        series=f"/series/{series.series_id}",
        introduction_name="Art Edit",
        self_link=f"/introductions/{introduction.introduction_id}",
        kind=m.Kind.introduction,
        introduction_id=introduction.introduction_id,
    )


def test_delete_introduction_introduction_id(cl: ApiClient):
    introduction_id = cl.create(f.Introduction).introduction_id
    cl(
        f"/introductions/{introduction_id}",
        method="DELETE",
        status=status.HTTP_204_NO_CONTENT,
    )
