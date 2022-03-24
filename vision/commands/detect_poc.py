import cv2
import numpy
import typer

import sql_models as sm
from utils.utils import postgres_session


def _get_image_descriptor(image_path: str):
    img = cv2.resize(
        cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY), (300, 450)
    )
    sift = cv2.ORB_create()
    keypoints, descriptors = sift.detectAndCompute(img, None)
    return descriptors


def main():
    with postgres_session() as db:
        artworks = (
            db.session.query(sm.Artwork)
            .order_by(sm.Artwork.artwork_id)
            .limit(1000)
            .all()
        )

    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    descriptor = _get_image_descriptor(
        "/Users/otto/Downloads/IMG_4939.jpg"
    )
    highest_score = 0
    id = 0
    for i in range(0, 1000):
        metrics = []
        for artwork in artworks[i * 1: (i + 1) * 1]:
            metrics += artwork.descriptors
            artwork_descriptors = numpy.asarray(
                metrics, dtype=numpy.uint8
            )
            matches = bf.match(descriptor, artwork_descriptors)
            score = len(matches) / len(artwork_descriptors)
            print(i, score)
            if score > highest_score:
                highest_score = score
                id = artwork.artwork_id
    print(id)


if __name__ == "__main__":
    typer.run(main)
