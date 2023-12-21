from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import PetForm
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'supersecret321'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

######## Pet Routes ##########

@app.route('/')
def home():
    """
    Display homepage of adoption website.
    Display all pets with photo, name, and availability
    """
    pets = Pet.query.all()
    return render_template('home.html', pets=pets)

def handle_file_uploads(file_data, path):
    # handling file upload
    if file_data:
        filename = secure_filename(file_data.filename)
        file_data.save(os.path.join(path, filename))  
    
        return filename

@app.route('/add', methods=['GET', 'POST'])
def add_pet_form():
    """Display add pet form and also post data for adding pets"""
    form = PetForm()
    path = 'static/'
    
    if form.validate_on_submit():
        pet_data = { k:v for (k, v) in form.data.items() if (k != 'csrf_token') if (k != 'photo_upload')}
        new_pet = Pet(**pet_data)
        # new pets should  be available when first added
        new_pet.available = True

        # handling file upload
        if form.photo_upload.data:
            filename = handle_file_uploads(form.photo_upload.data, path)        
            new_pet.photo_upload = filename
      
        db.session.add(new_pet)
        db.session.commit()

        flash('New Pet Added!', 'success')
        return redirect('/')
    
    else:
        # add pet form page is either being visited for the first time
        # or there was an error with the form submission
        return render_template('/add-pet-form.html', form=form)
    
@app.route('/<int:pet_id>', methods=["GET","POST"])
def show_edit_pet_page(pet_id):
    """Show pet page and handle edits"""
    pet = Pet.query.get_or_404(pet_id)
    
    form = PetForm(obj=pet)
    path = 'static/'

    if form.validate_on_submit():

        # handling file upload
        if not isinstance(form.photo_upload.data, str):
            filename = handle_file_uploads(form.photo_upload.data, path)        
            pet.photo_upload = filename

        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()
        flash('Changes Saved!', category='success')
        
        return redirect('/')
    
    else:
        # edit pet form page is either being visited for the first time
        # or there was an error with the form submission
        return render_template('pet-page.html', pet=pet, form=form)