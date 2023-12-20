from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import PetForm

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

@app.route('/add', methods=['GET', 'POST'])
def add_pet_form():
    """Display add pet form and also post data for adding pets"""
    form = PetForm()

    if form.validate_on_submit():
        
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        if photo_url == '':
            photo_url = None

        age = form.age.data
        notes = form.notes.data
        
        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)

        db.session.add(new_pet)
        db.session.commit()

        flash('New Pet Added!', 'success')
        return redirect('/')
    
    else:
        return render_template('/add-pet-form.html', form=form)
    
@app.route('/<int:pet_id>', methods=["GET","POST"])
def show_edit_pet_page(pet_id):
    """Show pet page and handle edits"""
    pet = Pet.query.get_or_404(pet_id)
    form = PetForm(obj=pet)
    
    if form.validate_on_submit():

        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()
        flash('Changes Saved!', category='success')
        
        return redirect('/')
    
    else:
        return render_template('pet-page.html', pet=pet, form=form)