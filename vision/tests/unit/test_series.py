from tests import ApiClient, m, f, status


def test_get_series_series_id(cl: ApiClient):
    series_id = cl.create(f.Series).series_id
    assert (
        series_id == m.Series.from_response(cl(f"/series/{series_id}")).series_id
    )


def test_get_series(cl: ApiClient):
    landmark = cl.create(f.Landmark)
    series_id = cl.create(f.Series, landmark=landmark).series_id
    assert m.SeriesCollection.from_response(
        cl(f"/landmarks/{landmark.landmark_id}/series")
    ).contents == [
        m.Series(
            series_name="Louvre",
            cover_image="louvre.jpg",
            description="This is Louvre introductions",
            landmark=f"/landmarks/{landmark.landmark_id}",
            self_link=f"/series/{series_id}",
            price=1.0,
            kind=m.Kind.series,
            series_id=series_id,
        )
    ]


def test_post_series(cl: ApiClient):
    landmark_id = cl.create(f.Landmark).landmark_id
    series = m.Series.from_response(
        cl(
            f"/landmarks/{landmark_id}/series",
            method="POST",
            data=m.SeriesCreate(
                series_name="Art",
                cover_image="art.jpg",
                description="This is Art",
                price=1.0,
            ),
        )
    )
    assert series == m.Series(
        series_id=series.series_id,
        cover_image="art.jpg",
        description="This is Art",
        landmark=f"/landmarks/{landmark_id}",
        series_name="Art",
        price=1.0,
        self_link=f"/series/{series.series_id}",
        kind=m.Kind.series,
        artwork_id=series.series_id,
    )


def test_patch_series_series_id(cl: ApiClient):
    landmark = cl.create(f.Landmark)
    series_id = cl.create(f.Series, landmark=landmark).series_id
    series = m.Series.from_response(
        cl(
            f"/series/{series_id}",
            method="PATCH",
            data=m.SeriesPatch(
                series_name="Art Edit",
                cover_image="art_edit.jpg",
                description="This is Art Edit",
                price=2.0,
            ),
        )
    )
    assert series == m.Series(
        cover_image="art_edit.jpg",
        description="This is Art Edit",
        landmark=f"/landmarks/{landmark.landmark_id}",
        series_name="Art Edit",
        self_link=f"/series/{series.series_id}",
        kind=m.Kind.series,
        series_id=series.series_id,
        price=2.0
    )


def test_delete_series_series_id(cl: ApiClient):
    series_id = cl.create(f.Series).series_id
    cl(
        f"/series/{series_id}",
        method="DELETE",
        status=status.HTTP_204_NO_CONTENT,
    )
