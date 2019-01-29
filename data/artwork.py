import json
from mongoengine import *

connect('louvre', host='localhost', port=27777)


class Author(EmbeddedDocument):
    name = StringField()
    dates = StringField()
    link = StringField()


class Image(EmbeddedDocument):
    img_url = StringField()
    img_path = StringField()


class Artwork(Document):
    title = StringField(unique=True)
    author = EmbeddedDocumentField(Author)
    origin_img = StringField()
    origin_img_path = StringField()
    description = StringField()
    detail_img = ListField(EmbeddedDocumentField(Image))
    training_img = ListField(EmbeddedDocumentField(Image))
