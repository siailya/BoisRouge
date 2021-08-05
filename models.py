from main import db


class NewText(db.EmbeddedDocument):
    header = db.StringField()
    brief_description = db.StringField()
    description = db.StringField()
