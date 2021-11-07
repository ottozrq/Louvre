from typing import List

import cv2
import numpy


def _get_image_descriptor(image_path: str):
    img = cv2.resize(
        cv2.cvtColor(cv2.imread(f"images/{image_path}"), cv2.COLOR_BGR2GRAY), (200, 300)
    )
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(img, None)
    return descriptors


def get_image_descriptor(image_path: str):
    return _get_image_descriptor(image_path).tolist()


def match_image(image_path, artworks: List):
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    descriptor = _get_image_descriptor(image_path)
    match_id = 0
    higest_match_score = 0
    for artwork in artworks:
        artwrork_descriptor = numpy.asarray(artwork[1], dtype=numpy.float32)
        matches = bf.match(descriptor, artwrork_descriptor)
        score = len(matches) / len(artwrork_descriptor)
        if higest_match_score < score:
            match_id = artwork[0]
            higest_match_score = score
    return match_id
