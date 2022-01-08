import json

import click_spinner
import typer


def main(out_file: str = "openapi.json"):
    typer.echo("Compiling OpenAPI Schema")
    with click_spinner.spinner():
        from app import app

        schema = app.openapi()
    with open(out_file, "w") as fn:
        json.dump(schema, fn)
    typer.echo(f"Wrote to {out_file}")


if __name__ == "__main__":
    typer.run(main)
