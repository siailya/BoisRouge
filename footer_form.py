from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Email


class FooterForm(FlaskForm):
    name = StringField()
    email = StringField()

    submit = SubmitField()
