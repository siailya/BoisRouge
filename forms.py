from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Email


class NewsForm(FlaskForm):
    ru_header = StringField("Заголовок (ru) ", validators=[DataRequired("Введите заголовок на русском языке")])
    ru_description = StringField("Описание (ru)", validators=[DataRequired("Введите описание на русском языке")])
    ru_text = TextAreaField("Текст (ru)", validators=[DataRequired("Введите текст новости на русском языке")])

    en_header = StringField("Заголовок (en) ", validators=[DataRequired("Введите заголовок на английском языке")])
    en_description = StringField("Описание (en)", validators=[DataRequired("Введите описание на английском языке")])
    en_text = TextAreaField("Текст (en)", validators=[DataRequired("Введите текст новости на английском языке")])

    de_header = StringField("Заголовок (de) ", validators=[DataRequired("Введите заголовок на немецком языке")])
    de_description = StringField("Описание (de)", validators=[DataRequired("Введите описание на немецком языке")])
    de_text = TextAreaField("Текст (de)", validators=[DataRequired("Введите текст новости на немецком языке")])

    zh_header = StringField("Заголовок (zh) ", validators=[DataRequired("Введите заголовок на китайском языке")])
    zh_description = StringField("Описание (zh)", validators=[DataRequired("Введите описание на китайском языке")])
    zh_text = TextAreaField("Текст (zh)", validators=[DataRequired("Введите текст новости на китайском языке")])

    vt_header = StringField("Заголовок (vt) ", validators=[DataRequired("Введите заголовок на вьетнамском языке")])
    vt_description = StringField("Описание (vt)", validators=[DataRequired("Введите описание на вьетнамском языке")])
    vt_text = TextAreaField("Текст (vt)", validators=[DataRequired("Введите текст новости на вьетнамском языке")])

    fr_header = StringField("Заголовок (fr) ", validators=[DataRequired("Введите заголовок на французском языке")])
    fr_description = StringField("Описание (fr)", validators=[DataRequired("Введите описание на французском языке")])
    fr_text = TextAreaField("Текст (fr)", validators=[DataRequired("Введите текст новости на французском языке")])

    pictures = FileField("Фотография")

    submit = SubmitField("Подтвердить")


class ContactsForm(FlaskForm):
    submit = SubmitField("Подтвердить")


class PhotosForm(FlaskForm):
    files = MultipleFileField("Фотографии")

    submit = SubmitField("Подтвердить")


class WoodTypeForm(FlaskForm):
    title = StringField("Название ", validators=[DataRequired("Введите название породы")])

    description = TextAreaField("Описание", validators=[DataRequired("Введите описание")])

    files = MultipleFileField("Фотографии")

    submit = SubmitField("Подтвердить")


class LogsForm(FlaskForm):
    ru_text = TextAreaField("Описание (ru)", validators=[DataRequired("Введите описание породы на русском языке")])
    en_text = TextAreaField("Описание (en)", validators=[DataRequired("Введите описание породы на английском языке")])
    de_text = TextAreaField("Описание (de)", validators=[DataRequired("Введите описание породы на немецком языке")])
    zh_text = TextAreaField("Описание (zh)", validators=[DataRequired("Введите описание породы на китайском языке")])
    vt_text = TextAreaField("Описание (vt)", validators=[DataRequired("Введите описание породы на вьетнамском языке")])
    fr_text = TextAreaField("Описание (fr)", validators=[DataRequired("Введите описание породы на французском языке")])

    pictures = FileField("Фотография")

    submit = SubmitField("Подтвердить")


class VideoForm(FlaskForm):
    url = StringField(validators=[DataRequired("Введите ссылку на видеоролик")])

    submit = SubmitField("Подтвердить")

    @staticmethod
    def validate_url(form, field):
        if "youtu" not in field.data:
            raise ValidationError("Ведите ссылку на youtube-видеоролик!")

