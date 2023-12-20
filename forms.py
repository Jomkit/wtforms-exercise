from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField 
from wtforms.validators import DataRequired, Optional, AnyOf, URL, NumberRange

class PetForm(FlaskForm):
    name = StringField("Pet Name", validators=[DataRequired()])
    species = StringField("Species", validators=[DataRequired(), AnyOf(values=['Dog', 'Cat', 'Porcupine'])])

    photo_url = StringField("Photo URL", validators=[Optional(), URL(require_tld=False)])
    age = IntegerField("Age", validators=[Optional(), 
                                          NumberRange(min=0, max=30, 
                                                      message="Age must be whole number between 0 and 30")])
    notes = TextAreaField("Notes", validators=[Optional()])
    available = BooleanField("Availability")