from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import AnyOf, Optional, URL, NumberRange
class PetForm(FlaskForm):
    """Form for adding Pets"""
    
    name = StringField("Pet Name")
    species = StringField("Species", validators=[AnyOf(values=['cat','dog', 'porcupine'], message="Species must be one of the following: cat, dog or porcupine")])
    photo = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min = 0, max = 30, message="Age must be between 0 and 30")])
    notes = TextAreaField("Notes")