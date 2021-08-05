from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Email


class NewsForm(FlaskForm):
    ru_header = StringField("Заголовок (ru) ", validators=[DataRequired("Введите заголовок на русском языке")])
    ru_description = StringField("Описание (ru)", validators=[DataRequired("Введите описание на русском языке")])
    ru_text = TextAreaField("Текст (ru)", validators=[DataRequired("Введите текст новости на русском языке")])

    en_header = StringField("Заголовок (en) ", validators=[DataRequired("Введите заголовок на русском языке")])
    en_description = StringField("Описание (en)", validators=[DataRequired("Введите описание на русском языке")])
    en_text = TextAreaField("Текст (en)", validators=[DataRequired("Введите текст новости на русском языке")])

    de_header = StringField("Заголовок (de) ")
    de_description = StringField("Описание (de)")
    de_text = TextAreaField("Текст (de)")

    cn_header = StringField("Заголовок (cn) ")
    cn_description = StringField("Описание (cn)")
    cn_text = TextAreaField("Текст (cn)")

    vt_header = StringField("Заголовок (vt) ")
    vt_description = StringField("Описание (vt)")
    vt_text = TextAreaField("Текст (vt)")

    fr_header = StringField("Заголовок (fr) ")
    fr_description = StringField("Описание (fr)")
    fr_text = TextAreaField("Текст (fr)")

    pictures = FileField("Фото к новости")

    submit = SubmitField("Submit")
