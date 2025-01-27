import os
from flask_admin import Admin
from models import db, User,People,Planet,Starship,Vehicle,Specie,Film,Favorite
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Starship, db.session))
    admin.add_view(ModelView(Vehicle, db.session))
    admin.add_view(ModelView(Specie, db.session))
    admin.add_view(ModelView(Film, db.session))
    admin.add_view(ModelView(Favorite, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))