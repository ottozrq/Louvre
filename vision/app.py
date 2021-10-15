from pathlib import Path

from fastapi import FastAPI

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

    return _global_app
