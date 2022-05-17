from tests import ApiClient, m, status


def test_get_activities_activity_id(cl: ApiClient, activity_1):
    assert m.Activity.from_db(activity_1) == m.Activity.from_response(
        cl(f"/activities/{activity_1.activity_id}")
    )


def test_get_activities(cl: ApiClient, activity_1):
    assert m.ActivityCollection.from_response(cl("/activities")).contents == [
        m.ActivityBrief.from_db(activity_1)
    ]


def test_post_activities(cl: ApiClient, mocker):
    # mocker.patch("utils.algo.get_image_descriptor")
    activity = m.Activity.from_response(
        cl(
            "/activities/",
            method="POST",
            data=m.ActivityCreate(
                activity_name={"en": "activity"},
                cover_image="activity.jpg",
                description={"en": "This is an activity"},
                extra={},
                geometry=m.GeometryElement(
                    coordinates=[1, 1], type=m.GeometryType.Point
                ),
            ),
        )
    )
    assert activity == m.Activity(
        cover_image="activity.jpg",
        description={"en": "This is an activity"},
        extra={},
        geometry=m.GeometryElement(coordinates=[1, 1], type=m.GeometryType.Point),
        activity_name={"en": "activity"},
        self_link=f"/activities/{activity.activity_id}",
        kind=m.Kind.activity,
        activity_id=activity.activity_id,
    )


def test_put_activities_activity_id(cl: ApiClient, mocker, activity_1):
    # mocker.patch("utils.algo.get_image_descriptor")
    activity = m.Activity.from_response(
        cl(
            f"/activities/{activity_1.activity_id}",
            method="PATCH",
            data=m.ActivityPatch(
                activity_name={"fr": "activity fr"},
                cover_image="activity.jpg",
                description={"en": "This is an activity edit"},
                geometry=m.GeometryElement(
                    coordinates=[2, 2], type=m.GeometryType.Point
                ),
            ),
        )
    )
    assert activity == m.Activity(
        cover_image="activity.jpg",
        description={"en": "This is an activity edit"},
        extra={},
        geometry=m.GeometryElement(coordinates=[2, 2], type=m.GeometryType.Point),
        activity_name={"en": "activity", "fr": "activity fr"},
        self_link=f"/activities/{activity.activity_id}",
        kind=m.Kind.activity,
        activity_id=activity.activity_id,
    )


def test_delete_activities_activity_id(cl: ApiClient, activity_1):
    cl(
        f"/activities/{activity_1.activity_id}",
        method="DELETE",
        status=status.HTTP_204_NO_CONTENT,
    )
