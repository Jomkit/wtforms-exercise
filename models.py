from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class Pet(db.Model):
    """Pet"""
    __tablename__ = "pets"
    
    default_url = 'https://img.freepik.com/free-vector/cute-dog-cute-cat-playing-box-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-3652.jpg?w=1060&t=st=1703081694~exp=1703082294~hmac=db61d9b57611e10722c6b2c9dc3713cc99b7fe2c60543ea8da814f9e267fc0aa'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.Text, 
                     nullable=False)

    species = db.Column(db.Text, 
                        nullable=False)

    # photo_upload is reference to filename
    photo_upload = db.Column(db.Text)

    photo_url = db.Column(db.Text, default=default_url)

    age = db.Column(db.Integer)

    notes = db.Column(db.Text)

    available = db.Column(db.Boolean,
                          nullable=False,
                          default=True)
    
    def __repr__(self):
        p = self
        return f"<Pet {p.id}, name={p.name}, species={p.species}, available={p.available}>"
    
    @validates('photo_url')
    def empty_string_to_null(self, key, value):
        if value == '':
            return None
        else:
            return value
