from typing import Union

import pydantic
import pytest
from starlette.routing import BaseRoute

from app import app
from tests import ApiClient, m, status


@pytest.mark.parametrize(
    ("path", "route"), [(route.path, route) for route in app.routes]
)
def test_all_routes(cl: ApiClient, path: str, route: BaseRoute):
    is_built_in = any(path.startswith(p) for p in {"/openapi.json", "/doc", "/redoc"})
    assert is_built_in or path.endswith("/")
    is_public = (
        any(
            path.startswith(p)
            for p in {
                "/openapi.json",
                "/token/",
                "/doc",
                "/redoc",
                "/register/",
                "/landmarks/",
                "/artworks/",
                "/images/",
                "/detect/",
            }
        )
        or path == "/"
    )
    assert (
        is_built_in
        or "DELETE" in route.methods
        or getattr(route.response_model, "__origin__", None) in (Union, set, list)
        or (
            route.response_model
            and isinstance(route.response_model, pydantic.BaseModel)
        )
        or isinstance(route.response_model, pydantic.main.ModelMetaclass)
        or ("GET" in route.methods and path.startswith("/images/"))
    )
    assert is_built_in or len(route.tags) == 1
    assert is_built_in or isinstance(route.tags[0], m.OpenAPITag)
    cl.logout()
    is_public or cl(
        path,
        method=list(route.methods)[0],
        status=status.HTTP_401_UNAUTHORIZED,
    )
