from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import PetForm
app = Flask(__name__)

app.debug = True

app.config['SECRET_KEY'] = '123'
app.config['DEBUG_TB_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pets_db'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    """show list of pets"""
    pets = db.session.query(Pet).all()
    return render_template('home.html', pets=pets)

@app.route('/add', methods=['GET','POST'])
def add_form():
    """Handle post and get requests"""
    form = PetForm()
    
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo = form.photo.data
        photo - photo if photo else None
        age = form.age.data
        age = age if age else None
        notes = form.notes.data
        notes = notes if notes else None
        
        pet = Pet(name = name, species = species, photo_url = photo, age = age, notes = notes)
        db.session.add(pet)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('add_form.html', form=form)
    
@app.route('/pets/<int:id>/edit', methods=['GET','POST'])
def edit_form(id):
    """Show edit form and handle data changes"""
    pet = db.session.query(Pet).get_or_404(id)
    form = PetForm(obj = pet)
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.photo_url = form.photo.data
        pet.age = form.age.data
        pet.notes = form.notes.data
        
        db.session.commit()
        return redirect(f'/pet/{pet.id}')
    else:
        return render_template('edit_form.html', form=form, pet=pet)
    
    
@app.route('/pet/<int:id>')
def show_pet(id):
    """Show a pet's details"""
    pet = db.session.query(Pet).get_or_404(id)
    return render_template('pet-details.html', pet=pet)
