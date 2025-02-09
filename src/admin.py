import os
from flask_admin import Admin
from models import db, User, Planets, People, Spaceships, Vehicles, Films, Species, Favourites
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm.properties import RelationshipProperty

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    # Sin mostrar el id como campo editable en la creación

class AdminView(ModelView):
    def __init__(self, model, *args, **kwargs):
        self.column_list = [c.key for c in model.__table__.columns]
        for attr_name, attr in model.__mapper__.attrs.items():
            if isinstance(attr, RelationshipProperty):
                self.column_list.append(attr_name)
        self.form_excluded_columns = ["id"]
        self.form_columns = [col for col in self.column_list if col != "id"]
        super().__init__(model, *args, **kwargs)

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    admin.add_view(AdminView(User, db.session))
    admin.add_view(AdminView(People, db.session))
    admin.add_view(AdminView(Planets, db.session))
    admin.add_view(AdminView(Spaceships, db.session))
    admin.add_view(AdminView(Vehicles, db.session))
    admin.add_view(AdminView(Species, db.session))
    admin.add_view(AdminView(Films, db.session))
    admin.add_view(AdminView(Favourites, db.session))
