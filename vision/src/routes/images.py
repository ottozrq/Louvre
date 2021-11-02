import os
import random
import string
import shutil

from fastapi import File, UploadFile
from fastapi.responses import FileResponse

from src.routes import app, delete_response, schema_show_all, TAG


def _random_string(string_length=8):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(string_length))


@app.post(
    "/images/upload/{dir}",
    tags=[TAG.Images],
    include_in_schema=schema_show_all,
)
def post_image(dir: str, image: UploadFile = File(...)):
    base_path = os.path.join("images", dir)
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    file_path = os.path.join(dir, _random_string(16) + image.filename.replace(" ", "-"))
    with open(f"images/{file_path}", "wb+") as f:
        shutil.copyfileobj(image.file, f)
    return {"file_path": file_path}


@app.get(
    "/images/{dir}/{file_path}",
    tags=[TAG.Images],
    include_in_schema=schema_show_all,
)
def get_image(dir: str, file_path: str):
    return FileResponse(os.path.join("images", dir, file_path))


@app.delete(
    "/images/{dir}/{file_path}",
    tags=[TAG.Images],
    include_in_schema=schema_show_all,
)
def delete_image(dir: str, file_path: str):
    os.remove(os.path.join("images", dir, file_path))
    return delete_response
