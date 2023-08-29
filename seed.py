from models import Pet, db
from app import app

db.drop_all()
db.create_all()

Pet1 = Pet(name = 'Pet1', species = 'dog', age = 2)
Pet2 = Pet(name = 'Pet2', species = 'cat', age = 5)
Pet3 = Pet(name = 'Pet3', species = 'porcupine', age = 30)

pets = [Pet1, Pet2, Pet3]

db.session.add_all(pets)
db.session.commit()