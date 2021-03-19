from flask_wtf import FlaskForm
from wtforms import StringField, validators


class YourForm(FlaskForm):
   username = StringField('Username', [validators.Length(min=4, max=25)])
   email = StringField('Email Address', [validators.Length(min=6, max=35)])
