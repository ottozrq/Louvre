import json

import requests
import typer


def get_activities_csv():
    url = "https://opendata.paris.fr/explore/dataset/que-faire-a-paris-/" \
          "download/?format=json&timezone=Europe/Berlin" \
          "&lang=fr&use_labels_for_header=true&csv_separator=%3B"
    resp = requests.get(url)
    data = json.loads(resp.content)
    for row in data:
       print(json.dumps(row))


def main():
    get_activities_csv()


if __name__ == "__main__":
    typer.run(main)
