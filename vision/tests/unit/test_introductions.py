from tests import ApiClient, m, status


def test_get_introduction_introduction_id(cl: ApiClient, introduction_1):
    assert m.Introduction.from_db(introduction_1) == m.Introduction.from_response(
        cl(f"/introductions/{introduction_1.introduction_id}")
    )


def test_get_introduction(cl: ApiClient, series_1, introduction_1):
    assert m.IntroductionCollection.from_response(
        cl(f"/series/{series_1.series_id}/introductions")
    ).contents == [m.Introduction.from_db(introduction_1)]


def test_post_introduction(cl: ApiClient, artwork_1, series_1, user_editor):
    cl(
        f"/series/{series_1.series_id}/introductions",
        method="POST",
        data=m.IntroductionCreate(
            introduction_name="Art",
            language="en",
            introduction={"content": "This is Art"},
            artwork_id=artwork_1.artwork_id,
        ),
        status=status.HTTP_403_FORBIDDEN,
    )
    cl.login(user_editor)
    introduction = m.Introduction.from_response(
        cl(
            f"/series/{series_1.series_id}/introductions",
            method="POST",
            data=m.IntroductionCreate(
                introduction_name="Art",
                language="en",
                introduction={"content": "This is Art"},
                artwork_id=artwork_1.artwork_id,
            ),
        )
    )
    assert introduction == m.Introduction(
        introduction_id=introduction.introduction_id,
        introduction={"content": "This is Art"},
        series=f"/series/{series_1.series_id}",
        introduction_name="Art",
        language="en",
        self_link=f"/introductions/{introduction.introduction_id}",
        kind=m.Kind.introduction,
        artwork=f"/artworks/{artwork_1.artwork_id}",
        artwork_id=artwork_1.artwork_id,
    )


def test_patch_introduction_introduction_id(
    cl: ApiClient, artwork_1, series_1, introduction_1, user_editor
):
    cl.login(user_editor)
    introduction = m.Introduction.from_response(
        cl(
            f"/introductions/{introduction_1.introduction_id}",
            method="PATCH",
            data=m.IntroductionPatch(
                introduction_name="Art Edit",
                introduction={"content": "This is Art Edit"},
            ),
        )
    )
    assert introduction == m.Introduction(
        introduction={"content": "This is Art Edit"},
        artwork=f"/artworks/{artwork_1.artwork_id}",
        artwork_id=artwork_1.artwork_id,
        series=f"/series/{series_1.series_id}",
        introduction_name="Art Edit",
        language="en",
        self_link=f"/introductions/{introduction.introduction_id}",
        kind=m.Kind.introduction,
        introduction_id=introduction.introduction_id,
    )


def test_delete_introduction_introduction_id(
    cl: ApiClient, introduction_1, user_editor
):
    cl.login(user_editor)
    cl(
        f"/introductions/{introduction_1.introduction_id}",
        method="DELETE",
        status=status.HTTP_204_NO_CONTENT,
    )
