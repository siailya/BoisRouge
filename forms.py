from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput


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
    title = StringField("Название", validators=[DataRequired("Введите название породы")])

    latin_title = StringField("Название на латинице", validators=[DataRequired("Введите название на латинице")])

    ru_description = TextAreaField("Описание (ru)",
                                   validators=[DataRequired("Введите описание изделия на русском языке")])
    en_description = TextAreaField("Описание (en)",
                                   validators=[DataRequired("Введите описание изделия на английском языке")])
    de_description = TextAreaField("Описание (de)",
                                   validators=[DataRequired("Введите описание изделия на немецком языке")])
    zh_description = TextAreaField("Описание (zh)",
                                   validators=[DataRequired("Введите описание изделия на китайском языке")])
    vt_description = TextAreaField("Описание (vt)",
                                   validators=[DataRequired("Введите описание изделия на вьетнамском языке")])
    fr_description = TextAreaField("Описание (fr)",
                                   validators=[DataRequired("Введите описание изделия на французском языке")])

    files = FileField("Фотографии")

    submit = SubmitField("Подтвердить")


class LogsForm(FlaskForm):
    log_title = StringField("Название", validators=[DataRequired("Введите название")])
    type = SelectField("Порода дерева", validators=[DataRequired("Введите породу дерева")])
    log_diameter = StringField("Диаметр", validators=[DataRequired("Введите диаметр")])
    log_length = StringField("Длина", validators=[DataRequired("Введите длину")])
    log_density_ah = StringField("Плотность при атмосферной влажности",
                                 validators=[DataRequired("Введите плотность при атмосферной влажности")])
    log_density_roll = StringField("Плотность древесины при валке",
                                   validators=[DataRequired("Введите плотность при валке")])

    ru_text = TextAreaField("Описание (ru)", validators=[DataRequired("Введите описание породы на русском языке")])
    en_text = TextAreaField("Описание (en)", validators=[DataRequired("Введите описание породы на английском языке")])
    de_text = TextAreaField("Описание (de)", validators=[DataRequired("Введите описание породы на немецком языке")])
    zh_text = TextAreaField("Описание (zh)", validators=[DataRequired("Введите описание породы на китайском языке")])
    vt_text = TextAreaField("Описание (vt)", validators=[DataRequired("Введите описание породы на вьетнамском языке")])
    fr_text = TextAreaField("Описание (fr)", validators=[DataRequired("Введите описание породы на французском языке")])

    pictures = FileField("Фотография")

    submit = SubmitField("Подтвердить")


class WoodBoardForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired("Введите название")])
    wood_board_section = StringField("Сечение", validators=[DataRequired("Введите сечение доски")])
    wood_board_length = StringField("Длина", validators=[DataRequired("Введите длину доски")])
    wood_board_humidity = StringField("Влажность", validators=[DataRequired("Введите влажность доски")])
    wood_board_subcategory = StringField("Подкатегория",
                                         validators=[DataRequired("Введите подкатегорию")])

    type = SelectField("Порода дерева")

    ru_text = TextAreaField("Описание (ru)", validators=[DataRequired("Введите описание доски на русском языке")])
    en_text = TextAreaField("Описание (en)",
                            validators=[DataRequired("Введите описание доски на английском языке")])
    de_text = TextAreaField("Описание (de)", validators=[DataRequired("Введите описание доски на немецком языке")])
    zh_text = TextAreaField("Описание (zh)",
                            validators=[DataRequired("Введите описание доски на китайском языке")])
    vt_text = TextAreaField("Описание (vt)",
                            validators=[DataRequired("Введите описание доски на вьетнамском языке")])
    fr_text = TextAreaField("Описание (fr)",
                            validators=[DataRequired("Введите описание доски на французском языке")])

    pictures = FileField("Фотография")

    submit = SubmitField("Подтвердить")


class VideoForm(FlaskForm):
    url = StringField(validators=[DataRequired("Введите ссылку на видеоролик")])

    submit = SubmitField("Подтвердить")

    @staticmethod
    def validate_url(form, field):
        if "youtu" not in field.data:
            raise ValidationError("Ведите ссылку на youtube-видеоролик!")


class ProductForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired("Введите название породы")])

    length = StringField("Длина", validators=[DataRequired("Введите длину")])
    width = StringField("Ширина", validators=[DataRequired("Введите ширину")])
    height = StringField("Высота", validators=[DataRequired("Введите высоту")])

    ru_text = TextAreaField("Описание (ru)", validators=[DataRequired("Введите описание изделия на русском языке")])
    en_text = TextAreaField("Описание (en)",
                            validators=[DataRequired("Введите описание изделия на английском языке")])
    de_text = TextAreaField("Описание (de)", validators=[DataRequired("Введите описание изделия на немецком языке")])
    zh_text = TextAreaField("Описание (zh)",
                            validators=[DataRequired("Введите описание изделия на китайском языке")])
    vt_text = TextAreaField("Описание (vt)",
                            validators=[DataRequired("Введите описание изделия на вьетнамском языке")])
    fr_text = TextAreaField("Описание (fr)",
                            validators=[DataRequired("Введите описание изделия на французском языке")])

    files = FileField("Фотографии")

    submit = SubmitField("Подтвердить")


class UserForm(FlaskForm):
    id = IntegerField("Индентификатор")
    username = StringField('Логин', validators=[DataRequired()])
    password = StringField('Пароль', widget=PasswordInput(hide_value=False))

    submit = SubmitField("Войти")
