from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from models import db, User
# Flask and Flask-SQLAlchemy initialization here
def setup_admin(app):
    admin = Admin(app, name='your_admin_name', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))