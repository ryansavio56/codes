from __future__ import annotations
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Length

CATEGORY_CHOICES = [
    ("resort", "Digital-free Resort"),
    ("retreat", "Nature Retreat"),
    ("mindfulness", "Mindfulness Spot"),
]

class DestinationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    location = StringField("Location", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Description", validators=[DataRequired()])
    category = SelectField("Category", choices=CATEGORY_CHOICES, validators=[DataRequired()])
    has_wifi = BooleanField("Has Wi-Fi (should be off for detox)")
    allows_screens = BooleanField("Allows Screens")
    submit = SubmitField("Save")

class ImageUploadForm(FlaskForm):
    image = FileField("Image", validators=[DataRequired()])
    caption = StringField("Caption", validators=[Length(max=255)])
    is_primary = BooleanField("Set as primary")
    submit = SubmitField("Upload")
