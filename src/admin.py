import os
from fastapi_amis_admin import i18n
i18n.set_language(language='en_US')
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.amis.components import PageSchema
from .models import User

# Create AdminSite instance
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
site = AdminSite(settings=Settings(database_url=SQLALCHEMY_DATABASE_URI))


# Registration management class
@site.register_admin
class GitHubIframeAdmin(admin.IframeAdmin):
    # Set page menu information
    page_schema = PageSchema(label='Documentation', icon='fa fa-github')
    # Set the jump link
    src = 'https://4geeksacademy.com'

# register ModelAdmin
@site.register_admin
class CategoryAdmin(admin.ModelAdmin):
    page_schema = 'User'
    # set model
    model = User