from yummyshare.db import Recipe, CUISINES, COURSES

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, ValidationError, TextAreaField, TextField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class RecipeForm(FlaskForm):
    """
    Form for users to create new recipe
    """
    name = StringField('Name', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    cuisine = SelectField('Cuisine', choices=CUISINES,
                          validators=[DataRequired()])
    course = SelectField('Course', choices=COURSES,
                         validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image = FileField('image', validators=[
        FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, message='File must be image.')])
    user_id = IntegerField()


class RecipeUpdateForm(FlaskForm):
    """
    Form for users to update their recipe
    """
    name = StringField('Name', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    cuisine = SelectField('Cuisine', choices=CUISINES,
                          validators=[DataRequired()])
    course = SelectField('Course', choices=COURSES,
                         validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image = FileField('image', validators=[Optional(),
                                           FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, message='File must be image.')])
    user_id = IntegerField()


class SearchForm(FlaskForm):
    """
    Form for users to create new recipe
    """
    name = StringField('Name', validators=[DataRequired()])
