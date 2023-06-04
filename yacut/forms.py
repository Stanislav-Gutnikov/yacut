from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from .models import URLMap


class URLForm(FlaskForm):
    original_link = URLField(
        'Добавьте свою ссылку',
        validators=[
            Length(1, 256),
            DataRequired(message='Обязательное поле')
        ]
    )
    custom_id = StringField(
        'Добавьте кастомный идентефикатор',
        validators=[
            Length(1, 16),
            Optional()
        ]
    )
    submit = SubmitField('Добавить')

    def validate_custom_id(self, field):
        if field.data and URLMap.query.filter_by(short=field.data).first():
            raise ValidationError(f'Имя {field.data} уже занято!"')
