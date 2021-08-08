import main
from mongoengine import *

db = main.db


class NewText(EmbeddedDocument):
    header = StringField()
    brief_description = StringField()
    description = StringField()


class New(Document):
    date = "14.15"
    text_ru = db.ReferenceField()
    # text_en = db.ReferenceField(NewText)
    # text_cn = db.ReferenceField(NewText)
    # text_vt = db.ReferenceField(NewText)
    # text_de = db.ReferenceField(NewText)
    # text_fr = db.ReferenceField(NewText)
    photos = db.StringField()
