from tests import ApiClient, m, status


def test_get_landmarks_landmark_id(cl: ApiClient, landmark_1):
    assert m.Landmark.from_db(landmark_1) == m.Landmark.from_response(
        cl(f"/landmarks/{landmark_1.landmark_id}")
    )


def test_get_landmarks(cl: ApiClient, landmark_1):
    assert m.LandmarkCollection.from_response(cl("/landmarks")).contents == [
        m.Landmark.from_db(landmark_1)
    ]


def test_post_landmarks(cl: ApiClient, mocker):
    mocker.patch("utils.algo.get_image_descriptor")
    landmark = m.Landmark.from_response(
        cl(
            "/landmarks",
            method="POST",
            data=m.LandmarkCreate(
                landmark_name={"en": "Louvre"},
                country=m.Country.France,
                city="Paris",
                cover_image="louvre.jpg",
                description={"en": "This is Louvre"},
                extra={},
                geometry=m.GeometryElement(
                    coordinates=[1, 1], type=m.GeometryType.Point
                ),
            ),
        )
    )
    assert landmark == m.Landmark(
        cover_image="louvre.jpg",
        description={"en": "This is Louvre"},
        extra={},
        geometry=m.GeometryElement(coordinates=[1, 1], type=m.GeometryType.Point),
        landmark_name={"en": "Louvre"},
        country=m.Country.France,
        city="Paris",
        self_link=f"/landmarks/{landmark.landmark_id}",
        kind=m.Kind.landmark,
        artworks=f"/landmarks/{landmark.landmark_id}/artworks",
        landmark_id=landmark.landmark_id,
    )


def test_put_landmarks_landmark_id(cl: ApiClient, mocker, landmark_1):
    mocker.patch("utils.algo.get_image_descriptor")
    landmark = m.Landmark.from_response(
        cl(
            f"/landmarks/{landmark_1.landmark_id}",
            method="PATCH",
            data=m.LandmarkPatch(
                landmark_name={"fr": "Louvre fr"},
                cover_image="louvre_edit.jpg",
                description={"en": "This is Louvre edit"},
                geometry=m.GeometryElement(
                    coordinates=[2, 2], type=m.GeometryType.Point
                ),
            ),
        )
    )
    assert landmark == m.Landmark(
        cover_image="louvre_edit.jpg",
        description={"en": "This is Louvre edit"},
        extra={},
        geometry=m.GeometryElement(coordinates=[2, 2], type=m.GeometryType.Point),
        landmark_name={"en": "Louvre", "fr": "Louvre fr"},
        country=m.Country.France,
        city="Paris",
        self_link=f"/landmarks/{landmark.landmark_id}",
        kind=m.Kind.landmark,
        artworks=f"/landmarks/{landmark.landmark_id}/artworks",
        landmark_id=landmark.landmark_id,
    )


def test_delete_landmark_landmark_id(cl: ApiClient, landmark_1):
    cl(
        f"/landmarks/{landmark_1.landmark_id}",
        method="DELETE",
        status=status.HTTP_204_NO_CONTENT,
    )
