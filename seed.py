from models import db, Pet
from app import app

# Make sure to create db "adopt" before running seed.py

# create all tables fresh
db.drop_all()
db.create_all()

# Make sure tables are empty
Pet.query.delete()

# Add pets
doug = Pet(name='Doug', species='Dog', age=2, photo_url='https://images.pexels.com/photos/1805164/pexels-photo-1805164.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', notes='Good boy')
kathy = Pet(name='Kathy', species='Cat', age=1, photo_url='https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', notes='nervous around people', available=False)
kristy = Pet(name='Kristine', species='Cat', age=9,photo_url='https://images.pexels.com/photos/1170986/pexels-photo-1170986.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', available=False)
porcules = Pet(name='Porcules', species='Porcupine', age=3, photo_url='https://images.pexels.com/photos/11961230/pexels-photo-11961230.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', available=True, notes='This is a weird dog')

catrice = Pet(name='Catrice', species='Cat')

db.session.add_all([doug, kathy, kristy, porcules, catrice])
db.session.commit()