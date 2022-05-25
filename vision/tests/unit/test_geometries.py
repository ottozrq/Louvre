from tests import ApiClient, m


def test_get_geometries(cl: ApiClient, geometry_1):
    assert m.GeometryItemCollection.from_response(
        cl("/geometries?lat=1&lon=1")
    ).contents == [m.GeometryItem.from_db(geometry_1)]
    assert m.GeometryItemCollection.from_response(
        cl("/geometries?lat=1&lon=1&geometry_type=nothing")
    ).contents == []
