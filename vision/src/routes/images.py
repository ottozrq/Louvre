import os
import random
import string
import shutil

from fastapi import File, UploadFile, Depends
from fastapi.responses import FileResponse

from src.routes import app, d, delete_response, m, schema_show_all, sm, TAG
from utils.algo import match_image
from utils.utils import VisionDb


def _random_string(string_length: int = 8):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(string_length))


def _save_image(dir: str, image: UploadFile):
    base_path = os.path.join("images", dir)
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    file_path = os.path.join(dir, _random_string(16) + image.filename.replace(" ", "-"))
    with open(f"images/{file_path}", "wb+") as f:
        shutil.copyfileobj(image.file, f)
    return file_path


def _delete_image(dir: str, file_path: str):
    os.remove(os.path.join("images", file_path))


class ImageUploadResponse(m.Model):
    file_path: str


@app.post(
    "/images/{dir}/",
    tags=[TAG.Images],
    response_model=ImageUploadResponse,
    include_in_schema=schema_show_all,
)
def post_image(
    dir: str,
    image: UploadFile = File(...),
    user: sm.User = Depends(d.get_logged_in_user),
):
    return ImageUploadResponse(file_path=_save_image(dir, image))


@app.get(
    "/images/{dir}/{file_path}/",
    tags=[TAG.Images],
    include_in_schema=schema_show_all,
)
def get_image(dir: str, file_path: str):
    return FileResponse(os.path.join("images", dir, file_path))


@app.delete(
    "/images/{dir}/{file_path}/",
    tags=[TAG.Images],
    include_in_schema=schema_show_all,
)
def delete_image(
    dir: str,
    file_path: str,
    user: sm.User = Depends(d.get_logged_in_user),
):
    _delete_image(os.path.join(dir, file_path))
    return delete_response


@app.post(
    "/detect/",
    response_model=m.Artwork,
    tags=[TAG.Images],
    include_in_schema=schema_show_all,
)
def detect_image(
    image: UploadFile = File(...),
    db: VisionDb = Depends(d.get_psql),
):
    image_path = _save_image("tmp", image)
    artworks = db.session.query(sm.Artwork.artwork_id, sm.Artwork.descriptors).all()
    matched_id = match_image(image_path, artworks)
    _delete_image("tmp", image_path)
    return m.Artwork.db(db).from_id(matched_id)
