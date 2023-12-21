from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES

from wtforms import StringField, IntegerField, TextAreaField, BooleanField 
from wtforms.validators import DataRequired, Optional, AnyOf, URL, NumberRange

class PetForm(FlaskForm):
    name = StringField("Pet Name", validators=[DataRequired()])
    # Only Dog, Cat, and Porcupine allowed for species
    species = StringField("Species", validators=[DataRequired(), AnyOf(values=['Dog', 'Cat', 'Porcupine'])])

    allowed_images = UploadSet('Images', IMAGES)

    photo_upload = FileField('Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])

    photo_url = StringField("Photo URL", validators=[Optional(), URL(require_tld=False)])
    
    age = IntegerField("Age", validators=[Optional(), 
                                          NumberRange(min=0, max=30, 
                                                      message="Age must be whole number between 0 and 30")])
    notes = TextAreaField("Notes", validators=[Optional()])
    available = BooleanField("Availability")