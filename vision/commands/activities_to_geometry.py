import typer

import sql_models as sm
from utils.utils import postgres_session


def main():
    with postgres_session() as db:
        activities = db.session.query(sm.Activity).all()
        for activity in activities:
            geometry = activity.to_geometry()
            db.session.add(geometry)
        db.session.commit()


if __name__ == "__main__":
    typer.run(main)
