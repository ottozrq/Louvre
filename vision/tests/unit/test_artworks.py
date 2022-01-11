from tests import ApiClient, m, f, status


def test_get_artworks_artwork_id(cl: ApiClient):
    artwork_id = cl.create(f.Artwork).artwork_id
    assert (
        artwork_id == m.Artwork.from_response(cl(f"/artworks/{artwork_id}")).artwork_id
    )


def test_get_artworks(cl: ApiClient):
    landmark = cl.create(f.Landmark)
    artwork_id = cl.create(f.Artwork, landmark=landmark).artwork_id
    assert m.ArtworkCollection.from_response(
        cl(f"/landmarks/{landmark.landmark_id}/artworks")
    ).contents == [
        m.Artwork(
            cover_image="art.jpg",
            description={"en": "This is Art"},
            extra={},
            landmark=f"/landmarks/{landmark.landmark_id}",
            geometry=m.GeometryElement(coordinates=[1, 1], type=m.GeometryType.Point),
            artwork_name={"en": "Art"},
            self_link=f"/artworks/{artwork_id}",
            kind=m.Kind.artwork,
            artwork_id=artwork_id,
        )
    ]


def test_post_artworks(cl: ApiClient, mocker):
    landmark_id = cl.create(f.Landmark).landmark_id
    mocker.patch("utils.algo.get_image_descriptor")
    artwork = m.Artwork.from_response(
        cl(
            f"/landmarks/{landmark_id}/artworks",
            method="POST",
            data=m.ArtworkCreate(
                artwork_name={"en": "Art"},
                cover_image="art.jpg",
                description={"en":  "This is Art"},
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
        landmark=f"/landmarks/{landmark_id}",
        extra={},
        geometry=m.GeometryElement(coordinates=[1, 1], type=m.GeometryType.Point),
        artwork_name={"en": "Art"},
        self_link=f"/artworks/{artwork.artwork_id}",
        kind=m.Kind.artwork,
        artwork_id=artwork.artwork_id,
    )


def test_patch_artworks_artwork_id(cl: ApiClient, mocker):
    landmark = cl.create(f.Landmark)
    artwork_id = cl.create(f.Artwork, landmark=landmark).artwork_id
    mocker.patch("utils.algo.get_image_descriptor")
    artwork = m.Artwork.from_response(
        cl(
            f"/artworks/{artwork_id}",
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
        landmark=f"/landmarks/{landmark.landmark_id}",
        extra={"edit": "sth"},
        geometry=m.GeometryElement(coordinates=[2, 2], type=m.GeometryType.Point),
        artwork_name={"en": "Art", "fr": "Art fr"},
        self_link=f"/artworks/{artwork.artwork_id}",
        kind=m.Kind.artwork,
        artwork_id=artwork.artwork_id,
    )


def test_delete_artwork_artwork_id(cl: ApiClient):
    artwork_id = cl.create(f.Artwork).artwork_id
    cl(
        f"/artworks/{artwork_id}",
        method="DELETE",
        status=status.HTTP_204_NO_CONTENT,
    )
