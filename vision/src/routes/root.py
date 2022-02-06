from src.routes import app, m, TAG


@app.get("/", response_model=m.Root, tags=[TAG.Root])
def read_root():
    return m.Root(
        **{
            **{k: f"/{k}" for k in m.Root.schema()["required"]},
            "openapi": "/openapi.json",
            "docs": "/docs",
        }
    )
