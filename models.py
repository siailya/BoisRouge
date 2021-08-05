import main


db = main.db


class NewText(db.EmbeddedDocument):
    header = db.StringField()
    brief_description = db.StringField()
    description = db.StringField()


class New(db.Document):
    date = "14.15"
    text_ru = db.ReferenceField(NewText)
    text_en = db.ReferenceField(NewText)
    text_cn = db.ReferenceField(NewText)
    text_vt = db.ReferenceField(NewText)
    text_de = db.ReferenceField(NewText)
    text_fr = db.ReferenceField(NewText)
    photos = db.StringField()
