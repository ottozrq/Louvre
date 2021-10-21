from src.routes import app, TAG


@app.get("/", tags=[TAG.Root])
def read_root():
    return {"Hello": "Vision"}
