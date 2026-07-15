import os
from flask import request
from flask_admin import Admin, BaseView, expose
from models import Personaje, Planeta, Vehiculo, db, User
from flask_admin.contrib.sqla import ModelView


class SearchByIdView(BaseView):
    model = None
    entity_name = None

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        result = None
        object_id = None

        if request.method == 'POST':
            object_id = request.form.get('object_id', type=int)
            if object_id is not None:
                registro = db.session.get(self.model, object_id)
                if registro is None:
                    result = {"message": f"{self.entity_name} no encontrado"}
                else:
                    result = registro.serialize()

        return self.render(
            'admin/search_by_id.html',
            result=result,
            entity_name=self.entity_name,
            object_id=object_id
        )


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Personaje, db.session))
    admin.add_view(ModelView(Vehiculo, db.session))
    admin.add_view(ModelView(Planeta, db.session))

    personaje_search = SearchByIdView(
        name='Personaje', category='ID', endpoint='personaje_search')
    personaje_search.model = Personaje
    personaje_search.entity_name = 'Personaje'
    admin.add_view(personaje_search)

    vehiculo_search = SearchByIdView(
        name='Vehiculo', category='ID', endpoint='vehiculo_search')
    vehiculo_search.model = Vehiculo
    vehiculo_search.entity_name = 'Vehiculo'
    admin.add_view(vehiculo_search)

    planeta_search = SearchByIdView(
        name='Planeta', category='ID', endpoint='planeta_search')
    planeta_search.model = Planeta
    planeta_search.entity_name = 'Planeta'
    admin.add_view(planeta_search)

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
