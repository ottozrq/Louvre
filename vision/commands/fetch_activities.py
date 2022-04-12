import json

import requests
import typer
from shapely.geometry import shape

import sql_models as sm
from utils.utils import VisionSearch, postgres_session


MAPPING = {
    "dynamic_templates": [
        {
            "all_text": {
                "match_mapping_type": "string",
                "mapping": {"copy_to": "_all", "type": "text"},
            }
        }
    ],
    "properties": {
        "_all": {"type": "text"},
        "id": {"type": "integer"},
        "name": {
            "type": "object",
            "properties": {
                "en": {"type": "text", "copy_to": ["_all"]},
                "cn": {"type": "text", "copy_to": ["_all"]},
                "fr": {"type": "text", "copy_to": ["_all"]},
            },
        },
        "description": {
            "type": "object",
            "properties": {
                "en": {"type": "text", "copy_to": ["_all"]},
                "cn": {"type": "text", "copy_to": ["_all"]},
                "fr": {"type": "text", "copy_to": ["_all"]},
            },
        },
        "category": {"type": "text", "copy_to": ["_all"]},
        "keywords": {"type": "text", "copy_to": ["_all"]},
        "start_date": {"type": "date", "format": "YYYY-MM-dd'T'HH:mm:ss"},
        "end_date": {"type": "date", "format": "YYYY-MM-dd'T'HH:mm:ss"},
    },
}

INDEX_NAME = "activity"


def create_activity(row):
    vs = VisionSearch()
    vs.initialize(INDEX_NAME, MAPPING)
    with postgres_session() as db:
        activity = (
            db.session.query(sm.Activity)
            .filter(sm.Activity.activity_unique_id == row["recordid"])
            .all()
        )
        if len(activity) > 0:
            activity = activity[0]
            activity.activity_name = {"fr": row["fields"]["title"]}
            activity.activity_unique_id = row["recordid"]
            activity.description = {"fr": row["fields"].get("description", "")}
            activity.cover_image = row["fields"].get("cover_url", "")
            activity.geometry = (
                shape(row.get("geometry", None)).wkt
                if row.get("geometry", None)
                else None
            )
            activity.extra = row["fields"]
            activity.start_time = row["fields"].get("date_start")
            activity.end_time = row["fields"].get("date_end")
        else:
            activity = sm.Activity(
                activity_name={"fr": row["fields"]["title"]},
                activity_unique_id=row["recordid"],
                description={"fr": row["fields"].get("description", "")},
                cover_image=row["fields"].get("cover_url", ""),
                geometry=shape(row.get("geometry", None)).wkt
                if row.get("geometry", None)
                else None,
                extra=row["fields"],
                start_time=row["fields"].get("date_start"),
                end_time=row["fields"].get("date_end"),
            )
        print(activity.activity_name)
        vs.es.index(
            index=INDEX_NAME,
            id=activity.activity_id,
            body={
                "id": activity.activity_id,
                "name": activity.activity_name,
                "description": activity.description,
                "category": activity.extra.get("category"),
                "keywords": activity.extra.get("tags"),
                "start_time": activity.extra.get("date_start"),
                "end_time": activity.extra.get("date_end"),
            },
            timeout="10m",
        )
        try:
            db.session.add(activity)
            db.session.commit()
        except Exception as e:
            print(e)


def main():
    url = (
        "https://opendata.paris.fr/explore/dataset/que-faire-a-paris-/"
        "download/?format=json&timezone=Europe/Berlin"
        "&lang=fr&use_labels_for_header=true&csv_separator=%3B"
    )
    resp = requests.get(url)
    data = json.loads(resp.content)
    for row in data:
        create_activity(row)


if __name__ == "__main__":
    typer.run(main)
