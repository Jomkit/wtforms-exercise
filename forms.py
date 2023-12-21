from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms import StringField, IntegerField, TextAreaField, BooleanField 
from wtforms.validators import DataRequired, Optional, AnyOf, URL, NumberRange, ValidationError

class PetForm(FlaskForm):
    name = StringField("Pet Name", validators=[DataRequired()])
    # Only Dog, Cat, and Porcupine allowed for species
    species = StringField("Species", validators=[DataRequired(), AnyOf(values=['Dog', 'Cat', 'Porcupine'])])

    photo_upload = FileField('Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!'), Optional()])

    photo_url = StringField("Photo URL", validators=[Optional(), URL(require_tld=False)])
    
    age = IntegerField("Age", validators=[Optional(), 
                                          NumberRange(min=0, max=30, 
                                                      message="Age must be whole number between 0 and 30")])
    notes = TextAreaField("Notes", validators=[Optional()])
    available = BooleanField("Availability")

    # Inline custom validator for the very specific case of 
    # checking that either photo_upload or photo_url
    def validate_photo_upload(self, photo_upload):
        if photo_upload.data and self.photo_url.data: 
            raise ValidationError('Please provide either an image file or a photo URL, not both')