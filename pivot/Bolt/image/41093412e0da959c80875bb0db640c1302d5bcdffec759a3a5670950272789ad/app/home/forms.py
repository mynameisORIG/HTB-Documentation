# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, DataRequired

## Profile form

class UpdateProfileForm(FlaskForm):
    name = TextField('Name', id='name', validators=[DataRequired()])
    experience = TextField('Experience', id='experience', validators=[DataRequired()])
    skills = TextField('Skills', id='skills', validators=[DataRequired()])
