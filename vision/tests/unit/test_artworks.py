from tests import ApiClient, m, status


def test_get_artworks_artwork_id(cl: ApiClient, artwork_1):
    assert m.Artwork.from_db(artwork_1) == m.Artwork.from_response(
        cl(f"/artworks/{artwork_1.artwork_id}")
    )


def test_get_artworks(cl: ApiClient, landmark_1, artwork_1):
    assert m.ArtworkCollection.from_response(
        cl(f"/landmarks/{landmark_1.landmark_id}/artworks")
    ).contents == [
        m.Artwork.from_db(artwork_1)
    ]


def test_post_artworks(cl: ApiClient, mocker, landmark_1):
    mocker.patch("utils.algo.get_image_descriptor")
    artwork = m.Artwork.from_response(
        cl(
            f"/landmarks/{landmark_1.landmark_id}/artworks",
            method="POST",
            data=m.ArtworkCreate(
                artwork_name={"en": "Art"},
                cover_image="art.jpg",
                description={"en": "This is Art"},
                extra={},
                geometry=m.GeometryElement(
                    coordinates=[1, 1], type=m.GeometryType.Point
                ),
            ),
        )
    )
    assert artwork == m.Artwork(
        cover_image="art.jpg",
        description={"en": "This is Art"},
        landmark=f"/landmarks/{landmark_1.landmark_id}",
        extra={},
        geometry=m.GeometryElement(coordinates=[1, 1], type=m.GeometryType.Point),
        artwork_name={"en": "Art"},
        self_link=f"/artworks/{artwork.artwork_id}",
        kind=m.Kind.artwork,
        artwork_id=artwork.artwork_id,
    )


def test_patch_artworks_artwork_id(cl: ApiClient, mocker, landmark_1, artwork_1):
    mocker.patch("utils.algo.get_image_descriptor")
    artwork = m.Artwork.from_response(
        cl(
            f"/artworks/{artwork_1.artwork_id}",
            method="PATCH",
            data=m.ArtworkPatch(
                artwork_name={"fr": "Art fr"},
                cover_image="art_edit.jpg",
                description={"fr": "This is Art fr"},
                extra={"edit": "sth"},
                geometry=m.GeometryElement(
                    coordinates=[2, 2], type=m.GeometryType.Point
                ),
            ),
        )
    )
    assert artwork == m.Artwork(
        cover_image="art_edit.jpg",
        description={"en": "This is Art", "fr": "This is Art fr"},
        landmark=f"/landmarks/{landmark_1.landmark_id}",
        extra={"edit": "sth"},
        artwork_rate=1,
        geometry=m.GeometryElement(coordinates=[2, 2], type=m.GeometryType.Point),
        artwork_name={"en": "Art", "fr": "Art fr"},
        self_link=f"/artworks/{artwork.artwork_id}",
        kind=m.Kind.artwork,
        artwork_id=artwork.artwork_id,
    )


def test_delete_artwork_artwork_id(cl: ApiClient, artwork_1):
    cl(
        f"/artworks/{artwork_1.artwork_id}",
        method="DELETE",
        status=status.HTTP_204_NO_CONTENT,
    )
