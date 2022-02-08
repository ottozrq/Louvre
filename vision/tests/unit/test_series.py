from tests import ApiClient, m, status


def test_get_series_series_id(cl: ApiClient, series_1):
    # series_id = cl.create(f.Series).series_id
    assert m.Series.from_db(series_1) == m.Series.from_response(
        cl(f"/series/{series_1.series_id}")
    )


def test_get_series(cl: ApiClient, landmark_1, series_1, user_editor):
    assert m.SeriesCollection.from_response(
        cl(f"/landmarks/{landmark_1.landmark_id}/series")
    ).contents == [m.Series.from_db(series_1)]


def test_post_series(cl: ApiClient, landmark_1, user_admin):
    series = m.Series.from_response(
        cl(
            f"/landmarks/{landmark_1.landmark_id}/series",
            method="POST",
            data=m.SeriesCreate(
                series_name="Art",
                lang="en",
                cover_image="art.jpg",
                description="This is Art",
                price=1.0,
            ),
        )
    )
    assert series == m.Series(
        series_id=series.series_id,
        cover_image="art.jpg",
        lang="en",
        description="This is Art",
        landmark=f"/landmarks/{landmark_1.landmark_id}",
        author=f"/users/{user_admin.user_id}",
        series_name="Art",
        price=1.0,
        self_link=f"/series/{series.series_id}",
        kind=m.Kind.series,
        artwork_id=series.series_id,
    )


def test_patch_series_series_id(cl: ApiClient, landmark_1, series_1, user_editor):
    cl(
        f"/series/{series_1.series_id}",
        method="PATCH",
        data=m.SeriesPatch(
            series_name="Art Edit",
            cover_image="art_edit.jpg",
            description="This is Art Edit",
            price=2.0,
        ),
        status=status.HTTP_403_FORBIDDEN,
    )
    cl.login(user_editor)
    series = m.Series.from_response(
        cl(
            f"/series/{series_1.series_id}",
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
        landmark=f"/landmarks/{landmark_1.landmark_id}",
        author=f"/users/{user_editor.user_id}",
        series_name="Art Edit",
        lang="en",
        self_link=f"/series/{series.series_id}",
        kind=m.Kind.series,
        series_id=series.series_id,
        price=2.0,
    )


def test_delete_series_series_id(cl: ApiClient, series_1, user_editor):
    cl.login(user_editor)
    cl(
        f"/series/{series_1.series_id}",
        method="DELETE",
        status=status.HTTP_204_NO_CONTENT,
    )
