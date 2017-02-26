# _*_ coding: utf-8 _*_

from flask_wtf import FlaskForm as Form
from wtforms import StringField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class SearchForm(Form):
    price = FloatField('Limit_price', validators=[DataRequired()])
    key_word = StringField('Key_word', validators=[DataRequired(), Length(1, 64)])
    refresh = BooleanField('Forced refresh search')
    submit = SubmitField('Search')
