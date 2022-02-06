from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import Server
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette_context.middleware import RawContextMiddleware

from middleware.authentication import VisionAuthBackend, authentication_on_error
from middleware.authorization import CasbinMiddleware
from utils import flags
from utils.utils import (
    enforcer,
    get_postgres_sessionmaker,
)

VF = flags.VisionFlags.get()


servers = (
    Server(
        url="/"
        if VF.debug
        else "https://127.0.0.1"
        if "vision-production" in VF.namespace
        else "https://vision.ottozhang.com",
        description="Vision API",
    ),
)

app = FastAPI(
    title="Vision",
    version=(Path(__file__).parent / "VERSION.txt").read_text(),
    description="""
    Louvre / Vision API

    This API documentation is fully compatible with OpenAPI specification.

    For more information, please visit https://ottozhang.com
    """,
    openapi_tags=[
        {
            "name": "Root",
            "description": "Top-level operations",
            "externalDocs": {
                "description": "External Docs",
                "url": "https://vision.ottozhang.com",
            },
        },
        {
            "name": "Artworks",
            "description": "Artwork-related resources",
            "externalDocs": {
                "description": "External Docs",
                "url": "https://vision.ottozhang.com",
            },
        },
        {
            "name": "Images",
            "description": "Image-related resources",
            "externalDocs": {
                "description": "External Docs",
                "url": "https://vision.ottozhang.com",
            },
        },
        {
            "name": "Introductions",
            "description": "Introduction-related resources",
            "externalDocs": {
                "description": "External Docs",
                "url": "https://vision.ottozhang.com",
            },
        },
        {
            "name": "Landmarks",
            "description": "Landmark-related resources",
            "externalDocs": {
                "description": "External Docs",
                "url": "https://vision.ottozhang.com",
            },
        },
        {
            "name": "Series",
            "description": "Series-related resources",
            "externalDocs": {
                "description": "External Docs",
                "url": "https://vision.ottozhang.com",
            },
        },
    ]
)

# Delayed import to avoid circularity
import routes  # noqa


def origin(server: Server) -> str:
    parsed_uri = urlparse(server.url)
    return "{uri.scheme}://{uri.netloc}".format(uri=parsed_uri)


_global_app = None


def get_app(*_, url=None, **__):
    global _global_app
    if _global_app:
        return _global_app
    _global_app = app
    _global_app.postgres_sessionmaker = get_postgres_sessionmaker(init_url=url)
    _global_app.add_middleware(CasbinMiddleware, enforcer=enforcer)
    _global_app.add_middleware(
        AuthenticationMiddleware,
        backend=VisionAuthBackend(),
        on_error=authentication_on_error,
    )
    _global_app.add_middleware(RawContextMiddleware)
    _global_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_origin_regex=VF.allow_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _global_app
