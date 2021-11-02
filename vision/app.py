from pathlib import Path

from fastapi import FastAPI

from utils.utils import (
    get_postgres_sessionmaker,
)

app = FastAPI(
    title="Hawkeye",
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
            "name": "Landmarks",
            "description": "Landmark-related resources",
            "externalDocs": {
                "description": "External Docs",
                "url": "https://vision.ottozhang.com",
            },
        },
    ]
)

# Delayed import to avoid circularity
import routes  # noqa

_global_app = None


def get_app(*_, url=None, **__):
    global _global_app
    if _global_app:
        return _global_app
    _global_app = app
    _global_app.postgres_sessionmaker = get_postgres_sessionmaker(init_url=url)

    return _global_app
