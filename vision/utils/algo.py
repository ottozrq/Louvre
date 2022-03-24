import cv2
import numpy

import sql_models as sm
from utils.utils import VisionDb


def _get_image_descriptor(image_path: str):
    img = cv2.resize(
        cv2.cvtColor(cv2.imread(f"images/{image_path}"), cv2.COLOR_BGR2GRAY), (300, 450)
    )
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(img, None)
    return descriptors


def get_image_descriptor(image_path: str):
    return _get_image_descriptor(image_path).tolist()


def match_image(image_path, db: VisionDb):
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    image_descriptor = _get_image_descriptor(image_path)
    artworks = db.session.query(sm.Artwork).filter(sm.Artwork.artwork_rate >= 2).all()
    highest = {"id": 0, "score": 0}
    for artwork in artworks:
        artwork_descriptors = numpy.asarray(
                artwork.descriptors, dtype=numpy.uint8
            )
        matches = bf.match(image_descriptor, artwork_descriptors)
        score = len(matches) / len(artwork_descriptors)
        if score > highest["score"]:
            highest = {"id": artwork.artwork_id, "score": score}
    return highest["id"]
