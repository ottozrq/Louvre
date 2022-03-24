import typer

import sql_models as sm
from utils import algo
from utils.utils import postgres_session

MAX_DESCRIPTOR_SIZE = 50
STEP = 10


def main():
    with postgres_session() as db:
        artworks = (
            db.session.query(sm.Artwork)
            .filter(sm.Artwork.artwork_id > 42808)
            .order_by(sm.Artwork.artwork_id)
            .all()
        )
        for artwork in artworks:
            print(artwork.artwork_id)
            artwork.descriptors = algo.get_image_descriptor(artwork.cover_image)
            db.session.add(artwork)
            db.session.flush()
            db.session.commit()


if __name__ == "__main__":
    typer.run(main)
