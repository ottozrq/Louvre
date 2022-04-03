import typer

import sql_models as sm
from utils.utils import VisionSearch, postgres_session


MAPPING = {
    "dynamic_templates": [
        {
            "all_text": {
                "match_mapping_type": "string",
                "mapping": {"copy_to": "_all", "type": "text"},
            }
        }
    ],
    "properties": {
        "_all": {"type": "text"},
        "id": {"type": "integer"},
        "name": {
            "type": "object",
            "properties": {
                "en": {"type": "text", "copy_to": ["_all"]},
                "cn": {"type": "text", "copy_to": ["_all"]},
                "fr": {"type": "text", "copy_to": ["_all"]},
            },
        },
        "description": {
            "type": "object",
            "properties": {
                "en": {"type": "text", "copy_to": ["_all"]},
                "cn": {"type": "text", "copy_to": ["_all"]},
                "fr": {"type": "text", "copy_to": ["_all"]},
            },
        },
        "author": {"type": "text", "copy_to": ["_all"]},
        "date": {"type": "text", "copy_to": ["_all"]},
        "number": {"type": "text", "copy_to": ["_all"]},
        "category": {"type": "text", "copy_to": ["_all"]},
        "Imagery": {"type": "text", "copy_to": ["_all"]},
        "Places": {"type": "text", "copy_to": ["_all"]},
    },
}

INDEX_NAME = "artwork"


def main():
    vs = VisionSearch()
    vs.initialize(INDEX_NAME, MAPPING)
    with postgres_session() as db:
        artworks = db.session.query(sm.Artwork).all()
    for artwork in artworks:
        print(artwork.artwork_id, artwork.artwork_name)
        vs.es.index(
            index=INDEX_NAME,
            id=artwork.artwork_id,
            body={
                "id": artwork.artwork_id,
                "name": artwork.artwork_name,
                "description": artwork.description,
                "author": artwork.extra.get("author", ""),
                "date": artwork.extra.get("date", ""),
                "number": artwork.extra.get("Inventory number", ""),
                "category": artwork.extra.get("Category", ""),
                "Imagery": artwork.extra.get("Imagery", ""),
                "Places": artwork.extra.get("Places", ""),
            },
            timeout='10m',
        )


if __name__ == "__main__":
    typer.run(main)
