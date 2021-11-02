import cv2


def get_image_descriptor(image_path: str):
    img = cv2.resize(
        cv2.cvtColor(cv2.imread(f"images/{image_path}"), cv2.COLOR_BGR2GRAY), (200, 300)
    )
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(img, None)
    return descriptors.tolist()
